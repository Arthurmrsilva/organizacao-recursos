import os
import secrets
from datetime import datetime

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import insert, select, update
from werkzeug.security import check_password_hash

from banco import (
    auditoria_reservas,
    criar_tabelas,
    engine,
    manutencoes,
    notificacoes,
    recursos,
    reservas,
    usuarios,
)
from servico_materiais import (
    registrar_devolucao,
    registrar_retirada,
)
from servico_relatorios import gerar_relatorio
from servico_reservas import (
    alterar_reserva,
    avaliar_reserva,
    cancelar_reserva,
    criar_manutencao,
    criar_reserva,
)

app = Flask(__name__)

# Em desenvolvimento local, gera uma chave ao iniciar o servidor.
app.config["SECRET_KEY"] = (
    os.environ.get("SECRET_KEY") or secrets.token_hex(32)
)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

criar_tabelas()


@app.before_request
def preparar_requisicao():
    g.usuario = None

    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)

    # Verifica os formulários que alteram dados.
    if request.method == "POST":
        token = request.form.get("csrf_token", "")

        if not secrets.compare_digest(
            token.encode("utf-8"),
            session["csrf_token"].encode("utf-8"),
        ):
            return (
                "Formulário expirado. Atualize a página e tente novamente.",
                400,
            )

    usuario_id = session.get("usuario_id")

    if usuario_id is not None:
        with engine.connect() as conexao:
            g.usuario = conexao.execute(
                select(usuarios).where(
                    usuarios.c.id == usuario_id,
                    usuarios.c.ativo.is_(True),
                )
            ).mappings().first()

        if g.usuario is None:
            session.pop("usuario_id", None)


@app.route("/")
def inicio():
    if g.usuario is None:
        return redirect(url_for("login"))

    tipo = request.args.get("tipo", "").strip().upper()
    localizacao = request.args.get("localizacao", "").strip()
    competencia = request.args.get("competencia", "").strip()
    capacidade_texto = request.args.get("capacidade", "").strip()
    inicio_texto = request.args.get("inicio", "").strip()
    fim_texto = request.args.get("fim", "").strip()

    erros = []
    capacidade = None
    inicio_periodo = None
    fim_periodo = None

    if tipo not in ("SALA", "PROFESSOR", "MATERIAL"):
        tipo = ""

    if len(localizacao) > 120:
        erros.append("A localização deve ter até 120 caracteres.")

    if len(competencia) > 150:
        erros.append("A competência deve ter até 150 caracteres.")

    if capacidade_texto:
        try:
            capacidade = int(capacidade_texto)

            if not 1 <= capacidade <= 10000:
                erros.append("A capacidade deve estar entre 1 e 10000.")
        except ValueError:
            erros.append("A capacidade deve ser um número inteiro.")

    # O período é opcional, mas os dois campos devem ser preenchidos.
    if inicio_texto or fim_texto:
        if not inicio_texto or not fim_texto:
            erros.append(
                "Informe o início e o término para consultar a disponibilidade."
            )
        else:
            try:
                inicio_periodo = datetime.strptime(
                    inicio_texto,
                    "%Y-%m-%dT%H:%M",
                )
                fim_periodo = datetime.strptime(
                    fim_texto,
                    "%Y-%m-%dT%H:%M",
                )
            except ValueError:
                erros.append("Informe datas e horários válidos.")
            else:
                if fim_periodo <= inicio_periodo:
                    erros.append(
                        "O término deve ser posterior ao início."
                    )

    consulta = select(recursos).where(
        recursos.c.ativo.is_(True)
    )

    if tipo:
        consulta = consulta.where(recursos.c.tipo == tipo)

    if localizacao and len(localizacao) <= 120:
        consulta = consulta.where(
            recursos.c.localizacao.icontains(
                localizacao,
                autoescape=True,
            )
        )

    if competencia and len(competencia) <= 150:
        consulta = consulta.where(
            recursos.c.competencia.icontains(
                competencia,
                autoescape=True,
            )
        )

    if capacidade is not None and not erros:
        consulta = consulta.where(
            recursos.c.capacidade >= capacidade
        )

    if inicio_periodo is not None and fim_periodo is not None and not erros:
        # Horários consecutivos são permitidos.
        reserva_conflitante = (
            select(reservas.c.id)
            .where(
                reservas.c.recurso_id == recursos.c.id,
                reservas.c.status.in_(
                    ("SOLICITADA", "APROVADA", "EM_USO")
                ),
                reservas.c.inicio < fim_periodo,
                reservas.c.fim > inicio_periodo,
            )
            .exists()
        )

        manutencao_conflitante = (
            select(manutencoes.c.id)
            .where(
                manutencoes.c.recurso_id == recursos.c.id,
                manutencoes.c.ativo.is_(True),
                manutencoes.c.inicio < fim_periodo,
                manutencoes.c.fim > inicio_periodo,
            )
            .exists()
        )

        consulta = consulta.where(
            ~reserva_conflitante,
            ~manutencao_conflitante,
        )

    lista_recursos = []

    if not erros:
        with engine.connect() as conexao:
            lista_recursos = conexao.execute(
                consulta.order_by(recursos.c.nome)
            ).mappings().all()

    return render_template(
        "index.html",
        recursos=lista_recursos,
        tipo_selecionado=tipo,
        localizacao=localizacao,
        competencia=competencia,
        capacidade=capacidade_texto,
        inicio=inicio_texto,
        fim=fim_texto,
        erros=erros,
    ), 400 if erros else 200


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.usuario is not None:
        return redirect(url_for("inicio"))

    erro = None
    status = 200

    if request.method == "POST":
        identificador = request.form.get("login", "").strip()
        senha = request.form.get("senha", "")

        with engine.connect() as conexao:
            usuario = conexao.execute(
                select(usuarios).where(
                    usuarios.c.login == identificador,
                    usuarios.c.ativo.is_(True),
                )
            ).mappings().first()

        if usuario and check_password_hash(usuario["senha_hash"], senha):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["csrf_token"] = secrets.token_hex(32)
            return redirect(url_for("inicio"))

        erro = "Login ou senha inválidos."
        status = 401

    return render_template("login.html", erro=erro), status


