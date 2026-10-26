import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select, update

from banco import (
    auditoria_reservas,
    manutencoes,
    metadata,
    recursos,
    reservas,
    usuarios,
)
from servico_materiais import (
    registrar_devolucao,
    registrar_retirada,
)
from servico_reservas import registrar_auditoria


class TestMateriais(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        # Relógio fixo para os testes não dependerem da hora real.
        self.agora = datetime(2026, 11, 10, 14, 30)

        relogio = patch("servico_materiais.datetime")
        self.relogio = relogio.start()
        self.relogio.now.return_value = self.agora
        self.addCleanup(relogio.stop)

        with self.engine.begin() as conexao:
            for usuario_id, perfil in (
                (1, "ADMIN"),
                (2, "RESPONSAVEL"),
                (3, "SOLICITANTE"),
                (4, "RESPONSAVEL"),
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
                    nome="Projetor",
                    tipo="MATERIAL",
                    localizacao="Secretaria",
                    responsavel_id=2,
                    restrito=False,
                    ativo=True,
                )
            )

            conexao.execute(
                insert(reservas).values(
                    id=1,
                    recurso_id=1,
                    usuario_id=3,
                    inicio=self.agora - timedelta(minutes=30),
                    fim=self.agora + timedelta(minutes=30),
                    finalidade="Apresentação",
                    status="APROVADA",
                )
            )

    def alterar_reserva(self, **valores):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == 1)
                .values(**valores)
            )

    def alterar_recurso(self, **valores):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(**valores)
            )

    def situacao(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(reservas.c.status)
                .where(reservas.c.id == 1)
            ).scalar_one()

    def eventos(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(auditoria_reservas)
                .order_by(auditoria_reservas.c.id)
            ).mappings().all()

    def test_admin_registra_retirada_e_devolucao(self):
        registrar_retirada(self.engine, 1, 1)
        self.assertEqual(self.situacao(), "EM_USO")

        registrar_devolucao(self.engine, 1, 1)
        self.assertEqual(self.situacao(), "CONCLUIDA")

        eventos = self.eventos()

        self.assertEqual(len(eventos), 2)
        self.assertEqual(eventos[0]["acao"], "RETIRADA")
        self.assertEqual(eventos[0]["status_anterior"], "APROVADA")
        self.assertEqual(eventos[0]["status_novo"], "EM_USO")
        self.assertEqual(eventos[1]["acao"], "DEVOLUCAO")
        self.assertEqual(eventos[1]["status_anterior"], "EM_USO")
        self.assertEqual(eventos[1]["status_novo"], "CONCLUIDA")

        for evento in eventos:
            self.assertEqual(evento["reserva_id"], 1)
            self.assertEqual(evento["usuario_id"], 1)
            self.assertIsInstance(evento["data_hora"], datetime)

    def test_responsavel_vinculado_pode_movimentar(self):
        registrar_retirada(self.engine, 2, 1)
        registrar_devolucao(self.engine, 2, 1)

        self.assertEqual(self.situacao(), "CONCLUIDA")
        self.assertEqual(
            [evento["usuario_id"] for evento in self.eventos()],
            [2, 2],
        )

    def test_solicitante_nao_pode_movimentar(self):
        for operacao, status in (
            (registrar_retirada, "APROVADA"),
            (registrar_devolucao, "EM_USO"),
        ):
            with self.subTest(operacao=operacao.__name__):
                self.alterar_reserva(status=status)

                with self.assertRaisesRegex(
                    ValueError, "Somente administradores"
                ):
                    operacao(self.engine, 3, 1)

                self.assertEqual(self.situacao(), status)
                self.assertEqual(self.eventos(), [])

    def test_responsavel_sem_vinculo_nao_pode_movimentar(self):
        for operacao, status in (
            (registrar_retirada, "APROVADA"),
            (registrar_devolucao, "EM_USO"),
        ):
            with self.subTest(operacao=operacao.__name__):
                self.alterar_reserva(status=status)

                with self.assertRaisesRegex(
                    ValueError, "não é o responsável"
                ):
                    operacao(self.engine, 4, 1)

                self.assertEqual(self.situacao(), status)
                self.assertEqual(self.eventos(), [])

    def test_usuario_inativo_nao_pode_movimentar(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 1)
                .values(ativo=False)
            )

        for operacao, status in (
            (registrar_retirada, "APROVADA"),
            (registrar_devolucao, "EM_USO"),
        ):
            with self.subTest(operacao=operacao.__name__):
                self.alterar_reserva(status=status)

                with self.assertRaises(ValueError):
                    operacao(self.engine, 1, 1)

                self.assertEqual(self.situacao(), status)
                self.assertEqual(self.eventos(), [])

    def test_reserva_inexistente_nao_gera_auditoria(self):
        for operacao in (registrar_retirada, registrar_devolucao):
            with self.subTest(operacao=operacao.__name__):
                with self.assertRaisesRegex(
                    ValueError, "Reserva não encontrada"
                ):
                    operacao(self.engine, 1, 999)

        self.assertEqual(self.eventos(), [])

    def test_sala_e_professor_nao_permitem_movimentacao(self):
        for tipo in ("SALA", "PROFESSOR"):
            for operacao, status in (
                (registrar_retirada, "APROVADA"),
                (registrar_devolucao, "EM_USO"),
            ):
                with self.subTest(
                    tipo=tipo,
                    operacao=operacao.__name__,
                ):
                    self.alterar_recurso(tipo=tipo)
                    self.alterar_reserva(status=status)

                    with self.assertRaisesRegex(
                        ValueError, "exclusiva para materiais"
                    ):
                        operacao(self.engine, 1, 1)

                    self.assertEqual(self.situacao(), status)
                    self.assertEqual(self.eventos(), [])

    def test_retirada_exige_reserva_aprovada(self):
        for status in (
            "SOLICITADA",
            "EM_USO",
            "CONCLUIDA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        ):
            with self.subTest(status=status):
                self.alterar_reserva(status=status)

                with self.assertRaisesRegex(
                    ValueError, "Somente reservas aprovadas"
                ):
                    registrar_retirada(self.engine, 1, 1)

                self.assertEqual(self.situacao(), status)
                self.assertEqual(self.eventos(), [])

    def test_retirada_antes_do_inicio_e_bloqueada(self):
        self.alterar_reserva(
            inicio=self.agora + timedelta(minutes=1),
            fim=self.agora + timedelta(hours=1),
        )

        with self.assertRaisesRegex(
            ValueError, "a partir do início"
        ):
            registrar_retirada(self.engine, 1, 1)

        self.assertEqual(self.situacao(), "APROVADA")
        self.assertEqual(self.eventos(), [])

    def test_retirada_no_inicio_e_permitida(self):
        self.alterar_reserva(inicio=self.agora)

        registrar_retirada(self.engine, 1, 1)

        self.assertEqual(self.situacao(), "EM_USO")
        self.assertEqual(len(self.eventos()), 1)

    def test_retirada_no_termino_ou_depois_e_bloqueada(self):
        for fim in (
            self.agora,
            self.agora - timedelta(minutes=1),
        ):
            with self.subTest(fim=fim):
                self.alterar_reserva(fim=fim)

                with self.assertRaisesRegex(
                    ValueError, "período para retirada já terminou"
                ):
                    registrar_retirada(self.engine, 1, 1)

                self.assertEqual(self.situacao(), "APROVADA")
                self.assertEqual(self.eventos(), [])

    def test_material_inativo_nao_permite_retirada(self):
        self.alterar_recurso(ativo=False)

        with self.assertRaisesRegex(ValueError, "material inativo"):
            registrar_retirada(self.engine, 1, 1)

        self.assertEqual(self.situacao(), "APROVADA")
        self.assertEqual(self.eventos(), [])

    def test_manutencao_impede_retirada(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                insert(manutencoes).values(
                    recurso_id=1,
                    usuario_id=1,
                    inicio=self.agora,
                    fim=self.agora + timedelta(hours=1),
                    motivo="Reparo",
                    criado_em=self.agora,
                    ativo=True,
                )
            )

        with self.assertRaisesRegex(ValueError, "em manutenção"):
            registrar_retirada(self.engine, 1, 1)

        self.assertEqual(self.situacao(), "APROVADA")
        self.assertEqual(self.eventos(), [])

    def test_material_nao_devolvido_impede_nova_retirada(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                insert(reservas).values(
                    recurso_id=1,
                    usuario_id=3,
                    inicio=self.agora - timedelta(hours=3),
                    fim=self.agora - timedelta(hours=2),
                    finalidade="Uso anterior atrasado",
                    status="EM_USO",
                )
            )

        with self.assertRaisesRegex(ValueError, "ainda está em uso"):
            registrar_retirada(self.engine, 1, 1)

        self.assertEqual(self.situacao(), "APROVADA")
        self.assertEqual(self.eventos(), [])

    def test_devolucao_exige_material_em_uso(self):
        for status in (
            "SOLICITADA",
            "APROVADA",
            "CONCLUIDA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        ):
            with self.subTest(status=status):
                self.alterar_reserva(status=status)

                with self.assertRaisesRegex(
                    ValueError, "Somente materiais em uso"
                ):
                    registrar_devolucao(self.engine, 1, 1)

                self.assertEqual(self.situacao(), status)
                self.assertEqual(self.eventos(), [])

    def test_devolucao_atrasada_de_material_inativo_e_permitida(self):
        self.alterar_reserva(
            status="EM_USO",
            fim=self.agora - timedelta(minutes=1),
        )
        self.alterar_recurso(ativo=False)

        registrar_devolucao(self.engine, 1, 1)

        self.assertEqual(self.situacao(), "CONCLUIDA")
        self.assertEqual(self.eventos()[0]["acao"], "DEVOLUCAO")

    def test_falha_na_auditoria_desfaz_movimentacao(self):
        def gravar_e_falhar(**argumentos):
            registrar_auditoria(**argumentos)
            raise RuntimeError("Falha simulada")

        for operacao, status in (
            (registrar_retirada, "APROVADA"),
            (registrar_devolucao, "EM_USO"),
        ):
            with self.subTest(operacao=operacao.__name__):
                self.alterar_reserva(status=status)

                with patch(
                    "servico_materiais.registrar_auditoria",
                    side_effect=gravar_e_falhar,
                ):
                    with self.assertRaisesRegex(
                        RuntimeError, "Falha simulada"
                    ):
                        operacao(self.engine, 1, 1)

                self.assertEqual(self.situacao(), status)
                self.assertEqual(self.eventos(), [])


if __name__ == "__main__":
    unittest.main()