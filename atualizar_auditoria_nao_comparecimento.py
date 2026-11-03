import re
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
        str(CAMINHO_BANCO),
        isolation_level=None,
    )

    try:
        conexao.execute("PRAGMA foreign_keys = ON")

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

        # Verifica especificamente as ações permitidas.
        # NAO_COMPARECEU já existe nas restrições de status.
        regra_acoes = re.search(
            r"\bacao\s+IN\s*\(([^)]*)\)",
            tabela[0],
            flags=re.IGNORECASE,
        )

        if regra_acoes is None:
            raise RuntimeError(
                "Não foi possível identificar a regra "
                "das ações da auditoria."
            )

        acoes = set(
            re.findall(
                r"'([^']+)'",
                regra_acoes.group(1),
            )
        )

        colunas = {
            linha[1]
            for linha in conexao.execute(
                "PRAGMA table_info(auditoria_reservas)"
            )
        }

        colunas_esperadas = {
            "id",
            "reserva_id",
            "usuario_id",
            "acao",
            "data_hora",
            "status_anterior",
            "status_novo",
            "detalhes",
        }

        if colunas != colunas_esperadas:
            raise RuntimeError(
                "A estrutura da auditoria está diferente "
                "da esperada. Nenhuma alteração foi realizada."
            )

        if "NAO_COMPARECEU" in acoes:
            print("A auditoria já permite não comparecimento.")
            return

        acoes_novas = {
            "CRIACAO",
            "CANCELAMENTO",
            "APROVACAO",
            "REJEICAO",
            "RETIRADA",
            "DEVOLUCAO",
            "ALTERACAO",
            "NAO_COMPARECEU",
        }

        if not acoes.issubset(acoes_novas):
            raise RuntimeError(
                "Existem ações desconhecidas na estrutura atual. "
                "Nenhuma alteração foi realizada."
            )

        temporaria = conexao.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE name = 'auditoria_reservas_nova'
            """
        ).fetchone()

        if temporaria is not None:
            raise RuntimeError(
                "Já existe uma tabela temporária com esse nome. "
                "Nenhuma alteração foi realizada."
            )

        # Backup completo antes da migração.
        pasta_backups = PASTA_PROJETO / "backups"
        pasta_backups.mkdir(exist_ok=True)

        momento = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        caminho_backup = pasta_backups / (
            f"recursos_antes_nao_comparecimento_{momento}.db"
        )

        destino = sqlite3.connect(str(caminho_backup))

        try:
            conexao.backup(destino)
        finally:
            destino.close()

        print(f"Backup criado em: {caminho_backup}")

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

        if (
            sql_temporaria == sql_tabela
            or "'NAO_COMPARECEU'" not in sql_tabela
        ):
            raise RuntimeError(
                "Não foi possível preparar a estrutura nova."
            )

        # Confere a ação na definição do banco.py também.
        regra_nova = re.search(
            r"\bacao\s+IN\s*\(([^)]*)\)",
            sql_tabela,
            flags=re.IGNORECASE,
        )

        if (
            regra_nova is None
            or "'NAO_COMPARECEU'" not in regra_nova.group(1)
        ):
            raise RuntimeError(
                "Salve o banco.py atualizado antes de executar."
            )

        conexao.execute("BEGIN IMMEDIATE")

        try:
            objetos = conexao.execute(
                """
                SELECT sql
                FROM sqlite_master
                WHERE tbl_name = 'auditoria_reservas'
                  AND type IN ('index', 'trigger')
                  AND sql IS NOT NULL
                """
            ).fetchall()

            registros_antes = conexao.execute(
                """
                SELECT
                    id,
                    reserva_id,
                    usuario_id,
                    acao,
                    data_hora,
                    status_anterior,
                    status_novo,
                    detalhes
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
                    status_novo,
                    detalhes
                )
                SELECT
                    id,
                    reserva_id,
                    usuario_id,
                    acao,
                    data_hora,
                    status_anterior,
                    status_novo,
                    detalhes
                FROM auditoria_reservas
                """
            )

            registros_copiados = conexao.execute(
                """
                SELECT
                    id,
                    reserva_id,
                    usuario_id,
                    acao,
                    data_hora,
                    status_anterior,
                    status_novo,
                    detalhes
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
                    "Foram encontrados vínculos inválidos "
                    "na auditoria."
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
    