@app.route("/sair", methods=["POST"])
def sair():
    session.clear()
    return redirect(url_for("login"))


@app.route("/recursos/novo", methods=["GET", "POST"])
def novo_recurso():
    if g.usuario is None:
        return redirect(url_for("login"))

    if g.usuario["perfil"] != "ADMIN":
        return (
            "Acesso negado. Somente administradores podem cadastrar recursos.",
            403,
        )

    erros = []
    dados = {}
    status = 200

    if request.method == "POST":
        dados = {
            "nome": request.form.get("nome", "").strip(),
            "tipo": request.form.get("tipo", "").strip(),
            "localizacao": request.form.get("localizacao", "").strip(),
            "capacidade": request.form.get("capacidade", "").strip(),
            "competencia": request.form.get("competencia", "").strip(),
            "restrito": request.form.get("restrito") == "sim",
        }

        if not 1 <= len(dados["nome"]) <= 120:
            erros.append("Informe um nome com até 120 caracteres.")

        if dados["tipo"] not in ("SALA", "PROFESSOR", "MATERIAL"):
            erros.append("Selecione um tipo de recurso válido.")

        if not 1 <= len(dados["localizacao"]) <= 120:
            erros.append("Informe uma localização com até 120 caracteres.")

        capacidade = None

        if dados["tipo"] == "SALA":
            try:
                capacidade = int(dados["capacidade"])

                if not 1 <= capacidade <= 10000:
                    erros.append("A capacidade deve estar entre 1 e 10000.")
            except ValueError:
                erros.append("Informe uma capacidade inteira para a sala.")

        competencia = None

        if dados["tipo"] == "PROFESSOR":
            competencia = dados["competencia"]

            if not 1 <= len(competencia) <= 150:
                erros.append(
                    "Informe a competência do professor com até 150 caracteres."
                )

        if not erros:
            with engine.begin() as conexao:
                conexao.execute(
                    insert(recursos).values(
                        nome=dados["nome"],
                        tipo=dados["tipo"],
                        localizacao=dados["localizacao"],
                        capacidade=capacidade,
                        competencia=competencia,
                        restrito=dados["restrito"],
                        ativo=True,
                    )
                )

            return redirect(url_for("inicio"))

        status = 400

    return render_template(
        "novo_recurso.html",
        erros=erros,
        dados=dados,
    ), status


