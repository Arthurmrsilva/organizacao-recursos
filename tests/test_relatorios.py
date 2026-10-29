import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, insert, update

from banco import (
    conflitos_reservas,
    metadata,
    recursos,
    reservas,
    usuarios,
)
from servico_relatorios import gerar_relatorio


class TestRelatorios(unittest.TestCase):
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
            for usuario_id, perfil, ativo in (
                (1, "ADMIN", True),
                (2, "SOLICITANTE", True),
                (3, "RESPONSAVEL", True),
                (4, "ADMIN", False),
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

            for recurso_id, nome, ativo in (
                (1, "Sala A", True),
                (2, "Sala B", True),
                (3, "Sala inativa", False),
            ):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=nome,
                        tipo="SALA",
                        localizacao="Bloco A",
                        capacidade=30,
                        restrito=False,
                        ativo=ativo,
                    )
                )

    def cadastrar(
        self,
        status="APROVADA",
        inicio="2030-06-10T10:00",
        fim="2030-06-10T12:00",
        recurso_id=1,
    ):
        with self.engine.begin() as conexao:
            resultado = conexao.execute(
                insert(reservas).values(
                    recurso_id=recurso_id,
                    usuario_id=2,
                    inicio=datetime.fromisoformat(inicio),
                    fim=datetime.fromisoformat(fim),
                    finalidade="Teste de relatório",
                    status=status,
                )
            )

            return resultado.inserted_primary_key[0]

    def cadastrar_conflito(
        self,
        reserva_id,
        criado_em,
        operacao="CRIACAO",
        recurso_id=1,
        usuario_id=2,
        inicio="2030-06-10T10:30",
        fim="2030-06-10T11:30",
    ):
        # Insere uma tentativa já registrada para testar o relatório.
        # O bloqueio pelo serviço será testado separadamente.
        with self.engine.begin() as conexao:
            conexao.execute(
                insert(conflitos_reservas).values(
                    usuario_id=usuario_id,
                    recurso_id=recurso_id,
                    reserva_conflitante_id=reserva_id,
                    operacao=operacao,
                    inicio=datetime.fromisoformat(inicio),
                    fim=datetime.fromisoformat(fim),
                    criado_em=datetime.fromisoformat(criado_em),
                )
            )

    def test_relatorio_vazio(self):
        relatorio = gerar_relatorio(self.engine, 1)

        self.assertEqual(relatorio["total_reservas"], 0)
        self.assertEqual(relatorio["horas_previstas"], 0)
        self.assertEqual(relatorio["recursos"], [])
        self.assertEqual(len(relatorio["situacoes"]), 7)
        self.assertEqual(relatorio["conflitos_evitados"], 0)
        self.assertTrue(
            all(
                item["quantidade"] == 0
                for item in relatorio["situacoes"]
            )
        )

    def test_somente_administrador_ativo_pode_consultar(self):
        for usuario_id in (2, 3, 4, 999):
            with self.subTest(usuario_id=usuario_id):
                with self.assertRaisesRegex(
                    ValueError,
                    "Somente administradores",
                ):
                    gerar_relatorio(self.engine, usuario_id)

    def test_contagem_de_todas_as_situacoes(self):
        situacoes = (
            "SOLICITADA",
            "APROVADA",
            "EM_USO",
            "CONCLUIDA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        )

        for status in situacoes:
            self.cadastrar(status=status)

        relatorio = gerar_relatorio(self.engine, 1)
        contagens = {
            item["codigo"]: item["quantidade"]
            for item in relatorio["situacoes"]
        }

        self.assertEqual(relatorio["total_reservas"], 7)
        self.assertEqual(
            contagens,
            {status: 1 for status in situacoes},
        )

        # Três situações contam horas, com duas horas cada.
        self.assertEqual(relatorio["horas_previstas"], 6)

    def test_situacoes_sem_horas_continuam_na_contagem(self):
        for status in (
            "SOLICITADA",
            "REJEITADA",
            "CANCELADA",
            "NAO_COMPARECEU",
        ):
            self.cadastrar(status=status)

        relatorio = gerar_relatorio(self.engine, 1)
        recurso = relatorio["recursos"][0]

        self.assertEqual(relatorio["total_reservas"], 4)
        self.assertEqual(relatorio["horas_previstas"], 0)
        self.assertEqual(recurso["total_reservas"], 4)
        self.assertEqual(recurso["reservas_com_horas"], 0)
        self.assertEqual(recurso["horas_previstas"], 0)

    def test_agrupar_horas_por_recurso(self):
        self.cadastrar(
            inicio="2030-06-10T10:00",
            fim="2030-06-10T11:30",
        )
        self.cadastrar(
            status="CONCLUIDA",
            inicio="2030-06-11T10:00",
            fim="2030-06-11T12:00",
        )
        self.cadastrar(
            recurso_id=2,
            inicio="2030-06-10T14:00",
            fim="2030-06-10T14:45",
        )

        relatorio = gerar_relatorio(self.engine, 1)
        por_recurso = {
            item["id"]: item
            for item in relatorio["recursos"]
        }

        self.assertEqual(relatorio["total_reservas"], 3)
        self.assertEqual(relatorio["horas_previstas"], 4.25)
        self.assertEqual(
            por_recurso[1]["horas_previstas"],
            3.5,
        )
        self.assertEqual(
            por_recurso[1]["reservas_com_horas"],
            2,
        )
        self.assertEqual(
            por_recurso[2]["horas_previstas"],
            0.75,
        )

    def test_recurso_inativo_com_reserva_aparece(self):
        self.cadastrar(recurso_id=3)

        relatorio = gerar_relatorio(self.engine, 1)

        self.assertEqual(relatorio["total_reservas"], 1)
        self.assertEqual(
            relatorio["recursos"][0]["nome"],
            "Sala inativa",
        )
        self.assertEqual(relatorio["horas_previstas"], 2)

    def test_periodo_inclui_dia_final_inteiro(self):
        self.cadastrar(
            inicio="2030-06-10T23:00",
            fim="2030-06-10T23:30",
        )

        relatorio = gerar_relatorio(
            self.engine,
            1,
            {"inicio": "2030-06-10", "fim": "2030-06-10"},
        )

        self.assertEqual(relatorio["total_reservas"], 1)
        self.assertEqual(relatorio["horas_previstas"], 0.5)

    def test_periodo_conta_apenas_parte_sobreposta(self):
        self.cadastrar(
            inicio="2030-06-09T23:00",
            fim="2030-06-10T02:00",
        )
        self.cadastrar(
            inicio="2030-06-10T23:00",
            fim="2030-06-11T02:00",
        )
        self.cadastrar(
            recurso_id=2,
            inicio="2030-06-09T12:00",
            fim="2030-06-11T12:00",
        )

        relatorio = gerar_relatorio(
            self.engine,
            1,
            {"inicio": "2030-06-10", "fim": "2030-06-10"},
        )
        por_recurso = {
            item["id"]: item
            for item in relatorio["recursos"]
        }

        self.assertEqual(relatorio["total_reservas"], 3)
        self.assertEqual(relatorio["horas_previstas"], 27)
        self.assertEqual(
            por_recurso[1]["horas_previstas"],
            3,
        )
        self.assertEqual(
            por_recurso[2]["horas_previstas"],
            24,
        )

    def test_reservas_fora_ou_nos_limites_nao_entram(self):
        for inicio, fim in (
            ("2030-06-09T10:00", "2030-06-09T11:00"),
            ("2030-06-09T23:00", "2030-06-10T00:00"),
            ("2030-06-11T00:00", "2030-06-11T01:00"),
            ("2030-06-12T10:00", "2030-06-12T11:00"),
        ):
            self.cadastrar(inicio=inicio, fim=fim)

        relatorio = gerar_relatorio(
            self.engine,
            1,
            {"inicio": "2030-06-10", "fim": "2030-06-10"},
        )

        self.assertEqual(relatorio["total_reservas"], 0)
        self.assertEqual(relatorio["horas_previstas"], 0)
        self.assertEqual(relatorio["recursos"], [])

    def test_periodo_incompleto_e_recusado(self):
        for dados in (
            {"inicio": "2030-06-10"},
            {"fim": "2030-06-10"},
        ):
            with self.subTest(dados=dados):
                with self.assertRaisesRegex(
                    ValueError,
                    "data inicial e a data final",
                ):
                    gerar_relatorio(self.engine, 1, dados)

    def test_datas_invalidas_sao_recusadas(self):
        for dados in (
            {"inicio": "invalida", "fim": "2030-06-10"},
            {"inicio": "2030-06-10", "fim": "2030-02-30"},
        ):
            with self.subTest(dados=dados):
                with self.assertRaisesRegex(
                    ValueError,
                    "datas válidas",
                ):
                    gerar_relatorio(self.engine, 1, dados)

    def test_data_final_anterior_e_recusada(self):
        with self.assertRaisesRegex(
            ValueError,
            "não pode ser anterior",
        ):
            gerar_relatorio(
                self.engine,
                1,
                {"inicio": "2030-06-11", "fim": "2030-06-10"},
            )

    def test_data_final_sem_dia_seguinte_e_recusada(self):
        with self.assertRaisesRegex(
            ValueError,
            "fora do intervalo",
        ):
            gerar_relatorio(
                self.engine,
                1,
                {"inicio": "9999-12-31", "fim": "9999-12-31"},
            )

    def test_datas_vazias_consultam_todo_historico(self):
        self.cadastrar()

        relatorio = gerar_relatorio(
            self.engine,
            1,
            {"inicio": "  ", "fim": ""},
        )

        self.assertEqual(relatorio["total_reservas"], 1)
        self.assertEqual(relatorio["horas_previstas"], 2)

    def test_arredondamento_acontece_apos_a_soma(self):
        for minuto in range(3):
            self.cadastrar(
                inicio=f"2030-06-10T10:0{minuto}",
                fim=f"2030-06-10T10:0{minuto + 1}",
            )

        relatorio = gerar_relatorio(self.engine, 1)

        # Três minutos = 0,05 hora.
        self.assertEqual(relatorio["horas_previstas"], 0.05)
        self.assertEqual(
            relatorio["recursos"][0]["horas_previstas"],
            0.05,
        )

    def test_sem_conflitos_registrados_retorna_zero(self):
        # Ter uma reserva não significa ter uma tentativa bloqueada.
        self.cadastrar()

        relatorio = gerar_relatorio(self.engine, 1)

        self.assertEqual(relatorio["conflitos_evitados"], 0)

    def test_contar_tentativas_das_tres_operacoes(self):
        reserva_id = self.cadastrar()

        for operacao, usuario_id in (
            ("CRIACAO", 2),
            ("ALTERACAO", 2),
            ("APROVACAO", 3),
        ):
            self.cadastrar_conflito(
                reserva_id=reserva_id,
                criado_em="2030-06-01T10:00",
                operacao=operacao,
                usuario_id=usuario_id,
            )

        relatorio = gerar_relatorio(self.engine, 1)

        self.assertEqual(relatorio["conflitos_evitados"], 3)

        # Tentativas bloqueadas não aumentam reservas ou horas.
        self.assertEqual(relatorio["total_reservas"], 1)
        self.assertEqual(relatorio["horas_previstas"], 2)
        self.assertEqual(
            relatorio["recursos"][0]["total_reservas"],
            1,
        )

    def test_conflitos_filtrados_pela_data_do_registro(self):
        reserva_id = self.cadastrar()

        # A tentativa foi registrada em 1º de junho,
        # mas o horário solicitado é para 10 de junho.
        self.cadastrar_conflito(
            reserva_id=reserva_id,
            criado_em="2030-06-01T15:00",
        )

        dia_registro = gerar_relatorio(
            self.engine,
            1,
            {"inicio": "2030-06-01", "fim": "2030-06-01"},
        )

        dia_reserva = gerar_relatorio(
            self.engine,
            1,
            {"inicio": "2030-06-10", "fim": "2030-06-10"},
        )

        self.assertEqual(dia_registro["conflitos_evitados"], 1)
        self.assertEqual(dia_registro["total_reservas"], 0)
        self.assertEqual(dia_registro["horas_previstas"], 0)

        self.assertEqual(dia_reserva["conflitos_evitados"], 0)
        self.assertEqual(dia_reserva["total_reservas"], 1)

    def test_limites_de_datas_dos_conflitos(self):
        reserva_id = self.cadastrar()

        for momento in (
            "2030-06-09T23:59:59.999999",
            "2030-06-10T00:00:00",
            "2030-06-10T23:59:59.999999",
            "2030-06-11T00:00:00",
        ):
            self.cadastrar_conflito(
                reserva_id=reserva_id,
                criado_em=momento,
            )

        relatorio = gerar_relatorio(
            self.engine,
            1,
            {"inicio": "2030-06-10", "fim": "2030-06-10"},
        )

        # Inclui o início e o último instante do dia,
        # mas exclui os registros dos dias anterior e seguinte.
        self.assertEqual(relatorio["conflitos_evitados"], 2)

    def test_sem_datas_conta_tentativas_repetidas(self):
        reserva_id = self.cadastrar()

        for momento in (
            "2030-05-01T10:00",
            "2030-06-01T10:00",
            "2030-06-01T10:00",
        ):
            self.cadastrar_conflito(
                reserva_id=reserva_id,
                criado_em=momento,
            )

        for dados in (None, {"inicio": " ", "fim": ""}):
            with self.subTest(dados=dados):
                relatorio = gerar_relatorio(
                    self.engine,
                    1,
                    dados,
                )

                # Cada registro representa uma tentativa,
                # mesmo quando os dados e o horário se repetem.
                self.assertEqual(
                    relatorio["conflitos_evitados"],
                    3,
                )

    def test_cancelamento_e_inativacao_preservam_contagem(self):
        reserva_id = self.cadastrar()

        self.cadastrar_conflito(
            reserva_id=reserva_id,
            criado_em="2030-06-01T10:00",
        )

        with self.engine.begin() as conexao:
            conexao.execute(
                update(reservas)
                .where(reservas.c.id == reserva_id)
                .values(status="CANCELADA")
            )
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(ativo=False)
            )

        relatorio = gerar_relatorio(self.engine, 1)

        # O conflito aconteceu antes dessas alterações
        # e continua fazendo parte do histórico.
        self.assertEqual(relatorio["conflitos_evitados"], 1)
        self.assertEqual(relatorio["total_reservas"], 1)
        self.assertEqual(relatorio["horas_previstas"], 0)


if __name__ == "__main__":
    unittest.main()