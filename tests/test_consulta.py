import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine, insert, update
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
if __name__ == "__main__":
    unittest.main()