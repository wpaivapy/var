import streamlit as st
import pandas as pd
from decimal import Decimal
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Swap Dólar x Selic: Simulação", layout="wide")
st.title("Swap Dólar x Selic: Simulação")

st.write("""
O swap Dólar x Selic é uma operação financeira que troca a rentabilidade baseada na taxa Selic (juros locais) por uma 
rentabilidade atrelada à variação do dólar mais o cupom cambial (juros em dólar no Brasil). Quem entra no swap “paga” 
o valor acumulado da Selic e “recebe” o valor ajustado pela oscilação do câmbio e pelo cupom. Esse mecanismo é comum 
no mercado financeiro para ajustar exposições ao dólar ou à Selic, refletindo a Paridade Coberta de Juros: a relação 
entre taxas de juros locais, externas e a variação cambial esperada. Use esta ferramenta para simular o resultado 
dessa operação e entender seus fluxos!
""")

# Entrada do usuário
st.subheader("Insira os dados do swap")
nocional = st.number_input("💰 Valor nocional (R$)", min_value=0.0, value=20000000.0, format="%.2f")
taxa_cambio_inicial = st.number_input("💱 Taxa de câmbio inicial (D0)", min_value=0.0, value=3.1049, format="%.4f")
taxa_cambio_final = st.number_input("📊 Taxa de câmbio final (DT)", min_value=0.0, value=3.1800, format="%.4f")
taxa_selic_anual = st.number_input("📈 Taxa Selic anual (% a.a.)", min_value=0.0, value=13.25, format="%.2f")
taxa_cupom_cambial = st.number_input("🌐 Taxa do cupom cambial (% a.a.)", min_value=0.0, value=1.50, format="%.2f")
prazo_dias_uteis = st.number_input("📆 Prazo do swap (dias úteis)", min_value=1, value=150, format="%d")
prazo_dias_corridos = st.number_input("📅 Prazo do swap (dias corridos)", min_value=1, value=218, format="%d")

# Botão para calcular
if st.button("🚀 Calcular"):
    # Converter para Decimal sem perda de precisão
    nocional_dec = Decimal(str(nocional))
    taxa_cambio_inicial_dec = Decimal(str(taxa_cambio_inicial))
    taxa_cambio_final_dec = Decimal(str(taxa_cambio_final))
    taxa_selic_decimal = Decimal(str(taxa_selic_anual)) / Decimal('100')
    taxa_cupom_decimal = Decimal(str(taxa_cupom_cambial)) / Decimal('100')
    prazo_dias_uteis_dec = Decimal(str(prazo_dias_uteis))
    prazo_dias_corridos_dec = Decimal(str(prazo_dias_corridos))

    # Cálculo da ponta Selic
    fator_selic = (Decimal('1') + taxa_selic_decimal) ** (prazo_dias_uteis_dec / Decimal('252'))
    valor_atualizado_selic = nocional_dec * fator_selic
    st.write(f"✅ **Valor atualizado da ponta Selic (pagamento):** R$ {float(valor_atualizado_selic):,.2f}")

    # Cálculo da ponta Dólar + Cupom Cambial
    valor_atualizado_dolar = (nocional_dec * (1 + taxa_cupom_decimal * prazo_dias_corridos / 360)
                              * taxa_cambio_final_dec / taxa_cambio_inicial_dec)
    st.write(f"💲 **Valor atualizado da ponta Dólar + Cupom (recebimento):** R$ {float(valor_atualizado_dolar):,.2f}")

    # Resultado líquido do swap
    resultado_swap = valor_atualizado_dolar - valor_atualizado_selic
    st.subheader("📊 Resultado da Operação")

    if resultado_swap > 0:
        st.success(f"✅ Resultado líquido: **ganho** de R$ {float(resultado_swap):,.2f} no swap.")
        interpretacao = """
        O swap gerou um ganho porque o valor recebido (variação do dólar + cupom cambial) superou o valor pago (Selic). 
        Isso indica que a valorização do câmbio e o cupom foram mais vantajosos que a rentabilidade da Selic no período.
        """
    else:
        st.error(f"⚠️ Resultado líquido: **perda** de R$ {abs(float(resultado_swap)):,.2f} no swap.")
        interpretacao = """
        O swap resultou em uma perda porque o valor pago na ponta Selic foi maior que o recebido na ponta Dólar + Cupom. 
        Isso sugere que a Selic acumulou mais rentabilidade que a combinação da variação cambial e do cupom no período.
        """

    # Explicação detalhada do resultado
    variacao_cambio = ((taxa_cambio_final - taxa_cambio_inicial) / taxa_cambio_inicial) * 100
    rentabilidade_selic = (fator_selic - 1) * 100
    rentabilidade_dolar = ((valor_atualizado_dolar / nocional_dec) - 1) * 100

    st.write("🔍 **Entenda o resultado:**")
    st.write(interpretacao)
    st.write(f"""
    - **Ponta Dólar + Cupom:** O câmbio variou de {taxa_cambio_inicial:.4f} para {taxa_cambio_final:.4f} 
    ({variacao_cambio:.1f}%), e o cupom de {taxa_cupom_cambial:.2f}% a.a. rendeu ao todo {rentabilidade_dolar:.2f}% 
    sobre o nocional, totalizando R$ {float(valor_atualizado_dolar):,.2f}.
    - **Ponta Selic:** A taxa de {taxa_selic_anual:.2f}% a.a. sobre {prazo_dias_uteis} dias úteis gerou uma 
    rentabilidade de {rentabilidade_selic:.2f}%, totalizando R$ {float(valor_atualizado_selic):,.2f}.
    - **Dinâmica:** {'O ganho veio da forte valorização do dólar e/ou do cupom superando a Selic.' if resultado_swap > 0 
    else 'A perda reflete uma Selic mais alta que o retorno combinado do câmbio e cupom.'} O resultado depende do 
    comportamento relativo dessas variáveis no prazo escolhido.
    """)

    # Criar DataFrame para exportação
    df_resultado = pd.DataFrame({
        "Parâmetro": ["Nocional (R$)", "Taxa de Câmbio Inicial (D0)", "Taxa de Câmbio Final (DT)",
                      "Taxa Selic (% a.a.)", "Taxa Cupom Cambial (% a.a.)", "Prazo (dias úteis)",
                      "Prazo (dias corridos)", "Valor Atualizado Selic (R$)",
                      "Valor Atualizado Dólar + Cupom (R$)", "Resultado Líquido (R$)"],
        "Valor": [float(nocional), float(taxa_cambio_inicial), float(taxa_cambio_final), float(taxa_selic_anual),
                  float(taxa_cupom_cambial), int(prazo_dias_uteis), int(prazo_dias_corridos),
                  float(valor_atualizado_selic), float(valor_atualizado_dolar), float(resultado_swap)]
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_resultado.to_excel(writer, index=False, sheet_name="Resultado_Swap")
        writer.close()

    excel_data = output.getvalue()

    st.download_button(label="📥 Baixar resultado em Excel",
                       data=excel_data,
                       file_name="resultado_swap_dolar_selic.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Contato
st.markdown("""
Entre em contato comigo:  
📧 **E-mail:** william.paiva@outlook.com  
📱 **WhatsApp:** +55 11 98576-0234  
🔗 **LinkedIn:** [William Paiva](https://www.linkedin.com/in/william-paiva-fin/)  
""")

# Botão para LinkedIn
st.markdown("""
<a href="https://www.linkedin.com/in/william-paiva-fin/" target="_blank">
    <button style="background-color: #0A66C2; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        Conectar no LinkedIn
    </button>
</a>
""", unsafe_allow_html=True)