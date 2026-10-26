import sqlite3
from datetime import datetime

from sqlalchemy.schema import CreateTable

from banco import (
    CAMINHO_BANCO,
    PASTA_PROJETO,
    auditoria_reservas,
    engine,
)


def atualizar_auditoria():
    if not CAMINHO_BANCO.is_file():
        raise RuntimeError(
            "Banco não encontrado. Confira a pasta do projeto."
        )

    conexao = sqlite3.connect(
        CAMINHO_BANCO,
        isolation_level=None,
    )

    try:
        tabela = conexao.execute(
            """
            SELECT sql
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'auditoria_reservas'
            """
        ).fetchone()

        if tabela is None:
            raise RuntimeError(
                "A tabela de auditoria não foi encontrada."
            )

        if "'RETIRADA'" in tabela[0] and "'DEVOLUCAO'" in tabela[0]:
            print("A auditoria já está atualizada.")
            return

        # Backup completo antes da migração.
        pasta_backups = PASTA_PROJETO / "backups"
        pasta_backups.mkdir(exist_ok=True)

        momento = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        caminho_backup = (
            pasta_backups / f"recursos_antes_auditoria_{momento}.db"
        )

        destino = sqlite3.connect(caminho_backup)

        try:
            conexao.backup(destino)
        finally:
            destino.close()

        print(f"Backup criado em: {caminho_backup}")

        # Guarda índices e gatilhos existentes para recriá-los.
        objetos = conexao.execute(
            """
            SELECT sql
            FROM sqlite_master
            WHERE tbl_name = 'auditoria_reservas'
              AND type IN ('index', 'trigger')
              AND sql IS NOT NULL
            """
        ).fetchall()

        # Obtém a estrutura nova definida em banco.py.
        sql_tabela = str(
            CreateTable(auditoria_reservas).compile(
                dialect=engine.dialect
            )
        )

        sql_temporaria = sql_tabela.replace(
            "CREATE TABLE auditoria_reservas",
            "CREATE TABLE auditoria_reservas_nova",
            1,
        )

        if sql_temporaria == sql_tabela:
            raise RuntimeError(
                "Não foi possível preparar a estrutura da auditoria."
            )

        # A troca inteira acontece em uma única transação.
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.execute("BEGIN IMMEDIATE")

        try:
            registros_antes = conexao.execute(
                """
                SELECT *
                FROM auditoria_reservas
                ORDER BY id
                """
            ).fetchall()

            conexao.execute(sql_temporaria)

            conexao.execute(
                """
                INSERT INTO auditoria_reservas_nova (
                    id,
                    reserva_id,
                    usuario_id,
                    acao,
                    data_hora,
                    status_anterior,
                    status_novo
                )
                SELECT
                    id,
                    reserva_id,
                    usuario_id,
                    acao,
                    data_hora,
                    status_anterior,
                    status_novo
                FROM auditoria_reservas
                """
            )

            registros_copiados = conexao.execute(
                """
                SELECT *
                FROM auditoria_reservas_nova
                ORDER BY id
                """
            ).fetchall()

            if registros_antes != registros_copiados:
                raise RuntimeError(
                    "A conferência dos registros falhou."
                )

            conexao.execute("DROP TABLE auditoria_reservas")

            conexao.execute(
                """
                ALTER TABLE auditoria_reservas_nova
                RENAME TO auditoria_reservas
                """
            )

            for (sql_objeto,) in objetos:
                conexao.execute(sql_objeto)

            problemas = conexao.execute(
                "PRAGMA foreign_key_check(auditoria_reservas)"
            ).fetchall()

            if problemas:
                raise RuntimeError(
                    "Foram encontrados vínculos inválidos na auditoria."
                )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        print(
            "Auditoria atualizada com sucesso! "
            f"{len(registros_antes)} registros preservados."
        )

    finally:
        conexao.close()


if __name__ == "__main__":
    atualizar_auditoria()