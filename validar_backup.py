import argparse
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path


def conferir_integridade(conexao):
    resultado = conexao.execute(
        "PRAGMA integrity_check"
    ).fetchall()

    if resultado != [("ok",)]:
        raise RuntimeError("Falha na integridade do banco.")


def obter_conteudo(conexao):
    # Inclui estrutura e dados, sem exibir informações sensíveis.
    return tuple(conexao.iterdump())


def validar_backup(caminho):
    origem = caminho.resolve(strict=True)

    if not origem.is_file():
        raise ValueError("Informe um arquivo de banco existente.")

    # A origem é aberta somente para leitura.
    endereco = origem.as_uri() + "?mode=ro"

    with tempfile.TemporaryDirectory(
        prefix="validacao_backup_"
    ) as pasta:
        backup = Path(pasta) / "backup.db"
        restaurado = Path(pasta) / "restaurado.db"

        with closing(
            sqlite3.connect(endereco, uri=True)
        ) as conexao_origem:
            conferir_integridade(conexao_origem)

            # Mantém uma visão consistente durante a cópia.
            conexao_origem.execute("BEGIN")
            conteudo_original = obter_conteudo(conexao_origem)

            with closing(
                sqlite3.connect(backup)
            ) as conexao_backup:
                conexao_origem.backup(conexao_backup)

            conexao_origem.rollback()

        # Restaura em outro arquivo, sem sobrescrever a origem.
        with closing(
            sqlite3.connect(backup)
        ) as conexao_backup:
            conferir_integridade(conexao_backup)

            with closing(
                sqlite3.connect(restaurado)
            ) as conexao_restaurada:
                conexao_backup.backup(conexao_restaurada)

        # Reabre o arquivo para conferir a restauração persistida.
        with closing(
            sqlite3.connect(restaurado)
        ) as conexao_restaurada:
            conferir_integridade(conexao_restaurada)

            if obter_conteudo(conexao_restaurada) != conteudo_original:
                raise RuntimeError(
                    "A restauração difere da estrutura ou dos "
                    "dados originais."
                )

            tabelas = conexao_restaurada.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name NOT LIKE 'sqlite_%'
                """
            ).fetchall()

        print("OK: integridade da origem conferida.")
        print("OK: backup criado em diretório temporário.")
        print("OK: restauração reaberta e íntegra.")
        print("OK: estrutura e dados preservados.")
        print(f"Tabelas de aplicação conferidas: {len(tabelas)}.")
        print("Banco de origem aberto somente para leitura.")


def main():
    argumentos = argparse.ArgumentParser(
        description="Valida backup e restauração de SQLite."
    )
    argumentos.add_argument("banco", type=Path)
    opcoes = argumentos.parse_args()
    validar_backup(opcoes.banco)


if __name__ == "__main__":
    main()