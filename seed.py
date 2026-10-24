from sqlalchemy import insert, select

from banco import criar_tabelas, engine, recursos


def cadastrar_exemplos():
    criar_tabelas()

    exemplos = [
        {
            "nome": "Sala 101",
            "tipo": "SALA",
            "localizacao": "Bloco A",
            "capacidade": 30,
            "competencia": None,
            "restrito": False,
            "ativo": True,
        },
        {
            "nome": "Professor Carlos",
            "tipo": "PROFESSOR",
            "localizacao": "Bloco A",
            "capacidade": None,
            "competencia": "Programação em Python",
            "restrito": False,
            "ativo": True,
        },
        {
            "nome": "Projetor 01",
            "tipo": "MATERIAL",
            "localizacao": "Sala de equipamentos",
            "capacidade": None,
            "competencia": None,
            "restrito": True,
            "ativo": True,
        },
    ]

    # Confirma as alterações juntas ao terminar sem erros.
    with engine.begin() as conexao:
        for exemplo in exemplos:
            consulta = select(recursos.c.id).where(
                recursos.c.nome == exemplo["nome"],
                recursos.c.tipo == exemplo["tipo"],
            )

            existente = conexao.execute(consulta).first()

            if existente is None:
                conexao.execute(insert(recursos).values(**exemplo))
                print(f"Cadastrado: {exemplo['nome']}")
            else:
                print(f"Já existe: {exemplo['nome']}")


if __name__ == "__main__":
    cadastrar_exemplos()