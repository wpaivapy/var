import streamlit as st
import pandas as pd
from babel.numbers import format_currency
from io import BytesIO

# Configurar layout wide
st.set_page_config(layout="wide")

# Título do app
st.title("Simulação de Ajuste NDF")

# Explicação sobre NDF e objetivo da aplicação
st.markdown("""
### O que é um NDF (Non-Deliverable Forward)?
Um NDF é um contrato a termo de câmbio sem entrega física da moeda, utilizado para proteger empresas contra variações cambiais. No vencimento, ocorre a liquidação financeira com base na diferença entre a cotação contratada e a cotação de fechamento.

### Objetivo da Aplicação
Esta ferramenta permite simular o ajuste financeiro de um NDF com base nos dados inseridos. Importante: **não estamos considerando os impostos aplicáveis na operação**, como:
- **IR de 15% compensável** sobre o ganho financeiro.
- **PIS/COFINS** para operações não caracterizadas como hedge.
""")

# Seleção de posição
posicao = st.selectbox("Posição", ["Importador", "Exportador"])

# Seleção de moeda
moeda = st.selectbox("Moeda", ["USD", "EUR"])

# Determinar rótulo da cotação fechada com base na posição
rotulo_cotacao = "Cotação de Compra Fechada" if posicao == "Importador" else "Cotação de Venda Fechada"
cotacao_fechada = st.number_input(rotulo_cotacao, min_value=0.0001, format="%.4f")

# Notional
notional = st.number_input("Notional Montante na Moeda Selecionada", min_value=1_000.0, format="%.2f")

# Cotação de fechamento
cotacao_fechamento = st.number_input("Cotação de Fechamento", min_value=0.0001, format="%.4f")

# Cálculo do ajuste
diferenca_cotacao = cotacao_fechamento - cotacao_fechada
ajuste = diferenca_cotacao * notional

# Pagamento
pagamento = cotacao_fechamento * notional

# Valor Líquido
valor_liquido = pagamento - ajuste

# Exibir resultados
st.subheader("Resultado da Operação")
st.write("**Ajuste**")
st.write(format_currency(abs(ajuste), "BRL", locale="pt_BR"))

st.write("**Pagamento**")
st.write(format_currency(pagamento, "BRL", locale="pt_BR"))

st.write("**Valor Líquido**")
st.write(format_currency(valor_liquido, "BRL", locale="pt_BR"))

# Interpretação do ajuste
st.subheader("Interpretação da Operação")
if (posicao == "Importador" and cotacao_fechamento > cotacao_fechada) or (posicao == "Exportador" and cotacao_fechamento < cotacao_fechada):
    st.info("Como a cotação de fechamento foi desfavorável à posição assumida, a empresa **deverá receber** o ajuste na moeda local. Isso ocorre porque a NDF protegeu a empresa contra a variação cambial.")
else:
    st.info("Como a cotação de fechamento foi favorável à posição assumida, a empresa **deverá pagar** o ajuste na moeda local. Isso ocorre porque a NDF garantiu um valor protegido, mas a cotação de mercado foi mais vantajosa.")

# Criar DataFrame para exportação
df = pd.DataFrame({
    "Parâmetro": [
        "Posição", "Moeda", rotulo_cotacao, "Notional", "Cotação de Fechamento",
        "Ajuste", "Pagamento", "Valor Líquido"
    ],
    "Valor": [
        posicao, moeda, cotacao_fechada, notional, cotacao_fechamento,
        ajuste, pagamento, valor_liquido
    ]
})

# Criar botão para exportar para Excel
output = BytesIO()
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Ajuste NDF", index=False)
    writer.close()
output.seek(0)

st.download_button(
    label="📥 Baixar Resultados em Excel",
    data=output,
    file_name="ajuste_ndf.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Contato
st.markdown("""
Entre em contato comigo:  
📧 **E-mail:** william.paiva@outlook.com  
📱 **WhatsApp:** +55 11 98576-0234  
🔗 **LinkedIn:** [William Paiva](https://www.linkedin.com/in/william-paiva-fin/)  
""")

# Botão para redirecionar para o LinkedIn
st.markdown("""
<a href="https://www.linkedin.com/in/william-paiva-fin/" target="_blank">
    <button style="background-color: #0A66C2; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        Conectar no LinkedIn
    </button>
</a>
""", unsafe_allow_html=True)
