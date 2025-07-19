from conexao_mysql import Db
from mysql.connector import Error

class ElencoRepository:
    
    def __init__(self):
        self.connection = Db.get_connection()
        if not self.connection:
            raise Exception("Não foi possível conectar ao banco de dados.")

    def create(self, num_filme, nome_ator, protagonista):
        if not nome_ator or not nome_ator.strip():
            print("ERRO: O nome do ator não pode ser vazio.")
            return
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES (%s, %s, %s)"
            cursor.execute(query, (num_filme, nome_ator, protagonista))
            self.connection.commit()
            print(f"Ator '{nome_ator}' adicionado ao elenco do filme ID {num_filme}.")
            cursor.close()
        except Error as e:
            print(f"Falha ao adicionar ator ao elenco: {e}")
            raise e

    def find_by_filme_id(self, num_filme):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT nome_ator, protagonista FROM Elenco WHERE num_filme = %s ORDER BY protagonista DESC, nome_ator ASC"
            cursor.execute(query, (num_filme,))
            elenco = cursor.fetchall()
            cursor.close()
            return elenco
        except Error as e:
            print(f"Falha ao buscar elenco para o filme ID {num_filme}: {e}")
            return []

    def delete(self, num_filme, nome_ator):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Elenco WHERE num_filme = %s AND nome_ator = %s"
            cursor.execute(query, (num_filme, nome_ator))
            self.connection.commit()
            print(f"Ator '{nome_ator}' removido do elenco do filme ID {num_filme}.")
            cursor.close()
        except Error as e:
            print(f"Falha ao deletar ator do elenco: {e}")
            raise e
