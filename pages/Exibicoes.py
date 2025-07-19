import streamlit as st
import pandas as pd
from repositories.ExibicoesRepository import ExibicoesRepository
from repositories.FilmeRepository import FilmeRepository
from repositories.CanalRepository import CanalRepository
import datetime
import math

def tela_exibicao_crud():
    st.header("Gerenciamento de Exibições")

    exibicao_repo = ExibicoesRepository()
    filme_repo = FilmeRepository()
    canal_repo = CanalRepository()

    try:
        filmes = filme_repo.find_all()
        canais = canal_repo.find_all()

        filme_opcoes = {filme['nome']: filme['num_filme'] for filme in filmes}
        canal_opcoes = {canal['nome']: canal['num_canal'] for canal in canais}
    except Exception as e:
        st.error(f"Não foi possível carregar os dados de Filmes e Canais: {e}")
        return

    st.subheader("Agendar Nova Exibição")
    with st.form(key="add_exibicao_form", clear_on_submit=True):
        filme_selecionado = st.selectbox("Selecione o Filme", options=list(filme_opcoes.keys()))
        canal_selecionado = st.selectbox("Selecione o Canal", options=list(canal_opcoes.keys()))
        data_exibicao = st.date_input("Data da Exibição", value=datetime.date.today())
        hora_exibicao = st.time_input("Hora da Exibição", value=datetime.time(20, 0))
        
        submit_button = st.form_submit_button(label="Agendar Exibição")

        if submit_button:
            if filme_selecionado and canal_selecionado:
                try:
                    filme_id = filme_opcoes[filme_selecionado]
                    canal_id = canal_opcoes[canal_selecionado]
                    
                    exibicao_repo.create(filme_id, canal_id, data_exibicao, hora_exibicao)
                    st.success("Exibição agendada com sucesso!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Falha ao agendar exibição: {e}")
            else:
                st.warning("É necessário selecionar um filme e um canal.")

    st.markdown("---")

    st.subheader("Exibições Agendadas")
    try:
        exibicoes = exibicao_repo.find_all()
        if not exibicoes:
            st.info("Nenhuma exibição encontrada.")
        else:
            df = pd.DataFrame(exibicoes)
            st.dataframe(df[['filme', 'canal', 'data_exibicao', 'hora_exibicao']], use_container_width=True)

            st.markdown("#### Ações")
            for index, exibicao in df.iterrows():
                st.write(f"**Exibição:** {exibicao['filme']} no canal {exibicao['canal']}")
                
                col_edit, col_delete = st.columns([3, 1])

                with col_edit:
                    form_key = f"edit_form_{exibicao['num_filme']}_{exibicao['num_canal']}_{exibicao['data_exibicao']}_{exibicao['hora_exibicao']}"
                    with st.expander("Editar"):
                        with st.form(key=form_key):
                            filme_edit_selecionado = st.selectbox("Filme", options=list(filme_opcoes.keys()), index=list(filme_opcoes.keys()).index(exibicao['filme']), key=f"edit_filme_{form_key}")
                            canal_edit_selecionado = st.selectbox("Canal", options=list(canal_opcoes.keys()), index=list(canal_opcoes.keys()).index(exibicao['canal']), key=f"edit_canal_{form_key}")
                            
                            data_atual = exibicao['data_exibicao']
                            hora_atual_str = exibicao['hora_exibicao']
                            hora_atual_obj = datetime.datetime.strptime(hora_atual_str, '%H:%M:%S').time()

                            data_edit = st.date_input("Data", value=data_atual, key=f"edit_data_{form_key}")
                            hora_edit = st.time_input("Hora", value=hora_atual_obj, key=f"edit_hora_{form_key}")

                            if st.form_submit_button("Salvar Alterações"):
                                try:
                                    novo_filme_id = filme_opcoes[filme_edit_selecionado]
                                    novo_canal_id = canal_opcoes[canal_edit_selecionado]
                                    
                                    exibicao_repo.update(
                                        exibicao['num_filme'], exibicao['num_canal'], exibicao['data_exibicao'], exibicao['hora_exibicao'],
                                        novo_filme_id, novo_canal_id, data_edit, hora_edit
                                    )
                                    st.success("Exibição atualizada!")
                                    st.experimental_rerun()
                                except Exception as e:
                                    st.error(f"Erro ao atualizar: {e}")
                
                with col_delete:
                    delete_key = f"delete_{exibicao['num_filme']}_{exibicao['num_canal']}_{exibicao['data_exibicao']}_{exibicao['hora_exibicao']}"
                    if st.button("Deletar", key=delete_key, type="primary", use_container_width=True):
                        try:
                            exibicao_repo.delete(exibicao['num_filme'], exibicao['num_canal'], exibicao['data_exibicao'], exibicao['hora_exibicao'])
                            st.success("Exibição deletada.")
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Erro ao deletar: {e}")
                
                st.markdown("---")

    except Exception as e:
        st.error(f"Não foi possível carregar as exibições: {e}")
