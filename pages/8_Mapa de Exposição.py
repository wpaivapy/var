import streamlit as st
import pandas as pd
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Mapa de Exposição Cambial", layout="wide")

# Título
st.title("📊 Mapa de Exposição Cambial")

st.write("""
Este aplicativo permite mapear a exposição cambial de uma empresa em diferentes moedas e prazos.  
O objetivo é entender o risco cambial total e ajudar na definição da estratégia de hedge.
""")

# Criando uma sessão para armazenar os dados inseridos pelo usuário
if "exposicao_data" not in st.session_state:
    st.session_state.exposicao_data = []

# Formulário para inserir nova exposição
st.subheader("📝 Inserir Nova Exposição Cambial")
col1, col2, col3 = st.columns(3)

with col1:
    moeda = st.selectbox("Moeda", ["USD", "EUR", "GBP", "JPY", "BRL", "CNY", "ARS"])

with col2:
    montante = st.number_input("Montante na Moeda Selecionada", min_value=0.0, format="%.2f")

with col3:
    prazo = st.number_input("Prazo da Exposição (dias)", min_value=1, format="%d")

# Botão para adicionar exposição
if st.button("Adicionar Exposição"):
    if montante > 0:
        st.session_state.exposicao_data.append({"Moeda": moeda, "Montante": montante, "Prazo": prazo})
        st.success("Exposição adicionada com sucesso!")

# Criando DataFrame com as exposições inseridas
if st.session_state.exposicao_data:
    df_exposicao = pd.DataFrame(st.session_state.exposicao_data)

    # Exibir DataFrame completo
    st.subheader("📋 Exposição Cambial Registrada")
    st.dataframe(df_exposicao)

    # Exposição total por moeda
    st.subheader("🔍 Exposição Total por Moeda")
    df_total_moeda = df_exposicao.groupby("Moeda")["Montante"].sum().reset_index()
    st.dataframe(df_total_moeda)

    # Exposição total por prazo
    st.subheader("⏳ Exposição Total por Prazo")
    df_total_prazo = df_exposicao.groupby("Prazo")["Montante"].sum().reset_index()
    st.dataframe(df_total_prazo)

    # Exportação dos dados para Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_exposicao.to_excel(writer, sheet_name="Exposicao_Completa", index=False)
        df_total_moeda.to_excel(writer, sheet_name="Total_Por_Moeda", index=False)
        df_total_prazo.to_excel(writer, sheet_name="Total_Por_Prazo", index=False)
        writer.close()

    st.download_button(
        label="📥 Baixar Mapa de Exposição em Excel",
        data=output.getvalue(),
        file_name="mapa_exposicao_cambial.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
