import streamlit as st
import pandas as pd
from repositories.FilmeRepository import FilmeRepository
from repositories.ExibicoesRepository import ExibicoesRepository
from repositories.ElencoRepository import ElencoRepository
import datetime

def tela_filme_crud():
    st.header("Gerenciamento de Filmes")

    filme_repository = FilmeRepository()
    exibicao_repository = ExibicoesRepository()
    elenco_repository = ElencoRepository()

    st.subheader("Adicionar Novo Filme")
    with st.form(key="add_filme_form", clear_on_submit=True):
        nome = st.text_input("Nome do Filme")
        ano = st.number_input("Ano de Lançamento", min_value=1888, max_value=datetime.date.today().year + 5, value=datetime.date.today().year, step=1, format="%d")
        duracao = st.number_input("Duração (minutos)", min_value=1, step=1, value=120)
        submit_button = st.form_submit_button(label="Adicionar Filme")

        if submit_button:
            if nome:
                try:
                    filme_repository.create(nome, int(ano), int(duracao))
                    st.success(f"Filme '{nome}' adicionado com sucesso!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Falha ao adicionar filme: {e}")
            else:
                st.warning("O nome do filme não pode ser vazio.")

    st.markdown("---")

    st.subheader("Filmes Cadastrados")
    try:
        filmes = filme_repository.find_all()
        if not filmes:
            st.info("Nenhum filme encontrado.")
        else:
            for filme in filmes:
                with st.container():
                    st.markdown('<hr style="margin-top: 0; margin-bottom: 1rem;">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"##### {filme['nome']} ({filme['ano'] or 'N/A'})")
                        st.caption(f"Duração: {filme['duracao'] or 'N/A'} min | ID: {filme['num_filme']}")
                    
                    with col2:
                        if st.button("Deletar", key=f"delete_{filme['num_filme']}", type="primary", use_container_width=True):
                            try:
                                filme_repository.delete(filme['num_filme'])
                                st.success(f"Filme '{filme['nome']}' deletado.")
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"Erro ao deletar: {e}")
                    
                    with st.expander("Editar Filme"):
                        with st.form(key=f"edit_form_{filme['num_filme']}"):
                            novo_nome = st.text_input("Novo Nome", value=filme['nome'], key=f"edit_nome_{filme['num_filme']}")
                            
                            ano_default = int(filme['ano'] or datetime.date.today().year)
                            duracao_default = int(filme['duracao'] or 0)

                            novo_ano = st.number_input("Novo Ano", value=ano_default, min_value=1888, max_value=2100, step=1, format="%d", key=f"edit_ano_{filme['num_filme']}")
                            nova_duracao = st.number_input("Nova Duração (min)", value=duracao_default, min_value=1, step=1, key=f"edit_duracao_{filme['num_filme']}")
                            
                            if st.form_submit_button("Salvar Alterações"):
                                try:
                                    filme_repository.update(filme['num_filme'], novo_nome, int(novo_ano), int(nova_duracao))
                                    st.success("Filme atualizado!")
                                    st.experimental_rerun()
                                except Exception as e:
                                    st.error(f"Erro ao atualizar: {e}")
                    
                    with st.expander("Ver Detalhes (Exibições e Elenco)"):
                        st.markdown("###### Próximas Exibições")
                        exibicoes_do_filme = exibicao_repository.find_by_filme_id(filme['num_filme'])
                        
                        if not exibicoes_do_filme:
                            st.info("Nenhuma exibição agendada para este filme.")
                        else:
                            df_exibicoes = pd.DataFrame(exibicoes_do_filme)
                            st.dataframe(df_exibicoes, use_container_width=True)

                        st.markdown("###### Elenco")
                        elenco_do_filme = elenco_repository.find_by_filme_id(filme['num_filme'])

                        if not elenco_do_filme:
                            st.info("Nenhum ator cadastrado para este filme.")
                        else:
                            for ator in elenco_do_filme:
                                col_ator, col_delete_ator = st.columns([4, 1])
                                with col_ator:
                                    protagonista_str = "⭐ Protagonista" if ator['protagonista'] else "Coadjuvante"
                                    st.text(f"{ator['nome_ator']} ({protagonista_str})")
                                with col_delete_ator:
                                    if st.button("Remover", key=f"delete_ator_{filme['num_filme']}_{ator['nome_ator']}", type="secondary"):
                                        elenco_repository.delete(filme['num_filme'], ator['nome_ator'])
                                        st.experimental_rerun()
                        
                        with st.form(key=f"add_ator_form_{filme['num_filme']}", clear_on_submit=True):
                            st.markdown("Adicionar Ator ao Elenco")
                            nome_ator = st.text_input("Nome do Ator", key=f"ator_nome_{filme['num_filme']}")
                            protagonista = st.checkbox("É protagonista?", key=f"ator_protagonista_{filme['num_filme']}")
                            if st.form_submit_button("Adicionar"):
                                if nome_ator:
                                    elenco_repository.create(filme['num_filme'], nome_ator, protagonista)
                                    st.experimental_rerun()
                                else:
                                    st.warning("O nome do ator não pode ser vazio.")

    except Exception as e:
        st.error(f"Não foi possível carregar os filmes: {e}")
