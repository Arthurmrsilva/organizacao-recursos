import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select

import servico_reservas as servico
from banco import (
    auditoria_reservas,
    metadata,
    recursos,
    reservas,
    usuarios,
)


class TestAuditoria(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        with self.engine.begin() as conexao:
            for usuario_id, perfil in (
                (1, "SOLICITANTE"),
                (2, "RESPONSAVEL"),
                (3, "SOLICITANTE"),
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

            for recurso_id, restrito in ((1, False), (2, True)):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=f"Sala {recurso_id}",
                        tipo="SALA",
                        localizacao="Bloco A",
                        capacidade=30,
                        restrito=restrito,
                        ativo=True,
                        responsavel_id=2,
                    )
                )

        inicio = datetime.now() + timedelta(days=7)

        self.dados = {
            "recurso_id": "1",
            "inicio": inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": (
                inicio + timedelta(hours=1)
            ).strftime("%Y-%m-%dT%H:%M"),
            "finalidade": "Teste de auditoria",
        }

    def tearDown(self):
        self.engine.dispose()
        self.pasta.cleanup()

    def listar(self, tabela):
        with self.engine.connect() as conexao:
            return [
                dict(registro)
                for registro in conexao.execute(
                    select(tabela).order_by(tabela.c.id)
                ).mappings().all()
            ]

    def criar(self, restrita=False):
        dados = {
            **self.dados,
            "recurso_id": "2" if restrita else "1",
        }
        return servico.criar_reserva(self.engine, 1, dados)

    def conferir_evento(
        self,
        evento,
        reserva_id,
        usuario_id,
        acao,
        anterior,
        novo,
    ):
        self.assertEqual(evento["reserva_id"], reserva_id)
        self.assertEqual(evento["usuario_id"], usuario_id)
        self.assertEqual(evento["acao"], acao)
        self.assertEqual(evento["status_anterior"], anterior)
        self.assertEqual(evento["status_novo"], novo)
        self.assertIsInstance(evento["data_hora"], datetime)

    def test_criacao_registra_status_inicial(self):
        for restrita, status in (
            (False, "APROVADA"),
            (True, "SOLICITADA"),
        ):
            with self.subTest(restrita=restrita):
                antes = datetime.now()
                reserva_id = self.criar(restrita)
                depois = datetime.now()

                eventos = self.listar(auditoria_reservas)
                evento = eventos[-1]

                self.assertEqual(
                    len([
                        item for item in eventos
                        if item["reserva_id"] == reserva_id
                    ]),
                    1,
                )
                self.conferir_evento(
                    evento,
                    reserva_id,
                    1,
                    "CRIACAO",
                    None,
                    status,
                )
                self.assertLessEqual(antes, evento["data_hora"])
                self.assertLessEqual(evento["data_hora"], depois)

    def test_cancelamento_preserva_historico(self):
        reserva_id = self.criar()
        evento_criacao = self.listar(auditoria_reservas)[0]

        servico.cancelar_reserva(self.engine, 1, reserva_id)

        eventos = self.listar(auditoria_reservas)

        self.assertEqual(len(eventos), 2)
        self.assertEqual(eventos[0], evento_criacao)
        self.conferir_evento(
            eventos[1],
            reserva_id,
            1,
            "CANCELAMENTO",
            "APROVADA",
            "CANCELADA",
        )

    def test_avaliacao_registra_responsavel(self):
        for decisao, acao in (
            ("APROVADA", "APROVACAO"),
            ("REJEITADA", "REJEICAO"),
        ):
            with self.subTest(decisao=decisao):
                # Cada cenário usa seu próprio banco temporário.
                # A primeira reserva é cancelada após a aprovação
                # para liberar o período do segundo cenário.
                reserva_id = self.criar(restrita=True)

                servico.avaliar_reserva(
                    self.engine, 2, reserva_id, decisao
                )

                eventos = [
                    evento
                    for evento in self.listar(auditoria_reservas)
                    if evento["reserva_id"] == reserva_id
                ]

                self.assertEqual(len(eventos), 2)
                self.conferir_evento(
                    eventos[1],
                    reserva_id,
                    2,
                    acao,
                    "SOLICITADA",
                    decisao,
                )

                if decisao == "APROVADA":
                    servico.cancelar_reserva(
                        self.engine, 1, reserva_id
                    )

    def test_tentativa_negada_nao_registra_mudanca(self):
        reserva_id = self.criar()
        eventos_antes = self.listar(auditoria_reservas)
        reservas_antes = self.listar(reservas)

        with self.assertRaises(ValueError):
            servico.cancelar_reserva(
                self.engine, 3, reserva_id
            )

        self.assertEqual(
            self.listar(auditoria_reservas), eventos_antes
        )
        self.assertEqual(
            self.listar(reservas), reservas_antes
        )

    def test_falha_na_auditoria_desfaz_criacao(self):
        registrar_original = servico.registrar_auditoria

        def registrar_e_falhar(*args, **kwargs):
            registrar_original(*args, **kwargs)
            raise RuntimeError("Falha simulada de auditoria")

        with patch.object(
            servico,
            "registrar_auditoria",
            side_effect=registrar_e_falhar,
        ):
            with self.assertRaisesRegex(
                RuntimeError, "Falha simulada"
            ):
                self.criar()

        self.assertEqual(self.listar(reservas), [])
        self.assertEqual(self.listar(auditoria_reservas), [])

    def test_falha_na_auditoria_desfaz_mudancas_de_status(self):
        reserva_id = self.criar(restrita=True)
        registrar_original = servico.registrar_auditoria

        def registrar_e_falhar(*args, **kwargs):
            registrar_original(*args, **kwargs)
            raise RuntimeError("Falha simulada de auditoria")

        operacoes = (
            lambda: servico.cancelar_reserva(
                self.engine, 1, reserva_id
            ),
            lambda: servico.avaliar_reserva(
                self.engine, 2, reserva_id, "APROVADA"
            ),
            lambda: servico.avaliar_reserva(
                self.engine, 2, reserva_id, "REJEITADA"
            ),
        )

        for indice, operacao in enumerate(operacoes):
            with self.subTest(operacao=indice):
                reservas_antes = self.listar(reservas)
                eventos_antes = self.listar(auditoria_reservas)

                with patch.object(
                    servico,
                    "registrar_auditoria",
                    side_effect=registrar_e_falhar,
                ):
                    with self.assertRaisesRegex(
                        RuntimeError, "Falha simulada"
                    ):
                        operacao()

                self.assertEqual(
                    self.listar(reservas), reservas_antes
                )
                self.assertEqual(
                    self.listar(auditoria_reservas), eventos_antes
                )


if __name__ == "__main__":
    unittest.main()