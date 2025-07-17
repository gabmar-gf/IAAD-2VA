from conexao_mysql import Db
from mysql.connector import Error

class ExibicoesRepository:

    def __init__(self):
        self.connection = Db.get_connection()

    def create(self, filme_id, canal_id, data_exibicao):
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO Exibicao (filme_id, canal_id, data_exibicao)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (filme_id, canal_id, data_exibicao))
            self.connection.commit()
            print(f"Exibição adicionada com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao adicionar exibição: {e}")
            raise e

    def find_all(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT e.id, f.titulo AS filme, c.nome AS canal, e.data_exibicao
                FROM Exibicao e
                JOIN Filme f ON e.filme_id = f.id
                JOIN Canal c ON e.canal_id = c.num_canal
                ORDER BY e.data_exibicao DESC
            """
            cursor.execute(query)
            exibicoes = cursor.fetchall()
            cursor.close()
            return exibicoes
        except Error as e:
            print(f"Falha ao buscar exibições: {e}")
            return []

    def update(self, id, novo_filme_id, novo_canal_id, nova_data):
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Exibicao
                SET filme_id = %s, canal_id = %s, data_exibicao = %s
                WHERE id = %s
            """
            cursor.execute(query, (novo_filme_id, novo_canal_id, nova_data, id))
            self.connection.commit()
            print(f"Exibição ID {id} atualizada com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao atualizar exibição ID {id}: {e}")
            raise e

    def delete(self, id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Exibicao WHERE id = %s"
            cursor.execute(query, (id,))
            self.connection.commit()
            print(f"Exibição ID {id} deletada com sucesso.")
            cursor.close()
        except Error as e:
            print(f"Falha ao deletar exibição ID {id}: {e}")
            raise e
