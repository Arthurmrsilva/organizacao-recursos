import sqlite3
import tempfile
import unittest
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine

import atualizar_auditoria as migracao
from banco import metadata


class TestAtualizarAuditoria(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)

        self.raiz = Path(self.pasta.name)
        self.caminho = self.raiz / "teste.db"

        self.engine = create_engine(
            f"sqlite:///{self.caminho.as_posix()}"
        )
        self.addCleanup(self.engine.dispose)

        for nome, valor in (
            ("CAMINHO_BANCO", self.caminho),
            ("PASTA_PROJETO", self.raiz),
            ("engine", self.engine),
        ):
            troca = patch.object(migracao, nome, valor)
            troca.start()
            self.addCleanup(troca.stop)

    @contextmanager
    def conectar(self, caminho=None):
        if caminho is None:
            caminho = self.caminho

        conexao = sqlite3.connect(caminho)

        try:
            with conexao:
                yield conexao
        finally:
            # Fecha o arquivo também no Windows.
            conexao.close()

    def executar_migracao(self):
        saida = StringIO()

        with redirect_stdout(saida):
            migracao.atualizar_auditoria()

        return saida.getvalue()

    def preparar_banco_antigo(self, acao="CRIACAO"):
        with self.conectar() as conexao:
            conexao.executescript(
                """
                CREATE TABLE usuarios (
                    id INTEGER PRIMARY KEY
                );

                CREATE TABLE reservas (
                    id INTEGER PRIMARY KEY
                );

                INSERT INTO usuarios (id) VALUES (1);
                INSERT INTO reservas (id) VALUES (1);

                CREATE TABLE auditoria_reservas (
                    id INTEGER PRIMARY KEY,
                    reserva_id INTEGER NOT NULL
                        REFERENCES reservas(id),
                    usuario_id INTEGER NOT NULL
                        REFERENCES usuarios(id),
                    acao VARCHAR(30) NOT NULL,
                    data_hora DATETIME NOT NULL,
                    status_anterior VARCHAR(20),
                    status_novo VARCHAR(20) NOT NULL
                );

                CREATE INDEX indice_auditoria_teste
                ON auditoria_reservas(reserva_id);

                CREATE TABLE log_teste (
                    evento_id INTEGER
                );

                CREATE TRIGGER gatilho_auditoria_teste
                AFTER INSERT ON auditoria_reservas
                BEGIN
                    INSERT INTO log_teste(evento_id)
                    VALUES (NEW.id);
                END;
                """
            )

            conexao.execute(
                """
                INSERT INTO auditoria_reservas (
                    id,
                    reserva_id,
                    usuario_id,
                    acao,
                    data_hora,
                    status_anterior,
                    status_novo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    1,
                    1,
                    1,
                    acao,
                    "2030-06-10 10:00:00",
                    None,
                    "APROVADA",
                ),
            )

    def consultar_registros(self, caminho=None):
        with self.conectar(caminho) as conexao:
            return conexao.execute(
                """
                SELECT
                    id,
                    reserva_id,
                    usuario_id,
                    acao,
                    data_hora,
                    status_anterior,
                    status_novo
                FROM auditoria_reservas
                ORDER BY id
                """
            ).fetchall()

    def test_banco_inexistente_nao_cria_arquivo(self):
        with self.assertRaisesRegex(
            RuntimeError,
            "Banco não encontrado",
        ):
            self.executar_migracao()

        self.assertFalse(self.caminho.exists())

    def test_tabela_inexistente_nao_cria_backup(self):
        with self.conectar() as conexao:
            conexao.execute(
                "CREATE TABLE outra_tabela (id INTEGER)"
            )

        with self.assertRaisesRegex(
            RuntimeError,
            "tabela de auditoria não foi encontrada",
        ):
            self.executar_migracao()

        self.assertFalse((self.raiz / "backups").exists())

    def test_estrutura_atualizada_nao_precisa_migrar(self):
        metadata.create_all(self.engine)

        mensagem = self.executar_migracao()

        self.assertIn(
            "A auditoria já está atualizada.",
            mensagem,
        )
        self.assertFalse((self.raiz / "backups").exists())

    def test_migracao_preserva_registros_e_cria_backup(self):
        self.preparar_banco_antigo()
        antes = self.consultar_registros()

        mensagem = self.executar_migracao()

        self.assertEqual(self.consultar_registros(), antes)
        self.assertIn("1 registros preservados.", mensagem)

        backups = list(
            (self.raiz / "backups").glob("*.db")
        )
        self.assertEqual(len(backups), 1)
        self.assertEqual(
            self.consultar_registros(backups[0]),
            antes,
        )

        with self.conectar() as conexao:
            detalhes = conexao.execute(
                """
                SELECT detalhes
                FROM auditoria_reservas
                WHERE id = 1
                """
            ).fetchone()

            estrutura = conexao.execute(
                """
                SELECT sql
                FROM sqlite_master
                WHERE name = 'auditoria_reservas'
                """
            ).fetchone()[0]

        self.assertEqual(detalhes, (None,))
        self.assertIn("'ALTERACAO'", estrutura)

        with self.conectar(backups[0]) as conexao:
            colunas_backup = {
                linha[1]
                for linha in conexao.execute(
                    "PRAGMA table_info(auditoria_reservas)"
                )
            }

        self.assertNotIn("detalhes", colunas_backup)

    def test_migracao_preserva_indice_e_gatilho(self):
        self.preparar_banco_antigo()

        self.executar_migracao()

        with self.conectar() as conexao:
            objetos = {
                linha[0]
                for linha in conexao.execute(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE tbl_name = 'auditoria_reservas'
                      AND type IN ('index', 'trigger')
                    """
                )
            }

            self.assertIn(
                "indice_auditoria_teste",
                objetos,
            )
            self.assertIn(
                "gatilho_auditoria_teste",
                objetos,
            )

            conexao.execute(
                """
                INSERT INTO auditoria_reservas (
                    id,
                    reserva_id,
                    usuario_id,
                    acao,
                    data_hora,
                    status_anterior,
                    status_novo
                )
                VALUES (
                    2,
                    1,
                    1,
                    'ALTERACAO',
                    '2030-06-10 11:00:00',
                    'APROVADA',
                    'SOLICITADA'
                )
                """
            )

            eventos = conexao.execute(
                """
                SELECT evento_id
                FROM log_teste
                ORDER BY evento_id
                """
            ).fetchall()

        self.assertEqual(eventos, [(1,), (2,)])

    def test_coluna_desconhecida_impede_migracao(self):
        self.preparar_banco_antigo()

        with self.conectar() as conexao:
            conexao.execute(
                """
                ALTER TABLE auditoria_reservas
                ADD COLUMN campo_extra TEXT
                """
            )

        antes = self.consultar_registros()

        with self.assertRaisesRegex(
            RuntimeError,
            "colunas não previstas: campo_extra",
        ):
            self.executar_migracao()

        self.assertEqual(self.consultar_registros(), antes)
        self.assertFalse((self.raiz / "backups").exists())

    def test_falha_na_copia_reverte_migracao(self):
        self.preparar_banco_antigo(
            acao="ACAO_DESCONHECIDA"
        )
        antes = self.consultar_registros()

        with self.assertRaises(sqlite3.IntegrityError):
            self.executar_migracao()

        self.assertEqual(self.consultar_registros(), antes)

        with self.conectar() as conexao:
            colunas = {
                linha[1]
                for linha in conexao.execute(
                    "PRAGMA table_info(auditoria_reservas)"
                )
            }

            temporaria = conexao.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE name = 'auditoria_reservas_nova'
                """
            ).fetchone()

        self.assertNotIn("detalhes", colunas)
        self.assertIsNone(temporaria)

    def test_executar_duas_vezes_nao_duplica_dados(self):
        self.preparar_banco_antigo()

        self.executar_migracao()
        antes = self.consultar_registros()

        mensagem = self.executar_migracao()

        self.assertIn(
            "A auditoria já está atualizada.",
            mensagem,
        )
        self.assertEqual(self.consultar_registros(), antes)
        self.assertEqual(
            len(list((self.raiz / "backups").glob("*.db"))),
            1,
        )


if __name__ == "__main__":
    unittest.main()