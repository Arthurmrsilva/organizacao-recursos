from getpass import getpass

from sqlalchemy import insert, select
from werkzeug.security import generate_password_hash

from banco import criar_tabelas, engine, usuarios


def criar_administrador():
    criar_tabelas()

    with engine.connect() as conexao:
        existente = conexao.execute(
            select(usuarios.c.id).where(
                usuarios.c.login == "admin"
            )
        ).first()

    if existente is not None:
        print("O usuário admin já existe. Nenhum dado foi alterado.")
        return

    senha = getpass("Crie a senha do admin (mínimo de 8 caracteres): ")

    if len(senha) < 8:
        print("Senha muito curta. Execute novamente.")
        return

    confirmacao = getpass("Digite a senha novamente: ")

    if senha != confirmacao:
        print("As senhas são diferentes. Execute novamente.")
        return

    with engine.begin() as conexao:
        conexao.execute(
            insert(usuarios).values(
                nome="Administrador do projeto",
                login="admin",
                senha_hash=generate_password_hash(senha),
                perfil="ADMIN",
                ativo=True,
            )
        )

    print("Administrador criado com sucesso!")
    print("Login: admin")


if __name__ == "__main__":
    criar_administrador()