@app.route("/reservas/nova", methods=["GET", "POST"])
def nova_reserva():
    if g.usuario is None:
        return redirect(url_for("login"))

    erros = []
    dados = {}
    status = 200

    if request.method == "POST":
        dados = {
            "recurso_id": request.form.get("recurso_id", "").strip(),
            "inicio": request.form.get("inicio", "").strip(),
            "fim": request.form.get("fim", "").strip(),
            "finalidade": request.form.get("finalidade", "").strip(),
        }

        try:
            reserva_id = criar_reserva(
                engine,
                g.usuario["id"],
                dados,
            )
        except ValueError as erro:
            erros.append(str(erro))
            status = 400
        else:
            session["reserva_criada"] = reserva_id
            return redirect(url_for("nova_reserva"))

    with engine.connect() as conexao:
        lista_recursos = conexao.execute(
            select(recursos)
            .where(recursos.c.ativo.is_(True))
            .order_by(recursos.c.nome)
        ).mappings().all()

    reserva_criada = session.pop("reserva_criada", None)

    return render_template(
        "nova_reserva.html",
        recursos=lista_recursos,
        erros=erros,
        dados=dados,
        reserva_criada=reserva_criada,
    ), status


@app.route(
    "/reservas/<int:reserva_id>/editar",
    methods=["GET", "POST"],
)
def editar_minha_reserva(reserva_id):
    if g.usuario is None:
        return redirect(url_for("login"))

    with engine.connect() as conexao:
        reserva = conexao.execute(
            select(reservas).where(
                reservas.c.id == reserva_id,
                reservas.c.usuario_id == g.usuario["id"],
            )
        ).mappings().first()

    if reserva is None:
        return "Reserva não encontrada para este usuário.", 404

    if reserva["status"] not in ("SOLICITADA", "APROVADA"):
        return (
            "Esta reserva não pode ser alterada na situação atual.",
            400,
        )

    if reserva["inicio"] <= datetime.now():
        return (
            "Não é possível alterar uma reserva que já começou.",
            400,
        )

    erros = []
    status = 200

    dados = {
        "recurso_id": str(reserva["recurso_id"]),
        "inicio": reserva["inicio"].strftime("%Y-%m-%dT%H:%M"),
        "fim": reserva["fim"].strftime("%Y-%m-%dT%H:%M"),
        "finalidade": reserva["finalidade"],
    }

    if request.method == "POST":
        dados = {
            "recurso_id": request.form.get("recurso_id", "").strip(),
            "inicio": request.form.get("inicio", "").strip(),
            "fim": request.form.get("fim", "").strip(),
            "finalidade": request.form.get("finalidade", "").strip(),
        }

        try:
            alterar_reserva(
                engine,
                g.usuario["id"],
                reserva_id,
                dados,
            )
        except ValueError as erro:
            erros.append(str(erro))
            status = 400
        else:
            session["mensagem_reserva"] = (
                f"Reserva nº {reserva_id} alterada com sucesso! "
                "Recursos restritos e professores aguardam nova aprovação."
            )
            return redirect(url_for("minhas_reservas"))

    with engine.connect() as conexao:
        lista_recursos = conexao.execute(
            select(recursos)
            .where(recursos.c.ativo.is_(True))
            .order_by(recursos.c.nome)
        ).mappings().all()

    return render_template(
        "editar_reserva.html",
        reserva=reserva,
        recursos=lista_recursos,
        dados=dados,
        erros=erros,
    ), status


