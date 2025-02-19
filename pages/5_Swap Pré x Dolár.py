import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Título e explicação breve

st.set_page_config(page_title="Swap Pré x Dólar: Hedge de Exportação", layout="wide")
st.title("Swap Pré x Dólar: Hedge de Exportação")

st.write("""
O swap pré x dólar é um instrumento de hedge utilizado por exportadores para reduzir a exposição à volatilidade cambial. 
Nesta operação, o exportador troca a variação do dólar por um fluxo de caixa previsível em reais. 
O swap é contratado com uma instituição financeira, onde o exportador paga a variação cambial e recebe uma taxa pré-fixada em reais.
""")

# Entrada do usuário
valor_exportacao = st.number_input("💰 Digite o valor da exportação em dólares (US$)", min_value=0.0, format="%.2f")
taxa_cambio_inicial = st.number_input("💱 Digite a taxa de câmbio inicial (D0)", min_value=0.0, format="%.4f")
taxa_cambio_final = st.number_input("📊 Digite a taxa de câmbio final (DT)", min_value=0.0, format="%.4f")
taxa_pre_anual = st.number_input("📈 Digite a taxa pré-fixada anual (%)", min_value=0.0, format="%.2f")
prazo_dias = st.number_input("📆 Digite o prazo do swap (dias úteis)", min_value=1, format="%d")

# Botão para calcular
if st.button("🚀 Calcular"):
    # Cálculo do Nocional
    if valor_exportacao > 0 and taxa_cambio_inicial > 0:
        nocional = valor_exportacao * taxa_cambio_inicial
        st.write(f"✅ **Valor nocional do contrato:** R$ {nocional:,.2f}")

        # Cálculo do Valor Atualizado na ponta Dólar
        valor_atualizado_dolar = valor_exportacao * taxa_cambio_final
        st.write(f"💲 **Valor atualizado da ponta Dólar:** R$ {valor_atualizado_dolar:,.2f}")

        # Cálculo do Valor Atualizado na ponta Pré-fixada
        taxa_pre_decimal = taxa_pre_anual / 100
        fator_prazo = (1 + taxa_pre_decimal) ** (prazo_dias / 252)
        valor_atualizado_pre = nocional * fator_prazo
        st.write(f"📈 **Valor atualizado da ponta Pré-fixada:** R$ {valor_atualizado_pre:,.2f}")

        # Cálculo do Resultado do Exportador
        resultado_exportador = valor_atualizado_pre - valor_atualizado_dolar
        st.subheader("📊 Resultado da Operação")

        if resultado_exportador > 0:
            st.success(f"✅ O exportador teve um **ganho** de R$ {resultado_exportador:,.2f} no swap.")
            interpretacao = "O hedge foi bem-sucedido e protegeu a receita do exportador da desvalorização cambial."
        else:
            st.error(f"⚠️ O exportador teve uma **perda** de R$ {abs(resultado_exportador):,.2f} no swap.")
            interpretacao = "O hedge resultou em uma perda devido à valorização inesperada do dólar."

        # Explicação final
        st.write("🔍 **Interpretação do resultado:**")
        st.write(interpretacao)

        st.write("""
        O resultado do swap mostra a diferença entre o valor atualizado da ponta pré-fixada e a ponta cambial.  
        Se o resultado for positivo, significa que o exportador conseguiu fixar um valor mais alto em reais.  
        Se for negativo, significa que teria sido melhor manter a exposição cambial.
        """)

        # Criar DataFrame para exportação
        df_resultado = pd.DataFrame({
            "Parâmetro": ["Valor da Exportação (US$)", "Taxa de Câmbio Inicial (D0)", "Taxa de Câmbio Final (DT)",
                          "Taxa Pré-Fixada (%)", "Prazo do Swap (dias úteis)", "Nocional (R$)",
                          "Valor Atualizado Dólar (R$)", "Valor Atualizado Pré-Fixado (R$)",
                          "Resultado do Exportador (R$)"],
            "Valor": [valor_exportacao, taxa_cambio_inicial, taxa_cambio_final, taxa_pre_anual, prazo_dias, nocional,
                      valor_atualizado_dolar, valor_atualizado_pre, resultado_exportador]
        })

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_resultado.to_excel(writer, index=False, sheet_name="Resultado_Swap")
            writer.close()

        excel_data = output.getvalue()

        st.download_button(label="📥 Baixar resultado em Excel",
                           data=excel_data,
                           file_name="resultado_swap.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


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
