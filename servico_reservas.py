import json
from datetime import datetime

from sqlalchemy import insert, select, update

from banco import (
    auditoria_reservas,
    manutencoes,
    notificacoes,
    recursos,
    reservas,
    usuarios,
)


def registrar_notificacao(
    conexao,
    usuario_id,
    reserva_id,
    mensagem,
):
    # Usa a transação da reserva, sem commit separado.
    conexao.execute(
        insert(notificacoes).values(
            usuario_id=usuario_id,
            reserva_id=reserva_id,
            mensagem=mensagem,
            criado_em=datetime.now(),
            lida=False,
        )
    )


def registrar_auditoria(
    conexao,
    reserva_id,
    usuario_id,
    acao,
    status_anterior,
    status_novo,
    detalhes=None,
):
    # Usa a conexão da operação, sem fazer um commit separado.
    conexao.execute(
        insert(auditoria_reservas).values(
            reserva_id=reserva_id,
            usuario_id=usuario_id,
            acao=acao,
            data_hora=datetime.now(),
            status_anterior=status_anterior,
            status_novo=status_novo,
            detalhes=(
                json.dumps(detalhes, ensure_ascii=False)
                if detalhes is not None
                else None
            ),
        )
    )


def verificar_manutencao(conexao, recurso_id, inicio, fim):
    bloqueio = conexao.execute(
        select(manutencoes.c.id).where(
            manutencoes.c.recurso_id == recurso_id,
            manutencoes.c.ativo.is_(True),
            manutencoes.c.inicio < fim,
            manutencoes.c.fim > inicio,
        ).limit(1)
    ).first()

    if bloqueio is not None:
        raise ValueError(
            "O recurso está em manutenção no período informado."
        )


