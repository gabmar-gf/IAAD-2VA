from conexao_mysql import Db
from mysql.connector import Error
import datetime

class ExibicoesRepository:

    def __init__(self):
        self.connection = Db.get_connection()
        if not self.connection:
            raise Exception("Não foi possível conectar ao banco de dados.")

    def create(self, num_filme, num_canal, data_exibicao, hora_exibicao):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (num_filme, num_canal, data_exibicao, hora_exibicao))
            self.connection.commit()
            print("Exibição adicionada com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao adicionar exibição: {e}")
            raise e

    def find_all(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    f.nome AS filme, 
                    c.nome AS canal, 
                    e.data_exibicao, 
                    TIME_FORMAT(e.hora_exibicao, '%H:%i:%s') AS hora_exibicao,
                    e.num_filme,
                    e.num_canal
                FROM Exibicao e
                JOIN Filme f ON e.num_filme = f.num_filme
                JOIN Canal c ON e.num_canal = c.num_canal
                ORDER BY e.data_exibicao DESC, e.hora_exibicao DESC
            """
            cursor.execute(query)
            exibicoes = cursor.fetchall()
            cursor.close()
            return exibicoes
        except Error as e:
            print(f"Falha ao buscar exibições: {e}")
            return []

    def get_total_count(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM Exibicao"
            cursor.execute(query)
            total = cursor.fetchone()[0]
            cursor.close()
            return total
        except Error as e:
            print(f"Falha ao contar exibições: {e}")
            return 0
        
    def find_by_filme_id(self, num_filme):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT
                    c.nome AS canal,
                    e.data_exibicao,
                    TIME_FORMAT(e.hora_exibicao, '%H:%i') AS hora_exibicao
                FROM Exibicao e
                JOIN Canal c ON e.num_canal = c.num_canal
                WHERE e.num_filme = %s
                ORDER BY e.data_exibicao, e.hora_exibicao
            """
            cursor.execute(query, (num_filme,))
            exibicoes = cursor.fetchall()
            cursor.close()
            return exibicoes
        except Error as e:
            print(f"Falha ao buscar exibições para o filme ID {num_filme}: {e}")
            return []

    def update(self, old_num_filme, old_num_canal, old_data, old_hora, new_num_filme, new_num_canal, new_data, new_hora):
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Exibicao
                SET num_filme = %s, num_canal = %s, data_exibicao = %s, hora_exibicao = %s
                WHERE num_filme = %s AND num_canal = %s AND data_exibicao = %s AND hora_exibicao = %s
            """
            cursor.execute(query, (new_num_filme, new_num_canal, new_data, new_hora, old_num_filme, old_num_canal, old_data, old_hora))
            self.connection.commit()
            print(f"Exibição atualizada com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao atualizar exibição: {e}")
            raise e

    def delete(self, num_filme, num_canal, data_exibicao, hora_exibicao):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Exibicao WHERE num_filme = %s AND num_canal = %s AND data_exibicao = %s AND hora_exibicao = %s"
            cursor.execute(query, (num_filme, num_canal, data_exibicao, hora_exibicao))
            self.connection.commit()
            print(f"Exibição deletada com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao deletar exibição: {e}")
            raise e
