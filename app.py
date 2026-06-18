# CATEGORIA 1: CONFIGURAÇÕES INICIAIS E IMPORTAÇÕES

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Monitor Financeiro", layout="wide")
st.title("💰 Meu Monitor Financeiro Pessoal")


# CATEGORIA 2: PERSISTÊNCIA

DATA_FILE = "dados_financeiros.csv"


def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)

    return pd.DataFrame(
        columns=[
            "Data",
            "Tipo",
            "Categoria",
            "Valor",
            "Descrição"
        ]
    )


df = carregar_dados()


# CATEGORIA 3: ENTRADA

st.sidebar.header("Nova Transação")

with st.sidebar.form(
    key="form_transacao",
    clear_on_submit=True
):

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

    descricao = st.text_input(
        "Descrição"
    )

    botao_salvar = st.form_submit_button(
        "Adicionar"
    )


# CATEGORIA 4: SALVAR

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

    df.to_csv(
        DATA_FILE,
        index=False
    )

    st.rerun()


# CATEGORIA 5: VISUALIZAÇÃO

if not df.empty:

    df["Valor"] = pd.to_numeric(
        df["Valor"]
    )

    receitas = (
        df[df["Tipo"] == "Receita"]["Valor"]
        .sum()
    )

    despesas = (
        df[df["Tipo"] == "Despesa"]["Valor"]
        .sum()
    )

    saldo = receitas - despesas


    cores = {
        "Alimentação": "#FF6B6B",
        "Transporte": "#4ECDC4",
        "Moradia": "#FFA94D",
        "Lazer": "#845EF7",
        "Investimentos": "#51CF66",
        "Outros": "#868E96",
        "Salário": "#339AF0"
    }


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Receitas",
        f"R$ {receitas:,.2f}"
    )

    col2.metric(
        "Despesas",
        f"R$ {despesas:,.2f}"
    )

    col3.metric(
        "Saldo",
        f"R$ {saldo:,.2f}"
    )

    st.markdown("---")


    col_g1, col_g2 = st.columns(2)


    with col_g1:

        st.subheader(
            "🍕 Gastos por Categoria"
        )

        df_despesas = (
            df[df["Tipo"] == "Despesa"]
        )

        if not df_despesas.empty:

            fig = px.pie(
                df_despesas,
                values="Valor",
                names="Categoria",
                hole=0.4,
                color="Categoria",
                color_discrete_map=cores
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    with col_g2:

        st.subheader(
            "📊 Histórico"
        )

        fig = px.bar(
            df,
            x="Data",
            y="Valor",
            color="Tipo",
            barmode="group",
            color_discrete_map={
                "Receita": "green",
                "Despesa": "red"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown("---")


    # HISTÓRICO

    st.subheader(
        "📋 Histórico de Transações"
    )

    st.dataframe(
        df.sort_values(
            by="Data",
            ascending=False
        ),
        use_container_width=True
    )


    st.markdown("---")


    # GERENCIAMENTO

    st.subheader(
        "⚙️ Gerenciar Histórico"
    )

    col_A, col_B = st.columns(2)


    with col_A:

        linha = st.selectbox(
            "Selecione para excluir:",
            options=df.index,
            format_func=lambda x:
            f"{df.loc[x,'Data']} | "
            f"{df.loc[x,'Tipo']} | "
            f"R$ {df.loc[x,'Valor']}"
        )

        if st.button(
            "🗑️ Excluir Item"
        ):

            df = df.drop(
                linha
            )

            df.to_csv(
                DATA_FILE,
                index=False
            )

            st.success(
                "Item removido!"
            )

            st.rerun()


    with col_B:

        st.write(
            "Apagar todos os dados"
        )

        if st.button(
            "💥 Limpar Tudo"
        ):

            pd.DataFrame(
                columns=[
                    "Data",
                    "Tipo",
                    "Categoria",
                    "Valor",
                    "Descrição"
                ]
            ).to_csv(
                DATA_FILE,
                index=False
            )

            st.warning(
                "Histórico apagado!"
            )

            st.rerun()


else:

    st.info(
        "Use a barra lateral para cadastrar sua primeira transação!"
    )
