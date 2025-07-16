import streamlit as st
from repositories.CanalRepository import CanalRepository
import pandas as pd

def tela_canal_crud():
    st.subheader("Cadastro de canais")
    repository = CanalRepository()
    nome = st.text_input("Nome")
    
    if st.button("Adicionar Canal"):
        try:
            repository.create(nome)
            st.success("Canal adicionado")
        except Exception as e:
            st.error(f"Falha ao adicionar canal: {e}")
    
    st.subheader("Canais Cadastrados")
    canais = repository.find_all()

    if not canais:
        st.info("Nenhum canal encontrado.")
    else:
        df = pd.DataFrame(canais)
        st.dataframe(df, use_container_width=True)

        st.markdown("#### Ações")
        for index, canal in df.iterrows():
                st.write(f"**Canal:** {canal['nome']}")
            
                col_edit, col_delete = st.columns([3, 1])
                
                with col_edit:
                    with st.expander(f"Editar"):
                        with st.form(key=f"edit_form_{canal['num_canal']}"):
                            nome_atualizado = st.text_input("Novo nome", value=canal['nome'], key=f"edit_input_{canal['num_canal']}")
                            if st.form_submit_button("Salvar Alterações"):
                                try:
                                    repository.update(canal['num_canal'], nome_atualizado)
                                    st.success(f"Canal atualizado para '{nome_atualizado}'!")
                                    st.rerun() 
                                except Exception as e:
                                    st.error(f"Erro ao atualizar: {e}")
                
                with col_delete:
                    if st.button("Deletar", key=f"delete_{canal['num_canal']}", type="primary", use_container_width=True):
                        try:
                            repository.delete(canal['num_canal'])
                            st.success(f"Canal '{canal['nome']}' deletado.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao deletar: {e}")
                
