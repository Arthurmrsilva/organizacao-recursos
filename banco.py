from pathlib import Path

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

# Salva o banco na mesma pasta deste arquivo.
PASTA_PROJETO = Path(__file__).resolve().parent
CAMINHO_BANCO = PASTA_PROJETO / "recursos.db"

engine = create_engine(
    f"sqlite:///{CAMINHO_BANCO.as_posix()}"
)

metadata = MetaData()

recursos = Table(
    "recursos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(120), nullable=False),
    Column("tipo", String(20), nullable=False),
    Column("localizacao", String(120), nullable=False),
    Column("capacidade", Integer, nullable=True),
    Column("competencia", String(150), nullable=True),
    Column("restrito", Boolean, nullable=False, default=False),
    Column("ativo", Boolean, nullable=False, default=True),
    CheckConstraint(
        "tipo IN ('SALA', 'PROFESSOR', 'MATERIAL')",
        name="tipo_recurso_valido",
    ),
    CheckConstraint(
        "capacidade IS NULL OR capacidade > 0",
        name="capacidade_positiva",
    ),
)


def criar_tabelas():
    metadata.create_all(engine)


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso!")