def criar_manutencao(engine, usuario_id, dados):
    motivo = dados.get("motivo", "").strip()

    if not 1 <= len(motivo) <= 200:
        raise ValueError(
            "Informe o motivo da manutenção com até 200 caracteres."
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

    if inicio <= datetime.now():
        raise ValueError(
            "O início da manutenção deve estar no futuro."
        )

    with engine.connect() as conexao:
        try:
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            usuario = conexao.execute(
                select(usuarios).where(
                    usuarios.c.id == usuario_id,
                    usuarios.c.ativo.is_(True),
                )
            ).mappings().first()

            if usuario is None or usuario["perfil"] != "ADMIN":
                raise ValueError(
                    "Somente administradores podem cadastrar manutenção."
                )

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

            verificar_manutencao(
                conexao,
                recurso_id,
                inicio,
                fim,
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
                    "no período da manutenção. Resolva a reserva "
                    "antes de cadastrar o bloqueio."
                )

            resultado = conexao.execute(
                insert(manutencoes).values(
                    recurso_id=recurso_id,
                    usuario_id=usuario_id,
                    inicio=inicio,
                    fim=fim,
                    motivo=motivo,
                    criado_em=datetime.now(),
                    ativo=True,
                )
            )

            manutencao_id = resultado.inserted_primary_key[0]

            conexao.commit()
            return manutencao_id

        except Exception:
            conexao.rollback()
            raise


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

    # Os horários seguem o relógio local do servidor.
    if inicio <= datetime.now():
        raise ValueError(
            "O início da reserva deve estar no futuro."
        )

    with engine.connect() as conexao:
        try:
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

            verificar_manutencao(
                conexao,
                recurso_id,
                inicio,
                fim,
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

            registrar_auditoria(
                conexao=conexao,
                reserva_id=reserva_id,
                usuario_id=usuario_id,
                acao="CRIACAO",
                status_anterior=None,
                status_novo=status,
            )

            if precisa_aprovacao:
                mensagem = (
                    f"Reserva nº {reserva_id} criada. "
                    "Sua solicitação está aguardando aprovação."
                )
            else:
                mensagem = (
                    f"Reserva nº {reserva_id} criada "
                    "e aprovada automaticamente."
                )

            registrar_notificacao(
                conexao=conexao,
                usuario_id=usuario_id,
                reserva_id=reserva_id,
                mensagem=mensagem,
            )

            conexao.commit()
            return reserva_id

        except Exception:
            conexao.rollback()
            raise


def alterar_reserva(engine, usuario_id, reserva_id, dados):
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

    if inicio <= datetime.now():
        raise ValueError(
            "O início da reserva deve estar no futuro."
        )

    with engine.connect() as conexao:
        try:
            # Impede outra gravação entre a verificação e a alteração.
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            usuario = conexao.execute(
                select(usuarios).where(
                    usuarios.c.id == usuario_id,
                    usuarios.c.ativo.is_(True),
                )
            ).mappings().first()

            if usuario is None:
                raise ValueError(
                    "Usuário não encontrado ou inativo."
                )

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
                    "Esta reserva não pode ser alterada "
                    "na situação atual."
                )

            if reserva["inicio"] <= datetime.now():
                raise ValueError(
                    "Não é possível alterar uma reserva "
                    "que já começou."
                )

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

            verificar_manutencao(
                conexao,
                recurso_id,
                inicio,
                fim,
            )

            conflito = conexao.execute(
                select(reservas.c.id).where(
                    # A reserva não pode conflitar com ela mesma.
                    reservas.c.id != reserva_id,
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

            houve_alteracao = (
                reserva["recurso_id"] != recurso_id
                or reserva["inicio"] != inicio
                or reserva["fim"] != fim
                or reserva["finalidade"] != finalidade
            )

            if not houve_alteracao:
                raise ValueError(
                    "Nenhuma alteração foi informada."
                )

            precisa_aprovacao = (
                recurso["restrito"]
                or recurso["tipo"] == "PROFESSOR"
            )

            # Recursos restritos e professores passam por nova aprovação.
            status_novo = (
                "SOLICITADA"
                if precisa_aprovacao
                else "APROVADA"
            )

            detalhes = {
                "antes": {
                    "recurso_id": reserva["recurso_id"],
                    "inicio": reserva["inicio"].isoformat(),
                    "fim": reserva["fim"].isoformat(),
                    "finalidade": reserva["finalidade"],
                    "status": reserva["status"],
                },
                "depois": {
                    "recurso_id": recurso_id,
                    "inicio": inicio.isoformat(),
                    "fim": fim.isoformat(),
                    "finalidade": finalidade,
                    "status": status_novo,
                },
            }

            conexao.execute(
                update(reservas)
                .where(
                    reservas.c.id == reserva_id,
                    reservas.c.usuario_id == usuario_id,
                )
                .values(
                    recurso_id=recurso_id,
                    inicio=inicio,
                    fim=fim,
                    finalidade=finalidade,
                    status=status_novo,
                )
            )

            registrar_auditoria(
                conexao=conexao,
                reserva_id=reserva_id,
                usuario_id=usuario_id,
                acao="ALTERACAO",
                status_anterior=reserva["status"],
                status_novo=status_novo,
                detalhes=detalhes,
            )

            if precisa_aprovacao:
                mensagem = (
                    f"Reserva nº {reserva_id} alterada. "
                    "Sua solicitação está aguardando nova aprovação."
                )
            else:
                mensagem = (
                    f"Reserva nº {reserva_id} alterada. "
                    "A reserva está aprovada."
                )

            registrar_notificacao(
                conexao=conexao,
                usuario_id=reserva["usuario_id"],
                reserva_id=reserva_id,
                mensagem=mensagem,
            )

            # Reserva, auditoria e notificação são confirmadas juntas.
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

            registrar_auditoria(
                conexao=conexao,
                reserva_id=reserva_id,
                usuario_id=usuario_id,
                acao="CANCELAMENTO",
                status_anterior=reserva["status"],
                status_novo="CANCELADA",
            )

            registrar_notificacao(
                conexao=conexao,
                usuario_id=reserva["usuario_id"],
                reserva_id=reserva_id,
                mensagem=f"Reserva nº {reserva_id} cancelada.",
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

                verificar_manutencao(
                    conexao,
                    recurso["id"],
                    reserva["inicio"],
                    reserva["fim"],
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

            acao = (
                "APROVACAO"
                if decisao == "APROVADA"
                else "REJEICAO"
            )

            registrar_auditoria(
                conexao=conexao,
                reserva_id=reserva_id,
                usuario_id=usuario_id,
                acao=acao,
                status_anterior=reserva["status"],
                status_novo=decisao,
            )

            situacao = (
                "aprovada"
                if decisao == "APROVADA"
                else "rejeitada"
            )

            # O destinatário é o solicitante, não quem avaliou.
            registrar_notificacao(
                conexao=conexao,
                usuario_id=reserva["usuario_id"],
                reserva_id=reserva_id,
                mensagem=(
                    f"Reserva nº {reserva_id} "
                    f"{situacao} pelo responsável."
                ),
            )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise