from datetime import datetime, timedelta

from sqlalchemy import func, select

from banco import conflitos_reservas, recursos, reservas, usuarios


SITUACOES = {
    "SOLICITADA": "Aguardando aprovação",
    "APROVADA": "Aprovada",
    "EM_USO": "Em uso",
    "CONCLUIDA": "Concluída",
    "REJEITADA": "Rejeitada",
    "CANCELADA": "Cancelada",
    "NAO_COMPARECEU": "Não compareceu",
}

SITUACOES_COM_HORAS = (
    "APROVADA",
    "EM_USO",
    "CONCLUIDA",
)


def validar_periodo(dados):
    inicio_texto = dados.get("inicio", "").strip()
    fim_texto = dados.get("fim", "").strip()

    # Sem datas, consulta todo o histórico.
    if not inicio_texto and not fim_texto:
        return None, None

    if not inicio_texto or not fim_texto:
        raise ValueError(
            "Informe a data inicial e a data final."
        )

    try:
        inicio = datetime.strptime(inicio_texto, "%Y-%m-%d")
        fim = datetime.strptime(fim_texto, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError(
            "Informe datas válidas para o relatório."
        ) from None

    if fim < inicio:
        raise ValueError(
            "A data final não pode ser anterior à data inicial."
        )

    try:
        # Inclui o dia final inteiro.
        fim_exclusivo = fim + timedelta(days=1)
    except OverflowError:
        raise ValueError(
            "A data final está fora do intervalo permitido."
        ) from None

    return inicio, fim_exclusivo


def gerar_relatorio(engine, usuario_id, dados=None):
    if dados is None:
        dados = {}

    with engine.connect() as conexao:
        usuario = conexao.execute(
            select(usuarios).where(
                usuarios.c.id == usuario_id,
                usuarios.c.ativo.is_(True),
            )
        ).mappings().first()

        if usuario is None or usuario["perfil"] != "ADMIN":
            raise ValueError(
                "Somente administradores podem consultar os relatórios."
            )

        inicio_periodo, fim_periodo = validar_periodo(dados)

        consulta = (
            select(
                reservas.c.id,
                reservas.c.recurso_id,
                reservas.c.inicio,
                reservas.c.fim,
                reservas.c.status,
                recursos.c.nome.label("recurso_nome"),
                recursos.c.tipo.label("recurso_tipo"),
            )
            .join(
                recursos,
                reservas.c.recurso_id == recursos.c.id,
            )
        )

        if inicio_periodo is not None:
            # Inclui reservas que tenham parte do período
            # dentro das datas consultadas.
            consulta = consulta.where(
                reservas.c.inicio < fim_periodo,
                reservas.c.fim > inicio_periodo,
            )

        registros = conexao.execute(
            consulta.order_by(
                recursos.c.nome,
                recursos.c.id,
                reservas.c.inicio,
                reservas.c.id,
            )
        ).mappings().all()

        consulta_conflitos = select(
            func.count(conflitos_reservas.c.id)
        )

        if inicio_periodo is not None:
            # Para conflitos, o filtro considera quando a tentativa
            # foi bloqueada, não o horário solicitado para a reserva.
            consulta_conflitos = consulta_conflitos.where(
                conflitos_reservas.c.criado_em >= inicio_periodo,
                conflitos_reservas.c.criado_em < fim_periodo,
            )

        quantidade_conflitos = conexao.execute(
            consulta_conflitos
        ).scalar_one()

    contagem_situacoes = {
        situacao: 0
        for situacao in SITUACOES
    }

    recursos_agrupados = {}
    segundos_totais = 0.0

    for reserva in registros:
        status = reserva["status"]
        contagem_situacoes[status] += 1

        recurso_id = reserva["recurso_id"]

        if recurso_id not in recursos_agrupados:
            recursos_agrupados[recurso_id] = {
                "id": recurso_id,
                "nome": reserva["recurso_nome"],
                "tipo": reserva["recurso_tipo"],
                "total_reservas": 0,
                "reservas_com_horas": 0,
                "segundos_previstos": 0.0,
            }

        resumo = recursos_agrupados[recurso_id]
        resumo["total_reservas"] += 1

        if status not in SITUACOES_COM_HORAS:
            continue

        inicio_contagem = reserva["inicio"]
        fim_contagem = reserva["fim"]

        if inicio_periodo is not None:
            # Conta somente a parte da reserva que está
            # dentro do período escolhido.
            inicio_contagem = max(
                inicio_contagem,
                inicio_periodo,
            )
            fim_contagem = min(
                fim_contagem,
                fim_periodo,
            )

        segundos = (
            fim_contagem - inicio_contagem
        ).total_seconds()

        resumo["reservas_com_horas"] += 1
        resumo["segundos_previstos"] += segundos
        segundos_totais += segundos

    lista_recursos = []

    for resumo in recursos_agrupados.values():
        lista_recursos.append(
            {
                "id": resumo["id"],
                "nome": resumo["nome"],
                "tipo": resumo["tipo"],
                "total_reservas": resumo["total_reservas"],
                "reservas_com_horas": resumo["reservas_com_horas"],
                "horas_previstas": round(
                    resumo["segundos_previstos"] / 3600,
                    2,
                ),
            }
        )

    lista_situacoes = [
        {
            "codigo": codigo,
            "rotulo": rotulo,
            "quantidade": contagem_situacoes[codigo],
        }
        for codigo, rotulo in SITUACOES.items()
    ]

    return {
        "total_reservas": len(registros),
        "horas_previstas": round(segundos_totais / 3600, 2),
        "situacoes": lista_situacoes,
        "recursos": lista_recursos,
        "conflitos_evitados": quantidade_conflitos,
    }