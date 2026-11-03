import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select, update

import app as aplicativo
from banco import (
    auditoria_reservas,
    metadata,
    recursos,
    reservas,
    usuarios,
)


class TestEdicaoHTTP(unittest.TestCase):
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

        self.fim = self.inicio + timedelta(hours=1)

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

            conexao.execute(
                insert(reservas).values(
                    id=1,
                    recurso_id=1,
                    usuario_id=1,
                    inicio=self.inicio,
                    fim=self.fim,
                    finalidade="Finalidade original",
                    status="APROVADA",
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
        self.endereco = "/reservas/1/editar"
        self.token = "token-csrf-de-teste"

    def preparar_sessao(self, usuario_id=1):
        # Simula a autenticação para testar a rota de edição.
        # A validação de login e senha possui testes próprios.
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["csrf_token"] = self.token

            if usuario_id is not None:
                sessao["usuario_id"] = usuario_id

    def dados(self, **alteracoes):
        dados = {
            "csrf_token": self.token,
            "recurso_id": "1",
            "inicio": self.inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": self.fim.strftime("%Y-%m-%dT%H:%M"),
            "finalidade": "Finalidade atualizada",
        }
        dados.update(alteracoes)
        return dados

    def buscar_reserva(self):
        with self.engine.connect() as conexao:
            return dict(
                conexao.execute(
                    select(reservas).where(reservas.c.id == 1)
                ).mappings().one()
            )

    def listar_eventos(self):
        with self.engine.connect() as conexao:
            return [
                dict(evento)
                for evento in conexao.execute(
                    select(auditoria_reservas)
                    .order_by(auditoria_reservas.c.id)
                ).mappings().all()
            ]

    def conferir_sem_alteracoes(self):
        reserva = self.buscar_reserva()

        self.assertEqual(
            reserva["finalidade"],
            "Finalidade original",
        )
        self.assertEqual(reserva["inicio"], self.inicio)
        self.assertEqual(reserva["fim"], self.fim)
        self.assertEqual(self.listar_eventos(), [])

    def test_get_exige_login(self):
        resposta = self.cliente.get(self.endereco)

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))
        self.conferir_sem_alteracoes()

    def test_post_exige_login_com_csrf_valido(self):
        self.preparar_sessao(usuario_id=None)

        resposta = self.cliente.post(
            self.endereco,
            data=self.dados(),
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))
        self.conferir_sem_alteracoes()

    def test_dono_abre_formulario_preenchido(self):
        self.preparar_sessao()

        resposta = self.cliente.get(self.endereco)
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Editar reserva nº 1", pagina)
        self.assertIn("Finalidade original", pagina)
        self.assertIn(
            self.inicio.strftime("%Y-%m-%dT%H:%M"),
            pagina,
        )
        self.assertIn('name="csrf_token"', pagina)
        self.assertIn(self.token, pagina)
        self.conferir_sem_alteracoes()

    def test_edicao_valida_redireciona_e_registra_auditoria(self):
        self.preparar_sessao()

        resposta = self.cliente.post(
            self.endereco,
            data=self.dados(),
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/reservas"))
        self.assertEqual(
            self.buscar_reserva()["finalidade"],
            "Finalidade atualizada",
        )

        eventos = self.listar_eventos()

        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]["acao"], "ALTERACAO")
        self.assertEqual(eventos[0]["usuario_id"], 1)

        detalhes = json.loads(eventos[0]["detalhes"])

        self.assertEqual(
            detalhes["antes"]["finalidade"],
            "Finalidade original",
        )
        self.assertEqual(
            detalhes["depois"]["finalidade"],
            "Finalidade atualizada",
        )

        with self.cliente.session_transaction() as sessao:
            self.assertIn(
                "alterada com sucesso",
                sessao["mensagem_reserva"],
            )

    def test_outro_usuario_nao_acessa_nem_altera(self):
        self.preparar_sessao(usuario_id=2)

        resposta_get = self.cliente.get(self.endereco)
        resposta_post = self.cliente.post(
            self.endereco,
            data=self.dados(),
        )

        self.assertEqual(resposta_get.status_code, 404)
        self.assertEqual(resposta_post.status_code, 404)
        self.assertNotIn(
            "Finalidade original",
            resposta_get.get_data(as_text=True),
        )
        self.conferir_sem_alteracoes()

    def test_reserva_inexistente_retorna_404(self):
        self.preparar_sessao()

        for metodo in ("GET", "POST"):
            with self.subTest(metodo=metodo):
                resposta = self.cliente.open(
                    "/reservas/999/editar",
                    method=metodo,
                    data=self.dados() if metodo == "POST" else None,
                )

                self.assertEqual(resposta.status_code, 404)

        self.conferir_sem_alteracoes()

    def test_post_sem_csrf_e_recusado(self):
        self.preparar_sessao()
        dados = self.dados()
        dados.pop("csrf_token")

        resposta = self.cliente.post(
            self.endereco,
            data=dados,
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertIn(
            "Formulário expirado",
            resposta.get_data(as_text=True),
        )
        self.conferir_sem_alteracoes()

    def test_post_com_csrf_incorreto_e_recusado(self):
        self.preparar_sessao()

        resposta = self.cliente.post(
            self.endereco,
            data=self.dados(csrf_token="token-incorreto"),
        )

        self.assertEqual(resposta.status_code, 400)
        self.conferir_sem_alteracoes()

    def test_dados_invalidos_preservam_formulario_e_banco(self):
        self.preparar_sessao()

        resposta = self.cliente.post(
            self.endereco,
            data=self.dados(
                fim=self.inicio.strftime("%Y-%m-%dT%H:%M"),
            ),
        )
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("O término deve ser posterior ao início.", pagina)
        self.assertIn("Finalidade atualizada", pagina)
        self.conferir_sem_alteracoes()

    def test_reserva_cancelada_nao_pode_ser_editada(self):
        self.preparar_sessao()

        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == 1)
                .values(status="CANCELADA")
            )

        for metodo in ("GET", "POST"):
            with self.subTest(metodo=metodo):
                resposta = self.cliente.open(
                    self.endereco,
                    method=metodo,
                    data=self.dados() if metodo == "POST" else None,
                )

                self.assertEqual(resposta.status_code, 400)

        self.assertEqual(
            self.buscar_reserva()["status"],
            "CANCELADA",
        )
        self.conferir_sem_alteracoes()

    def test_reserva_iniciada_nao_pode_ser_editada(self):
        self.preparar_sessao()
        inicio_passado = datetime.now() - timedelta(minutes=30)

        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == 1)
                .values(inicio=inicio_passado)
            )

        for metodo in ("GET", "POST"):
            with self.subTest(metodo=metodo):
                resposta = self.cliente.open(
                    self.endereco,
                    method=metodo,
                    data=self.dados() if metodo == "POST" else None,
                )

                self.assertEqual(resposta.status_code, 400)

        reserva = self.buscar_reserva()

        self.assertEqual(reserva["inicio"], inicio_passado)
        self.assertEqual(reserva["finalidade"], "Finalidade original")
        self.assertEqual(self.listar_eventos(), [])

    def test_usuario_inativo_perde_acesso(self):
        self.preparar_sessao()

        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 1)
                .values(ativo=False)
            )

        resposta = self.cliente.get(self.endereco)

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith("/login"))

        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

        self.conferir_sem_alteracoes()


if __name__ == "__main__":
    unittest.main()