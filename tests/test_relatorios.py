import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, insert

from banco import metadata, recursos, reservas, usuarios
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
            conexao.execute(
                insert(reservas).values(
                    recurso_id=recurso_id,
                    usuario_id=2,
                    inicio=datetime.fromisoformat(inicio),
                    fim=datetime.fromisoformat(fim),
                    finalidade="Teste de relatório",
                    status=status,
                )
            )

    def test_relatorio_vazio(self):
        relatorio = gerar_relatorio(self.engine, 1)

        self.assertEqual(relatorio["total_reservas"], 0)
        self.assertEqual(relatorio["horas_previstas"], 0)
        self.assertEqual(relatorio["recursos"], [])
        self.assertEqual(len(relatorio["situacoes"]), 7)
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

    def test_conflitos_indisponiveis_nao_sao_zero(self):
        relatorio = gerar_relatorio(self.engine, 1)

        self.assertIsNone(relatorio["conflitos_evitados"])


if __name__ == "__main__":
    unittest.main()