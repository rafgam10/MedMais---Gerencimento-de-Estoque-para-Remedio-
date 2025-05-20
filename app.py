from flask import Flask, render_template, redirect, url_for, request
from db_config import conectar_banco  # certifique-se que está importando corretamente

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/medicamentos")
def listar_medicamento():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Medicamento")
    medicamentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("medicamentos.html", medicamentos=medicamentos)


@app.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome_medicamento"]
    marca = request.form["marca_medicamento"]
    preco = float(request.form["preco_medicamento"])
    estoque_min = int(request.form["estoque_minimo"])

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO Medicamento (nome_medicamento, marca_medicamento, preco_medicamento, estoque_minimo)
        VALUES (%s, %s, %s, %s)
    """, (nome, marca, preco, estoque_min))
    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect(url_for("listar_medicamento"))

@app.route("/relatorios")
def relatorios():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    # Total de medicamentos
    cursor.execute("SELECT COUNT(*) AS total FROM Medicamento")
    total_medicamentos = cursor.fetchone()["total"]

    # Média de preço dos medicamentos
    cursor.execute("SELECT AVG(preco_medicamento) AS media_preco FROM Medicamento")
    media_preco = round(cursor.fetchone()["media_preco"] or 0, 2)

    # Medicamentos com estoque abaixo do mínimo
    cursor.execute("SELECT * FROM Medicamento WHERE estoque_minimo > 0 AND estoque_minimo <= 5")
    criticos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("relatorio.html", total=total_medicamentos, media=media_preco, criticos=criticos)


if __name__ == "__main__":
    app.run(debug=True)
