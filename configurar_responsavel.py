from getpass import getpass

from sqlalchemy import insert, select, update
from werkzeug.security import generate_password_hash

from banco import engine, recursos, usuarios


def configurar():
    login = input("Login do responsável: ").strip()

    if not 1 <= len(login) <= 80:
        print("Informe um login com até 80 caracteres.")
        return

    with engine.connect() as conexao:
        usuario = conexao.execute(
            select(usuarios).where(
                usuarios.c.login == login
            )
        ).mappings().first()

    if usuario is not None:
        if (
            usuario["perfil"] != "RESPONSAVEL"
            or not usuario["ativo"]
        ):
            print(
                "Este login já pertence a outro perfil "
                "ou está inativo. Use outro login."
            )
            return

        responsavel_id = usuario["id"]
        print(f"Responsável encontrado: {usuario['nome']}")

    else:
        nome = input("Nome do responsável: ").strip()

        if not 1 <= len(nome) <= 120:
            print("Informe um nome com até 120 caracteres.")
            return

        senha = getpass("Crie uma senha com pelo menos 8 caracteres: ")
        confirmacao = getpass("Repita a senha: ")

        if len(senha) < 8:
            print("A senha deve ter pelo menos 8 caracteres.")
            return

        if senha != confirmacao:
            print("As senhas não conferem.")
            return

        with engine.begin() as conexao:
            resultado = conexao.execute(
                insert(usuarios).values(
                    nome=nome,
                    login=login,
                    senha_hash=generate_password_hash(senha),
                    perfil="RESPONSAVEL",
                    ativo=True,
                )
            )
            responsavel_id = resultado.inserted_primary_key[0]

        print("Usuário responsável criado com sucesso!")

    with engine.connect() as conexao:
        lista = conexao.execute(
            select(recursos)
            .where(recursos.c.ativo.is_(True))
            .order_by(recursos.c.id)
        ).mappings().all()

    print("\nRecursos ativos:")

    for recurso in lista:
        print(
            f"{recurso['id']} - {recurso['nome']} "
            f"({recurso['tipo']})"
        )

    if not lista:
        print("Cadastre um recurso antes de fazer a vinculação.")
        return

    try:
        recurso_id = int(
            input("\nDigite o número do recurso: ")
        )
    except ValueError:
        print("Digite um número inteiro.")
        return

    with engine.begin() as conexao:
        resultado = conexao.execute(
            update(recursos)
            .where(
                recursos.c.id == recurso_id,
                recursos.c.ativo.is_(True),
                (
                    recursos.c.responsavel_id.is_(None)
                    | (recursos.c.responsavel_id == responsavel_id)
                ),
            )
            .values(responsavel_id=responsavel_id)
        )

    if resultado.rowcount == 0:
        print(
            "Recurso inválido, inativo ou já vinculado "
            "a outro responsável."
        )
        return

    print("Responsável vinculado ao recurso com sucesso!")


if __name__ == "__main__":
    configurar()