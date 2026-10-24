from flask import Flask, render_template, request
from sqlalchemy import select

from banco import criar_tabelas, engine, recursos

app = Flask(__name__)

criar_tabelas()


@app.route("/")
def inicio():
    tipo = request.args.get("tipo", "").strip().upper()

    tipos_validos = ("SALA", "PROFESSOR", "MATERIAL")

    if tipo not in tipos_validos:
        tipo = ""

    consulta = select(recursos).where(
        recursos.c.ativo.is_(True)
    )

    if tipo:
        consulta = consulta.where(recursos.c.tipo == tipo)

    consulta = consulta.order_by(recursos.c.nome)

    with engine.connect() as conexao:
        lista_recursos = conexao.execute(consulta).mappings().all()

    return render_template(
        "index.html",
        recursos=lista_recursos,
        tipo_selecionado=tipo,
    )


if __name__ == "__main__":
    app.run(debug=False)