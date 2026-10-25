import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select

import app as aplicativo
from banco import (
    manutencoes,
    metadata,
    recursos,
    reservas,
    usuarios,
)


class TestManutencoesHTTP(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        self.inicio = (
            datetime.now() + timedelta(days=7)
        ).replace(hour=14, minute=0, second=0, microsecond=0)
        self.fim = self.inicio + timedelta(hours=2)

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
            sessao["csrf_token"] = "token-de-teste"

    def dados_validos(self):
        return {
            "csrf_token": "token-de-teste",
            "recurso_id": "1",
            "inicio": self.inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": self.fim.strftime("%Y-%m-%dT%H:%M"),
            "motivo": "Reparo do ar-condicionado",
        }

    def listar_manutencoes(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(manutencoes)
            ).mappings().all()

    def test_consulta_exige_login(self):
        resposta = self.cliente.get("/manutencoes")

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

    def test_cadastro_exige_login(self):
        # Token válido para verificar especificamente a autenticação.
        with self.cliente.session_transaction() as sessao:
            sessao["csrf_token"] = "token-de-teste"

        resposta = self.cliente.post(
            "/manutencoes",
            data=self.dados_validos(),
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))
        self.assertEqual(self.listar_manutencoes(), [])

    def test_outros_perfis_nao_acessam_manutencoes(self):
        for usuario_id in (2, 3):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.cliente.get("/manutencoes")

                self.assertEqual(resposta.status_code, 403)

                inicio = self.cliente.get("/")
                self.assertEqual(inicio.status_code, 200)
                self.assertNotIn(
                    'href="/manutencoes"',
                    inicio.get_data(as_text=True),
                )

    def test_outros_perfis_nao_cadastram_manutencoes(self):
        for usuario_id in (2, 3):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.cliente.post(
                    "/manutencoes",
                    data=self.dados_validos(),
                )

                self.assertEqual(resposta.status_code, 403)
                self.assertEqual(self.listar_manutencoes(), [])

    def test_admin_visualiza_formulario_e_botao(self):
        self.autenticar(1)

        resposta = self.cliente.get("/manutencoes")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Cadastrar manutenção", pagina)
        self.assertIn("Sala de teste", pagina)
        self.assertIn("Nenhuma manutenção cadastrada.", pagina)

        inicio = self.cliente.get("/")
        self.assertEqual(inicio.status_code, 200)
        self.assertIn(
            'href="/manutencoes"',
            inicio.get_data(as_text=True),
        )

    def test_cadastro_sem_csrf_ou_com_token_invalido_nao_grava(self):
        self.autenticar(1)

        for token in (None, "token-incorreto"):
            with self.subTest(token=token):
                dados = self.dados_validos()

                if token is None:
                    dados.pop("csrf_token")
                else:
                    dados["csrf_token"] = token

                resposta = self.cliente.post(
                    "/manutencoes",
                    data=dados,
                )

                self.assertEqual(resposta.status_code, 400)
                self.assertEqual(self.listar_manutencoes(), [])

    def test_admin_cadastra_e_consulta_manutencao(self):
        self.autenticar(1)

        resposta = self.cliente.post(
            "/manutencoes",
            data=self.dados_validos(),
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(
            resposta.location.endswith("/manutencoes")
        )

        registros = self.listar_manutencoes()

        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["usuario_id"], 1)
        self.assertEqual(registros[0]["recurso_id"], 1)
        self.assertEqual(registros[0]["inicio"], self.inicio)
        self.assertEqual(registros[0]["fim"], self.fim)
        self.assertEqual(
            registros[0]["motivo"],
            "Reparo do ar-condicionado",
        )

        pagina = self.cliente.get(
            resposta.location
        ).get_data(as_text=True)

        self.assertIn("cadastrada com sucesso!", pagina)
        self.assertIn("Reparo do ar-condicionado", pagina)
        self.assertIn("Usuário ADMIN", pagina)

        # Atualizar a consulta não deve repetir o cadastro.
        self.cliente.get("/manutencoes")
        self.assertEqual(len(self.listar_manutencoes()), 1)

    def test_cadastro_invalido_preserva_dados_sem_gravar(self):
        self.autenticar(1)
        dados = self.dados_validos()
        dados["fim"] = dados["inicio"]

        resposta = self.cliente.post(
            "/manutencoes",
            data=dados,
        )
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 400)
        self.assertIn(
            "O término deve ser posterior ao início.",
            pagina,
        )
        self.assertIn("Reparo do ar-condicionado", pagina)
        self.assertIn(dados["inicio"], pagina)
        self.assertEqual(self.listar_manutencoes(), [])

    def test_reserva_http_e_bloqueada_pela_manutencao(self):
        self.autenticar(1)

        cadastro = self.cliente.post(
            "/manutencoes",
            data=self.dados_validos(),
        )
        self.assertEqual(cadastro.status_code, 302)

        self.autenticar(3)

        resposta = self.cliente.post(
            "/reservas/nova",
            data={
                "csrf_token": "token-de-teste",
                "recurso_id": "1",
                "inicio": self.inicio.strftime("%Y-%m-%dT%H:%M"),
                "fim": self.fim.strftime("%Y-%m-%dT%H:%M"),
                "finalidade": "Aula durante manutenção",
            },
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertIn(
            "O recurso está em manutenção no período informado.",
            resposta.get_data(as_text=True),
        )

        with self.engine.connect() as conexao:
            registros = conexao.execute(
                select(reservas)
            ).mappings().all()

        self.assertEqual(registros, [])


if __name__ == "__main__":
    unittest.main()