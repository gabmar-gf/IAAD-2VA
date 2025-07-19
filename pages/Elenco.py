import streamlit as st
import pandas as pd
from repositories.ElencoRepository import ElencoRepository
from repositories.FilmeRepository import FilmeRepository

def tela_elenco_crud():
    st.header("Gerenciamento de Elenco")

    elenco_repo = ElencoRepository()
    filme_repo = FilmeRepository()

    try:
        filmes = filme_repo.find_all()
        if not filmes:
            st.warning("Nenhum filme cadastrado. Por favor, adicione um filme primeiro.")
            return

        filme_opcoes = {filme['nome']: filme['num_filme'] for filme in filmes}
    except Exception as e:
        st.error(f"Não foi possível carregar os filmes: {e}")
        return

    st.subheader("Adicionar Ator a um Filme")
    with st.form(key="add_elenco_form", clear_on_submit=True):
        filme_selecionado = st.selectbox("Selecione o Filme", options=list(filme_opcoes.keys()))
        nome_ator = st.text_input("Nome do Ator")
        protagonista = st.checkbox("É protagonista?")
        
        submit_button = st.form_submit_button(label="Adicionar ao Elenco")

        if submit_button:
            if filme_selecionado and nome_ator:
                try:
                    filme_id = filme_opcoes[filme_selecionado]
                    elenco_repo.create(filme_id, nome_ator, protagonista)
                    st.success(f"Ator '{nome_ator}' adicionado ao filme '{filme_selecionado}'!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Falha ao adicionar ator: {e}")
            else:
                st.warning("É necessário selecionar um filme e preencher o nome do ator.")

    st.markdown("---")

    st.subheader("Visualizar Elenco por Filme")
    
    filme_para_ver = st.selectbox("Selecione um filme para ver o elenco", options=list(filme_opcoes.keys()))

    if filme_para_ver:
        filme_id_selecionado = filme_opcoes[filme_para_ver]
        
        try:
            elenco = elenco_repo.find_by_filme_id(filme_id_selecionado)
            if not elenco:
                st.info(f"Nenhum ator encontrado para o filme '{filme_para_ver}'.")
            else:
                st.markdown(f"#### Elenco de '{filme_para_ver}'")
                for ator in elenco:
                    col_ator, col_delete = st.columns([4, 1])
                    with col_ator:
                        protagonista_str = "⭐ Protagonista" if ator['protagonista'] else "Coadjuvante"
                        st.text(f"{ator['nome_ator']} ({protagonista_str})")
                    with col_delete:
                        delete_key = f"delete_ator_{filme_id_selecionado}_{ator['nome_ator']}"
                        if st.button("Remover", key=delete_key, type="secondary", use_container_width=True):
                            try:
                                elenco_repo.delete(filme_id_selecionado, ator['nome_ator'])
                                st.success(f"Ator '{ator['nome_ator']}' removido do elenco.")
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"Erro ao remover ator: {e}")
        except Exception as e:
            st.error(f"Não foi possível carregar o elenco: {e}")

