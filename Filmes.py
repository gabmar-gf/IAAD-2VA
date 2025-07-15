import streamlit as st
from conexao_mysql import conectar_mysql

def tela_cadastro_filmes():
    st.subheader("Cadastro de Filmes")

    id = st.text_input("ID")
    nome = st.text_input("Nome")
    ano = st.text_input("Ano")
    duracao = st.text_input("Duração (minutos)")

    if st.button("Adicionar Filme"):
        try:
            conexao = conectar_mysql()
            cursor = conexao.cursor()
            sql = '''
            INSERT INTO Filme(num_filme, nome, ano, duracao)
            VALUES(%s, %s, %s, %s)
            '''
            cursor.execute(sql, (id, nome, ano, duracao))
            conexao.commit()
            st.success("🎉 Filme adicionado com sucesso!")
            conexao.close()
        except Exception as e:
            st.error(f"Erro ao adicionar filme: {e}")

    if st.button("Ver Filmes Cadastrados"):
        try:
            conexao = conectar_mysql()
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM Filme")
            filmes = cursor.fetchall()
            if filmes:
                st.markdown("### 🎬 Filmes Cadastrados:")
                for filme in filmes:
                    st.write(f"- {filme[0]}")
            else:
                st.info("Nenhum filme encontrado.")
            conexao.close()
        except Exception as e:
            st.error(f"Erro ao buscar filmes: {e}")
