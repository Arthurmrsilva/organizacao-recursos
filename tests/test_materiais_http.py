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


class TestMateriaisHTTP(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        agora = datetime.now()

        with self.engine.begin() as conexao:
            for usuario_id, perfil, ativo in (
                (1, "ADMIN", True),
                (2, "RESPONSAVEL", True),
                (3, "RESPONSAVEL", True),
                (4, "SOLICITANTE", True),
                (5, "ADMIN", False),
            ):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuário {usuario_id}",
                        login=f"usuario{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil=perfil,
                        ativo=ativo,
                    )
                )

            for recurso_id, nome, tipo, responsavel_id in (
                (1, "Projetor exclusivo A", "MATERIAL", 2),
                (2, "Projetor exclusivo B", "MATERIAL", 3),
                (3, "Sala exclusiva C", "SALA", 2),
            ):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=nome,
                        tipo=tipo,
                        localizacao="Bloco de teste",
                        capacidade=30 if tipo == "SALA" else None,
                        restrito=False,
                        ativo=True,
                        responsavel_id=responsavel_id,
                    )
                )

            for reserva_id, recurso_id in (
                (1, 1),
                (2, 2),
                (3, 3),
            ):
                conexao.execute(
                    insert(reservas).values(
                        id=reserva_id,
                        recurso_id=recurso_id,
                        usuario_id=4,
                        inicio=agora - timedelta(days=1),
                        fim=agora + timedelta(days=1),
                        finalidade=f"Finalidade exclusiva {reserva_id}",
                        status="APROVADA",
                    )
                )

        substituicao = patch.object(
            aplicativo,
            "engine",
            self.engine,
        )
        substituicao.start()
        self.addCleanup(substituicao.stop)

        self.cliente = aplicativo.app.test_client()

    def autenticar(self, usuario_id):
        # Simula a sessão; o login possui testes próprios.
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["usuario_id"] = usuario_id
            sessao["csrf_token"] = "token-teste"

    def preparar_visitante(self):
        # Permite testar o acesso sem login com CSRF válido.
        with self.cliente.session_transaction() as sessao:
            sessao.clear()
            sessao["csrf_token"] = "token-teste"

    def movimentar(self, reserva_id=1, acao="RETIRADA"):
        return self.cliente.post(
            f"/materiais/{reserva_id}/movimentar",
            data={
                "csrf_token": "token-teste",
                "acao": acao,
            },
        )

    def alterar_reserva(self, reserva_id=1, **valores):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == reserva_id)
                .values(**valores)
            )

    def consultar_reserva(self, reserva_id=1):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(reservas).where(
                    reservas.c.id == reserva_id
                )
            ).mappings().one()

    def consultar_auditoria(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(auditoria_reservas).order_by(
                    auditoria_reservas.c.id
                )
            ).mappings().all()

    def conferir_redirecionamento(self, resposta, destino):
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(resposta.location.endswith(destino))

    def conferir_sem_movimentacao(self):
        self.assertEqual(
            self.consultar_reserva()["status"],
            "APROVADA",
        )
        self.assertEqual(self.consultar_auditoria(), [])

    def conferir_erro_na_sessao(self):
        with self.cliente.session_transaction() as sessao:
            self.assertTrue(sessao.get("erro_material"))
            self.assertNotIn("mensagem_material", sessao)

    def conferir_evento(
        self,
        acao,
        usuario_id,
        status_anterior,
        status_novo,
    ):
        eventos = self.consultar_auditoria()

        self.assertEqual(len(eventos), 1)
        evento = eventos[0]

        self.assertEqual(evento["reserva_id"], 1)
        self.assertEqual(evento["usuario_id"], usuario_id)
        self.assertEqual(evento["acao"], acao)
        self.assertEqual(
            evento["status_anterior"],
            status_anterior,
        )
        self.assertEqual(
            evento["status_novo"],
            status_novo,
        )
        self.assertIsInstance(
            evento["data_hora"],
            datetime,
        )

    def test_listagem_exige_login(self):
        resposta = self.cliente.get("/materiais")

        self.conferir_redirecionamento(
            resposta,
            "/login",
        )

    def test_movimentacao_exige_login(self):
        self.preparar_visitante()

        resposta = self.movimentar()

        self.conferir_redirecionamento(
            resposta,
            "/login",
        )
        self.conferir_sem_movimentacao()

    def test_solicitante_nao_acessa_listagem(self):
        self.autenticar(4)

        resposta = self.cliente.get("/materiais")

        self.assertEqual(resposta.status_code, 403)
        self.assertNotIn(
            "Projetor exclusivo A",
            resposta.get_data(as_text=True),
        )

    def test_solicitante_nao_movimenta_material(self):
        self.autenticar(4)

        resposta = self.movimentar()

        self.assertEqual(resposta.status_code, 403)
        self.conferir_sem_movimentacao()

    def test_usuario_inativo_perde_acesso(self):
        self.autenticar(5)

        resposta = self.cliente.get("/materiais")

        self.conferir_redirecionamento(
            resposta,
            "/login",
        )

        with self.cliente.session_transaction() as sessao:
            self.assertNotIn("usuario_id", sessao)

        self.autenticar(5)
        resposta = self.movimentar()

        self.conferir_redirecionamento(
            resposta,
            "/login",
        )
        self.conferir_sem_movimentacao()

    def test_admin_lista_materiais_de_todos_responsaveis(self):
        self.autenticar(1)

        resposta = self.cliente.get("/materiais")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Projetor exclusivo A", pagina)
        self.assertIn("Projetor exclusivo B", pagina)
        self.assertNotIn("Sala exclusiva C", pagina)

    def test_responsavel_lista_apenas_seus_materiais(self):
        for usuario_id, nome_proprio, nome_alheio in (
            (2, "Projetor exclusivo A", "Projetor exclusivo B"),
            (3, "Projetor exclusivo B", "Projetor exclusivo A"),
        ):
            with self.subTest(usuario_id=usuario_id):
                self.autenticar(usuario_id)

                resposta = self.cliente.get("/materiais")
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)
                self.assertIn(nome_proprio, pagina)
                self.assertNotIn(nome_alheio, pagina)
                self.assertNotIn("Sala exclusiva C", pagina)

    def test_listagem_filtra_situacoes(self):
        self.autenticar(1)

        for status in (
            "SOLICITADA",
            "APROVADA",
            "EM_USO",
            "CONCLUIDA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        ):
            with self.subTest(status=status):
                self.alterar_reserva(status=status)

                resposta = self.cliente.get("/materiais")
                pagina = resposta.get_data(as_text=True)

                self.assertEqual(resposta.status_code, 200)

                if status in ("APROVADA", "EM_USO"):
                    self.assertIn(
                        "Projetor exclusivo A",
                        pagina,
                    )
                else:
                    self.assertNotIn(
                        "Projetor exclusivo A",
                        pagina,
                    )

    def test_material_em_uso_atrasado_continua_visivel(self):
        agora = datetime.now()

        self.alterar_reserva(
            status="EM_USO",
            inicio=agora - timedelta(days=2),
            fim=agora - timedelta(days=1),
        )
        self.autenticar(2)

        resposta = self.cliente.get("/materiais")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(
            "Projetor exclusivo A",
            resposta.get_data(as_text=True),
        )
        self.assertEqual(
            self.consultar_reserva()["status"],
            "EM_USO",
        )

    def test_admin_registra_retirada_com_auditoria(self):
        self.autenticar(1)

        resposta = self.movimentar()

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.assertEqual(
            self.consultar_reserva()["status"],
            "EM_USO",
        )
        self.conferir_evento(
            "RETIRADA",
            1,
            "APROVADA",
            "EM_USO",
        )

        with self.cliente.session_transaction() as sessao:
            self.assertIn(
                "Retirada",
                sessao["mensagem_material"],
            )

    def test_responsavel_vinculado_registra_retirada(self):
        self.autenticar(2)

        resposta = self.movimentar()

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.assertEqual(
            self.consultar_reserva()["status"],
            "EM_USO",
        )
        self.conferir_evento(
            "RETIRADA",
            2,
            "APROVADA",
            "EM_USO",
        )

    def test_devolucao_atrasada_com_recurso_inativo(self):
        agora = datetime.now()

        self.alterar_reserva(
            status="EM_USO",
            inicio=agora - timedelta(days=2),
            fim=agora - timedelta(days=1),
        )

        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(ativo=False)
            )

        self.autenticar(2)

        resposta = self.movimentar(acao="DEVOLUCAO")

        self.conferir_redirecionamento(
            resposta,
            "/materiais",
        )
        self.assertEqual(
            self.consultar_reserva()["status"],
            "CONCLUIDA",
        )
        self.conferir_evento(
            "DEVOLUCAO",
            2,
            "EM_USO",
            "CONCLUIDA",
        )

        with self.cliente.session_transaction() as sessao:
            self.assertIn(
                "Devolução",
                sessao["mensagem_material"],
            )

        pagina = self.cliente.get(
            "/materiais"
        ).get_data(as_text=True)

        self.assertNotIn("Projetor exclusivo A", pagina)

    def test_responsavel_nao_movimenta_material_alheio(self):
        for acao, status in (
            ("RETIRADA", "APROVADA"),
            ("DEVOLUCAO", "EM_USO"),
        ):
            with self.subTest(acao=acao):
                self.alterar_reserva(status=status)
                self.autenticar(3)

                resposta = self.movimentar(acao=acao)

                self.conferir_redirecionamento(
                    resposta,
                    "/materiais",
                )
                self.assertEqual(
                    self.consultar_reserva()["status"],
                    status,
                )
                self.assertEqual(
                    self.consultar_auditoria(),
                    [],
                )
                self.conferir_erro_na_sessao()

    def test_csrf_ausente_ou_incorreto_bloqueia_movimentacao(self):
        for acao in ("RETIRADA", "DEVOLUCAO"):
            for token in (None, "token-incorreto"):
                with self.subTest(acao=acao, token=token):
                    self.autenticar(1)
                    dados = {"acao": acao}

                    if token is not None:
                        dados["csrf_token"] = token

                    resposta = self.cliente.post(
                        "/materiais/1/movimentar",
                        data=dados,
                    )

                    self.assertEqual(
                        resposta.status_code,
                        400,
                    )
                    self.conferir_sem_movimentacao()

    def test_get_nao_realiza_movimentacao(self):
        self.autenticar(1)

        resposta = self.cliente.get(
            "/materiais/1/movimentar",
            query_string={"acao": "RETIRADA"},
        )

        self.assertEqual(resposta.status_code, 405)
        self.conferir_sem_movimentacao()

    def test_acao_invalida_nao_altera_reserva(self):
        for acao in ("", "APAGAR", "retirada"):
            with self.subTest(acao=acao):
                self.autenticar(1)

                resposta = self.movimentar(acao=acao)

                self.conferir_redirecionamento(
                    resposta,
                    "/materiais",
                )
                self.conferir_sem_movimentacao()
                self.conferir_erro_na_sessao()

    def test_reserva_inexistente_nao_gera_auditoria(self):
        for acao in ("RETIRADA", "DEVOLUCAO"):
            with self.subTest(acao=acao):
                self.autenticar(1)

                resposta = self.movimentar(
                    reserva_id=999,
                    acao=acao,
                )

                self.conferir_redirecionamento(
                    resposta,
                    "/materiais",
                )
                self.conferir_sem_movimentacao()
                self.conferir_erro_na_sessao()

    def test_estado_incompativel_recusa_operacao(self):
        for acao, status in (
            ("RETIRADA", "SOLICITADA"),
            ("RETIRADA", "CONCLUIDA"),
            ("DEVOLUCAO", "APROVADA"),
            ("DEVOLUCAO", "CANCELADA"),
        ):
            with self.subTest(acao=acao, status=status):
                self.alterar_reserva(status=status)
                self.autenticar(1)

                resposta = self.movimentar(acao=acao)

                self.conferir_redirecionamento(
                    resposta,
                    "/materiais",
                )
                self.assertEqual(
                    self.consultar_reserva()["status"],
                    status,
                )
                self.assertEqual(
                    self.consultar_auditoria(),
                    [],
                )
                self.conferir_erro_na_sessao()


if __name__ == "__main__":
    unittest.main()