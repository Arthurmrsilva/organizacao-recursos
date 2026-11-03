from pathlib import Path

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
)

# Salva o banco na mesma pasta deste arquivo.
PASTA_PROJETO = Path(__file__).resolve().parent
CAMINHO_BANCO = PASTA_PROJETO / "recursos.db"

engine = create_engine(
    f"sqlite:///{CAMINHO_BANCO.as_posix()}"
)

metadata = MetaData()

usuarios = Table(
    "usuarios",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(120), nullable=False),
    Column("login", String(80), nullable=False, unique=True),
    Column("senha_hash", String(255), nullable=False),
    Column("perfil", String(20), nullable=False),
    Column("ativo", Boolean, nullable=False, default=True),
    CheckConstraint(
        "perfil IN ('SOLICITANTE', 'RESPONSAVEL', 'ADMIN')",
        name="perfil_usuario_valido",
    ),
)

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
    Column(
        "responsavel_id",
        Integer,
        ForeignKey("usuarios.id"),
        nullable=True,
    ),
    CheckConstraint(
        "tipo IN ('SALA', 'PROFESSOR', 'MATERIAL')",
        name="tipo_recurso_valido",
    ),
    CheckConstraint(
        "capacidade IS NULL OR capacidade > 0",
        name="capacidade_positiva",
    ),
)

reservas = Table(
    "reservas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "recurso_id",
        Integer,
        ForeignKey("recursos.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "usuario_id",
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    ),
    Column("inicio", DateTime, nullable=False),
    Column("fim", DateTime, nullable=False),
    Column("finalidade", String(200), nullable=False),
    Column(
        "status",
        String(20),
        nullable=False,
        default="SOLICITADA",
    ),
    CheckConstraint(
        "fim > inicio",
        name="periodo_reserva_valido",
    ),
    CheckConstraint(
        "status IN ("
        "'SOLICITADA', 'APROVADA', 'EM_USO', 'CONCLUIDA', "
        "'REJEITADA', 'CANCELADA', 'NAO_COMPARECEU'"
        ")",
        name="status_reserva_valido",
    ),
)

auditoria_reservas = Table(
    "auditoria_reservas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "reserva_id",
        Integer,
        ForeignKey("reservas.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "usuario_id",
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    ),
    Column("acao", String(30), nullable=False),
    Column("data_hora", DateTime, nullable=False),
    Column("status_anterior", String(20), nullable=True),
    Column("status_novo", String(20), nullable=False),

    # Guarda os dados anteriores e novos nas alterações.
    # Eventos antigos podem permanecer sem detalhes.
    Column("detalhes", Text, nullable=True),

    CheckConstraint(
        "acao IN ("
        "'CRIACAO', 'CANCELAMENTO', 'APROVACAO', 'REJEICAO', "
        "'RETIRADA', 'DEVOLUCAO', 'ALTERACAO', "
        "'NAO_COMPARECEU'"
        ")",
        name="acao_auditoria_valida",
    ),
    CheckConstraint(
        "status_anterior IS NULL OR status_anterior IN ("
        "'SOLICITADA', 'APROVADA', 'EM_USO', 'CONCLUIDA', "
        "'REJEITADA', 'CANCELADA', 'NAO_COMPARECEU'"
        ")",
        name="status_anterior_auditoria_valido",
    ),
    CheckConstraint(
        "status_novo IN ("
        "'SOLICITADA', 'APROVADA', 'EM_USO', 'CONCLUIDA', "
        "'REJEITADA', 'CANCELADA', 'NAO_COMPARECEU'"
        ")",
        name="status_novo_auditoria_valido",
    ),
)

# Períodos em que um recurso fica indisponível para manutenção.
manutencoes = Table(
    "manutencoes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "recurso_id",
        Integer,
        ForeignKey("recursos.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "usuario_id",
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    ),
    Column("inicio", DateTime, nullable=False),
    Column("fim", DateTime, nullable=False),
    Column("motivo", String(200), nullable=False),
    Column("criado_em", DateTime, nullable=False),
    Column("ativo", Boolean, nullable=False, default=True),
    CheckConstraint(
        "fim > inicio",
        name="periodo_manutencao_valido",
    ),
    CheckConstraint(
        "length(trim(motivo)) BETWEEN 1 AND 200",
        name="motivo_manutencao_valido",
    ),
)

# Avisos internos que simulam notificações aos usuários.
notificacoes = Table(
    "notificacoes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "usuario_id",
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "reserva_id",
        Integer,
        ForeignKey("reservas.id"),
        nullable=False,
        index=True,
    ),
    Column("mensagem", String(300), nullable=False),
    Column("criado_em", DateTime, nullable=False),
    Column("lida", Boolean, nullable=False, default=False),
    CheckConstraint(
        "length(trim(mensagem)) BETWEEN 1 AND 300",
        name="mensagem_notificacao_valida",
    ),
)

# Cada registro representa uma tentativa bloqueada por outra reserva.
# Não registra a finalidade nem cria uma reserva para a tentativa.
conflitos_reservas = Table(
    "conflitos_reservas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "usuario_id",
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "recurso_id",
        Integer,
        ForeignKey("recursos.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "reserva_conflitante_id",
        Integer,
        ForeignKey("reservas.id"),
        nullable=False,
    ),
    Column("operacao", String(20), nullable=False),
    Column("inicio", DateTime, nullable=False),
    Column("fim", DateTime, nullable=False),
    Column("criado_em", DateTime, nullable=False, index=True),
    CheckConstraint(
        "fim > inicio",
        name="periodo_conflito_valido",
    ),
    CheckConstraint(
        "operacao IN ('CRIACAO', 'ALTERACAO', 'APROVACAO')",
        name="operacao_conflito_valida",
    ),
)


def criar_tabelas():
    metadata.create_all(engine)


if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas do banco verificadas e criadas com sucesso!")