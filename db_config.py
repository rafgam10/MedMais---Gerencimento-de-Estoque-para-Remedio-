import mysql.connector

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="rafael",
        password="root",  # Coloque sua senha do MySQL aqui se tiver
        database="gerenciamento_de_estoque"
    )