@app.route("/reservas")
def minhas_reservas():
    if g.usuario is None:
        return redirect(url_for("login"))

    filtro = request.args.get("filtro", "ativas").strip().lower()

    if filtro not in ("ativas", "historico", "todas"):
        filtro = "ativas"

    agora = datetime.now()

    # Em uso continua ativo até a devolução, mesmo após o prazo.
    condicao_ativa = (
        (reservas.c.status == "EM_USO")
        | (
            reservas.c.status.in_(("SOLICITADA", "APROVADA"))
            & (reservas.c.fim > agora)
        )
    )

    consulta = (
        select(
            reservas.c.id,
            recursos.c.nome.label("recurso_nome"),
            recursos.c.tipo.label("recurso_tipo"),
            reservas.c.inicio,
            reservas.c.fim,
            reservas.c.finalidade,
            reservas.c.status,
        )
        .join(
            recursos,
            reservas.c.recurso_id == recursos.c.id,
        )
        .where(reservas.c.usuario_id == g.usuario["id"])
    )

    if filtro == "ativas":
        consulta = consulta.where(condicao_ativa)
        consulta = consulta.order_by(
            reservas.c.inicio,
            reservas.c.id,
        )
    else:
        if filtro == "historico":
            consulta = consulta.where(~condicao_ativa)

        consulta = consulta.order_by(
            reservas.c.inicio.desc(),
            reservas.c.id.desc(),
        )

    with engine.connect() as conexao:
        lista_reservas = conexao.execute(
            consulta
        ).mappings().all()

    return render_template(
        "minhas_reservas.html",
        reservas=lista_reservas,
        filtro_selecionado=filtro,
        agora=agora,
    )


@app.route("/reservas/<int:reserva_id>/cancelar", methods=["POST"])
def cancelar_minha_reserva(reserva_id):
    if g.usuario is None:
        return redirect(url_for("login"))

    try:
        cancelar_reserva(
            engine,
            g.usuario["id"],
            reserva_id,
        )
    except ValueError as erro:
        session["erro_reserva"] = str(erro)
    else:
        session["mensagem_reserva"] = (
            f"Reserva nº {reserva_id} cancelada com sucesso!"
        )

    return redirect(url_for("minhas_reservas"))


@app.route("/aprovacoes")
def aprovacoes():
    if g.usuario is None:
        return redirect(url_for("login"))

    if g.usuario["perfil"] != "RESPONSAVEL":
        return "Acesso negado. Área exclusiva do responsável.", 403

    consulta = (
        select(
            reservas.c.id,
            recursos.c.nome.label("recurso_nome"),
            recursos.c.tipo.label("recurso_tipo"),
            usuarios.c.nome.label("solicitante_nome"),
            reservas.c.inicio,
            reservas.c.fim,
            reservas.c.finalidade,
        )
        .select_from(
            reservas.join(
                recursos,
                reservas.c.recurso_id == recursos.c.id,
            ).join(
                usuarios,
                reservas.c.usuario_id == usuarios.c.id,
            )
        )
        .where(
            recursos.c.responsavel_id == g.usuario["id"],
            reservas.c.status == "SOLICITADA",
        )
        .order_by(reservas.c.inicio, reservas.c.id)
    )

    with engine.connect() as conexao:
        pendentes = conexao.execute(
            consulta
        ).mappings().all()

    return render_template(
        "aprovacoes.html",
        reservas=pendentes,
        mensagem=session.pop("mensagem_aprovacao", None),
        erro=session.pop("erro_aprovacao", None),
    )


@app.route(
    "/reservas/<int:reserva_id>/avaliar",
    methods=["POST"],
)
def avaliar_minha_solicitacao(reserva_id):
    if g.usuario is None:
        return redirect(url_for("login"))

    if g.usuario["perfil"] != "RESPONSAVEL":
        return "Acesso negado. Área exclusiva do responsável.", 403

    decisao = request.form.get("decisao", "").strip()

    try:
        avaliar_reserva(
            engine,
            g.usuario["id"],
            reserva_id,
            decisao,
        )
    except ValueError as erro:
        session["erro_aprovacao"] = str(erro)
    else:
        situacao = (
            "aprovada" if decisao == "APROVADA" else "rejeitada"
        )
        session["mensagem_aprovacao"] = (
            f"Reserva nº {reserva_id} {situacao} com sucesso!"
        )

    return redirect(url_for("aprovacoes"))


