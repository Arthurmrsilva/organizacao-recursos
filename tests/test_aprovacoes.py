import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, insert, select, update

from banco import metadata, recursos, reservas, usuarios
from servico_reservas import avaliar_reserva, criar_reserva


class TestAprovacoes(unittest.TestCase):
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

    def tearDown(self):
        self.engine.dispose()
        self.pasta.cleanup()

    def consultar_reserva(self):
        with self.engine.connect() as conexao:
            return dict(
                conexao.execute(
                    select(reservas).where(
                        reservas.c.id == self.reserva_id
                    )
                ).mappings().one()
            )

    def test_professor_aguarda_aprovacao(self):
        self.assertEqual(
            self.consultar_reserva()["status"],
            "SOLICITADA",
        )

    def test_responsavel_vinculado_pode_aprovar(self):
        original = self.consultar_reserva()

        avaliar_reserva(
            self.engine, 2, self.reserva_id, "APROVADA"
        )

        self.assertEqual(
            self.consultar_reserva(),
            {**original, "status": "APROVADA"},
        )

    def test_responsavel_vinculado_pode_rejeitar(self):
        original = self.consultar_reserva()

        avaliar_reserva(
            self.engine, 2, self.reserva_id, "REJEITADA"
        )

        self.assertEqual(
            self.consultar_reserva(),
            {**original, "status": "REJEITADA"},
        )

    def test_outro_responsavel_nao_pode_avaliar(self):
        original = self.consultar_reserva()

        for decisao in ("APROVADA", "REJEITADA"):
            with self.subTest(decisao=decisao):
                with self.assertRaisesRegex(
                    ValueError, "não é o responsável"
                ):
                    avaliar_reserva(
                        self.engine, 3, self.reserva_id, decisao
                    )

                self.assertEqual(
                    self.consultar_reserva(), original
                )

    def test_outros_perfis_nao_podem_avaliar(self):
        original = self.consultar_reserva()

        for usuario_id in (1, 4):
            for decisao in ("APROVADA", "REJEITADA"):
                with self.subTest(
                    usuario_id=usuario_id,
                    decisao=decisao,
                ):
                    with self.assertRaisesRegex(
                        ValueError, "Somente um responsável"
                    ):
                        avaliar_reserva(
                            self.engine,
                            usuario_id,
                            self.reserva_id,
                            decisao,
                        )

                    self.assertEqual(
                        self.consultar_reserva(), original
                    )

    def test_responsavel_inativo_nao_pode_avaliar(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 2)
                .values(ativo=False)
            )

        with self.assertRaisesRegex(
            ValueError, "Somente um responsável"
        ):
            avaliar_reserva(
                self.engine, 2, self.reserva_id, "APROVADA"
            )

        self.assertEqual(
            self.consultar_reserva()["status"],
            "SOLICITADA",
        )

    def test_decisao_invalida_nao_altera_reserva(self):
        with self.assertRaisesRegex(
            ValueError, "decisão válida"
        ):
            avaliar_reserva(
                self.engine, 2, self.reserva_id, "CONCLUIDA"
            )

        self.assertEqual(
            self.consultar_reserva()["status"],
            "SOLICITADA",
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

                with self.assertRaisesRegex(
                    ValueError, "aguardando aprovação"
                ):
                    avaliar_reserva(
                        self.engine, 2, self.reserva_id, "APROVADA"
                    )

                self.assertEqual(
                    self.consultar_reserva()["status"], status
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
                with self.assertRaisesRegex(
                    ValueError, "prazo"
                ):
                    avaliar_reserva(
                        self.engine, 2, self.reserva_id, decisao
                    )

                self.assertEqual(
                    self.consultar_reserva()["status"],
                    "SOLICITADA",
                )

    def test_recurso_inativo_nao_permite_aprovacao(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(ativo=False)
            )

        with self.assertRaisesRegex(
            ValueError, "recurso inativo"
        ):
            avaliar_reserva(
                self.engine, 2, self.reserva_id, "APROVADA"
            )

        self.assertEqual(
            self.consultar_reserva()["status"],
            "SOLICITADA",
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

    def test_aprovacao_bloqueia_conflito_existente(self):
        # Simula um conflito já presente no banco.
        with self.engine.begin() as conexao:
            conexao.execute(
                insert(reservas).values(
                    recurso_id=1,
                    usuario_id=1,
                    inicio=self.inicio,
                    fim=self.inicio + timedelta(hours=1),
                    finalidade="Conflito de teste",
                    status="APROVADA",
                )
            )

        with self.assertRaisesRegex(
            ValueError, "Existe outra reserva"
        ):
            avaliar_reserva(
                self.engine, 2, self.reserva_id, "APROVADA"
            )

        self.assertEqual(
            self.consultar_reserva()["status"],
            "SOLICITADA",
        )


if __name__ == "__main__":
    unittest.main()