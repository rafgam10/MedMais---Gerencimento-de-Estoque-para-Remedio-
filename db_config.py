import os
import mysql.connector

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="rafael",
        password="root",  # Coloque sua senha do MySQL aqui se tiver
        database="gerenciamento_de_estoque"
    )
    
def conectar_banco2():
    conexao = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "rafael"),
        password=os.environ.get("DB_PASSWORD", "root"),
        database=os.environ.get("DB_NAME", "gerenciamento_de_estoque"),
        **{'dictionary': True}
    )
    return conexao