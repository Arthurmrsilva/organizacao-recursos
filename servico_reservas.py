import json
from datetime import datetime

from sqlalchemy import insert, select, update

from banco import (
    auditoria_reservas,
    conflitos_reservas,
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
    # Participa da transação da operação.
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
    # Participa da transação da operação.
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


def bloquear_por_conflito(
    conexao,
    usuario_id,
    recurso_id,
    reserva_conflitante_id,
    operacao,
    inicio,
    fim,
    mensagem,
):
    # Deve ser chamada antes de qualquer gravação na reserva.
    conexao.execute(
        insert(conflitos_reservas).values(
            usuario_id=usuario_id,
            recurso_id=recurso_id,
            reserva_conflitante_id=reserva_conflitante_id,
            operacao=operacao,
            inicio=inicio,
            fim=fim,
            criado_em=datetime.now(),
        )
    )

    # Preserva a tentativa bloqueada mesmo com o erro posterior.
    conexao.commit()
    raise ValueError(mensagem)


def verificar_manutencao(conexao, recurso_id, inicio, fim):
    bloqueio = conexao.execute(
        select(manutencoes.c.id)
        .where(
            manutencoes.c.recurso_id == recurso_id,
            manutencoes.c.ativo.is_(True),
            manutencoes.c.inicio < fim,
            manutencoes.c.fim > inicio,
        )
        .limit(1)
    ).first()

    if bloqueio is not None:
        raise ValueError(
            "O recurso está em manutenção no período informado."
        )


def _validar_agendamento(dados, manutencao=False):
    if manutencao:
        campo = "motivo"
        mensagem_texto = (
            "Informe o motivo da manutenção com até 200 caracteres."
        )
        mensagem_inicio = (
            "O início da manutenção deve estar no futuro."
        )
    else:
        campo = "finalidade"
        mensagem_texto = (
            "Informe a finalidade com até 200 caracteres."
        )
        mensagem_inicio = (
            "O início da reserva deve estar no futuro."
        )

    texto = dados.get(campo, "").strip()

    if not 1 <= len(texto) <= 200:
        raise ValueError(mensagem_texto)

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
        raise ValueError(mensagem_inicio)

    return recurso_id, inicio, fim, texto


def _buscar_usuario_ativo(conexao, usuario_id):
    return conexao.execute(
        select(usuarios).where(
            usuarios.c.id == usuario_id,
            usuarios.c.ativo.is_(True),
        )
    ).mappings().first()


def _exigir_usuario_ativo(conexao, usuario_id):
    usuario = _buscar_usuario_ativo(conexao, usuario_id)

    if usuario is None:
        raise ValueError(
            "Usuário não encontrado ou inativo."
        )

    return usuario


def _buscar_recurso_disponivel(conexao, recurso_id):
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

    return recurso


def _buscar_reserva_do_usuario(
    conexao,
    usuario_id,
    reserva_id,
):
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

    return reserva


def _validar_operacao_do_solicitante(reserva, operacao):
    if operacao == "ALTERACAO":
        mensagem_status = (
            "Esta reserva não pode ser alterada "
            "na situação atual."
        )
        mensagem_inicio = (
            "Não é possível alterar uma reserva "
            "que já começou."
        )
    else:
        mensagem_status = (
            "Esta reserva não pode ser cancelada "
            "na situação atual."
        )
        mensagem_inicio = (
            "Não é possível cancelar uma reserva "
            "que já começou."
        )

    if reserva["status"] not in ("SOLICITADA", "APROVADA"):
        raise ValueError(mensagem_status)

    if reserva["inicio"] <= datetime.now():
        raise ValueError(mensagem_inicio)


def _buscar_conflito(
    conexao,
    recurso_id,
    inicio,
    fim,
    reserva_id=None,
):
    consulta = select(reservas.c.id).where(
        reservas.c.recurso_id == recurso_id,
        reservas.c.status.in_(
            ("SOLICITADA", "APROVADA", "EM_USO")
        ),
        reservas.c.inicio < fim,
        reservas.c.fim > inicio,
    )

    if reserva_id is not None:
        # A reserva não pode conflitar com ela mesma.
        consulta = consulta.where(
            reservas.c.id != reserva_id
        )

    return conexao.execute(
        consulta.order_by(reservas.c.id).limit(1)
    ).first()


def _verificar_disponibilidade(
    conexao,
    usuario_id,
    recurso_id,
    inicio,
    fim,
    operacao,
    reserva_id=None,
):
    verificar_manutencao(
        conexao,
        recurso_id,
        inicio,
        fim,
    )

    conflito = _buscar_conflito(
        conexao,
        recurso_id,
        inicio,
        fim,
        reserva_id=reserva_id,
    )

    if conflito is None:
        return

    if operacao == "APROVACAO":
        mensagem = (
            "Existe outra reserva para este recurso "
            "no período informado."
        )
    else:
        mensagem = (
            "Já existe uma reserva para esse recurso "
            "no período informado."
        )

    bloquear_por_conflito(
        conexao=conexao,
        usuario_id=usuario_id,
        recurso_id=recurso_id,
        reserva_conflitante_id=conflito.id,
        operacao=operacao,
        inicio=inicio,
        fim=fim,
        mensagem=mensagem,
    )


def _status_inicial(recurso):
    precisa_aprovacao = (
        recurso["restrito"]
        or recurso["tipo"] == "PROFESSOR"
    )

    return (
        "SOLICITADA"
        if precisa_aprovacao
        else "APROVADA"
    )


def _dados_para_auditoria(
    recurso_id,
    inicio,
    fim,
    finalidade,
    status,
):
    return {
        "recurso_id": recurso_id,
        "inicio": inicio.isoformat(),
        "fim": fim.isoformat(),
        "finalidade": finalidade,
        "status": status,
    }


def criar_manutencao(engine, usuario_id, dados):
    recurso_id, inicio, fim, motivo = _validar_agendamento(
        dados,
        manutencao=True,
    )

    with engine.connect() as conexao:
        try:
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            usuario = _buscar_usuario_ativo(
                conexao,
                usuario_id,
            )

            if usuario is None or usuario["perfil"] != "ADMIN":
                raise ValueError(
                    "Somente administradores podem cadastrar manutenção."
                )

            _buscar_recurso_disponivel(
                conexao,
                recurso_id,
            )

            verificar_manutencao(
                conexao,
                recurso_id,
                inicio,
                fim,
            )

            conflito = _buscar_conflito(
                conexao,
                recurso_id,
                inicio,
                fim,
            )

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
    recurso_id, inicio, fim, finalidade = _validar_agendamento(
        dados
    )

    with engine.connect() as conexao:
        try:
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            _exigir_usuario_ativo(
                conexao,
                usuario_id,
            )

            recurso = _buscar_recurso_disponivel(
                conexao,
                recurso_id,
            )

            _verificar_disponibilidade(
                conexao=conexao,
                usuario_id=usuario_id,
                recurso_id=recurso_id,
                inicio=inicio,
                fim=fim,
                operacao="CRIACAO",
            )

            status = _status_inicial(recurso)

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

            if status == "SOLICITADA":
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
    recurso_id, inicio, fim, finalidade = _validar_agendamento(
        dados
    )

    with engine.connect() as conexao:
        try:
            # Impede gravações entre a verificação e a alteração.
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            _exigir_usuario_ativo(
                conexao,
                usuario_id,
            )

            reserva = _buscar_reserva_do_usuario(
                conexao,
                usuario_id,
                reserva_id,
            )

            _validar_operacao_do_solicitante(
                reserva,
                "ALTERACAO",
            )

            recurso = _buscar_recurso_disponivel(
                conexao,
                recurso_id,
            )

            _verificar_disponibilidade(
                conexao=conexao,
                usuario_id=usuario_id,
                recurso_id=recurso_id,
                inicio=inicio,
                fim=fim,
                operacao="ALTERACAO",
                reserva_id=reserva_id,
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

            # Recursos restritos e professores exigem nova aprovação.
            status_novo = _status_inicial(recurso)

            detalhes = {
                "antes": _dados_para_auditoria(
                    reserva["recurso_id"],
                    reserva["inicio"],
                    reserva["fim"],
                    reserva["finalidade"],
                    reserva["status"],
                ),
                "depois": _dados_para_auditoria(
                    recurso_id,
                    inicio,
                    fim,
                    finalidade,
                    status_novo,
                ),
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

            if status_novo == "SOLICITADA":
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

            # Confirma reserva, auditoria e notificação juntas.
            conexao.commit()
            return reserva_id

        except Exception:
            conexao.rollback()
            raise


def cancelar_reserva(engine, usuario_id, reserva_id):
    with engine.connect() as conexao:
        try:
            conexao.exec_driver_sql("BEGIN IMMEDIATE")

            reserva = _buscar_reserva_do_usuario(
                conexao,
                usuario_id,
                reserva_id,
            )

            _validar_operacao_do_solicitante(
                reserva,
                "CANCELAMENTO",
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

            usuario = _buscar_usuario_ativo(
                conexao,
                usuario_id,
            )

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

            # A rejeição também pode ocorrer com recurso inativo.
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

                _verificar_disponibilidade(
                    conexao=conexao,
                    usuario_id=usuario_id,
                    recurso_id=recurso["id"],
                    inicio=reserva["inicio"],
                    fim=reserva["fim"],
                    operacao="APROVACAO",
                    reserva_id=reserva_id,
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

            # O destinatário é o solicitante.
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