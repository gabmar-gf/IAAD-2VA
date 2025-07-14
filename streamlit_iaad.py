import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error

# Função para conectar ao banco
def conectar_mysql():
    try:
        conexao = mysql.connector.connect(
            host='187.87.135.21',       # ou o IP/host do servidor
            user='root',
            password='Rural@2025',
            database='Programacoes_Filmes'
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        st.error(f"Erro ao conectar ao MySQL: {e}")
        return None

def buscar_dados(conexao, tabela):
    try:
        consulta = f"SELECT * FROM {tabela}"
        df = pd.read_sql(consulta, con=conexao)
        return df
    except Exception as e:
        st.warning(f"Erro ao buscar dados: {e}")
        return None

# Interface principal
def main():
    st.set_page_config(page_title="Programação de Filmes", layout="wide")
    st.markdown("<h1 style='text-align: center; color: #2E8B57;'>Programação de Filmes</h1>", unsafe_allow_html=True)

    menu = ["Início", "Visualizar Banco de Dados"]
    escolha = st.sidebar.radio("Navegação", menu)

    conexao = conectar_mysql()
    if not conexao:
        st.stop()

    cursor = conexao.cursor()

    if escolha == "Início":
        st.subheader("Bem-vindo ao sistema de programação de filmes!")
        st.write("Utilize o menu lateral para visualizar os dados do banco.")

    elif escolha == "Visualizar Banco de Dados":
        st.subheader("Dados do Banco de Dados")
        st.markdown("Selecione uma tabela para visualizar os dados:")

        try:
            cursor.execute("SHOW TABLES")
            tabelas = [item[0] for item in cursor.fetchall()]

            if tabelas:
                tabela_escolhida = st.selectbox("Tabelas disponíveis", tabelas)
                df = buscar_dados(conexao, tabela_escolhida)
                if df is not None:
                    st.success(f"Mostrando dados da tabela: `{tabela_escolhida}`")
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("Nenhuma tabela encontrada no banco de dados.")

        except Error as e:
            st.error(f"Erro ao recuperar tabelas: {e}")

    cursor.close()
    conexao.close()

if __name__ == '__main__':
    main()