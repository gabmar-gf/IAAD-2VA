import streamlit as st
import pandas as pd
from datetime import time
from conexao_mysql import FilmesCRUD
from repositories.ExibicoesRepository import ExibicoesRepository

def tela_exibicoes_crud():
    st.subheader("Gerenciamento de Exibições")
    crud = FilmesCRUD()


    filmes = crud.read_filmes()
    canais = crud.read_canais()

    filmes_dict = {f"{f[0]} - {f[1]}": f[0] for f in filmes}  
    canais_dict = {f"{c[0]} - {c[1]}": c[0] for c in canais}  

    st.markdown("### Cadastrar nova exibição")
    with st.form("form_exibicao"):
        filme_escolhido = st.selectbox("Filme", list(filmes_dict.keys()))
        canal_escolhido = st.selectbox("Canal", list(canais_dict.keys()))
        data_exibicao = st.date_input("Data da exibição")
        hora_exibicao = st.time_input("Hora da exibição", value=time(20, 0))
        cadastrar = st.form_submit_button("Agendar")

        if cadastrar:
            try:
                crud.create_exibicao(
                    num_filme=filmes_dict[filme_escolhido],
                    num_canal=canais_dict[canal_escolhido],
                    data_exibicao=data_exibicao,
                    hora_exibicao=hora_exibicao
                )
                st.success("Exibição cadastrada com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao cadastrar exibição: {e}")

    st.markdown("### Exibições cadastradas")

    exibicoes = crud.read_exibicoes()
    if not exibicoes:
        st.info("Nenhuma exibição encontrada.")
        return

    df = pd.DataFrame(exibicoes, columns=["Filme", "Canal", "Data", "Hora"])
    st.dataframe(df, use_container_width=True)

    st.markdown("#### Ações")

    import datetime
    for ex in exibicoes:
        num_filme, num_canal, data, hora = ex[0], ex[1], ex[2], ex[3]
        st.write(f"🎬 Filme {num_filme}, Canal {num_canal}, em {data} às {hora}")

        col1, col2 = st.columns([3, 1])

        with col1:
            with st.expander("Editar"):
                with st.form(f"editar_{num_filme}_{num_canal}_{data}_{hora}"):
                    novo_data = st.date_input("Nova data", value=data)
                    
                    if isinstance(hora, str):
                        try:
                            hora_obj = datetime.datetime.strptime(hora, "%H:%M:%S").time()
                        except Exception:
                            hora_obj = datetime.time(20, 0)
                    elif isinstance(hora, datetime.time):
                        hora_obj = hora
                    else:
                        hora_obj = datetime.time(20, 0)
                    nova_hora = st.time_input("Nova hora", value=hora_obj)
                    editar = st.form_submit_button("Salvar alterações")

                    if editar:
                        try:
                            crud.update_exibicao(
                                num_filme, num_canal,
                                data_original=data,
                                hora_original=hora,
                                nova_data=novo_data,
                                nova_hora=nova_hora
                            )
                            st.success("Exibição atualizada!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao atualizar: {e}")

        with col2:
            if st.button("Excluir", key=f"delete_{num_filme}_{num_canal}_{data}_{hora}"):
                try:
                    crud.delete_exibicao(num_filme, num_canal, data, hora)
                    st.success("Exibição removida!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {e}")
