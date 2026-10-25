import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine, insert, select, update
from werkzeug.security import generate_password_hash

import app as aplicativo
from banco import metadata, recursos, usuarios


class TestSistema(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        with self.engine.begin() as conexao:
            conexao.execute(
                insert(usuarios).values(
                    id=1,
                    nome="Usuário de Teste",
                    login="teste",
                    senha_hash=generate_password_hash("SenhaTeste123!"),
                    perfil="SOLICITANTE",
                    ativo=True,
                )
            )

            exemplos = [
                ("Sala Teste", "SALA", True),
                ("Professor Teste", "PROFESSOR", True),
                ("Projetor Teste", "MATERIAL", True),
                ("Sala Inativa", "SALA", False),
            ]

            for nome, tipo, ativo in exemplos:
                conexao.execute(
                    insert(recursos).values(
                        nome=nome,
                        tipo=tipo,
                        localizacao="Bloco Teste",
                        restrito=False,
                        ativo=ativo,
                    )
                )

        self.engine_original = aplicativo.engine
        aplicativo.engine = self.engine
        self.cliente = aplicativo.app.test_client()

    def tearDown(self):
        aplicativo.engine = self.engine_original
        self.engine.dispose()
        self.pasta.cleanup()

    def obter_token(self):
        with self.cliente.session_transaction() as sessao:
            return sessao["csrf_token"]

    def entrar(self, senha="SenhaTeste123!"):
        self.cliente.get("/login")

        return self.cliente.post(
            "/login",
            data={
                "login": "teste",
                "senha": senha,
                "csrf_token": self.obter_token(),
            },
        )

    def test_inicio_exige_login(self):
        resposta = self.cliente.get("/")

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.headers["Location"], "/login")

    def test_login_correto(self):
        resposta = self.entrar()

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.headers["Location"], "/")

        with self.cliente.session_transaction() as sessao:
            self.assertEqual(sessao["usuario_id"], 1)

        pagina = self.cliente.get("/")
        self.assertEqual(pagina.status_code, 200)
        self.assertIn("Usuário de Teste", pagina.get_data(as_text=True))

    def test_senha_incorreta(self):
        resposta = self.entrar(senha="SenhaErrada!")

        self.assertEqual(resposta.status_code, 401)
        self.assertIn(
            "Login ou senha inválidos.",
            resposta.get_data(as_text=True),
        )

        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

    def test_usuario_inativo_nao_entra(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 1)
                .values(ativo=False)
            )

        resposta = self.entrar()

        self.assertEqual(resposta.status_code, 401)

        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

    def test_login_sem_token_e_bloqueado(self):
        resposta = self.cliente.post(
            "/login",
            data={
                "login": "teste",
                "senha": "SenhaTeste123!",
            },
        )

        self.assertEqual(resposta.status_code, 400)

        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

    def test_sair_encerra_acesso(self):
        self.entrar()

        resposta = self.cliente.post(
            "/sair",
            data={"csrf_token": self.obter_token()},
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.headers["Location"], "/login")

        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

        resposta = self.cliente.get("/")
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.headers["Location"], "/login")

    def test_listar_recursos_ativos(self):
        self.entrar()

        resposta = self.cliente.get("/")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Sala Teste", pagina)
        self.assertIn("Professor Teste", pagina)
        self.assertIn("Projetor Teste", pagina)
        self.assertNotIn("Sala Inativa", pagina)

    def test_filtrar_por_tipo(self):
        self.entrar()

        casos = {
            "SALA": "Sala Teste",
            "PROFESSOR": "Professor Teste",
            "MATERIAL": "Projetor Teste",
        }

        for tipo, nome_esperado in casos.items():
            with self.subTest(tipo=tipo):
                resposta = self.cliente.get(f"/?tipo={tipo}")
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(nome_esperado, pagina)
                self.assertNotIn("Sala Inativa", pagina)

                for outro_tipo, outro_nome in casos.items():
                    if outro_tipo != tipo:
                        self.assertNotIn(outro_nome, pagina)

    def test_tipo_invalido_mostra_todos_os_ativos(self):
        self.entrar()

        resposta = self.cliente.get("/?tipo=INVALIDO")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Sala Teste", pagina)
        self.assertIn("Professor Teste", pagina)
        self.assertIn("Projetor Teste", pagina)
        self.assertNotIn("Sala Inativa", pagina)

    def test_cadastro_exige_login(self):
        resposta = self.cliente.get("/recursos/novo")

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.headers["Location"], "/login")

    def test_admin_pode_abrir_cadastro(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 1)
                .values(perfil="ADMIN")
            )

        self.entrar()
        resposta = self.cliente.get("/recursos/novo")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            'name="nome"',
            resposta.get_data(as_text=True),
        )

    def test_outros_perfis_nao_podem_abrir_cadastro(self):
        for perfil in ("SOLICITANTE", "RESPONSAVEL"):
            with self.subTest(perfil=perfil):
                with self.engine.begin() as conexao:
                    conexao.execute(
                        update(usuarios)
                        .where(usuarios.c.id == 1)
                        .values(perfil=perfil)
                    )

                self.cliente = aplicativo.app.test_client()
                self.entrar()

                resposta = self.cliente.get("/recursos/novo")

                self.assertEqual(resposta.status_code, 403)

    def preparar_admin(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 1)
                .values(perfil="ADMIN")
            )

        self.entrar()

    def dados_cadastro(self):
        return {
            "nome": "Novo Recurso",
            "tipo": "SALA",
            "localizacao": "Bloco B",
            "capacidade": "40",
            "competencia": "",
            "csrf_token": self.obter_token(),
        }

    def buscar_recurso(self, nome):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(recursos).where(recursos.c.nome == nome)
            ).mappings().first()

    def test_admin_cadastra_os_tres_tipos(self):
        self.preparar_admin()

        casos = [
            ("SALA", "Sala Nova", "40", "", False),
            ("PROFESSOR", "Professora Ana", "", "Python", False),
            ("MATERIAL", "Notebook Novo", "", "", True),
        ]

        for tipo, nome, capacidade, competencia, restrito in casos:
            with self.subTest(tipo=tipo):
                dados = self.dados_cadastro()
                dados.update(
                    tipo=tipo,
                    nome=nome,
                    capacidade=capacidade,
                    competencia=competencia,
                )

                if restrito:
                    dados["restrito"] = "sim"

                resposta = self.cliente.post(
                    "/recursos/novo", data=dados
                )

                self.assertEqual(resposta.status_code, 302)
                self.assertEqual(resposta.headers["Location"], "/")

                salvo = self.buscar_recurso(nome)

                self.assertIsNotNone(salvo)
                self.assertEqual(salvo["tipo"], tipo)
                self.assertEqual(salvo["localizacao"], "Bloco B")
                self.assertEqual(salvo["restrito"], restrito)
                self.assertTrue(salvo["ativo"])
                self.assertEqual(
                    salvo["capacidade"],
                    40 if tipo == "SALA" else None,
                )
                self.assertEqual(
                    salvo["competencia"],
                    "Python" if tipo == "PROFESSOR" else None,
                )

    def test_cadastro_invalido_nao_grava(self):
        self.preparar_admin()

        casos = [
            {"nome": "   "},
            {"nome": "A" * 121},
            {"tipo": "INVALIDO"},
            {"localizacao": ""},
            {"capacidade": "0"},
            {"capacidade": "-1"},
            {"capacidade": "10001"},
            {"capacidade": "2.5"},
            {"capacidade": "abc"},
            {"tipo": "PROFESSOR", "competencia": ""},
            {"tipo": "PROFESSOR", "competencia": "A" * 151},
        ]

        for numero, alteracoes in enumerate(casos):
            with self.subTest(caso=numero):
                dados = self.dados_cadastro()
                dados["nome"] = f"Invalido {numero}"
                dados.update(alteracoes)

                resposta = self.cliente.post(
                    "/recursos/novo", data=dados
                )

                self.assertEqual(resposta.status_code, 400)
                self.assertIn(
                    "Confira os campos abaixo:",
                    resposta.get_data(as_text=True),
                )
                self.assertIsNone(
                    self.buscar_recurso(dados["nome"].strip())
                )

    def test_outros_perfis_nao_podem_gravar_recurso(self):
        for perfil in ("SOLICITANTE", "RESPONSAVEL"):
            with self.subTest(perfil=perfil):
                with self.engine.begin() as conexao:
                    conexao.execute(
                        update(usuarios)
                        .where(usuarios.c.id == 1)
                        .values(perfil=perfil)
                    )

                self.cliente = aplicativo.app.test_client()
                self.entrar()
                dados = self.dados_cadastro()

                resposta = self.cliente.post(
                    "/recursos/novo", data=dados
                )

                self.assertEqual(resposta.status_code, 403)
                self.assertIsNone(
                    self.buscar_recurso(dados["nome"])
                )

    def test_cadastro_sem_token_nao_grava(self):
        self.preparar_admin()
        dados = self.dados_cadastro()
        dados.pop("csrf_token")

        resposta = self.cliente.post(
            "/recursos/novo", data=dados
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertIsNone(self.buscar_recurso(dados["nome"]))     
    def test_filtros_de_pesquisa(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.nome == "Sala Teste")
                .values(capacidade=40, localizacao="Bloco B")
            )
            conexao.execute(
                update(recursos)
                .where(recursos.c.nome == "Professor Teste")
                .values(competencia="Programação em Python")
            )

        self.entrar()

        casos = [
            (
                {"capacidade": "35"},
                ["Sala Teste"],
                ["Professor Teste", "Projetor Teste"],
            ),
            (
                {"localizacao": "bloco b"},
                ["Sala Teste"],
                ["Professor Teste", "Projetor Teste"],
            ),
            (
                {"competencia": "python"},
                ["Professor Teste"],
                ["Sala Teste", "Projetor Teste"],
            ),
            (
                {
                    "tipo": "SALA",
                    "localizacao": "Bloco B",
                    "capacidade": "40",
                },
                ["Sala Teste"],
                ["Professor Teste", "Projetor Teste"],
            ),
            (
                {"capacidade": "41"},
                [],
                ["Sala Teste", "Professor Teste", "Projetor Teste"],
            ),
            (
                {"competencia": "Python", "capacidade": "35"},
                [],
                ["Sala Teste", "Professor Teste", "Projetor Teste"],
            ),
        ]

        for filtros, presentes, ausentes in casos:
            with self.subTest(filtros=filtros):
                resposta = self.cliente.get(
                    "/", query_string=filtros
                )
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertNotIn("Sala Inativa", pagina)

                for nome in presentes:
                    self.assertIn(nome, pagina)

                for nome in ausentes:
                    self.assertNotIn(nome, pagina)

                if not presentes:
                    self.assertIn(
                        "Nenhum recurso encontrado para esta consulta.",
                        pagina,
                    )

    def test_filtros_invalidos(self):
        self.entrar()

        casos = [
            {"capacidade": "abc"},
            {"capacidade": "2.5"},
            {"capacidade": "0"},
            {"capacidade": "-1"},
            {"capacidade": "10001"},
            {"localizacao": "A" * 121},
            {"competencia": "A" * 151},
        ]

        for filtros in casos:
            with self.subTest(filtros=filtros):
                resposta = self.cliente.get(
                    "/", query_string=filtros
                )
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 400)
                self.assertIn('role="alert"', pagina)
                self.assertNotIn("Sala Teste", pagina)
                self.assertNotIn("Professor Teste", pagina)
                self.assertNotIn("Projetor Teste", pagina)
if __name__ == "__main__":
    unittest.main()