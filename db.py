import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASS = os.getenv('PASS')
DBNAME = os.getenv('DBNAME')

db_connection = mysql.connector.connect(host=HOST, user=USER, password=PASS, database=DBNAME)
print("Conectado")
cursor = db_connection.cursor()
sql = """CREATE TABLE IF NOT EXISTS user(
    nome VARCHAR(20),
    senha VARCHAR(20),
    id INT
)"""
cursor.execute(sql)


def salvarDados(nome, senha, id):
    sql = (
        "INSERT INTO user (nome, senha, id)"
        "VALUES (%s, %s, %s)"
    )
    # values = (nome, senha, id)
    cursor.execute(sql, (nome, senha, id))
    db_connection.commit()
    print(nome, senha, id)