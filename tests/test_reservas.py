from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from threading import Barrier
import tempfile
import unittest

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
from servico_reservas import cancelar_reserva, criar_reserva


class TestReservas(unittest.TestCase):
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

    def listar_conflitos(self):
        # Abre outra conexão para conferir os dados confirmados.
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(conflitos_reservas)
                .order_by(conflitos_reservas.c.id)
            ).mappings().all()

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
        self.assertEqual(self.listar_conflitos(), [])

    def test_bloquear_horarios_sobrepostos(self):
        reserva_id = self.criar_reserva_de_teste()
        reservas_antes = self.listar_reservas()
        eventos_antes = self.listar_eventos_e_notificacoes()

        inicio_tentativa = self.inicio + timedelta(minutes=30)
        fim_tentativa = self.inicio + timedelta(minutes=90)

        antes = datetime.now()

        with self.assertRaisesRegex(
            ValueError,
            "Já existe uma reserva",
        ):
            criar_reserva(
                self.engine,
                2,
                self.dados_reserva(
                    inicio_tentativa,
                    fim_tentativa,
                ),
            )

        depois = datetime.now()
        conflitos = self.listar_conflitos()

        self.assertEqual(self.listar_reservas(), reservas_antes)
        self.assertEqual(
            self.listar_eventos_e_notificacoes(),
            eventos_antes,
        )

        # O erro não pode apagar o registro do conflito.
        self.assertEqual(len(conflitos), 1)

        conflito = conflitos[0]

        self.assertEqual(conflito["usuario_id"], 2)
        self.assertEqual(conflito["recurso_id"], 1)
        self.assertEqual(
            conflito["reserva_conflitante_id"],
            reserva_id,
        )
        self.assertEqual(conflito["operacao"], "CRIACAO")
        self.assertEqual(conflito["inicio"], inicio_tentativa)
        self.assertEqual(conflito["fim"], fim_tentativa)
        self.assertGreaterEqual(conflito["criado_em"], antes)
        self.assertLessEqual(conflito["criado_em"], depois)

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
        self.assertEqual(self.listar_conflitos(), [])

    def test_duas_solicitacoes_simultaneas(self):
        barreira = Barrier(2)

        def tentar_reservar(usuario_id):
            dados = self.dados_reserva(
                self.inicio,
                self.inicio + timedelta(hours=1),
            )

            barreira.wait(timeout=10)

            try:
                criar_reserva(self.engine, usuario_id, dados)
                return usuario_id, "ACEITA"
            except ValueError as erro:
                if "Já existe uma reserva" in str(erro):
                    return usuario_id, "CONFLITO"
                raise

        with ThreadPoolExecutor(max_workers=2) as executor:
            primeira = executor.submit(tentar_reservar, 1)
            segunda = executor.submit(tentar_reservar, 2)

            resultados = [
                primeira.result(timeout=15),
                segunda.result(timeout=15),
            ]

        self.assertCountEqual(
            [situacao for _, situacao in resultados],
            ["ACEITA", "CONFLITO"],
        )

        usuario_aceito = next(
            usuario_id
            for usuario_id, situacao in resultados
            if situacao == "ACEITA"
        )
        usuario_bloqueado = next(
            usuario_id
            for usuario_id, situacao in resultados
            if situacao == "CONFLITO"
        )

        registros = self.listar_reservas()
        conflitos = self.listar_conflitos()

        self.assertEqual(len(registros), 1)
        self.assertEqual(len(conflitos), 1)
        self.assertEqual(
            registros[0]["usuario_id"],
            usuario_aceito,
        )
        self.assertEqual(
            conflitos[0]["usuario_id"],
            usuario_bloqueado,
        )
        self.assertEqual(
            conflitos[0]["reserva_conflitante_id"],
            registros[0]["id"],
        )
        self.assertEqual(conflitos[0]["operacao"], "CRIACAO")

        eventos, avisos = self.listar_eventos_e_notificacoes()

        # Somente a reserva aceita gera auditoria e notificação.
        self.assertEqual(len(eventos), 1)
        self.assertEqual(len(avisos), 1)
        self.assertEqual(eventos[0]["acao"], "CRIACAO")
        self.assertEqual(
            avisos[0]["usuario_id"],
            usuario_aceito,
        )

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

        for situacao in (
            "EM_USO",
            "CONCLUIDA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        ):
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
        self.assertEqual(registros[0]["status"], "CANCELADA")
        self.assertEqual(registros[1]["status"], "APROVADA")
        self.assertEqual(registros[1]["usuario_id"], 2)
        self.assertEqual(
            registros[0]["inicio"],
            registros[1]["inicio"],
        )
        self.assertEqual(
            registros[0]["fim"],
            registros[1]["fim"],
        )
        self.assertEqual(self.listar_conflitos(), [])

    def test_tentativas_repetidas_geram_registros_separados(self):
        reserva_id = self.criar_reserva_de_teste()

        for _ in range(2):
            with self.assertRaisesRegex(
                ValueError,
                "Já existe uma reserva",
            ):
                criar_reserva(
                    self.engine,
                    2,
                    self.dados_reserva(
                        self.inicio,
                        self.inicio + timedelta(hours=1),
                    ),
                )

        conflitos = self.listar_conflitos()

        self.assertEqual(len(self.listar_reservas()), 1)
        self.assertEqual(len(conflitos), 2)
        self.assertNotEqual(
            conflitos[0]["id"],
            conflitos[1]["id"],
        )
        self.assertTrue(
            all(
                item["reserva_conflitante_id"] == reserva_id
                for item in conflitos
            )
        )

    def test_erro_de_preenchimento_nao_registra_conflito(self):
        self.criar_reserva_de_teste()
        registros_antes = self.listar_reservas()

        dados = self.dados_reserva(
            self.inicio,
            self.inicio + timedelta(hours=1),
        )
        dados["finalidade"] = " "

        with self.assertRaisesRegex(
            ValueError,
            "Informe a finalidade",
        ):
            criar_reserva(self.engine, 2, dados)

        self.assertEqual(self.listar_conflitos(), [])
        self.assertEqual(
            self.listar_reservas(),
            registros_antes,
        )

    def test_usuario_invalido_nao_registra_conflito(self):
        self.criar_reserva_de_teste()

        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 2)
                .values(ativo=False)
            )

        for usuario_id in (2, 999):
            with self.subTest(usuario_id=usuario_id):
                with self.assertRaisesRegex(
                    ValueError,
                    "Usuário não encontrado ou inativo",
                ):
                    criar_reserva(
                        self.engine,
                        usuario_id,
                        self.dados_reserva(
                            self.inicio,
                            self.inicio + timedelta(hours=1),
                        ),
                    )

        self.assertEqual(self.listar_conflitos(), [])
        self.assertEqual(len(self.listar_reservas()), 1)


if __name__ == "__main__":
    unittest.main()