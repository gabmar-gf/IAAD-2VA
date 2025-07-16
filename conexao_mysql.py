import mysql.connector
from mysql.connector import Error
import threading

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

class FilmesCRUD:
    def __init__(self):
        try:
            self.connection = Db.get_connection()
            # if self.connection.is_connected():
            #     print("Conexão ao MySQL estabelecida com sucesso!")
            # Linhas comentadas para evitar prints desnecessários
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
    


    # Operações CRUD para a tabela Canal
    def create_canal(self, num_canal, nome):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Canal (num_canal, nome) VALUES (%s, %s)"
            cursor.execute(query, (num_canal, nome))
            self.connection.commit()
            print("Canal adicionado com sucesso!")
        except Error as e:
            print(f"Erro ao adicionar canal: {e}")
    
    def read_canais(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Canal")
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao ler canais: {e}")
            return []
    
    def update_canal(self, num_canal, novo_nome):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Canal SET nome = %s WHERE num_canal = %s"
            cursor.execute(query, (novo_nome, num_canal))
            self.connection.commit()
            print("Canal atualizado com sucesso!")
        except Error as e:
            print(f"Erro ao atualizar canal: {e}")
    
    def delete_canal(self, num_canal):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Canal WHERE num_canal = %s"
            cursor.execute(query, (num_canal,))
            self.connection.commit()
            print("Canal removido com sucesso!")
        except Error as e:
            print(f"Erro ao remover canal: {e}")

    # Operações CRUD para a tabela Filme
    def create_filme(self, num_filme, nome, ano=None, duracao=None):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Filme (num_filme, nome, ano, duracao) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (num_filme, nome, ano, duracao))
            self.connection.commit()
            print("Filme adicionado com sucesso!")
        except Error as e:
            print(f"Erro ao adicionar filme: {e}")
    
    def read_filmes(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Filme")
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao ler filmes: {e}")
            return []
    
    def update_filme(self, num_filme, novo_nome=None, novo_ano=None, nova_duracao=None):
        try:
            cursor = self.connection.cursor()
            
            # Primeiro, obtemos os valores atuais
            cursor.execute("SELECT nome, ano, duracao FROM Filme WHERE num_filme = %s", (num_filme,))
            atual = cursor.fetchone()
            
            if not atual:
                print("Filme não encontrado!")
                return
            
            # Usamos os valores atuais se novos não forem fornecidos
            nome = novo_nome if novo_nome is not None else atual[0]
            ano = novo_ano if novo_ano is not None else atual[1]
            duracao = nova_duracao if nova_duracao is not None else atual[2]
            
            query = "UPDATE Filme SET nome = %s, ano = %s, duracao = %s WHERE num_filme = %s"
            cursor.execute(query, (nome, ano, duracao, num_filme))
            self.connection.commit()
            print("Filme atualizado com sucesso!")
        except Error as e:
            print(f"Erro ao atualizar filme: {e}")
    
    def delete_filme(self, num_filme):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Filme WHERE num_filme = %s"
            cursor.execute(query, (num_filme,))
            self.connection.commit()
            print("Filme removido com sucesso!")
        except Error as e:
            print(f"Erro ao remover filme: {e}")

    # Operações CRUD para a tabela Elenco
    def create_elenco(self, num_filme, nome_ator, protagonista):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Elenco (num_filme, nome_ator, protagonista) VALUES (%s, %s, %s)"
            cursor.execute(query, (num_filme, nome_ator, protagonista))
            self.connection.commit()
            print("Ator adicionado ao elenco com sucesso!")
        except Error as e:
            print(f"Erro ao adicionar ator ao elenco: {e}")
    
    def read_elenco(self, num_filme=None):
        try:
            cursor = self.connection.cursor()
            if num_filme:
                query = "SELECT * FROM Elenco WHERE num_filme = %s"
                cursor.execute(query, (num_filme,))
            else:
                cursor.execute("SELECT * FROM Elenco")
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao ler elenco: {e}")
            return []
    
    def update_elenco(self, num_filme, nome_ator, novo_protagonista):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Elenco SET protagonista = %s WHERE num_filme = %s AND nome_ator = %s"
            cursor.execute(query, (novo_protagonista, num_filme, nome_ator))
            self.connection.commit()
            print("Elenco atualizado com sucesso!")
        except Error as e:
            print(f"Erro ao atualizar elenco: {e}")
    
    def delete_elenco(self, num_filme, nome_ator):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Elenco WHERE num_filme = %s AND nome_ator = %s"
            cursor.execute(query, (num_filme, nome_ator))
            self.connection.commit()
            print("Ator removido do elenco com sucesso!")
        except Error as e:
            print(f"Erro ao remover ator do elenco: {e}")

    # Operações CRUD para a tabela Exibicao
    def create_exibicao(self, num_filme, num_canal, data_exibicao, hora_exibicao):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (num_filme, num_canal, data_exibicao, hora_exibicao))
            self.connection.commit()
            print("Exibição adicionada com sucesso!")
        except Error as e:
            print(f"Erro ao adicionar exibição: {e}")
    
    def read_exibicoes(self, num_filme=None, num_canal=None):
        try:
            cursor = self.connection.cursor()
            
            if num_filme and num_canal:
                query = "SELECT * FROM Exibicao WHERE num_filme = %s AND num_canal = %s"
                cursor.execute(query, (num_filme, num_canal))
            elif num_filme:
                query = "SELECT * FROM Exibicao WHERE num_filme = %s"
                cursor.execute(query, (num_filme,))
            elif num_canal:
                query = "SELECT * FROM Exibicao WHERE num_canal = %s"
                cursor.execute(query, (num_canal,))
            else:
                cursor.execute("SELECT * FROM Exibicao")
            
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao ler exibições: {e}")
            return []
    
    def update_exibicao(self, num_filme, num_canal, data_original, hora_original, nova_data=None, nova_hora=None):
        try:
            cursor = self.connection.cursor()
            
            # Primeiro, obtemos os valores atuais
            query = """SELECT data_exibicao, hora_exibicao 
                       FROM Exibicao 
                       WHERE num_filme = %s AND num_canal = %s 
                       AND data_exibicao = %s AND hora_exibicao = %s"""
            cursor.execute(query, (num_filme, num_canal, data_original, hora_original))
            atual = cursor.fetchone()
            
            if not atual:
                print("Exibição não encontrada!")
                return
            
            # Usamos os valores atuais se novos não forem fornecidos
            data = nova_data if nova_data is not None else atual[0]
            hora = nova_hora if nova_hora is not None else atual[1]
            
            # Para atualizar uma chave primária, precisamos deletar e inserir novamente
            # Ou usar uma transação mais complexa
            # Aqui usamos a abordagem de DELETE + INSERT
            
            # Iniciar transação
            self.connection.start_transaction()
            
            # Remover a exibição original
            delete_query = """DELETE FROM Exibicao 
                             WHERE num_filme = %s AND num_canal = %s 
                             AND data_exibicao = %s AND hora_exibicao = %s"""
            cursor.execute(delete_query, (num_filme, num_canal, data_original, hora_original))
            
            # Inserir a exibição atualizada
            insert_query = """INSERT INTO Exibicao (num_filme, num_canal, data_exibicao, hora_exibicao) 
                               VALUES (%s, %s, %s, %s)"""
            cursor.execute(insert_query, (num_filme, num_canal, data, hora))
            
            # Confirmar transação
            self.connection.commit()
            print("Exibição atualizada com sucesso!")
            
        except Error as e:
            self.connection.rollback()
            print(f"Erro ao atualizar exibição: {e}")
    
    def delete_exibicao(self, num_filme, num_canal, data_exibicao, hora_exibicao):
        try:
            cursor = self.connection.cursor()
            query = """DELETE FROM Exibicao 
                        WHERE num_filme = %s AND num_canal = %s 
                        AND data_exibicao = %s AND hora_exibicao = %s"""
            cursor.execute(query, (num_filme, num_canal, data_exibicao, hora_exibicao))
            self.connection.commit()
            print("Exibição removida com sucesso!")
        except Error as e:
            print(f"Erro ao remover exibição: {e}")