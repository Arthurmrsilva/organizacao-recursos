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

        colunas_existentes = [
            coluna[1]
            for coluna in conexao.execute(
                "PRAGMA table_info(auditoria_reservas)"
            ).fetchall()
        ]

        acoes_necessarias = (
            "'CRIACAO'",
            "'CANCELAMENTO'",
            "'APROVACAO'",
            "'REJEICAO'",
            "'RETIRADA'",
            "'DEVOLUCAO'",
            "'ALTERACAO'",
        )

        estrutura_atualizada = (
            "detalhes" in colunas_existentes
            and all(
                acao in tabela[0]
                for acao in acoes_necessarias
            )
        )

        if estrutura_atualizada:
            print("A auditoria já está atualizada.")
            return

        # Confere a definição antes de modificar o banco.
        colunas_novas = [
            coluna.name
            for coluna in auditoria_reservas.columns
        ]

        if "detalhes" not in colunas_novas:
            raise RuntimeError(
                "Atualize o banco.py antes de executar este script."
            )

        # Evita descartar colunas desconhecidas.
        colunas_desconhecidas = (
            set(colunas_existentes) - set(colunas_novas)
        )

        if colunas_desconhecidas:
            raise RuntimeError(
                "A auditoria possui colunas não previstas: "
                + ", ".join(sorted(colunas_desconhecidas))
            )

        sql_tabela = str(
            CreateTable(auditoria_reservas).compile(
                dialect=engine.dialect
            )
        )

        if "'ALTERACAO'" not in sql_tabela:
            raise RuntimeError(
                "A definição em banco.py ainda não permite ALTERACAO."
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

        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.execute("BEGIN IMMEDIATE")

        try:
            # Guarda índices e gatilhos para recriá-los.
            objetos = conexao.execute(
                """
                SELECT sql
                FROM sqlite_master
                WHERE tbl_name = 'auditoria_reservas'
                  AND type IN ('index', 'trigger')
                  AND sql IS NOT NULL
                """
            ).fetchall()

            # Copia as colunas existentes, incluindo detalhes
            # caso uma versão anterior já tenha criado esse campo.
            nomes_colunas = ", ".join(
                f'"{nome}"'
                for nome in colunas_existentes
            )

            registros_antes = conexao.execute(
                f"""
                SELECT {nomes_colunas}
                FROM auditoria_reservas
                ORDER BY id
                """
            ).fetchall()

            conexao.execute(sql_temporaria)

            conexao.execute(
                f"""
                INSERT INTO auditoria_reservas_nova (
                    {nomes_colunas}
                )
                SELECT {nomes_colunas}
                FROM auditoria_reservas
                """
            )

            # Compara somente as colunas originais.
            # O novo campo detalhes fica NULL nos eventos antigos.
            registros_copiados = conexao.execute(
                f"""
                SELECT {nomes_colunas}
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