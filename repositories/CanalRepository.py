from conexao_mysql import Db
from mysql.connector import Error

class CanalRepository:
    
    def __init__(self):
        self.connection = Db.get_connection()
        
    def create(self, nome):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Canal (nome) VALUES (%s)"
            cursor.execute(query, (nome,))
            self.connection.commit()
            print(f"Canal '{nome}' adicionado com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao adicionar canal: {e}")
            raise e
        
    def find_all(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT num_canal, nome FROM Canal ORDER BY nome")
            canais = cursor.fetchall()
            cursor.close()
            return canais
        except Error as e:
            print(f"Falha ao buscar canais: {e}")
            return []

    def update(self, num_canal, novo_nome):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Canal SET nome = %s WHERE num_canal = %s"
            cursor.execute(query, (novo_nome, num_canal))
            self.connection.commit()
            print(f"Canal ID {num_canal} atualizado para '{novo_nome}'.")
            cursor.close()
        except Error as e:
            print(f"Falha ao atualizar canal ID {num_canal}: {e}")
            raise e

    def delete(self, num_canal):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Canal WHERE num_canal = %s"
            cursor.execute(query, (num_canal,))
            self.connection.commit()
            print(f"Canal ID {num_canal} deletado com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao deletar canal ID {num_canal}: {e}")
            raise e

