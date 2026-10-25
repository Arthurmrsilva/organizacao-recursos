import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, insert

import app as aplicativo
from banco import metadata, recursos, reservas, usuarios


class TestMinhasReservas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        inicio = datetime.now() + timedelta(days=7)

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

            for usuario_id in (1, 2):
                horario = inicio + timedelta(hours=usuario_id)

                conexao.execute(
                    insert(reservas).values(
                        recurso_id=1,
                        usuario_id=usuario_id,
                        inicio=horario,
                        fim=horario + timedelta(hours=1),
                        finalidade=f"Finalidade exclusiva {usuario_id}",
                        status="APROVADA",
                    )
                )

        self.engine_anterior = aplicativo.engine
        aplicativo.engine = self.engine
        self.cliente = aplicativo.app.test_client()

    def tearDown(self):
        aplicativo.engine = self.engine_anterior
        self.engine.dispose()
        self.pasta.cleanup()

    def autenticar(self, usuario_id):
        # Simula uma sessão autenticada para testar a listagem.
        # Os testes de login permanecem em test_consulta.py.
        with self.cliente.session_transaction() as sessao:
            sessao["usuario_id"] = usuario_id

    def test_listagem_exige_login(self):
        resposta = self.cliente.get("/reservas")

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

    def test_usuario_ve_apenas_suas_reservas(self):
        for usuario_id, outro_id in ((1, 2), (2, 1)):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.cliente.get("/reservas")
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(
                    f"Finalidade exclusiva {usuario_id}",
                    pagina,
                )
                self.assertNotIn(
                    f"Finalidade exclusiva {outro_id}",
                    pagina,
                )

    def test_usuario_sem_reservas_ve_mensagem(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                insert(usuarios).values(
                    id=3,
                    nome="Usuário sem reservas",
                    login="usuario3",
                    senha_hash="nao-utilizado-neste-teste",
                    perfil="SOLICITANTE",
                    ativo=True,
                )
            )

        self.autenticar(3)

        resposta = self.cliente.get("/reservas")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Você ainda não possui reservas.", pagina)
        self.assertNotIn("Finalidade exclusiva", pagina)


if __name__ == "__main__":
    unittest.main()