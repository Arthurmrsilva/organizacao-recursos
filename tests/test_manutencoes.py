import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, insert, select, update

from banco import (
    auditoria_reservas,
    manutencoes,
    metadata,
    recursos,
    reservas,
    usuarios,
)
from servico_reservas import (
    avaliar_reserva,
    criar_manutencao,
    criar_reserva,
)


class TestManutencoes(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        caminho = Path(self.pasta.name) / "teste.db"
        self.engine = create_engine(
            f"sqlite:///{caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)
        metadata.create_all(self.engine)

        self.inicio = (
            datetime.now() + timedelta(days=7)
        ).replace(hour=14, minute=0, second=0, microsecond=0)
        self.fim = self.inicio + timedelta(hours=2)

        with self.engine.begin() as conexao:
            for usuario_id, perfil in (
                (1, "ADMIN"),
                (2, "SOLICITANTE"),
                (3, "RESPONSAVEL"),
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

            for recurso_id in (1, 2):
                conexao.execute(
                    insert(recursos).values(
                        id=recurso_id,
                        nome=f"Sala {recurso_id}",
                        tipo="SALA",
                        localizacao="Bloco A",
                        capacidade=30,
                        responsavel_id=3,
                        restrito=False,
                        ativo=True,
                    )
                )

    def dados_manutencao(self, inicio=None, fim=None):
        return {
            "recurso_id": "1",
            "inicio": (inicio or self.inicio).strftime(
                "%Y-%m-%dT%H:%M"
            ),
            "fim": (fim or self.fim).strftime(
                "%Y-%m-%dT%H:%M"
            ),
            "motivo": "Reparo do ar-condicionado",
        }

    def dados_reserva(self, inicio, fim, recurso_id="1"):
        return {
            "recurso_id": recurso_id,
            "inicio": inicio.strftime("%Y-%m-%dT%H:%M"),
            "fim": fim.strftime("%Y-%m-%dT%H:%M"),
            "finalidade": "Aula de teste",
        }

    def listar(self, tabela):
        with self.engine.connect() as conexao:
            return conexao.execute(
                select(tabela).order_by(tabela.c.id)
            ).mappings().all()

    def test_admin_cadastra_manutencao(self):
        manutencao_id = criar_manutencao(
            self.engine, 1, self.dados_manutencao()
        )

        registros = self.listar(manutencoes)

        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["id"], manutencao_id)
        self.assertEqual(registros[0]["usuario_id"], 1)
        self.assertEqual(registros[0]["recurso_id"], 1)
        self.assertEqual(registros[0]["inicio"], self.inicio)
        self.assertEqual(registros[0]["fim"], self.fim)
        self.assertEqual(
            registros[0]["motivo"],
            "Reparo do ar-condicionado",
        )
        self.assertTrue(registros[0]["ativo"])
        self.assertIsInstance(registros[0]["criado_em"], datetime)

    def test_outros_perfis_nao_cadastram_manutencao(self):
        for usuario_id in (2, 3):
            with self.subTest(usuario_id=usuario_id):
                with self.assertRaisesRegex(
                    ValueError, "Somente administradores"
                ):
                    criar_manutencao(
                        self.engine,
                        usuario_id,
                        self.dados_manutencao(),
                    )

        self.assertEqual(self.listar(manutencoes), [])

    def test_admin_inativo_nao_cadastra_manutencao(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(usuarios)
                .where(usuarios.c.id == 1)
                .values(ativo=False)
            )

        with self.assertRaisesRegex(
            ValueError, "Somente administradores"
        ):
            criar_manutencao(
                self.engine, 1, self.dados_manutencao()
            )

        self.assertEqual(self.listar(manutencoes), [])

    def test_dados_invalidos_nao_gravam_manutencao(self):
        passado = datetime.now() - timedelta(days=1)

        casos = (
            {"motivo": ""},
            {"motivo": " "},
            {"motivo": "a" * 201},
            {"recurso_id": "abc"},
            {"recurso_id": "999"},
            {"inicio": "data-invalida"},
            {"fim": "data-invalida"},
            {"fim": self.inicio.strftime("%Y-%m-%dT%H:%M")},
            {
                "fim": (
                    self.inicio - timedelta(hours=1)
                ).strftime("%Y-%m-%dT%H:%M")
            },
            {"inicio": passado.strftime("%Y-%m-%dT%H:%M")},
        )

        for alteracoes in casos:
            with self.subTest(alteracoes=alteracoes):
                dados = self.dados_manutencao()
                dados.update(alteracoes)

                with self.assertRaises(ValueError):
                    criar_manutencao(self.engine, 1, dados)

                self.assertEqual(self.listar(manutencoes), [])

    def test_recurso_inativo_nao_recebe_manutencao(self):
        with self.engine.begin() as conexao:
            conexao.execute(
                update(recursos)
                .where(recursos.c.id == 1)
                .values(ativo=False)
            )

        with self.assertRaisesRegex(
            ValueError, "não está disponível"
        ):
            criar_manutencao(
                self.engine, 1, self.dados_manutencao()
            )

        self.assertEqual(self.listar(manutencoes), [])

    def test_manutencao_bloqueia_reservas_sobrepostas(self):
        criar_manutencao(
            self.engine, 1, self.dados_manutencao()
        )

        periodos = (
            (self.inicio, self.fim),
            (
                self.inicio + timedelta(minutes=30),
                self.fim - timedelta(minutes=30),
            ),
            (
                self.inicio - timedelta(hours=1),
                self.inicio + timedelta(minutes=30),
            ),
            (
                self.fim - timedelta(minutes=30),
                self.fim + timedelta(hours=1),
            ),
            (
                self.inicio - timedelta(hours=1),
                self.fim + timedelta(hours=1),
            ),
        )

        for inicio, fim in periodos:
            with self.subTest(inicio=inicio, fim=fim):
                with self.assertRaisesRegex(
                    ValueError, "em manutenção"
                ):
                    criar_reserva(
                        self.engine,
                        2,
                        self.dados_reserva(inicio, fim),
                    )

        self.assertEqual(self.listar(reservas), [])
        self.assertEqual(self.listar(auditoria_reservas), [])

    def test_reservas_consecutivas_a_manutencao_sao_permitidas(self):
        criar_manutencao(
            self.engine, 1, self.dados_manutencao()
        )

        for inicio, fim in (
            (self.inicio - timedelta(hours=1), self.inicio),
            (self.fim, self.fim + timedelta(hours=1)),
        ):
            criar_reserva(
                self.engine,
                2,
                self.dados_reserva(inicio, fim),
            )

        self.assertEqual(len(self.listar(reservas)), 2)
        self.assertEqual(len(self.listar(auditoria_reservas)), 2)

    def test_manutencao_nao_bloqueia_outro_recurso(self):
        criar_manutencao(
            self.engine, 1, self.dados_manutencao()
        )

        criar_reserva(
            self.engine,
            2,
            self.dados_reserva(
                self.inicio, self.fim, recurso_id="2"
            ),
        )

        registros = self.listar(reservas)
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["recurso_id"], 2)

    def test_manutencao_inativa_nao_bloqueia_reserva(self):
        manutencao_id = criar_manutencao(
            self.engine, 1, self.dados_manutencao()
        )

        with self.engine.begin() as conexao:
            conexao.execute(
                update(manutencoes)
                .where(manutencoes.c.id == manutencao_id)
                .values(ativo=False)
            )

        criar_reserva(
            self.engine,
            2,
            self.dados_reserva(self.inicio, self.fim),
        )

        self.assertEqual(len(self.listar(reservas)), 1)

    def test_reserva_existente_impede_manutencao(self):
        reserva_id = criar_reserva(
            self.engine,
            2,
            self.dados_reserva(self.inicio, self.fim),
        )

        for status in ("SOLICITADA", "APROVADA", "EM_USO"):
            with self.subTest(status=status):
                with self.engine.begin() as conexao:
                    conexao.execute(
                        update(reservas)
                        .where(reservas.c.id == reserva_id)
                        .values(status=status)
                    )

                with self.assertRaisesRegex(
                    ValueError, "Já existe uma reserva"
                ):
                    criar_manutencao(
                        self.engine, 1, self.dados_manutencao()
                    )

                self.assertEqual(self.listar(manutencoes), [])

    def test_manutencoes_sobrepostas_sao_bloqueadas(self):
        criar_manutencao(
            self.engine, 1, self.dados_manutencao()
        )

        with self.assertRaisesRegex(ValueError, "em manutenção"):
            criar_manutencao(
                self.engine,
                1,
                self.dados_manutencao(
                    self.inicio + timedelta(minutes=30),
                    self.fim + timedelta(hours=1),
                ),
            )

        self.assertEqual(len(self.listar(manutencoes)), 1)

    def test_aprovacao_e_bloqueada_durante_manutencao(self):
        criar_manutencao(
            self.engine, 1, self.dados_manutencao()
        )

        # Simula um registro inconsistente vindo de importação.
        # A aprovação precisa verificar o bloqueio novamente.
        with self.engine.begin() as conexao:
            resultado = conexao.execute(
                insert(reservas).values(
                    recurso_id=1,
                    usuario_id=2,
                    inicio=self.inicio,
                    fim=self.fim,
                    finalidade="Reserva importada",
                    status="SOLICITADA",
                )
            )
            reserva_id = resultado.inserted_primary_key[0]

        with self.assertRaisesRegex(ValueError, "em manutenção"):
            avaliar_reserva(
                self.engine, 3, reserva_id, "APROVADA"
            )

        self.assertEqual(
            self.listar(reservas)[0]["status"],
            "SOLICITADA",
        )
        self.assertEqual(self.listar(auditoria_reservas), [])


if __name__ == "__main__":
    unittest.main()