@app.route("/auditoria")
def consultar_auditoria():
    if g.usuario is None:
        return redirect(url_for("login"))

    if g.usuario["perfil"] != "ADMIN":
        return (
            "Acesso negado. Área exclusiva do administrador.",
            403,
        )

    consulta = (
        select(
            auditoria_reservas.c.id,
            auditoria_reservas.c.reserva_id,
            auditoria_reservas.c.acao,
            auditoria_reservas.c.data_hora,
            auditoria_reservas.c.status_anterior,
            auditoria_reservas.c.status_novo,
            auditoria_reservas.c.detalhes,
            usuarios.c.nome.label("usuario_nome"),
            recursos.c.nome.label("recurso_nome"),
        )
        .select_from(
            auditoria_reservas.join(
                usuarios,
                auditoria_reservas.c.usuario_id == usuarios.c.id,
            ).join(
                reservas,
                auditoria_reservas.c.reserva_id == reservas.c.id,
            ).join(
                recursos,
                reservas.c.recurso_id == recursos.c.id,
            )
        )
        .order_by(
            auditoria_reservas.c.data_hora.desc(),
            auditoria_reservas.c.id.desc(),
        )
        .limit(100)
    )

    with engine.connect() as conexao:
        eventos = conexao.execute(
            consulta
        ).mappings().all()

    return render_template(
        "auditoria.html",
        eventos=eventos,
    )


@app.route("/manutencoes", methods=["GET", "POST"])
def gerenciar_manutencoes():
    if g.usuario is None:
        return redirect(url_for("login"))

    if g.usuario["perfil"] != "ADMIN":
        return (
            "Acesso negado. Área exclusiva do administrador.",
            403,
        )

    erros = []
    dados = {}
    status = 200

    if request.method == "POST":
        dados = {
            "recurso_id": request.form.get("recurso_id", "").strip(),
            "inicio": request.form.get("inicio", "").strip(),
            "fim": request.form.get("fim", "").strip(),
            "motivo": request.form.get("motivo", "").strip(),
        }

        try:
            manutencao_id = criar_manutencao(
                engine,
                g.usuario["id"],
                dados,
            )
        except ValueError as erro:
            erros.append(str(erro))
            status = 400
        else:
            session["mensagem_manutencao"] = (
                f"Manutenção nº {manutencao_id} cadastrada com sucesso!"
            )
            return redirect(url_for("gerenciar_manutencoes"))

    consulta = (
        select(
            manutencoes.c.id,
            manutencoes.c.inicio,
            manutencoes.c.fim,
            manutencoes.c.motivo,
            manutencoes.c.ativo,
            manutencoes.c.criado_em,
            recursos.c.nome.label("recurso_nome"),
            usuarios.c.nome.label("usuario_nome"),
        )
        .select_from(
            manutencoes.join(
                recursos,
                manutencoes.c.recurso_id == recursos.c.id,
            ).join(
                usuarios,
                manutencoes.c.usuario_id == usuarios.c.id,
            )
        )
        .order_by(
            manutencoes.c.inicio.desc(),
            manutencoes.c.id.desc(),
        )
    )

    with engine.connect() as conexao:
        lista_recursos = conexao.execute(
            select(recursos)
            .where(recursos.c.ativo.is_(True))
            .order_by(recursos.c.nome)
        ).mappings().all()

        lista_manutencoes = conexao.execute(
            consulta
        ).mappings().all()

    return render_template(
        "manutencoes.html",
        recursos=lista_recursos,
        manutencoes=lista_manutencoes,
        dados=dados,
        erros=erros,
        mensagem=session.pop("mensagem_manutencao", None),
        agora=datetime.now(),
    ), status


@app.route("/materiais")
def movimentacoes_materiais():
    if g.usuario is None:
        return redirect(url_for("login"))

    if g.usuario["perfil"] not in ("ADMIN", "RESPONSAVEL"):
        return "Acesso negado. Área de gestão de materiais.", 403

    consulta = (
        select(
            reservas.c.id,
            reservas.c.inicio,
            reservas.c.fim,
            reservas.c.finalidade,
            reservas.c.status,
            recursos.c.nome.label("recurso_nome"),
            recursos.c.ativo.label("recurso_ativo"),
            usuarios.c.nome.label("solicitante_nome"),
        )
        .select_from(
            reservas.join(
                recursos,
                reservas.c.recurso_id == recursos.c.id,
            ).join(
                usuarios,
                reservas.c.usuario_id == usuarios.c.id,
            )
        )
        .where(
            recursos.c.tipo == "MATERIAL",
            reservas.c.status.in_(("APROVADA", "EM_USO")),
        )
    )

    if g.usuario["perfil"] == "RESPONSAVEL":
        consulta = consulta.where(
            recursos.c.responsavel_id == g.usuario["id"]
        )

    # Materiais em uso continuam visíveis mesmo após o prazo.
    consulta = consulta.order_by(
        reservas.c.inicio,
        reservas.c.id,
    )

    with engine.connect() as conexao:
        lista = conexao.execute(
            consulta
        ).mappings().all()

    return render_template(
        "materiais.html",
        reservas=lista,
        agora=datetime.now(),
        mensagem=session.pop("mensagem_material", None),
        erro=session.pop("erro_material", None),
    )


