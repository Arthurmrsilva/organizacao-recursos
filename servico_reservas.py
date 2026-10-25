from datetime import datetime

from sqlalchemy import insert, select, update

from banco import recursos, reservas, usuarios

def criar_reserva(engine, usuario_id, dados):
    finalidade = dados.get("finalidade", "").strip()

    if not 1 <= len(finalidade) <= 200:
        raise ValueError(
            "Informe a finalidade com até 200 caracteres."
        )

    try:
        recurso_id = int(dados.get("recurso_id", ""))
    except (TypeError, ValueError):
        raise ValueError("Selecione um recurso válido.") from None

    try:
        inicio = datetime.strptime(
            dados.get("inicio", ""),
            "%Y-%m-%dT%H:%M",
        )
        fim = datetime.strptime(
            dados.get("fim", ""),
            "%Y-%m-%dT%H:%M",
        )
    except (TypeError, ValueError):
        raise ValueError(
            "Informe datas e horários válidos."
        ) from None

    if fim <= inicio:
        raise ValueError(
            "O término deve ser posterior ao início."
        )

    # Nesta etapa, os horários seguem o relógio local do servidor.
    if inicio <= datetime.now():
        raise ValueError(
            "O início da reserva deve estar no futuro."
        )

    with engine.connect() as conexao:
        try:
            # No SQLite, serializa as gravações antes da consulta.
            # Assim, outra solicitação aguarda esta transação terminar.
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            recurso = conexao.execute(
                select(recursos).where(
                    recursos.c.id == recurso_id,
                    recursos.c.ativo.is_(True),
                )
            ).mappings().first()

            if recurso is None:
                raise ValueError(
                    "O recurso selecionado não está disponível."
                )

            conflito = conexao.execute(
                select(reservas.c.id).where(
                    reservas.c.recurso_id == recurso_id,
                    reservas.c.status.in_(
                        ("SOLICITADA", "APROVADA", "EM_USO")
                    ),
                    reservas.c.inicio < fim,
                    reservas.c.fim > inicio,
                ).limit(1)
            ).first()

            if conflito is not None:
                raise ValueError(
                    "Já existe uma reserva para esse recurso "
                    "no período informado."
                )

            # Recursos restritos e professores precisam de aprovação.
            precisa_aprovacao = (
                recurso["restrito"]
                or recurso["tipo"] == "PROFESSOR"
            )

            status = (
                "SOLICITADA"
                if precisa_aprovacao
                else "APROVADA"
            )

            resultado = conexao.execute(
                insert(reservas).values(
                    recurso_id=recurso_id,
                    usuario_id=usuario_id,
                    inicio=inicio,
                    fim=fim,
                    finalidade=finalidade,
                    status=status,
                )
            )

            reserva_id = resultado.inserted_primary_key[0]
            conexao.commit()

            return reserva_id

        except Exception:
            conexao.rollback()
            raise

def cancelar_reserva(engine, usuario_id, reserva_id):
    with engine.connect() as conexao:
        try:
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            reserva = conexao.execute(
                select(reservas).where(
                    reservas.c.id == reserva_id,
                    reservas.c.usuario_id == usuario_id,
                )
            ).mappings().first()

            if reserva is None:
                raise ValueError(
                    "Reserva não encontrada para este usuário."
                )

            if reserva["status"] not in ("SOLICITADA", "APROVADA"):
                raise ValueError(
                    "Esta reserva não pode ser cancelada "
                    "na situação atual."
                )

            if reserva["inicio"] <= datetime.now():
                raise ValueError(
                    "Não é possível cancelar uma reserva "
                    "que já começou."
                )

            conexao.execute(
                update(reservas)
                .where(
                    reservas.c.id == reserva_id,
                    reservas.c.usuario_id == usuario_id,
                )
                .values(status="CANCELADA")
            )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise
def avaliar_reserva(engine, usuario_id, reserva_id, decisao):
    if decisao not in ("APROVADA", "REJEITADA"):
        raise ValueError("Selecione uma decisão válida.")

    with engine.connect() as conexao:
        try:
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            usuario = conexao.execute(
                select(usuarios).where(
                    usuarios.c.id == usuario_id,
                    usuarios.c.ativo.is_(True),
                )
            ).mappings().first()

            if usuario is None or usuario["perfil"] != "RESPONSAVEL":
                raise ValueError(
                    "Somente um responsável pode avaliar reservas."
                )

            reserva = conexao.execute(
                select(reservas).where(
                    reservas.c.id == reserva_id
                )
            ).mappings().first()

            if reserva is None:
                raise ValueError("Reserva não encontrada.")

            recurso = conexao.execute(
                select(recursos).where(
                    recursos.c.id == reserva["recurso_id"]
                )
            ).mappings().first()

            if (
                recurso is None
                or recurso["responsavel_id"] != usuario_id
            ):
                raise ValueError(
                    "Você não é o responsável por este recurso."
                )

            if reserva["status"] != "SOLICITADA":
                raise ValueError(
                    "Somente reservas aguardando aprovação "
                    "podem ser avaliadas."
                )

            if reserva["inicio"] <= datetime.now():
                raise ValueError(
                    "O prazo para avaliar esta reserva terminou."
                )

            if decisao == "APROVADA":
                if not recurso["ativo"]:
                    raise ValueError(
                        "Não é possível aprovar uma reserva "
                        "de um recurso inativo."
                    )

                conflito = conexao.execute(
                    select(reservas.c.id).where(
                        reservas.c.id != reserva_id,
                        reservas.c.recurso_id == recurso["id"],
                        reservas.c.status.in_(
                            ("SOLICITADA", "APROVADA", "EM_USO")
                        ),
                        reservas.c.inicio < reserva["fim"],
                        reservas.c.fim > reserva["inicio"],
                    ).limit(1)
                ).first()

                if conflito is not None:
                    raise ValueError(
                        "Existe outra reserva para este recurso "
                        "no período informado."
                    )

            conexao.execute(
                update(reservas)
                .where(reservas.c.id == reserva_id)
                .values(status=decisao)
            )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise