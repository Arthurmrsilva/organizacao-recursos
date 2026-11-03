import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, insert, select, update

import servico_materiais
from banco import (
    auditoria_reservas,
    metadata,
    recursos,
    reservas,
    usuarios,
)
from servico_materiais import registrar_nao_comparecimento


class TestNaoComparecimento(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        # Relógio fixo para testar os limites sem depender
        # do horário em que os testes são executados.
        self.agora = datetime(2030, 6, 10, 15, 0)

        relogio = patch.object(
            servico_materiais,
            "datetime",
        )
        self.relogio = relogio.start()
        self.relogio.now.return_value = self.agora
        self.addCleanup(relogio.stop)

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

            conexao.execute(
                insert(recursos).values(
                    id=1,
                    nome="Projetor de teste",
                    tipo="MATERIAL",
                    localizacao="Bloco A",
                    restrito=False,
                    ativo=True,
                    responsavel_id=2,
                )
            )

            conexao.execute(
                insert(reservas).values(
                    id=1,
                    recurso_id=1,
                    usuario_id=4,
                    inicio=self.agora - timedelta(hours=2),
                    fim=self.agora - timedelta(hours=1),
                    finalidade="Apresentação de trabalho",
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

    def consultar_reserva(self):
        with self.engine.connect() as conexao:
            return dict(
                conexao.execute(
                    select(reservas).where(
                        reservas.c.id == 1
                    )
                ).mappings().one()
            )

    def consultar_auditoria(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(auditoria_reservas).order_by(
                    auditoria_reservas.c.id
                )
            ).mappings().all()

    def conferir_registro(self, usuario_id):
        self.assertEqual(
            self.consultar_reserva()["status"],
            "NAO_COMPARECEU",
        )

        eventos = self.consultar_auditoria()

        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]["reserva_id"], 1)
        self.assertEqual(eventos[0]["usuario_id"], usuario_id)
        self.assertEqual(
            eventos[0]["acao"],
            "NAO_COMPARECEU",
        )
        self.assertEqual(
            eventos[0]["status_anterior"],
            "APROVADA",
        )
        self.assertEqual(
            eventos[0]["status_novo"],
            "NAO_COMPARECEU",
        )
        self.assertIsInstance(
            eventos[0]["data_hora"],
            datetime,
        )

    def test_admin_registra_com_auditoria(self):
        antes = self.consultar_reserva()

        registrar_nao_comparecimento(self.engine, 1, 1)

        self.conferir_registro(1)

        depois = self.consultar_reserva()

        for campo in (
            "id",
            "recurso_id",
            "usuario_id",
            "inicio",
            "fim",
            "finalidade",
        ):
            with self.subTest(campo=campo):
                self.assertEqual(
                    antes[campo],
                    depois[campo],
                )

    def test_responsavel_vinculado_registra(self):
        registrar_nao_comparecimento(self.engine, 2, 1)

        self.conferir_registro(2)

    def test_responsavel_alheio_nao_registra(self):
        antes = self.consultar_reserva()

        with self.assertRaises(ValueError):
            registrar_nao_comparecimento(self.engine, 3, 1)

        self.assertEqual(self.consultar_reserva(), antes)
        self.assertEqual(self.consultar_auditoria(), [])

    def test_solicitante_nao_registra(self):
        antes = self.consultar_reserva()

        with self.assertRaises(ValueError):
            registrar_nao_comparecimento(self.engine, 4, 1)

        self.assertEqual(self.consultar_reserva(), antes)
        self.assertEqual(self.consultar_auditoria(), [])

    def test_usuario_inativo_nao_registra(self):
        antes = self.consultar_reserva()

        with self.assertRaises(ValueError):
            registrar_nao_comparecimento(self.engine, 5, 1)

        self.assertEqual(self.consultar_reserva(), antes)
        self.assertEqual(self.consultar_auditoria(), [])

    def test_usuario_inexistente_nao_registra(self):
        antes = self.consultar_reserva()

        with self.assertRaises(ValueError):
            registrar_nao_comparecimento(self.engine, 999, 1)

        self.assertEqual(self.consultar_reserva(), antes)
        self.assertEqual(self.consultar_auditoria(), [])

    def test_reserva_inexistente_nao_gera_evento(self):
        antes = self.consultar_reserva()

        with self.assertRaises(ValueError):
            registrar_nao_comparecimento(self.engine, 1, 999)

        self.assertEqual(self.consultar_reserva(), antes)
        self.assertEqual(self.consultar_auditoria(), [])

    def test_bloqueia_antes_do_termino(self):
        self.alterar_reserva(
            inicio=self.agora - timedelta(hours=1),
            fim=self.agora + timedelta(seconds=1),
        )
        antes = self.consultar_reserva()

        with self.assertRaisesRegex(
            ValueError,
            "encerramento",
        ):
            registrar_nao_comparecimento(self.engine, 1, 1)

        self.assertEqual(self.consultar_reserva(), antes)
        self.assertEqual(self.consultar_auditoria(), [])

    def test_permite_no_instante_exato_do_termino(self):
        self.alterar_reserva(fim=self.agora)

        registrar_nao_comparecimento(self.engine, 1, 1)

        self.conferir_registro(1)

    def test_bloqueia_demais_situacoes(self):
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
                antes = self.consultar_reserva()

                with self.assertRaises(ValueError):
                    registrar_nao_comparecimento(
                        self.engine,
                        1,
                        1,
                    )

                self.assertEqual(
                    self.consultar_reserva(),
                    antes,
                )
                self.assertEqual(
                    self.consultar_auditoria(),
                    [],
                )

    def test_permite_registro_com_recurso_inativo(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(ativo=False)
            )

        registrar_nao_comparecimento(self.engine, 2, 1)

        self.conferir_registro(2)

    def test_bloqueia_recurso_que_nao_e_material(self):
        for tipo in ("SALA", "PROFESSOR"):
            with self.subTest(tipo=tipo):
                with self.engine.begin() as conexao:
                    conexao.execute(
                        update(recursos)
                        .where(recursos.c.id == 1)
                        .values(tipo=tipo)
                    )

                antes = self.consultar_reserva()

                with self.assertRaisesRegex(
                    ValueError,
                    "exclusiva para materiais",
                ):
                    registrar_nao_comparecimento(
                        self.engine,
                        1,
                        1,
                    )

                self.assertEqual(
                    self.consultar_reserva(),
                    antes,
                )
                self.assertEqual(
                    self.consultar_auditoria(),
                    [],
                )

    def test_repeticao_nao_duplica_auditoria(self):
        registrar_nao_comparecimento(self.engine, 1, 1)

        with self.assertRaises(ValueError):
            registrar_nao_comparecimento(self.engine, 1, 1)

        self.conferir_registro(1)

    def test_falha_na_auditoria_desfaz_alteracao(self):
        antes = self.consultar_reserva()
        registrar_original = servico_materiais.registrar_auditoria

        def registrar_e_falhar(*args, **kwargs):
            registrar_original(*args, **kwargs)
            raise RuntimeError("Falha simulada após auditoria.")

        with patch.object(
            servico_materiais,
            "registrar_auditoria",
            side_effect=registrar_e_falhar,
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha simulada",
            ):
                registrar_nao_comparecimento(
                    self.engine,
                    1,
                    1,
                )

        self.assertEqual(self.consultar_reserva(), antes)
        self.assertEqual(self.consultar_auditoria(), [])


if __name__ == "__main__":
    unittest.main()