import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select, update
from werkzeug.security import generate_password_hash

import app as aplicativo
from banco import metadata, recursos, usuarios


class TestSistema(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)

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

        troca_engine = patch.object(
            aplicativo,
            "engine",
            self.engine,
        )
        troca_engine.start()
        self.addCleanup(troca_engine.stop)

        self.cliente = aplicativo.app.test_client()

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

    def listar_recursos(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(recursos).order_by(recursos.c.id)
            ).mappings().all()

    def cadastrar_usuarios_para_vinculo(self):
        with self.engine.begin() as conexao:
            for usuario_id, nome, perfil, ativo in (
                (2, "Responsável ativo", "RESPONSAVEL", True),
                (3, "Responsável inativo", "RESPONSAVEL", False),
                (4, "Solicitante adicional", "SOLICITANTE", True),
                (5, "Administrador adicional", "ADMIN", True),
            ):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=nome,
                        login=f"vinculo{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil=perfil,
                        ativo=ativo,
                    )
                )

    def obter_opcoes_responsavel(self, pagina):
        campo = re.search(
            r'<select\b[^>]*\bid="responsavel_id"[^>]*>'
            r"(.*?)</select>",
            pagina,
            flags=re.DOTALL,
        )

        self.assertIsNotNone(
            campo,
            "Campo de responsável não encontrado.",
        )

        return campo.group(1)

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
        self.assertIn(
            "Usuário de Teste",
            pagina.get_data(as_text=True),
        )

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
        self.preparar_admin()

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
                    "/recursos/novo",
                    data=dados,
                )

                self.assertEqual(resposta.status_code, 302)
                self.assertEqual(resposta.headers["Location"], "/")

                salvo = self.buscar_recurso(nome)

                self.assertIsNotNone(salvo)
                self.assertEqual(salvo["tipo"], tipo)
                self.assertEqual(salvo["localizacao"], "Bloco B")
                self.assertEqual(salvo["restrito"], restrito)
                self.assertTrue(salvo["ativo"])
                self.assertIsNone(salvo["responsavel_id"])
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
                    "/recursos/novo",
                    data=dados,
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
                    "/recursos/novo",
                    data=dados,
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
            "/recursos/novo",
            data=dados,
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
                    "/",
                    query_string=filtros,
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
                    "/",
                    query_string=filtros,
                )
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 400)
                self.assertIn('role="alert"', pagina)
                self.assertNotIn("Sala Teste", pagina)
                self.assertNotIn("Professor Teste", pagina)
                self.assertNotIn("Projetor Teste", pagina)

    def test_lista_mostra_somente_responsaveis_ativos(self):
        self.cadastrar_usuarios_para_vinculo()
        self.preparar_admin()

        resposta = self.cliente.get("/recursos/novo")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)

        opcoes = self.obter_opcoes_responsavel(pagina)

        self.assertIn("Responsável ativo", opcoes)
        self.assertIn('value="2"', opcoes)
        self.assertNotIn("Responsável inativo", opcoes)
        self.assertNotIn("Solicitante adicional", opcoes)
        self.assertNotIn("Administrador adicional", opcoes)
        self.assertNotIn("Usuário de Teste", opcoes)

    def test_admin_vincula_responsavel_aos_tres_tipos(self):
        self.cadastrar_usuarios_para_vinculo()
        self.preparar_admin()

        for tipo, capacidade, competencia in (
            ("SALA", "20", ""),
            ("PROFESSOR", "", "Python"),
            ("MATERIAL", "", ""),
        ):
            with self.subTest(tipo=tipo):
                dados = self.dados_cadastro()
                dados.update(
                    nome=f"Recurso vinculado {tipo}",
                    tipo=tipo,
                    capacidade=capacidade,
                    competencia=competencia,
                    responsavel_id="2",
                    restrito="sim",
                )

                resposta = self.cliente.post(
                    "/recursos/novo",
                    data=dados,
                )

                self.assertEqual(resposta.status_code, 302)
                self.assertEqual(resposta.headers["Location"], "/")

                salvo = self.buscar_recurso(dados["nome"])

                self.assertIsNotNone(salvo)
                self.assertEqual(salvo["responsavel_id"], 2)
                self.assertEqual(salvo["tipo"], tipo)
                self.assertTrue(salvo["restrito"])

    def test_responsavel_invalido_nao_grava_recurso(self):
        self.cadastrar_usuarios_para_vinculo()
        self.preparar_admin()
        antes = self.listar_recursos()

        casos = (
            ("3", "perfil RESPONSAVEL"),
            ("4", "perfil RESPONSAVEL"),
            ("5", "perfil RESPONSAVEL"),
            ("999", "perfil RESPONSAVEL"),
            ("abc", "responsável válido"),
            ("0", "responsável válido"),
            ("-1", "responsável válido"),
            ("2.5", "responsável válido"),
        )

        for numero, (responsavel_id, mensagem) in enumerate(casos):
            with self.subTest(responsavel_id=responsavel_id):
                dados = self.dados_cadastro()
                dados.update(
                    nome=f"Vínculo inválido {numero}",
                    responsavel_id=responsavel_id,
                )

                resposta = self.cliente.post(
                    "/recursos/novo",
                    data=dados,
                )
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 400)
                self.assertIn(mensagem, pagina)
                self.assertIsNone(
                    self.buscar_recurso(dados["nome"])
                )
                self.assertEqual(self.listar_recursos(), antes)

    def test_erro_preserva_responsavel_selecionado(self):
        self.cadastrar_usuarios_para_vinculo()
        self.preparar_admin()

        dados = self.dados_cadastro()
        dados.update(
            nome="Sala com capacidade inválida",
            capacidade="0",
            responsavel_id="2",
        )

        resposta = self.cliente.post(
            "/recursos/novo",
            data=dados,
        )
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("capacidade deve estar", pagina)

        opcoes = self.obter_opcoes_responsavel(pagina)

        self.assertRegex(
            opcoes,
            r'<option\s+value="2"\s+selected\s*>',
        )
        self.assertIsNone(self.buscar_recurso(dados["nome"]))

    def test_sem_responsaveis_permite_cadastro_sem_vinculo(self):
        self.preparar_admin()

        resposta = self.cliente.get("/recursos/novo")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            "Nenhum responsável ativo disponível para vincular.",
            pagina,
        )

        dados = self.dados_cadastro()
        dados["responsavel_id"] = ""

        resposta = self.cliente.post(
            "/recursos/novo",
            data=dados,
        )

        self.assertEqual(resposta.status_code, 302)

        salvo = self.buscar_recurso(dados["nome"])

        self.assertIsNotNone(salvo)
        self.assertIsNone(salvo["responsavel_id"])

    def test_responsavel_desativado_apos_abrir_formulario_e_recusado(self):
        self.cadastrar_usuarios_para_vinculo()
        self.preparar_admin()

        resposta = self.cliente.get("/recursos/novo")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            "Responsável ativo",
            self.obter_opcoes_responsavel(pagina),
        )

        # O usuário estava disponível quando a página abriu,
        # mas deixou de estar ativo antes do envio.
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 2)
                .values(ativo=False)
            )

        antes = self.listar_recursos()
        dados = self.dados_cadastro()
        dados["responsavel_id"] = "2"

        resposta = self.cliente.post(
            "/recursos/novo",
            data=dados,
        )
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 400)
        self.assertIn(
            "Selecione um responsável ativo",
            pagina,
        )
        self.assertEqual(self.listar_recursos(), antes)
        self.assertIsNone(self.buscar_recurso(dados["nome"]))
        self.assertNotIn(
            "Responsável ativo",
            self.obter_opcoes_responsavel(pagina),
        )


if __name__ == "__main__":
    unittest.main()