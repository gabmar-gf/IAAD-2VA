
import mysql.connector
from mysql.connector import Error

def conectar_mysql():
    try:
        conexao = mysql.connector.connect(
            host='187.87.135.21',       
            user='root',
            password='Rural@2025',
            database='Programacoes_Filmes'
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None