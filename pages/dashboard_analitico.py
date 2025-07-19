import streamlit as st
import pandas as pd
import altair as alt
from repositories.DashboardRepository import DashboardRepository
from repositories.CanalRepository import CanalRepository

def dashboard_analitico():
    st.title("📊 Dashboard Analítico de Programações de Filmes")

    try:
        dashboard_repo = DashboardRepository()
        canal_repo = CanalRepository()
    except Exception as e:
        st.error(f"Erro ao inicializar os repositórios: {e}")
        return

    st.markdown("## 🎬 Estatísticas Gerais")
    col1, col2, col3 = st.columns(3)

    try:
        stats = dashboard_repo.get_estatisticas_gerais()
        col1.metric("Filmes", stats.get("total_filmes", 0))
        col2.metric("Atores únicos", stats.get("total_atores", 0))
        col3.metric("Exibições agendadas", stats.get("total_exibicoes", 0))
    except Exception as e:
        st.error(f"Erro ao buscar estatísticas gerais: {e}")

    st.markdown("### 🎞️ Filmes com Duração Extrema")
    try:
        duracoes = dashboard_repo.get_filmes_duracao_extrema()
        if duracoes:
            col_min, col_max = st.columns(2)
            col_min.metric("🎬 Mais Curto", duracoes['filme_mais_curto'], f"{duracoes['duracao_minima']} min")
            col_max.metric("🎬 Mais Longo", duracoes['filme_mais_longo'], f"{duracoes['duracao_maxima']} min")
    except Exception as e:
        st.error(f"Erro ao buscar filmes com duração extrema: {e}")

    st.markdown("### 📺 Número de Exibições por Canal")
    try:
        data = dashboard_repo.get_exibicoes_por_canal()
        if data:
            df = pd.DataFrame(data)
            df["total_exibicoes"] = df["total_exibicoes"].astype(int)
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("canal", sort='-y', title="Canal", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("total_exibicoes", title="Total de Exibições", axis=alt.Axis(tickMinStep=1, format="d")),
                tooltip=["canal", "total_exibicoes"]
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de exibições por canal: {e}")


    st.markdown("### 🏆 Filmes com Mais Exibições")
    try:
        data = dashboard_repo.get_top_5_filmes_mais_exibidos()
        if data:
            df = pd.DataFrame(data)
            df["total_exibicoes"] = df["total_exibicoes"].astype(int)
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("nome", sort='-y', title="Filme", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("total_exibicoes", title="Total de Exibições", axis=alt.Axis(tickMinStep=1, format="d")),
                tooltip=["nome", "total_exibicoes"]
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de filmes com mais exibições: {e}")

    st.markdown("### 👥 Distribuição de Atores Protagonistas vs Não Protagonistas")
    try:
        data = dashboard_repo.get_distribuicao_protagonistas()
        if data:
            df = pd.DataFrame(data)
            chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="quantidade_atores", type="quantitative"),
                color=alt.Color(field="categoria", type="nominal", legend=alt.Legend(title="Categoria")),
                tooltip=[alt.Tooltip("categoria", title="Categoria"), alt.Tooltip("quantidade_atores", title="Quantidade de Atores")]
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de atores protagonistas: {e}")

    st.markdown("### 📅 Filtrando Exibições por Período e Canal")
    try:
        canais_data = canal_repo.find_all()
        canais = [c['nome'] for c in canais_data]
        
        canal = st.selectbox("Selecione o canal", canais)
        data_inicio = st.date_input("Data inicial", pd.to_datetime("2025-06-01"))
        data_fim = st.date_input("Data final", pd.to_datetime("2025-08-31"))

        if data_inicio > data_fim:
            st.warning("Data inicial não pode ser maior que a final.")
        else:
            dados_filtrados = dashboard_repo.get_exibicoes_filtradas(canal, data_inicio, data_fim)
            if not dados_filtrados:
                st.info("Nenhuma exibição encontrada para o período e canal selecionados.")
            else:
                df = pd.DataFrame(dados_filtrados)
                df["data_exibicao"] = pd.to_datetime(df["data_exibicao"]).dt.strftime("%d/%m/%Y")
                df_display = df.rename(columns={
                    "filme": "Filme", "canal": "Canal",
                    "data_exibicao": "Data de Exibição", "hora_exibicao": "Horário"
                })
                st.dataframe(df_display)
    except Exception as e:
        st.error(f"Erro ao buscar exibições filtradas: {e}")

    st.markdown("### 👥 Quantidade de Atores por Filme")
    try:
        data = dashboard_repo.get_atores_por_filme()
        if data:
            df = pd.DataFrame(data)
            df.rename(columns={"filme": "Filme", "qtd_atores": "Quantidade de Atores"}, inplace=True)
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("Filme:N", sort='-y', title="Filme", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Quantidade de Atores:Q", title="Quantidade de Atores", axis=alt.Axis(tickMinStep=1, format="d")),
                tooltip=["Filme", "Quantidade de Atores"]
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de quantidade de atores por filme: {e}")

    st.markdown("### 🎥 Quantidade de Filmes por Canal")
    try:
        data = dashboard_repo.get_filmes_distintos_por_canal()
        if data:
            df = pd.DataFrame(data)
            df.rename(columns={"canal": "Canal", "filmes_exibidos": "Quantidade de Filmes"}, inplace=True)
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("Canal:N", sort='-y', title="Canal", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Quantidade de Filmes:Q", title="Filmes Distintos Exibidos", axis=alt.Axis(tickMinStep=1, format="d")),
                tooltip=["Canal", "Quantidade de Filmes"]
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de quantidade de filmes por canal: {e}")
