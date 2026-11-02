import hashlib
import io
import sqlite3
import tempfile
import unittest
from contextlib import closing, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from validar_backup import main, validar_backup


class TestValidarBackup(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.raiz = Path(self.pasta.name)
        self.banco = self.raiz / "origem.db"

    def preparar_banco(self):
        with closing(sqlite3.connect(self.banco)) as conexao:
            conexao.executescript(
                """
                CREATE TABLE recursos (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL UNIQUE
                );

                CREATE TABLE reservas (
                    id INTEGER PRIMARY KEY,
                    recurso_id INTEGER NOT NULL,
                    finalidade TEXT NOT NULL,
                    FOREIGN KEY (recurso_id) REFERENCES recursos(id)
                );

                CREATE INDEX indice_reserva_recurso
                ON reservas(recurso_id);
                """
            )
            conexao.execute(
                "INSERT INTO recursos VALUES (?, ?)",
                (1, "Sala de reunião"),
            )
            conexao.execute(
                "INSERT INTO reservas VALUES (?, ?, ?)",
                (1, 1, "Informação privada de teste"),
            )
            conexao.commit()

    def hash_banco(self):
        return hashlib.sha256(
            self.banco.read_bytes()
        ).hexdigest()

    def test_restauracao_preserva_estrutura_dados_e_origem(self):
        self.preparar_banco()
        hash_original = self.hash_banco()
        arquivos_antes = set(self.raiz.iterdir())
        saida = io.StringIO()

        # Verifica também a entrada pelo argumento do programa.
        with patch(
            "sys.argv",
            ["validar_backup.py", str(self.banco)],
        ):
            with redirect_stdout(saida):
                main()

        self.assertEqual(self.hash_banco(), hash_original)
        self.assertEqual(
            set(self.raiz.iterdir()), arquivos_antes
        )

        texto = saida.getvalue()
        self.assertIn(
            "OK: estrutura e dados preservados.", texto
        )
        self.assertIn(
            "Tabelas de aplicação conferidas: 2.", texto
        )
        self.assertNotIn(
            "Informação privada de teste", texto
        )

        with closing(sqlite3.connect(self.banco)) as conexao:
            registros = conexao.execute(
                "SELECT recurso_id, finalidade FROM reservas"
            ).fetchall()

        self.assertEqual(
            registros,
            [(1, "Informação privada de teste")],
        )

    def test_arquivo_inexistente_nao_e_criado(self):
        inexistente = self.raiz / "inexistente.db"

        with self.assertRaises(FileNotFoundError):
            validar_backup(inexistente)

        self.assertFalse(inexistente.exists())

    def test_diretorio_e_recusado(self):
        with self.assertRaisesRegex(
            ValueError, "arquivo de banco existente"
        ):
            validar_backup(self.raiz)

    def test_arquivo_invalido_e_recusado_sem_alteracao(self):
        self.banco.write_bytes(
            b"Este arquivo nao e um banco SQLite."
        )
        hash_original = self.hash_banco()

        with self.assertRaises(sqlite3.DatabaseError):
            validar_backup(self.banco)

        self.assertEqual(self.hash_banco(), hash_original)


if __name__ == "__main__":
    unittest.main(verbosity=2)