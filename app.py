import os
import secrets

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import insert, select
from werkzeug.security import check_password_hash

from banco import criar_tabelas, engine, recursos, reservas, usuarios
from servico_reservas import criar_reserva

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

    # Verifica a proteção dos formulários que alteram dados.
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

    erros = []
    capacidade = None

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
@app.route("/reservas")
def minhas_reservas():
    if g.usuario is None:
        return redirect(url_for("login"))

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
        .order_by(reservas.c.inicio.desc(), reservas.c.id.desc())
    )

    with engine.connect() as conexao:
        lista_reservas = conexao.execute(
            consulta
        ).mappings().all()

    return render_template(
        "minhas_reservas.html",
        reservas=lista_reservas,
    )

if __name__ == "__main__":
    app.run(debug=False)