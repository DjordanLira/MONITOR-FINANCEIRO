# =====================================================================
# 🏗️ CATEGORIA 1: CONFIGURAÇÕES INICIAIS E IMPORTAÇÕES
# =====================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Monitor Financeiro", layout="wide")
st.title("💰 Meu Monitor Financeiro Pessoal")


# =====================================================================
# 💾 CATEGORIA 2: PERSISTÊNCIA E GERENCIAMENTO DE DADOS
# =====================================================================
DATA_FILE = "dados_financeiros.csv"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor", "Descrição"])

df = carregar_dados()


# =====================================================================
# 📥 CATEGORIA 3: INTERFACE DE ENTRADA (BARRA LATERAL)
# =====================================================================
st.sidebar.header("Nova Transação")
with st.sidebar.form(key="form_transacao", clear_on_submit=True):
    data = st.date_input("Data")
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    categoria = st.selectbox("Categoria", ["Salário", "Investimentos", "Alimentação", "Transporte", "Moradia", "Lazer", "Outros"])
    valor = st.number_input("Valor (R$)", min_value=0.0, step=5.0, format="%.2f")
    descricao = st.text_input("Descrição")
    botao_salvar = st.form_submit_button(label="Adicionar")


# =====================================================================
# ⚡ CATEGORIA 4: PROCESSAMENTO DE GATILHOS E SALVAMENTO
# =====================================================================
if botao_salvar and valor > 0:
    nova_linha = pd.DataFrame([{"Data": str(data), "Tipo": tipo, "Categoria": categoria, "Valor": valor, "Descrição": descricao}])
    df = pd.concat([df, nova_linha], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.sidebar.success("Salvo com sucesso!")
    st.rerun()


# =====================================================================
# 📊 CATEGORIA 5: INTERFACE DE SAÍDA E VISUALIZAÇÃO DO USUÁRIO
# =====================================================================
if not df.empty:
    # --- Processamento interno de exibição ---
    df["Valor"] = pd.to_numeric(df["Valor"])
    receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
    despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    saldo = receitas - despesas
    
    # --- Bloco de Cartões / Métricas ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Receitas", f"R$ {receitas:,.2f}")
    col2.metric("Total Despesas", f"R$ {despesas:,.2f}")
    col3.metric("Saldo Atual", f"R$ {saldo:,.2f}")

    st.markdown("---")
    
    # --- Bloco de Gráficos ---
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("🍕 Gastos por Categoria")
        df_despesas = df[df["Tipo"] == "Despesa"]
        if not df_despesas.empty:
            st.plotly_chart(px.pie(df_despesas, values="Valor", names="Categoria", hole=0.4), use_container_width=True)
        else:
            st.info("Nenhuma despesa cadastrada para exibir no gráfico.")

    with col_g2:
        st.subheader("📊 Histórico")
        st.plotly_chart(px.bar(df, x="Data", y="Valor", color="Tipo", barmode="group"), use_container_width=True)

    st.markdown("---")
    
    # --- Bloco da Tabela (Histórico das Transações) ---
    st.subheader("📋 Histórico de Transações")
    st.dataframe(df.sort_values(by="Data", ascending=False), use_container_width=True)

    st.markdown("---")
    
    # --- Bloco de Gerenciamento de Dados (Excluir / Resetar) ---
    st.subheader("⚙️ Gerenciar Histórico")
    col_A, col_B = st.columns(2)

    with col_A:
        st.write("**Excluir uma Única Informação**")
        linha_para_deletar = st.selectbox(
            "Selecione o registro que deseja remover:", 
            options=df.index,
            format_func=lambda x: f"ID {x} - {df.loc[x, 'Data']} | {df.loc[x, 'Tipo']} | R$ {df.loc[x, 'Valor']:.2f} ({df.loc[x, 'Descrição']})"
        )
        
        # Correção aplicada aqui (Código fechado com sucesso)
        if st.button("🗑️ Excluir Item Selecionado"):
            df = df.drop(linha_para_deletar)
            df.to_csv(DATA_FILE, index=False)
            st.success("Item removido com sucesso!")
            st.rerun()

    with col_B:
        st.write("**Resetar Todo o Banco de Dados**")
        st.write("Cuidado: Esta ação apagará todas as linhas do seu histórico permanentemente.")
        if st.button("💥 Limpar Todos os Dados"):
            df_vazio = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor", "Descrição"])
            df_vazio.to_csv(DATA_FILE, index=False)
            st.warning("Todos os dados foram apagados!")
            st.rerun()

else:
    # Estado Vazio (Caso o arquivo esteja sem dados)
    st.info("Use a barra lateral para cadastrar sua primeira receita ou despesa!")

