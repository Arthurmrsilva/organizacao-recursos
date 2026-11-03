import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select

import app as aplicativo
from banco import metadata, recursos, reservas, usuarios


class TestCancelamentoHTTP(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        with self.engine.begin() as conexao:
            for usuario_id in (1, 2):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuário {usuario_id}",
                        login=f"usuario{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil="SOLICITANTE",
                        ativo=True,
                    )
                )

            conexao.execute(
                insert(recursos).values(
                    id=1,
                    nome="Sala de teste",
                    tipo="SALA",
                    localizacao="Bloco A",
                    capacidade=30,
                    restrito=False,
                    ativo=True,
                )
            )

            inicio = (
                datetime.now() + timedelta(days=7)
            ).replace(second=0, microsecond=0)

            conexao.execute(
                insert(reservas).values(
                    id=1,
                    recurso_id=1,
                    usuario_id=1,
                    inicio=inicio,
                    fim=inicio + timedelta(hours=1),
                    finalidade="Teste de cancelamento HTTP",
                    status="APROVADA",
                )
            )

        self.patch_engine = patch.object(
            aplicativo,
            "engine",
            self.engine,
        )
        self.patch_engine.start()

        self.cliente = aplicativo.app.test_client()
        self.endereco = "/reservas/1/cancelar"

    def tearDown(self):
        self.patch_engine.stop()
        self.engine.dispose()
        self.pasta.cleanup()

    def preparar_sessao(self, usuario_id=None):
        # O login já é testado em outro arquivo.
        # Aqui preparamos a sessão para testar o cancelamento.
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["csrf_token"] = "token-de-teste"

            if usuario_id is not None:
                sessao["usuario_id"] = usuario_id

        return "token-de-teste"

    def consultar_status(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(reservas.c.status).where(
                    reservas.c.id == 1
                )
            ).scalar_one()

    def test_cancelamento_exige_login(self):
        token = self.preparar_sessao()

        resposta = self.cliente.post(
            self.endereco,
            data={"csrf_token": token},
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(
            resposta.headers["Location"].endswith("/login")
        )
        self.assertEqual(
            self.consultar_status(),
            "APROVADA",
        )

    def test_cancelamento_sem_token_e_bloqueado(self):
        self.preparar_sessao(usuario_id=1)

        resposta = self.cliente.post(self.endereco)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(
            self.consultar_status(),
            "APROVADA",
        )

    def test_cancelamento_com_token_invalido_e_bloqueado(self):
        self.preparar_sessao(usuario_id=1)

        resposta = self.cliente.post(
            self.endereco,
            data={"csrf_token": "token-incorreto"},
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(
            self.consultar_status(),
            "APROVADA",
        )

    def test_dono_cancela_e_recebe_mensagem(self):
        token = self.preparar_sessao(usuario_id=1)

        resposta = self.cliente.post(
            self.endereco,
            data={"csrf_token": token},
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(
            resposta.headers["Location"].endswith("/reservas")
        )
        self.assertEqual(
            self.consultar_status(),
            "CANCELADA",
        )

        pagina = self.cliente.get(
            resposta.headers["Location"]
        )

        self.assertEqual(pagina.status_code, 200)
        self.assertIn(
            "cancelada com sucesso",
            pagina.get_data(as_text=True),
        )

    def test_outro_usuario_nao_consegue_cancelar(self):
        token = self.preparar_sessao(usuario_id=2)

        resposta = self.cliente.post(
            self.endereco,
            data={"csrf_token": token},
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(
            resposta.headers["Location"].endswith("/reservas")
        )
        self.assertEqual(
            self.consultar_status(),
            "APROVADA",
        )

        pagina = self.cliente.get(
            resposta.headers["Location"]
        )

        self.assertEqual(pagina.status_code, 200)
        self.assertIn(
            "Reserva não encontrada para este usuário.",
            pagina.get_data(as_text=True),
        )

    def test_get_nao_cancela_reserva(self):
        self.preparar_sessao(usuario_id=1)

        resposta = self.cliente.get(self.endereco)

        self.assertEqual(resposta.status_code, 405)
        self.assertEqual(
            self.consultar_status(),
            "APROVADA",
        )


if __name__ == "__main__":
    unittest.main()