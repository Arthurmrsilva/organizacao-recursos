import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert

import app as aplicativo
from banco import metadata, usuarios


class TestAuditoriaHTTP(unittest.TestCase):
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
            for usuario_id, perfil in (
                (1, "ADMIN"),
                (2, "RESPONSAVEL"),
                (3, "SOLICITANTE"),
            ):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuário {perfil}",
                        login=f"usuario{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil=perfil,
                        ativo=True,
                    )
                )

        substituicao = patch.object(
            aplicativo, "engine", self.engine
        )
        substituicao.start()
        self.addCleanup(substituicao.stop)

        self.cliente = aplicativo.app.test_client()

    def autenticar(self, usuario_id):
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["usuario_id"] = usuario_id

    def test_auditoria_exige_login(self):
        resposta = self.cliente.get("/auditoria")

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

    def test_perfis_sem_permissao_nao_acessam_auditoria(self):
        for usuario_id in (2, 3):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.cliente.get("/auditoria")
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 403)
                self.assertIn("Acesso negado", pagina)

                inicio = self.cliente.get("/")
                self.assertEqual(inicio.status_code, 200)
                self.assertNotIn(
                    'href="/auditoria"',
                    inicio.get_data(as_text=True),
                )

    def test_admin_acessa_auditoria_e_visualiza_botao(self):
        self.autenticar(1)

        resposta = self.cliente.get("/auditoria")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Auditoria de reservas", pagina)
        self.assertIn(
            "Nenhum evento de auditoria registrado ainda.",
            pagina,
        )

        inicio = self.cliente.get("/")
        self.assertEqual(inicio.status_code, 200)
        self.assertIn(
            'href="/auditoria"',
            inicio.get_data(as_text=True),
        )


if __name__ == "__main__":
    unittest.main()