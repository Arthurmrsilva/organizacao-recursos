from datetime import datetime

from sqlalchemy import insert, select

from banco import recursos, reservas


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