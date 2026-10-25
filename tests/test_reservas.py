from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from threading import Barrier
import tempfile
import unittest

from sqlalchemy import create_engine, insert, select, update

from banco import metadata, recursos, reservas, usuarios
from servico_reservas import cancelar_reserva, criar_reserva


class TestReservas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        with self.engine.begin() as conexao:
            for usuario_id in (1, 2):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuário de teste {usuario_id}",
                        login=f"teste{usuario_id}",
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

        self.inicio = (
            datetime.now() + timedelta(days=7)
        ).replace(hour=14, minute=0, second=0, microsecond=0)

    def tearDown(self):
        self.engine.dispose()
        self.pasta.cleanup()

    def dados_reserva(self, inicio, fim):
        return {
            "recurso_id": "1",
            "inicio": inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": fim.strftime("%Y-%m-%dT%H:%M"),
            "finalidade": "Teste automatizado",
        }

    def listar_reservas(self):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(reservas).order_by(reservas.c.id)
            ).mappings().all()

    def criar_reserva_de_teste(self):
        return criar_reserva(
            self.engine,
            1,
            self.dados_reserva(
                self.inicio,
                self.inicio + timedelta(hours=1),
            ),
        )

    def test_criar_reserva_valida(self):
        fim = self.inicio + timedelta(hours=1)

        reserva_id = criar_reserva(
            self.engine,
            1,
            self.dados_reserva(self.inicio, fim),
        )

        registros = self.listar_reservas()

        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["id"], reserva_id)
        self.assertEqual(registros[0]["usuario_id"], 1)
        self.assertEqual(registros[0]["recurso_id"], 1)
        self.assertEqual(registros[0]["inicio"], self.inicio)
        self.assertEqual(registros[0]["fim"], fim)
        self.assertEqual(registros[0]["status"], "APROVADA")

    def test_bloquear_horarios_sobrepostos(self):
        self.criar_reserva_de_teste()

        with self.assertRaisesRegex(
            ValueError,
            "Já existe uma reserva",
        ):
            criar_reserva(
                self.engine,
                1,
                self.dados_reserva(
                    self.inicio + timedelta(minutes=30),
                    self.inicio + timedelta(minutes=90),
                ),
            )

        self.assertEqual(len(self.listar_reservas()), 1)

    def test_permitir_horarios_consecutivos(self):
        fim_primeira = self.inicio + timedelta(hours=1)

        criar_reserva(
            self.engine,
            1,
            self.dados_reserva(self.inicio, fim_primeira),
        )

        criar_reserva(
            self.engine,
            1,
            self.dados_reserva(
                fim_primeira,
                fim_primeira + timedelta(hours=1),
            ),
        )

        self.assertEqual(len(self.listar_reservas()), 2)

    def test_duas_solicitacoes_simultaneas(self):
        barreira = Barrier(2)

        def tentar_reservar():
            dados = self.dados_reserva(
                self.inicio,
                self.inicio + timedelta(hours=1),
            )

            barreira.wait(timeout=10)

            try:
                criar_reserva(self.engine, 1, dados)
                return "ACEITA"
            except ValueError as erro:
                if "Já existe uma reserva" in str(erro):
                    return "CONFLITO"
                raise

        with ThreadPoolExecutor(max_workers=2) as executor:
            primeira = executor.submit(tentar_reservar)
            segunda = executor.submit(tentar_reservar)

            resultados = [
                primeira.result(timeout=15),
                segunda.result(timeout=15),
            ]

        self.assertCountEqual(
            resultados,
            ["ACEITA", "CONFLITO"],
        )
        self.assertEqual(len(self.listar_reservas()), 1)

    def test_dono_pode_cancelar_reserva_aprovada(self):
        reserva_id = self.criar_reserva_de_teste()
        registro_original = dict(self.listar_reservas()[0])

        cancelar_reserva(self.engine, 1, reserva_id)

        registros = self.listar_reservas()
        esperado = {
            **registro_original,
            "status": "CANCELADA",
        }

        self.assertEqual(len(registros), 1)
        self.assertEqual(dict(registros[0]), esperado)

    def test_dono_pode_cancelar_reserva_solicitada(self):
        # Recursos restritos precisam de aprovação.
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(restrito=True)
            )

        reserva_id = self.criar_reserva_de_teste()

        self.assertEqual(
            self.listar_reservas()[0]["status"],
            "SOLICITADA",
        )

        cancelar_reserva(self.engine, 1, reserva_id)

        self.assertEqual(
            self.listar_reservas()[0]["status"],
            "CANCELADA",
        )

    def test_outro_usuario_nao_pode_cancelar(self):
        reserva_id = self.criar_reserva_de_teste()
        registro_original = dict(self.listar_reservas()[0])

        with self.assertRaisesRegex(
            ValueError,
            "Reserva não encontrada",
        ):
            cancelar_reserva(self.engine, 2, reserva_id)

        self.assertEqual(
            dict(self.listar_reservas()[0]),
            registro_original,
        )

    def test_nao_cancelar_reserva_que_ja_comecou(self):
        reserva_id = self.criar_reserva_de_teste()

        # Simula uma reserva cujo início já passou.
        agora = datetime.now()

        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == reserva_id)
                .values(
                    inicio=agora - timedelta(hours=1),
                    fim=agora + timedelta(hours=1),
                )
            )

        registro_original = dict(self.listar_reservas()[0])

        with self.assertRaisesRegex(
            ValueError,
            "já começou",
        ):
            cancelar_reserva(self.engine, 1, reserva_id)

        self.assertEqual(
            dict(self.listar_reservas()[0]),
            registro_original,
        )

    def test_nao_cancelar_situacoes_nao_permitidas(self):
        reserva_id = self.criar_reserva_de_teste()

        situacoes = (
            "EM_USO",
            "CONCLUIDA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        )

        for situacao in situacoes:
            with self.subTest(situacao=situacao):
                with self.engine.begin() as conexao:
                    conexao.execute(
                        update(reservas)
                        .where(reservas.c.id == reserva_id)
                        .values(status=situacao)
                    )

                with self.assertRaisesRegex(
                    ValueError,
                    "situação atual",
                ):
                    cancelar_reserva(
                        self.engine,
                        1,
                        reserva_id,
                    )

                self.assertEqual(
                    self.listar_reservas()[0]["status"],
                    situacao,
                )

    def test_cancelamento_libera_horario(self):
        reserva_cancelada_id = self.criar_reserva_de_teste()

        cancelar_reserva(
            self.engine,
            1,
            reserva_cancelada_id,
        )

        # Outro usuário reserva o mesmo recurso e período.
        nova_reserva_id = criar_reserva(
            self.engine,
            2,
            self.dados_reserva(
                self.inicio,
                self.inicio + timedelta(hours=1),
            ),
        )

        registros = self.listar_reservas()

        self.assertEqual(len(registros), 2)
        self.assertNotEqual(
            reserva_cancelada_id,
            nova_reserva_id,
        )
        self.assertEqual(
            registros[0]["status"],
            "CANCELADA",
        )
        self.assertEqual(
            registros[1]["status"],
            "APROVADA",
        )
        self.assertEqual(registros[1]["usuario_id"], 2)
        self.assertEqual(
            registros[0]["inicio"],
            registros[1]["inicio"],
        )
        self.assertEqual(
            registros[0]["fim"],
            registros[1]["fim"],
        )


if __name__ == "__main__":
    unittest.main()