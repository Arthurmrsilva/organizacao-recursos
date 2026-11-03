import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, insert, select, update

from banco import (
    auditoria_reservas,
    conflitos_reservas,
    metadata,
    notificacoes,
    recursos,
    reservas,
    usuarios,
)
from servico_reservas import avaliar_reserva, criar_reserva


class TestAprovacoes(unittest.TestCase):
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

            conexao.execute(
                insert(recursos).values(
                    id=1,
                    nome="Professor de teste",
                    tipo="PROFESSOR",
                    localizacao="Bloco A",
                    competencia="Python",
                    restrito=False,
                    ativo=True,
                    responsavel_id=2,
                )
            )

        self.inicio = (
            datetime.now() + timedelta(days=7)
        ).replace(second=0, microsecond=0)

        self.dados = {
            "recurso_id": "1",
            "inicio": self.inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": (
                self.inicio + timedelta(hours=1)
            ).strftime("%Y-%m-%dT%H:%M"),
            "finalidade": "Teste de aprovação",
        }

        self.reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados,
        )

    def consultar_reserva(self):
        with self.engine.connect() as conexao:
            return dict(
                conexao.execute(
                    select(reservas).where(
                        reservas.c.id == self.reserva_id
                    )
                ).mappings().one()
            )

    def listar_conflitos(self):
        with self.engine.connect() as conexao:
            return [
                dict(registro)
                for registro in conexao.execute(
                    select(conflitos_reservas)
                    .order_by(conflitos_reservas.c.id)
                ).mappings().all()
            ]

    def listar_eventos_e_notificacoes(self):
        with self.engine.connect() as conexao:
            eventos = conexao.execute(
                select(auditoria_reservas)
                .order_by(auditoria_reservas.c.id)
            ).mappings().all()

            avisos = conexao.execute(
                select(notificacoes)
                .order_by(notificacoes.c.id)
            ).mappings().all()

        return eventos, avisos

    def conferir_recusa(
        self,
        usuario_id,
        decisao,
        mensagem,
    ):
        original = self.consultar_reserva()
        eventos_antes = self.listar_eventos_e_notificacoes()
        conflitos_antes = self.listar_conflitos()

        with self.assertRaisesRegex(ValueError, mensagem):
            avaliar_reserva(
                self.engine,
                usuario_id,
                self.reserva_id,
                decisao,
            )

        self.assertEqual(self.consultar_reserva(), original)
        self.assertEqual(
            self.listar_eventos_e_notificacoes(),
            eventos_antes,
        )
        self.assertEqual(
            self.listar_conflitos(),
            conflitos_antes,
        )

    def test_professor_aguarda_aprovacao(self):
        self.assertEqual(
            self.consultar_reserva()["status"],
            "SOLICITADA",
        )
        self.assertEqual(self.listar_conflitos(), [])

    def test_responsavel_vinculado_pode_aprovar(self):
        original = self.consultar_reserva()

        avaliar_reserva(
            self.engine, 2, self.reserva_id, "APROVADA"
        )

        self.assertEqual(
            self.consultar_reserva(),
            {**original, "status": "APROVADA"},
        )
        self.assertEqual(self.listar_conflitos(), [])

    def test_responsavel_vinculado_pode_rejeitar(self):
        original = self.consultar_reserva()

        avaliar_reserva(
            self.engine, 2, self.reserva_id, "REJEITADA"
        )

        self.assertEqual(
            self.consultar_reserva(),
            {**original, "status": "REJEITADA"},
        )
        self.assertEqual(self.listar_conflitos(), [])

    def test_outro_responsavel_nao_pode_avaliar(self):
        for decisao in ("APROVADA", "REJEITADA"):
            with self.subTest(decisao=decisao):
                self.conferir_recusa(
                    3,
                    decisao,
                    "não é o responsável",
                )

    def test_outros_perfis_nao_podem_avaliar(self):
        for usuario_id in (1, 4):
            for decisao in ("APROVADA", "REJEITADA"):
                with self.subTest(
                    usuario_id=usuario_id,
                    decisao=decisao,
                ):
                    self.conferir_recusa(
                        usuario_id,
                        decisao,
                        "Somente um responsável",
                    )

    def test_responsavel_inativo_nao_pode_avaliar(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 2)
                .values(ativo=False)
            )

        self.conferir_recusa(
            2,
            "APROVADA",
            "Somente um responsável",
        )

    def test_decisao_invalida_nao_altera_reserva(self):
        self.conferir_recusa(
            2,
            "CONCLUIDA",
            "decisão válida",
        )

    def test_nao_avaliar_reserva_fora_do_estado_solicitada(self):
        for status in (
            "APROVADA",
            "REJEITADA",
            "CANCELADA",
            "EM_USO",
            "CONCLUIDA",
            "NAO_COMPARECEU",
        ):
            with self.subTest(status=status):
                with self.engine.begin() as conexao:
                    conexao.execute(
                        update(reservas)
                        .where(reservas.c.id == self.reserva_id)
                        .values(status=status)
                    )

                self.conferir_recusa(
                    2,
                    "APROVADA",
                    "aguardando aprovação",
                )

    def test_nao_avaliar_reserva_que_ja_comecou(self):
        agora = datetime.now()

        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == self.reserva_id)
                .values(
                    inicio=agora - timedelta(hours=1),
                    fim=agora + timedelta(hours=1),
                )
            )

        for decisao in ("APROVADA", "REJEITADA"):
            with self.subTest(decisao=decisao):
                self.conferir_recusa(
                    2,
                    decisao,
                    "prazo",
                )

    def test_recurso_inativo_nao_permite_aprovacao(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(ativo=False)
            )

        self.conferir_recusa(
            2,
            "APROVADA",
            "recurso inativo",
        )

    def test_rejeicao_libera_horario(self):
        avaliar_reserva(
            self.engine, 2, self.reserva_id, "REJEITADA"
        )

        nova_id = criar_reserva(self.engine, 1, self.dados)

        with self.engine.connect() as conexao:
            nova = conexao.execute(
                select(reservas).where(
                    reservas.c.id == nova_id
                )
            ).mappings().one()

        self.assertNotEqual(nova_id, self.reserva_id)
        self.assertEqual(nova["status"], "SOLICITADA")
        self.assertEqual(
            self.consultar_reserva()["status"],
            "REJEITADA",
        )
        self.assertEqual(self.listar_conflitos(), [])

    def test_aprovacao_bloqueia_conflito_existente(self):
        # Simula um conflito já presente no banco.
        # A criação normal impediria essa sobreposição.
        with self.engine.begin() as conexao:
            resultado = conexao.execute(
                insert(reservas).values(
                    recurso_id=1,
                    usuario_id=1,
                    inicio=self.inicio,
                    fim=self.inicio + timedelta(hours=1),
                    finalidade="Conflito de teste",
                    status="APROVADA",
                )
            )
            outra_reserva_id = resultado.inserted_primary_key[0]

            reservas_antes = conexao.execute(
                select(reservas).order_by(reservas.c.id)
            ).mappings().all()

        eventos_antes = self.listar_eventos_e_notificacoes()
        antes = datetime.now()

        with self.assertRaisesRegex(
            ValueError,
            "Existe outra reserva",
        ):
            avaliar_reserva(
                self.engine,
                2,
                self.reserva_id,
                "APROVADA",
            )

        depois = datetime.now()

        with self.engine.connect() as conexao:
            reservas_depois = conexao.execute(
                select(reservas).order_by(reservas.c.id)
            ).mappings().all()

        # Nenhuma das reservas pode ser alterada.
        self.assertEqual(reservas_depois, reservas_antes)
        self.assertEqual(
            self.consultar_reserva()["status"],
            "SOLICITADA",
        )

        # A tentativa recusada não gera aprovação nem notificação.
        self.assertEqual(
            self.listar_eventos_e_notificacoes(),
            eventos_antes,
        )

        conflitos = self.listar_conflitos()
        self.assertEqual(len(conflitos), 1)

        conflito = conflitos[0]

        self.assertEqual(conflito["operacao"], "APROVACAO")

        # Registra quem tentou aprovar, não o solicitante.
        self.assertEqual(conflito["usuario_id"], 2)
        self.assertEqual(conflito["recurso_id"], 1)
        self.assertEqual(
            conflito["reserva_conflitante_id"],
            outra_reserva_id,
        )
        self.assertEqual(conflito["inicio"], self.inicio)
        self.assertEqual(
            conflito["fim"],
            self.inicio + timedelta(hours=1),
        )
        self.assertGreaterEqual(conflito["criado_em"], antes)
        self.assertLessEqual(conflito["criado_em"], depois)


if __name__ == "__main__":
    unittest.main()