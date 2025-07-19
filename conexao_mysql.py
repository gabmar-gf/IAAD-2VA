
import mysql.connector
from mysql.connector import Error

class Db:
    
    @classmethod
    def get_connection(cls):
        print("--> Criando nova conexão com o banco de dados...")

        return mysql.connector.connect(
            host='187.87.135.21',
            user='root',
            password='Rural@2025',
            database='Programacoes_Filmes'
        )
        