from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, insert, select

from banco import metadata, recursos, reservas, usuarios
from servico_reservas import criar_reserva


class TestReservas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        caminho = Path(self.pasta.name) / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        metadata.create_all(self.engine)

        with self.engine.begin() as conexao:
            conexao.execute(
                insert(usuarios).values(
                    id=1,
                    nome="Usuário de teste",
                    login="teste",
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
                select(reservas)
            ).mappings().all()

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
        criar_reserva(
            self.engine,
            1,
            self.dados_reserva(
                self.inicio,
                self.inicio + timedelta(hours=1),
            ),
        )

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


if __name__ == "__main__":
    unittest.main()