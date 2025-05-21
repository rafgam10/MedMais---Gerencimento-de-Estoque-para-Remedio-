from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, request, jsonify
from db_config import conectar_banco  # certifique-se que está importando corretamente

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

# ============== ROTAS =============

## ===== ROTA DE MEDICAMENTOS:
@app.route("/medicamentos")
def listar_medicamento():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Medicamento")
    medicamentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("medicamentos.html", medicamentos=medicamentos)

## ===== ROTA DE FORNECEDOR:
@app.route("/fornecedor")
def listar_fornecedor():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Fornecedor")
    fornecedor = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("fornecedor.html", fornecedor=fornecedor)

## ====== ROTA DE LOTE:
@app.route("/lote")
def listar_lote():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            L.id_lote_pk,
            L.data_entrada_lote,
            L.quantidade,
            L.data_validade,
            M.nome_medicamento,
            F.nome_fornecedor
        FROM Lote L
        JOIN Medicamento M ON L.medicamento_id_pk = M.medicamento_id_pk
        JOIN Fornecedor F ON L.id_fornecedor_pk = F.id_fornecedor_pk
    """)

    lote = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template("lote.html", lote=lote)

# ====== ROTA DE CADASTROS DAS TABELAS ======

## ==== ROTA DE CADASTRO DE MEDICAMENTOS:
@app.route("/cadastroMedicamento", methods=["GET"])
def cadastro_Medicamento():
    return render_template("cadastroMedicamento.html")

@app.route("/cadastrarMedicamento", methods=["POST"])
def cadastrar_Medicamento():
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

## ==== ROTA DE CADASTRO DE FORNECEDOR:
@app.route("/cadastroFornecedor", methods=["GET"])
def cadastro_Fornecedor():
    return render_template("cadastroFornecedor.html")

@app.route("/cadastrarFornecedor", methods=["POST"])
def cadastrar_Fornecedor():
    nome = request.form["nome_fornecedor"]
    contato = request.form["contato_fornecedor"]
    cnpj = request.form["cnpj_fornecedor"]

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO Fornecedor (nome_fornecedor, contato_fornecedor, cnpj_fornecedor)
        VALUES (%s, %s, %s)
    """, (nome, contato, cnpj))
    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect(url_for("listar_fornecedor"))

## ==== ROTA DE CADASTRO DE LOTE:
@app.route("/cadastroLote", methods=["GET"])
def cadastro_Lote():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT medicamento_id_pk, nome_medicamento FROM Medicamento")
    medicamentos = cursor.fetchall()

    cursor.execute("SELECT id_fornecedor_pk, nome_fornecedor FROM Fornecedor")
    fornecedores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("cadastroLote.html", medicamentos=medicamentos, fornecedores=fornecedores)

@app.route("/cadastrarLote", methods=["POST"])
def cadastrar_Lote():
    data_entrada = request.form["data_entrada_lote"]
    quantidade = request.form["quantidade"]
    data_validade = request.form["data_validade"]
    medicamento_id_pk = request.form["medicamento_id_pk"]
    id_fornecedor_pk = request.form["id_fornecedor_pk"]

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO Lote (data_entrada_lote, quantidade, medicamento_id_pk, id_fornecedor_pk, data_validade)
        VALUES (%s, %s, %s, %s, %s)
    """, (data_entrada, quantidade, medicamento_id_pk, id_fornecedor_pk, data_validade))
    
    # cursor.execute("""
    #     UPDATE Medicamento
    #     SET estoque_atual = estoque_atual + %s
    #     WHERE medicamento_id_pk = %s
    # """, (quantidade, medicamento_id_pk))
    
    conexao.commit()
    cursor.close()
    conexao.close()
    
    return redirect(url_for("listar_lote"))

## ==== ROTA DE RELATÓRIOS:
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


def obter_lotes():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)  # ← ESSA LINHA É FUNDAMENTAL
    cursor.execute("""
        SELECT 
            l.id_lote_pk, 
            l.data_validade, 
            l.quantidade, 
            m.nome_medicamento 
        FROM Lote l
        JOIN Medicamento m ON l.medicamento_id_pk = m.medicamento_id_pk
    """)
    lotes = cursor.fetchall()
    conn.close()
    return lotes

@app.route('/relatorioValidade')
def relatorio_validade():
    data_atual = datetime.now().date()  # garantir que é do tipo date
    lotes_raw = obter_lotes()

    lote = []
    for l in lotes_raw:
        data_validade = l['data_validade']  # já vem como datetime.date no MySQL
        dias_restantes = (data_validade - data_atual).days

        if dias_restantes < 0:
            status_cor = 'table-danger'      # vencido
        elif dias_restantes <= 30:
            status_cor = 'table-warning'     # perto de vencer
        else:
            status_cor = 'table-success'     # válido

        lote.append({
            'id': l['id_lote_pk'],
            'nome_medicamento': l['nome_medicamento'],
            'data_validade': data_validade.strftime('%Y-%m-%d'),
            'quantidade': l['quantidade'],
            'status_cor': status_cor,
            'dias_restantes': dias_restantes
        })

    return render_template('relatorioValidade.html', lote=lote, data_atual=data_atual)



## ====== ROTAS PARA EDITAR E EXCLUIR ========

# === MEDICAMENTOS:
@app.route("/editar/medicamento/<int:id>", methods=["POST"])
def editar_medicamento(id):
    dados = request.get_json()
    novo_nome = dados.get("novo_nome")

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE Medicamento
        SET nome_medicamento = %s
        WHERE medicamento_id_pk = %s
    """, (novo_nome, id))
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"status": "sucesso"})

@app.route("/deletar/medicamento/<int:id>")
def deletar_medicamento(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Medicamento WHERE medicamento_id_pk = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/medicamentos")


# === FORNECEDORES:
@app.route("/editar/fornecedor/<int:id>", methods=["POST"])
def editar_fornecedor(id):
    dados = request.get_json()
    novo_nome = dados.get("novo_nome")

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE Fornecedor
        SET nome_fornecedor = %s
        WHERE id_fornecedor_pk = %s
    """, (novo_nome, id))
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"status": "sucesso"})

@app.route("/deletar/fornecedor/<int:id>")
def deletar_fornecedor(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Fornecedor WHERE id_fornecedor_pk = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/fornecedor")

# === LOTES:
@app.route("/editar/lote/<int:id>", methods=["POST"])
def editar_lote(id):
    dados = request.get_json()
    nova_quantidade = dados.get("nova_quantidade")

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE Lote
        SET quantidade = %s
        WHERE id_lote_pk = %s
    """, (nova_quantidade, id))
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"status": "sucesso"})


@app.route("/deletar/lote/<int:id>")
def deletar_lote(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Lote WHERE id_lote_pk = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect("/lote")



if __name__ == "__main__":
    from os import environ
    app.run(
        host="0.0.0.0",
        port=int(environ.get("PORT", 5000)),
        debug=True
    )
