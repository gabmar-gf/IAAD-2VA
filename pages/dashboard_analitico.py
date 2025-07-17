import streamlit as st
import pandas as pd
from conexao_mysql import Db
import altair as alt

def dashboard_analitico():
    st.title("📊 Dashboard Analítico de Programações de Filmes")

    conexao = Db.get_connection()
    if not conexao:
        st.warning("Erro ao conectar ao banco.")
        return

    st.markdown("## 🎬 Estatísticas Gerais")
    col1, col2, col3 = st.columns(3)

    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Filme")
            total_filmes = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT nome_ator) FROM Elenco")
            total_atores = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM Exibicao")
            total_exibicoes = cursor.fetchone()[0]
    except Exception as e:
        st.error(f"Erro ao buscar estatísticas gerais: {e}")
        total_filmes = total_atores = total_exibicoes = 0  # valores padrão


    col1.metric("Filmes", total_filmes)
    col2.metric("Atores únicos", total_atores)
    col3.metric("Exibições agendadas", total_exibicoes)

    # Duração mínima e máxima dos filmes
    st.markdown("### 🎞️ Filmes com Duração Extrema")
    query_duracoes = """
        SELECT 
            (SELECT nome FROM Filme WHERE duracao = (SELECT MIN(duracao) FROM Filme) LIMIT 1) AS filme_mais_curto,
            (SELECT MIN(duracao) FROM Filme) AS duracao_minima,
            (SELECT nome FROM Filme WHERE duracao = (SELECT MAX(duracao) FROM Filme) LIMIT 1) AS filme_mais_longo,
            (SELECT MAX(duracao) FROM Filme) AS duracao_maxima;
    """
    try:
        df_duracoes = pd.read_sql(query_duracoes, conexao)
    except Exception as e:
        st.error(f"Erro ao buscar filmes com duração extrema: {e}")
        df_duracoes = pd.DataFrame()

    if not df_duracoes.empty:
        col_min, col_max = st.columns(2)
        col_min.metric("🎬 Mais Curto", df_duracoes['filme_mais_curto'][0], f"{df_duracoes['duracao_minima'][0]} min")
        col_max.metric("🎬 Mais Longo", df_duracoes['filme_mais_longo'][0], f"{df_duracoes['duracao_maxima'][0]} min") 

    # Gráfico 1: Exibições por Canal
    st.markdown("### 📺 Número de Exibições por Canal")
    query1 = """
        SELECT C.nome AS canal, COUNT(*) AS total_exibicoes
        FROM Exibicao E
        LEFT JOIN Canal C ON E.num_canal = C.num_canal
        GROUP BY C.nome
        ORDER BY total_exibicoes DESC;
    """
    try:
        df1 = pd.read_sql(query1, conexao)
        df1["total_exibicoes"] = df1["total_exibicoes"].astype(int)
        chart = alt.Chart(df1).mark_bar().encode(
            x=alt.X("canal", sort='-y', title="Canal", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("total_exibicoes", title="Total de Exibições", axis=alt.Axis(tickMinStep=1, format="d")),
            tooltip=["canal", "total_exibicoes"]
        ).properties(width=700, height=400)
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de exibições por canal: {e}")

    # Gráfico 2: Duração média de filmes por ano
    st.markdown("### ⏱️ Duração Média dos Filmes por Ano")
    query2 = """
        SELECT ano, AVG(duracao) AS media_duracao
        FROM Filme
        WHERE duracao IS NOT NULL
        GROUP BY ano
        ORDER BY ano;
    """
    try:
        df2 = pd.read_sql(query2, conexao)
        chart2 = alt.Chart(df2).mark_line(point=True).encode(
            x=alt.X("ano", title="Ano", axis=alt.Axis(format="d", tickMinStep=1)),
            y=alt.Y("media_duracao", title="Duração Média (min)"),
            tooltip=["ano", "media_duracao"]
        ).properties(width=700, height=400)
        st.altair_chart(chart2, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de duração média: {e}")

    # Gráfico 3: Filmes com mais exibições
    st.markdown("### 🏆 Filmes com Mais Exibições")
    query3 = """
        SELECT F.nome, COUNT(*) AS total_exibicoes
        FROM Exibicao E
        LEFT JOIN Filme F ON E.num_filme = F.num_filme
        GROUP BY F.nome
        ORDER BY total_exibicoes DESC
        LIMIT 5;
    """
    try:
        df3 = pd.read_sql(query3, conexao)
        df3["total_exibicoes"] = df3["total_exibicoes"].astype(int)
        chart3 = alt.Chart(df3).mark_bar().encode(
            x=alt.X("nome", sort='-y', title="Filme", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("total_exibicoes", title="Total de Exibições", axis=alt.Axis(tickMinStep=1, format="d")),
            tooltip=["nome", "total_exibicoes"]
        ).properties(width=700, height=400)
        st.altair_chart(chart3, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de filmes com mais exibições: {e}")

    # Consulta 4: Atores Protagonistas X Não Protagonistas
    st.markdown("### 👥 Distribuição de Atores Protagonistas vs Não Protagonistas")
    query_atores_protagonistas = """
        SELECT 
            CASE WHEN protagonista = 1 THEN 'Protagonistas' ELSE 'Não Protagonistas' END AS categoria,
            COUNT(*) AS quantidade_atores
        FROM Elenco
        GROUP BY protagonista;
    """
    try:
        df_atores_protagonistas = pd.read_sql(query_atores_protagonistas, conexao)
        chart_atores_protagonistas = alt.Chart(df_atores_protagonistas).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="quantidade_atores", type="quantitative"),
            color=alt.Color(field="categoria", type="nominal", legend=alt.Legend(title="Categoria")),
            tooltip=[alt.Tooltip("categoria", title="Categoria"), alt.Tooltip("quantidade_atores", title="Quantidade de Atores")]
        ).properties(width=700, height=400)
        st.altair_chart(chart_atores_protagonistas, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de atores protagonistas: {e}")

    # Consulta 5: Filtro por período e canal
    st.markdown("### 📅 Filtrando Exibições por Período e Canal")
    try:
        canais_df = pd.read_sql("SELECT DISTINCT nome FROM Canal", conexao)
        canais = canais_df['nome'].tolist()
    except Exception as e:
        st.error(f"Erro ao buscar canais: {e}")
        canais = []
    canal = st.selectbox("Selecione o canal", canais)
    data_inicio = st.date_input(
    "Data inicial", pd.to_datetime("2025-06-01"), format="DD/MM/YYYY"
    )
    data_fim = st.date_input(
        "Data final", pd.to_datetime("2025-08-31"), format="DD/MM/YYYY"
    )

    if data_inicio > data_fim:
        st.warning("Data inicial não pode ser maior que a final.")
    else:
        query5 = f"""
            SELECT F.nome AS filme, C.nome AS canal, E.data_exibicao, E.hora_exibicao
            FROM Exibicao E
            LEFT JOIN Filme F ON E.num_filme = F.num_filme
            LEFT JOIN Canal C ON E.num_canal = C.num_canal
            WHERE C.nome = %s
            AND E.data_exibicao BETWEEN %s AND %s
            ORDER BY E.data_exibicao, E.hora_exibicao;
        """
        try:
            df5 = pd.read_sql(query5, conexao, params=(canal, data_inicio, data_fim))
            df5["data_exibicao"] = pd.to_datetime(df5["data_exibicao"]).dt.strftime("%d/%m/%Y")
            df5["hora_exibicao"] = df5["hora_exibicao"].apply(lambda x: (pd.Timestamp('1900-01-01') + x).strftime('%H:%M'))
            df5_display = df5.rename(columns={
                "filme": "Filme",
                "canal": "Canal",
                "data_exibicao": "Data de Exibição",
                "hora_exibicao": "Horário de Exibição"
            })
            if df5_display.empty:
                st.info("Nenhuma exibição encontrada para o período e canal selecionados.")
            else:
                st.dataframe(df5_display)
        except Exception as e:
            st.error(f"Erro ao buscar exibições filtradas: {e}")

    # Consulta 6: Quantidade de atores por filme
    st.markdown("### 👥 Quantidade de Atores por Filme")
    query6 = """
        SELECT F.nome AS filme, COUNT(*) AS qtd_atores
        FROM Elenco E
        LEFT JOIN Filme F ON E.num_filme = F.num_filme
        GROUP BY F.nome
        ORDER BY qtd_atores DESC;
    """
    try: 
        df6 = pd.read_sql(query6, conexao)
        df6.rename(columns={"filme": "Filme", "qtd_atores": "Quantidade de Atores"}, inplace=True)
        chart6 = alt.Chart(df6).mark_bar().encode(
            x=alt.X("Filme:N", sort='-y', title="Filme", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Quantidade de Atores:Q", title="Quantidade de Atores", axis=alt.Axis(tickMinStep=1, format="d")),
            tooltip=["Filme", "Quantidade de Atores"]
        ).properties(width=700, height=400)
        st.altair_chart(chart6, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de quantidade de atores por filme: {e}")

    # Consulta 7: Quantidade de filmes distintos por canal
    st.markdown("### 🎥 Quantidade de Filmes por Canal")
    query7 = """
        SELECT C.nome AS canal, COUNT(DISTINCT E.num_filme) AS filmes_exibidos
        FROM Exibicao E
        LEFT JOIN Canal C ON E.num_canal = C.num_canal
        GROUP BY C.nome
        ORDER BY filmes_exibidos DESC;
    """
    try:
        df7 = pd.read_sql(query7, conexao)
        df7.rename(columns={"canal": "Canal", "filmes_exibidos": "Quantidade de Filmes"}, inplace=True)
        chart7 = alt.Chart(df7).mark_bar().encode(
            x=alt.X("Canal:N", sort='-y', title="Canal", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Quantidade de Filmes:Q", title="Filmes Distintos Exibidos", axis=alt.Axis(tickMinStep=1, format="d")),
            tooltip=["Canal", "Quantidade de Filmes"]
        ).properties(width=700, height=400)
        st.altair_chart(chart7, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de quantidade de filmes por canal: {e}")

    conexao.close()