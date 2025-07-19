from conexao_mysql import Db
from mysql.connector import Error

class DashboardRepository:

    def __init__(self):
        self.connection = Db.get_connection()
        if not self.connection:
            raise Exception("Não foi possível conectar ao banco de dados.")

    def get_estatisticas_gerais(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT
                    (SELECT COUNT(*) FROM Filme) AS total_filmes,
                    (SELECT COUNT(DISTINCT nome_ator) FROM Elenco) AS total_atores,
                    (SELECT COUNT(*) FROM Exibicao) AS total_exibicoes;
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar estatísticas gerais: {e}")
            return {"total_filmes": 0, "total_atores": 0, "total_exibicoes": 0}

    def get_filmes_duracao_extrema(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    (SELECT nome FROM Filme WHERE duracao IS NOT NULL ORDER BY duracao ASC LIMIT 1) AS filme_mais_curto,
                    (SELECT MIN(duracao) FROM Filme) AS duracao_minima,
                    (SELECT nome FROM Filme WHERE duracao IS NOT NULL ORDER BY duracao DESC LIMIT 1) AS filme_mais_longo,
                    (SELECT MAX(duracao) FROM Filme) AS duracao_maxima;
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar filmes com duração extrema: {e}")
            return None

    def get_exibicoes_por_canal(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT C.nome AS canal, COUNT(*) AS total_exibicoes
                FROM Exibicao E
                JOIN Canal C ON E.num_canal = C.num_canal
                GROUP BY C.nome
                ORDER BY total_exibicoes DESC;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar exibições por canal: {e}")
            return []

    def get_duracao_media_por_ano(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT ano, AVG(duracao) AS media_duracao
                FROM Filme
                WHERE duracao IS NOT NULL AND ano IS NOT NULL
                GROUP BY ano
                ORDER BY ano;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar duração média por ano: {e}")
            return []

    def get_top_5_filmes_mais_exibidos(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT F.nome, COUNT(*) AS total_exibicoes
                FROM Exibicao E
                JOIN Filme F ON E.num_filme = F.num_filme
                GROUP BY F.nome
                ORDER BY total_exibicoes DESC
                LIMIT 5;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar top 5 filmes: {e}")
            return []

    def get_distribuicao_protagonistas(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    CASE WHEN protagonista = 1 THEN 'Protagonistas' ELSE 'Não Protagonistas' END AS categoria,
                    COUNT(*) AS quantidade_atores
                FROM Elenco
                GROUP BY protagonista;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar distribuição de protagonistas: {e}")
            return []

    def get_exibicoes_filtradas(self, canal, data_inicio, data_fim):
        try:
            cursor = self.connection.cursor(dictionary=True)
            # --- QUERY CORRIGIDA ---
            # Usa as colunas corretas 'data_exibicao' e 'hora_exibicao'
            query = """
                SELECT 
                    F.nome AS filme, 
                    C.nome AS canal, 
                    E.data_exibicao, 
                    TIME_FORMAT(E.hora_exibicao, '%H:%i') AS hora_exibicao
                FROM Exibicao E
                JOIN Filme F ON E.num_filme = F.num_filme
                JOIN Canal C ON E.num_canal = C.num_canal
                WHERE C.nome = %s
                AND E.data_exibicao BETWEEN %s AND %s
                ORDER BY E.data_exibicao, E.hora_exibicao;
            """
            cursor.execute(query, (canal, data_inicio, data_fim))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar exibições filtradas: {e}")
            return []

    def get_atores_por_filme(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT F.nome AS filme, COUNT(*) AS qtd_atores
                FROM Elenco E
                JOIN Filme F ON E.num_filme = F.num_filme
                GROUP BY F.nome
                ORDER BY qtd_atores DESC;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar atores por filme: {e}")
            return []

    def get_filmes_distintos_por_canal(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT C.nome AS canal, COUNT(DISTINCT E.num_filme) AS filmes_exibidos
                FROM Exibicao E
                JOIN Canal C ON E.num_canal = C.num_canal
                GROUP BY C.nome
                ORDER BY filmes_exibidos DESC;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar filmes distintos por canal: {e}")
            return []
