import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select
from werkzeug.security import generate_password_hash

import app as aplicativo
from banco import metadata, usuarios


class TestSegurancaLogin(unittest.TestCase):
    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)

        caminho = Path(pasta.name) / "seguranca.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        with self.engine.begin() as conexao:
            conexao.execute(
                insert(usuarios).values(
                    id=1,
                    nome="Usuário de segurança",
                    login="teste",
                    senha_hash=generate_password_hash(
                        "SenhaTeste123!"
                    ),
                    perfil="SOLICITANTE",
                    ativo=True,
                )
            )

        troca = patch.object(
            aplicativo, "engine", self.engine
        )
        troca.start()
        self.addCleanup(troca.stop)

        self.cliente = aplicativo.app.test_client()
        self.cliente.get("/login")

    def token(self, cliente):
        with cliente.session_transaction() as sessao:
            return sessao["csrf_token"]

    def enviar_login(self, login="teste", token=None):
        return self.cliente.post(
            "/login",
            data={
                "login": login,
                "senha": "SenhaTeste123!",
                "csrf_token": (
                    self.token(self.cliente)
                    if token is None else token
                ),
            },
        )

    def conferir_sem_autenticacao(self):
        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

        resposta = self.cliente.get("/")
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

    def test_token_de_outra_sessao_nao_autentica(self):
        outro_cliente = aplicativo.app.test_client()
        outro_cliente.get("/login")
        token_alheio = self.token(outro_cliente)

        self.assertNotEqual(
            self.token(self.cliente), token_alheio
        )

        resposta = self.enviar_login(token=token_alheio)

        self.assertEqual(resposta.status_code, 400)
        self.conferir_sem_autenticacao()

    def test_login_renova_token_e_recusa_token_anterior(self):
        token_anterior = self.token(self.cliente)

        resposta = self.enviar_login()

        self.assertEqual(resposta.status_code, 302)
        self.assertNotEqual(
            self.token(self.cliente), token_anterior
        )

        with self.cliente.session_transaction() as sessao:
            self.assertEqual(sessao["usuario_id"], 1)

        # O token antigo não pode executar o logout.
        resposta = self.cliente.post(
            "/sair",
            data={"csrf_token": token_anterior},
        )

        self.assertEqual(resposta.status_code, 400)

        with self.cliente.session_transaction() as sessao:
            self.assertEqual(sessao["usuario_id"], 1)

        # O token atual permite encerrar a sessão.
        resposta = self.cliente.post(
            "/sair",
            data={"csrf_token": self.token(self.cliente)},
        )

        self.assertEqual(resposta.status_code, 302)
        self.conferir_sem_autenticacao()

    def test_injecao_sql_no_login_nao_autentica(self):
        tentativas = (
            "' OR '1'='1' --",
            "teste' --",
            "'; DROP TABLE usuarios; --",
        )

        for tentativa in tentativas:
            with self.subTest(login=tentativa):
                resposta = self.enviar_login(
                    login=tentativa
                )

                self.assertEqual(resposta.status_code, 401)
                self.assertIn(
                    "Login ou senha inválidos.",
                    resposta.get_data(as_text=True),
                )
                self.conferir_sem_autenticacao()

                with self.engine.connect() as conexao:
                    registros = conexao.execute(
                        select(
                            usuarios.c.id,
                            usuarios.c.login,
                        )
                    ).all()

                self.assertEqual(registros, [(1, "teste")])


if __name__ == "__main__":
    unittest.main()