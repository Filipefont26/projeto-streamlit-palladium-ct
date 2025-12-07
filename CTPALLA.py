import pandas as pd
import streamlit as st



st.set_page_config(page_title="Dashboard Escolas", layout="wide")

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

st.title("Dashboard palladium ct")

uploaded = st.file_uploader("envie um arquivo csv", type = ["csv"])

st.sidebar.header("filtros")

if uploaded:
    df = load_data(uploaded)

    st.success("arquivo carregado com sucesso")


df["pontos_calculados"] = df ["idas_no_mes"] *3
st.success("Arquivo carregado com sucesso!")

status_filtrado = st.sidebar.multiselect(
    "status_pagamento",
    df ["status_pagamento"].unique(),
    default = df["status_pagamento"].unique()
)


    # Filtro por nome do aluno

nome_filtrado = st.sidebar.text_input("buscar alunos")

df_filtrado= df[df["status_pagamento"].isin(status_filtrado)]

if nome_filtrado:
    df_filtrado = df_filtrado[df_filtrado["nome_aluno"].str.contains(nome_filtrado, case = False)]

st.subheader("indicadores gerais")

col1,col2,col3,col4 = st.columns(4)

col1.metric ("alunos totais",len(df))
col2.metric("pagantes",sum(df["status_pagamento"] == "pagante"))
col3.metric("pendentes",sum(df["status_pagamento"] == "pendente"))
col4.metric("total de pontos somados", int(df["pontos_calculados"].sum()))

st.subheader("Dados filtrados")
st.dataframe(df_filtrado,use_container_width = True)

st.subheader("Tabela de Ranking")

st.subheader("🏆 Ranking de Alunos por Pontos (Top 5)")

ranking = (
    df.sort_values("pontos_calculados", ascending = False)
    .loc[:,["nome_aluno","idas_no_mes","pontos_calculados"]]
    .head(5)
)

st.dataframe(ranking, use_container_width=True)

st.download_button(
    "📥 Baixar CSV Filtrado",
    df.to_csv(index=False),
    file_name="dados_filtrados.csv",
    mime="text/csv"
)
