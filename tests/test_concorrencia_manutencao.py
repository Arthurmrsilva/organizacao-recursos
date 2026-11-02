import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, insert, select

from banco import (
    auditoria_reservas,
    manutencoes,
    metadata,
    notificacoes,
    recursos,
    reservas,
    usuarios,
)
from servico_reservas import criar_manutencao, criar_reserva


class TestConcorrenciaManutencao(unittest.TestCase):
    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)

        caminho = Path(pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}",
            connect_args={
                "check_same_thread": False,
                "timeout": 20,
            },
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        self.inicio = (
            datetime.now() + timedelta(days=7)
        ).replace(hour=14, minute=0, second=0, microsecond=0)
        self.fim = self.inicio + timedelta(hours=1)

        with self.engine.begin() as conexao:
            for usuario_id, perfil in (
                (1, "ADMIN"),
                (2, "SOLICITANTE"),
            ):
                conexao.execute(
                    insert(usuarios).values(
                        id=usuario_id,
                        nome=f"Usuario {usuario_id}",
                        login=f"concorrencia{usuario_id}",
                        senha_hash="nao-utilizado-neste-teste",
                        perfil=perfil,
                        ativo=True,
                    )
                )

            for recurso_id, tipo in enumerate(
                ("SALA", "PROFESSOR", "MATERIAL"),
                start=1,
            ):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=f"Recurso {tipo}",
                        tipo=tipo,
                        localizacao="Ambiente de teste",
                        restrito=False,
                        ativo=True,
                    )
                )

    def listar(self, tabela, recurso_id):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(tabela).where(
                    tabela.c.recurso_id == recurso_id
                )
            ).mappings().all()

    def disputar(self, recurso_id):
        barreira = threading.Barrier(2, timeout=15)
        periodo = {
            "recurso_id": str(recurso_id),
            "inicio": self.inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": self.fim.strftime("%Y-%m-%dT%H:%M"),
        }

        def executar(operacao):
            dados = dict(periodo)

            if operacao == "manutencao":
                funcao = criar_manutencao
                usuario_id = 1
                dados["motivo"] = "Reparo de teste"
            else:
                funcao = criar_reserva
                usuario_id = 2
                dados["finalidade"] = "Reserva de teste"

            barreira.wait()

            try:
                registro_id = funcao(
                    self.engine, usuario_id, dados
                )
                return operacao, True, registro_id
            except ValueError as erro:
                return operacao, False, str(erro)

        with ThreadPoolExecutor(max_workers=2) as executor:
            tarefas = [
                executor.submit(executar, operacao)
                for operacao in ("manutencao", "reserva")
            ]
            return [
                tarefa.result(timeout=30)
                for tarefa in tarefas
            ]

    def test_manutencao_e_reserva_nao_ocupam_mesmo_periodo(self):
        for recurso_id, tipo in enumerate(
            ("SALA", "PROFESSOR", "MATERIAL"),
            start=1,
        ):
            with self.subTest(tipo=tipo):
                resultados = self.disputar(recurso_id)

                aceitos = [
                    resultado
                    for resultado in resultados
                    if resultado[1]
                ]
                recusados = [
                    resultado
                    for resultado in resultados
                    if not resultado[1]
                ]

                self.assertEqual(len(aceitos), 1)
                self.assertEqual(len(recusados), 1)

                bloqueios = self.listar(
                    manutencoes, recurso_id
                )
                agendamentos = self.listar(
                    reservas, recurso_id
                )

                self.assertEqual(
                    len(bloqueios) + len(agendamentos),
                    1,
                )

                vencedor, _, registro_id = aceitos[0]
                mensagem = recusados[0][2]

                if vencedor == "manutencao":
                    self.assertEqual(agendamentos, [])
                    self.assertEqual(
                        bloqueios[0]["id"], registro_id
                    )
                    self.assertTrue(bloqueios[0]["ativo"])
                    self.assertIn(
                        "em manutenção", mensagem
                    )
                    registro = bloqueios[0]
                else:
                    self.assertEqual(bloqueios, [])
                    registro = agendamentos[0]
                    self.assertEqual(
                        registro["id"], registro_id
                    )
                    self.assertEqual(
                        registro["usuario_id"], 2
                    )
                    self.assertEqual(
                        registro["status"],
                        (
                            "SOLICITADA"
                            if tipo == "PROFESSOR"
                            else "APROVADA"
                        ),
                    )
                    self.assertIn(
                        "Já existe uma reserva", mensagem
                    )

                    with self.engine.connect() as conexao:
                        eventos = conexao.execute(
                            select(auditoria_reservas).where(
                                auditoria_reservas.c.reserva_id
                                == registro_id
                            )
                        ).mappings().all()

                        avisos = conexao.execute(
                            select(notificacoes).where(
                                notificacoes.c.reserva_id
                                == registro_id
                            )
                        ).mappings().all()

                    self.assertEqual(len(eventos), 1)
                    self.assertEqual(
                        eventos[0]["acao"], "CRIACAO"
                    )
                    self.assertEqual(
                        eventos[0]["usuario_id"], 2
                    )
                    self.assertEqual(len(avisos), 1)
                    self.assertEqual(
                        avisos[0]["usuario_id"], 2
                    )

                self.assertEqual(
                    registro["inicio"], self.inicio
                )
                self.assertEqual(
                    registro["fim"], self.fim
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)