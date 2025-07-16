import streamlit as st
from conexao_mysql import FilmesCRUD

def tela_cadastro_filmes():
    st.subheader("Cadastro de Filmes")

    id = st.text_input("ID")
    nome = st.text_input("Nome")
    ano = st.text_input("Ano")
    duracao = st.text_input("Duração (minutos)")

    crud = FilmesCRUD()

    if st.button("Adicionar Filme"):
        try:
            crud.create_filme(id, nome, ano, duracao)
            st.success("🎉 Filme adicionado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao adicionar filme: {e}")

    if st.button("Ver Filmes Cadastrados"):
        try:
            filmes = crud.read_filmes()
            if filmes:
                st.markdown("### 🎬 Filmes Cadastrados:")
                for filme in filmes:
                    st.write(f"- {filme[1]}")
            else:
                st.info("Nenhum filme encontrado.")
        except Exception as e:
            st.error(f"Erro ao buscar filmes: {e}")
