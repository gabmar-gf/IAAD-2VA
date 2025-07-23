import streamlit as st
import pandas as pd
from pages.Filmes import tela_filme_crud
from pages.Canal import tela_canal_crud
from pages.dashboard_analitico import dashboard_analitico
from pages.Exibicoes import tela_exibicao_crud
from pages.Elenco import tela_elenco_crud

from repositories.CanalRepository import CanalRepository
from repositories.FilmeRepository import FilmeRepository
from repositories.ElencoRepository import ElencoRepository
from repositories.ExibicoesRepository import ExibicoesRepository

def main():
    st.set_page_config(page_title="Programação de Filmes", layout="wide")
    st.markdown("<h1 style='text-align: center; color: #2E8B57;'>Programação de Filmes</h1>", unsafe_allow_html=True)

    menu = ["Início", "Visualizar Tabelas", "Dashboard Analítico", "Canais", "Filmes", "Exibições", "Elenco"]
    escolha = st.sidebar.radio("Navegação", menu)

    if escolha == "Início":
        st.subheader("Bem-vindo ao sistema de programação de filmes!")
        st.write("Utilize o menu lateral para navegar entre as funcionalidades.")

    elif escolha == "Visualizar Tabelas":
        st.subheader("Visualizar Dados das Tabelas")
        st.markdown("Selecione uma tabela para visualizar os dados:")

        repositorios = {
            "Canal": CanalRepository(),
            "Filme": FilmeRepository(),
            "Elenco": ElencoRepository(),
            "Exibicao": ExibicoesRepository()
        }

        tabela_escolhida = st.selectbox("Tabelas disponíveis", list(repositorios.keys()))

        if tabela_escolhida:
            try:
                repository = repositorios[tabela_escolhida]
                dados = repository.find_all()
                
                if dados:
                    df = pd.DataFrame(dados)
                    st.success(f"Mostrando dados da tabela: `{tabela_escolhida}`")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info(f"Nenhum dado encontrado na tabela `{tabela_escolhida}`.")
            except Exception as e:
                st.error(f"Erro ao buscar dados da tabela `{tabela_escolhida}`: {e}")

    elif escolha == "Filmes":
        tela_filme_crud()
        
    elif escolha == "Dashboard Analítico":
        dashboard_analitico()
        
    elif escolha == "Canais":
        tela_canal_crud()

    elif escolha == "Exibições":
        tela_exibicao_crud()
        
    elif escolha == "Elenco":
        tela_elenco_crud()

if __name__ == '__main__':
    main()
