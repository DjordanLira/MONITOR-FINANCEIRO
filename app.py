# CATEGORIA 1: CONFIGURAÇÕES INICIAIS E IMPORTAÇÕES

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Monitor Financeiro", layout="wide")
st.title("💰 Meu Monitor Financeiro Pessoal")


#
# CATEGORIA 2: PERSISTÊNCIA E GERENCIAMENTO DE DADOS
#

DATA_FILE = "dados_financeiros.csv"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor", "Descrição"])

df = carregar_dados()


# CATEGORIA 3: INTERFACE DE ENTRADA

st.sidebar.header("Nova Transação")

with st.sidebar.form(key="form_transacao", clear_on_submit=True):

    data = st.date_input("Data")

    tipo = st.selectbox(
        "Tipo",
        ["Receita", "Despesa"]
    )

    categoria = st.selectbox(
        "Categoria",
        [
            "Salário",
            "Investimentos",
            "Alimentação",
            "Transporte",
            "Moradia",
            "Lazer",
            "Outros"
        ]
    )

    valor = st.number_input(
        "Valor (R$)",
        min_value=0.0,
        step=5.0,
        format="%.2f"
    )

    descricao = st.text_input("Descrição")

    botao_salvar = st.form_submit_button(
        label="Adicionar"
    )


#
# CATEGORIA 4: SALVAR DADOS
#

if botao_salvar and valor > 0:

    nova_linha = pd.DataFrame([{
        "Data": str(data),
        "Tipo": tipo,
        "Categoria": categoria,
        "Valor": valor,
        "Descrição": descricao
    }])

    df = pd.concat(
        [df, nova_linha],
        ignore_index=True
    )

    df.to_csv(DATA_FILE, index=False)

    st.sidebar.success("Salvo com sucesso!")

    st.rerun()


#
# CATEGORIA 5: VISUALIZAÇÃO
#

if not df.empty:

    df["Valor"] = pd.to_numeric(df["Valor"])

    receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
    despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    saldo = receitas - despesas


    # CORES (ADICIONADO)

    cores = {
        "Alimentação": "#FF6B6B",
        "Transporte": "#4ECDC4",
        "Moradia": "#FFA94D",
        "Lazer": "#845EF7",
        "Investimentos": "#51CF66",
        "Outros": "#868E96",
        "Salário": "#339AF0"
    }


    # MÉTRICAS

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Receitas", f"R$ {receitas:,.2f}")
    col2.metric("Total Despesas", f"R$ {despesas:,.2f}")
    col3.metric("Saldo Atual", f"R$ {saldo:,.2f}")

    st.markdown("---")


    # GRÁFICOS

    col_g1, col_g2 = st.columns(2)


    with col_g1:

        st.subheader("🍕 Gastos por Categoria")

        df_despesas = df[df["Tipo"] == "Despesa"]

        if not df_despesas.empty:

            st.plotly_chart(
                px.pie(
                    df_despesas,
                    values="Valor",
                    names="Categoria",
                    hole=0.4,
                    color="Categoria",
                    color_discrete_map=cores
                ),
                use_container_width=True
            )

        else:

            st.info("Nenhuma despesa cadastrada.")


    with col_g2:

        st.subheader("📊 Histórico")

        st.plotly_chart(
            px.bar(
                df,
                x="Data",
                y="Valor",
                color="Tipo",
                barmode="group",
                color_discrete_map={
                    "Receita": "green",
                    "Despesa": "red"
                }
            ),
            use_container_width=True
        )


    st.markdown("---")


    # HISTÓRICO

    st.subheader("📋 Histórico de Transações")

    st.dataframe(
        df.sort_values(
            by="Data",
            ascending=False
        ),
        use_container_width=True
    )


else:

    st.info(
        "Use a barra lateral para cadastrar sua primeira transação!"
    )
        "Use a barra lateral para cadastrar sua primeira transação!"
    )
