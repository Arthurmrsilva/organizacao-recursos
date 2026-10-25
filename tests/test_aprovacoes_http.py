import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select

import app as aplicativo
from banco import metadata, recursos, reservas, usuarios


class TestAprovacoesHTTP(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        inicio = datetime.now() + timedelta(days=7)

        with self.engine.begin() as conexao:
            for usuario_id, perfil in (
                (1, "SOLICITANTE"),
                (2, "RESPONSAVEL"),
                (3, "RESPONSAVEL"),
                (4, "ADMIN"),
            ):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuário {usuario_id}",
                        login=f"usuario{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil=perfil,
                        ativo=True,
                    )
                )

            for recurso_id, responsavel_id in ((1, 2), (2, 3)):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=f"Professor exclusivo {recurso_id}",
                        tipo="PROFESSOR",
                        localizacao="Bloco A",
                        competencia="Python",
                        restrito=False,
                        ativo=True,
                        responsavel_id=responsavel_id,
                    )
                )

                conexao.execute(
                    insert(reservas).values(
                        id=recurso_id,
                        recurso_id=recurso_id,
                        usuario_id=1,
                        inicio=inicio,
                        fim=inicio + timedelta(hours=1),
                        finalidade=f"Solicitação exclusiva {recurso_id}",
                        status="SOLICITADA",
                    )
                )

        self.patch_engine = patch.object(
            aplicativo, "engine", self.engine
        )
        self.patch_engine.start()

        self.cliente = aplicativo.app.test_client()

    def tearDown(self):
        self.patch_engine.stop()
        self.engine.dispose()
        self.pasta.cleanup()

    def preparar_sessao(self, usuario_id=None):
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["csrf_token"] = "token-de-teste"

            if usuario_id is not None:
                sessao["usuario_id"] = usuario_id

        return "token-de-teste"

    def consultar_status(self, reserva_id=1):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(reservas.c.status).where(
                    reservas.c.id == reserva_id
                )
            ).scalar_one()

    def test_tela_e_avaliacao_exigem_login(self):
        token = self.preparar_sessao()

        tela = self.cliente.get("/aprovacoes")
        avaliacao = self.cliente.post(
            "/reservas/1/avaliar",
            data={
                "csrf_token": token,
                "decisao": "APROVADA",
            },
        )

        for resposta in (tela, avaliacao):
            self.assertEqual(resposta.status_code, 302)
            self.assertTrue(
                resposta.headers["Location"].endswith("/login")
            )

        self.assertEqual(
            self.consultar_status(), "SOLICITADA"
        )

    def test_outros_perfis_recebem_acesso_negado(self):
        for usuario_id in (1, 4):
            with self.subTest(usuario_id=usuario_id):
                token = self.preparar_sessao(usuario_id)

                tela = self.cliente.get("/aprovacoes")
                avaliacao = self.cliente.post(
                    "/reservas/1/avaliar",
                    data={
                        "csrf_token": token,
                        "decisao": "APROVADA",
                    },
                )

                self.assertEqual(tela.status_code, 403)
                self.assertEqual(avaliacao.status_code, 403)
                self.assertEqual(
                    self.consultar_status(), "SOLICITADA"
                )

    def test_listagem_mostra_apenas_recursos_do_responsavel(self):
        for usuario_id, propria, outra in (
            (2, 1, 2),
            (3, 2, 1),
        ):
            with self.subTest(usuario_id=usuario_id):
                self.preparar_sessao(usuario_id)

                resposta = self.cliente.get("/aprovacoes")
                html = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(
                    f"Solicitação exclusiva {propria}", html
                )
                self.assertNotIn(
                    f"Solicitação exclusiva {outra}", html
                )

    def test_token_ausente_ou_invalido_bloqueia_avaliacao(self):
        for token in (None, "token-incorreto"):
            with self.subTest(token=token):
                self.preparar_sessao(2)
                dados = {"decisao": "APROVADA"}

                if token is not None:
                    dados["csrf_token"] = token

                resposta = self.cliente.post(
                    "/reservas/1/avaliar",
                    data=dados,
                )

                self.assertEqual(resposta.status_code, 400)
                self.assertEqual(
                    self.consultar_status(), "SOLICITADA"
                )

    def test_responsavel_aprova_e_solicitante_ve_resultado(self):
        token = self.preparar_sessao(2)

        resposta = self.cliente.post(
            "/reservas/1/avaliar",
            data={
                "csrf_token": token,
                "decisao": "APROVADA",
            },
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(
            resposta.headers["Location"].endswith("/aprovacoes")
        )
        self.assertEqual(
            self.consultar_status(), "APROVADA"
        )

        pagina = self.cliente.get("/aprovacoes")
        html = pagina.get_data(as_text=True)

        self.assertEqual(pagina.status_code, 200)
        self.assertIn("aprovada com sucesso", html)
        self.assertNotIn("Solicitação exclusiva 1", html)

        self.preparar_sessao(1)
        pagina = self.cliente.get("/reservas")
        html = pagina.get_data(as_text=True)

        self.assertEqual(pagina.status_code, 200)
        self.assertIn("Solicitação exclusiva 1", html)
        self.assertIn("Aprovada", html)

    def test_responsavel_rejeita_reserva(self):
        token = self.preparar_sessao(2)

        resposta = self.cliente.post(
            "/reservas/1/avaliar",
            data={
                "csrf_token": token,
                "decisao": "REJEITADA",
            },
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(
            self.consultar_status(), "REJEITADA"
        )

        pagina = self.cliente.get("/aprovacoes")
        html = pagina.get_data(as_text=True)

        self.assertEqual(pagina.status_code, 200)
        self.assertIn("rejeitada com sucesso", html)
        self.assertNotIn("Solicitação exclusiva 1", html)

    def test_outro_responsavel_nao_avalia_por_url_direta(self):
        for decisao in ("APROVADA", "REJEITADA"):
            with self.subTest(decisao=decisao):
                token = self.preparar_sessao(3)

                resposta = self.cliente.post(
                    "/reservas/1/avaliar",
                    data={
                        "csrf_token": token,
                        "decisao": decisao,
                    },
                )

                self.assertEqual(resposta.status_code, 302)
                self.assertEqual(
                    self.consultar_status(), "SOLICITADA"
                )

                pagina = self.cliente.get("/aprovacoes")

                self.assertEqual(pagina.status_code, 200)
                self.assertIn(
                    "Você não é o responsável por este recurso.",
                    pagina.get_data(as_text=True),
                )


if __name__ == "__main__":
    unittest.main()