@app.route(
    "/materiais/<int:reserva_id>/movimentar",
    methods=["POST"],
)
def movimentar_material_reservado(reserva_id):
    if g.usuario is None:
        return redirect(url_for("login"))

    if g.usuario["perfil"] not in ("ADMIN", "RESPONSAVEL"):
        return "Acesso negado. Área de gestão de materiais.", 403

    acao = request.form.get("acao", "").strip()

    try:
        if acao == "RETIRADA":
            registrar_retirada(
                engine,
                g.usuario["id"],
                reserva_id,
            )
            mensagem = (
                f"Retirada da reserva nº {reserva_id} registrada!"
            )

        elif acao == "DEVOLUCAO":
            registrar_devolucao(
                engine,
                g.usuario["id"],
                reserva_id,
            )
            mensagem = (
                f"Devolução da reserva nº {reserva_id} registrada!"
            )

        else:
            raise ValueError("Selecione uma operação válida.")

    except ValueError as erro:
        session["erro_material"] = str(erro)
    else:
        session["mensagem_material"] = mensagem

    return redirect(url_for("movimentacoes_materiais"))


@app.route("/notificacoes")
def minhas_notificacoes():
    if g.usuario is None:
        return redirect(url_for("login"))

    # Todos os perfis consultam somente os próprios avisos.
    consulta = (
        select(notificacoes)
        .where(
            notificacoes.c.usuario_id == g.usuario["id"]
        )
        .order_by(
            notificacoes.c.criado_em.desc(),
            notificacoes.c.id.desc(),
        )
    )

    with engine.connect() as conexao:
        lista = conexao.execute(
            consulta
        ).mappings().all()

    return render_template(
        "notificacoes.html",
        notificacoes=lista,
        mensagem=session.pop("mensagem_notificacao", None),
    )


@app.route(
    "/notificacoes/<int:notificacao_id>/ler",
    methods=["POST"],
)
def marcar_notificacao_lida(notificacao_id):
    if g.usuario is None:
        return redirect(url_for("login"))

    # O vínculo com o usuário faz parte do próprio UPDATE.
    # Assim, nem o administrador marca avisos de outras pessoas.
    with engine.begin() as conexao:
        resultado = conexao.execute(
            update(notificacoes)
            .where(
                notificacoes.c.id == notificacao_id,
                notificacoes.c.usuario_id == g.usuario["id"],
            )
            .values(lida=True)
        )

        if resultado.rowcount == 0:
            return "Notificação não encontrada para este usuário.", 404

    session["mensagem_notificacao"] = "Notificação marcada como lida."
    return redirect(url_for("minhas_notificacoes"))


@app.route("/relatorios")
def consultar_relatorios():
    if g.usuario is None:
        return redirect(url_for("login"))

    if g.usuario["perfil"] != "ADMIN":
        return (
            "Acesso negado. Área exclusiva do administrador.",
            403,
        )

    inicio_texto = request.args.get("inicio", "").strip()
    fim_texto = request.args.get("fim", "").strip()

    erros = []
    relatorio = None
    status = 200

    try:
        relatorio = gerar_relatorio(
            engine,
            g.usuario["id"],
            {
                "inicio": inicio_texto,
                "fim": fim_texto,
            },
        )
    except ValueError as erro:
        erros.append(str(erro))
        status = 400

    return render_template(
        "relatorios.html",
        relatorio=relatorio,
        inicio=inicio_texto,
        fim=fim_texto,
        erros=erros,
    ), status


if __name__ == "__main__":
    app.run(debug=False)