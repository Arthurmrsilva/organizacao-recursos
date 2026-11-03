import sqlite3
from datetime import datetime

from banco import CAMINHO_BANCO


def atualizar_banco():
    if not CAMINHO_BANCO.is_file():
        print("Banco não encontrado. Nenhuma alteração foi feita.")
        return

    identificador = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    pasta_backup = CAMINHO_BANCO.parent / "backups"
    pasta_backup.mkdir(exist_ok=True)

    caminho_backup = pasta_backup / f"recursos_{identificador}.db"

    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        colunas = {
            coluna[1]
            for coluna in conexao.execute(
                "PRAGMA table_info(recursos)"
            )
        }

        if not colunas:
            raise RuntimeError(
                "A tabela recursos não foi encontrada."
            )

        if "responsavel_id" in colunas:
            print("O banco já possui o campo responsavel_id.")
            return

        # Copia o banco antes de alterar sua estrutura.
        with sqlite3.connect(caminho_backup) as backup:
            conexao.backup(backup)

        conexao.execute(
            "ALTER TABLE recursos "
            "ADD COLUMN responsavel_id INTEGER "
            "REFERENCES usuarios(id)"
        )

    print(f"Cópia de segurança criada em: {caminho_backup}")
    print("Campo responsavel_id adicionado com sucesso!")
    print("Os cadastros e as reservas foram preservados.")


if __name__ == "__main__":
    atualizar_banco()