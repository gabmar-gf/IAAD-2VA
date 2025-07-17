from conexao_mysql import Db
from mysql.connector import Error

class FilmeRepository:
    
    def __init__(self):
        self.connection = Db.get_connection()
        if not self.connection:
            raise Exception("Não foi possível conectar ao banco de dados.")
        
    def create(self, nome, ano, duracao):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Filme (nome, ano, duracao) VALUES (%s, %s, %s)"
            cursor.execute(query, (nome, ano, duracao))
            self.connection.commit()
            print(f"Filme '{nome}' adicionado com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao adicionar filme: {e}")
            raise e
        
    def find_all(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT num_filme, nome, ano, duracao FROM Filme ORDER BY nome")
            filmes = cursor.fetchall()
            cursor.close()
            return filmes
        except Error as e:
            print(f"Falha ao buscar filmes: {e}")
            return []

    def update(self, num_filme, nome, ano, duracao):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Filme SET nome = %s, ano = %s, duracao = %s WHERE num_filme = %s"
            cursor.execute(query, (nome, ano, duracao, num_filme))
            self.connection.commit()
            print(f"Filme ID {num_filme} atualizado para '{nome}'.")
            cursor.close()
        except Error as e:
            print(f"Falha ao atualizar filme ID {num_filme}: {e}")
            raise e

    def delete(self, num_filme):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Filme WHERE num_filme = %s"
            cursor.execute(query, (num_filme,))
            self.connection.commit()
            print(f"Filme ID {num_filme} deletado com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao deletar filme ID {num_filme}: {e}")
            raise e
