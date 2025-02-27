import streamlit as st
from decimal import Decimal
import pandas as pd
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Swap IGP-M x DI: Simulação", layout="wide")
st.title("Swap IGP-M x DI: Simulação")

st.write("""
O swap IGP-M x DI é uma operação financeira que troca a rentabilidade baseada no IGP-M (Índice Geral de Preços do Mercado) 
mais um cupom por uma rentabilidade atrelada à taxa DI (Depósitos Interbancários). Quem entra no swap “paga” o valor 
acumulado da DI e “recebe” o valor ajustado pela variação do IGP-M mais o cupom negociado. Essa operação é comum para 
empresas que desejam converter despesas ou passivos indexados ao IGP-M em taxas DI, ajustando sua exposição a índices 
de inflação e juros. Use esta ferramenta para simular o resultado do swap!
""")

# Entrada do usuário
st.subheader("Insira os dados do swap")
nocional = st.number_input("💰 Valor nocional (R$)", min_value=0.0, value=20000000.0, format="%.2f")
prazo_dias_uteis = st.number_input("📆 Prazo do swap (dias úteis)", min_value=1, value=78, format="%d")
cupom_igpm = st.number_input("📈 Cupom IGP-M (% a.a.)", min_value=0.0, value=8.50, format="%.2f")
igpm_variacao = st.number_input("📊 Variação IGP-M (% a.a.)", min_value=0.0, value=5.85, format="%.2f")
taxa_di = st.number_input("🌐 Taxa DI (% a.a.)", min_value=0.0, value=13.40, format="%.2f")

# Botão para calcular
if st.button("🚀 Calcular"):
    # Converter para Decimal sem perda de precisão
    nocional_dec = Decimal(str(nocional))
    prazo_dias_uteis_dec = Decimal(str(prazo_dias_uteis))
    cupom_igpm_dec = Decimal(str(cupom_igpm)) / Decimal('100')
    igpm_variacao_dec = Decimal(str(igpm_variacao)) / Decimal('100')
    taxa_di_dec = Decimal(str(taxa_di)) / Decimal('100')

    # Cálculo da ponta IGP-M + Cupom
    # A fórmula considera a soma da variação do IGP-M com o cupom, anualizada em 252 dias úteis



    taxa_total_igpm = igpm_variacao_dec + cupom_igpm_dec
    fator_igpm = (Decimal('1') + taxa_total_igpm) ** (prazo_dias_uteis_dec / Decimal('252'))

    valor_atualizado_igpm = nocional_dec*(1+igpm_variacao_dec)**(prazo_dias_uteis_dec/252)*(1+cupom_igpm_dec)**(prazo_dias_uteis_dec/252)
    #valor_atualizado_igpm = nocional_dec * fator_igpm
    st.write(f"✅ **Valor atualizado da ponta IGP-M + Cupom (recebimento):** R$ {float(valor_atualizado_igpm):,.2f}")

    # Cálculo da ponta DI
    fator_di = (Decimal('1') + taxa_di_dec) ** (prazo_dias_uteis_dec / Decimal('252'))
    valor_atualizado_di = nocional_dec * fator_di
    st.write(f"💲 **Valor atualizado da ponta DI (pagamento):** R$ {float(valor_atualizado_di):,.2f}")

    # Resultado líquido do swap
    resultado_swap = valor_atualizado_igpm - valor_atualizado_di
    st.subheader("📊 Resultado da Operação")

    if resultado_swap > 0:
        st.success(f"✅ Resultado líquido: **ganho** de R$ {float(resultado_swap):,.2f} no swap.")
        interpretacao = """
        O swap gerou um ganho porque o valor recebido (variação do IGP-M + cupom) superou o valor pago (DI). 
        Isso indica que a combinação da inflação medida pelo IGP-M e o cupom foi mais vantajosa que a taxa DI no período.
        """
    else:
        st.error(f"⚠️ Resultado líquido: **perda** de R$ {abs(float(resultado_swap)):,.2f} no swap.")
        interpretacao = """
        O swap resultou em uma perda porque o valor pago na ponta DI foi maior que o recebido na ponta IGP-M + Cupom. 
        Isso sugere que a taxa DI acumulou mais rentabilidade que a combinação da variação do IGP-M e do cupom no período.
        """

    # Explicação detalhada do resultado
    rentabilidade_igpm = (fator_igpm - 1) * 100
    rentabilidade_di = (fator_di - 1) * 100

    st.write("🔍 **Entenda o resultado:**")
    st.write(interpretacao)
    st.write(f"""
    - **Ponta IGP-M + Cupom:** A variação do IGP-M de {igpm_variacao:.2f}% a.a. somada ao cupom de {cupom_igpm:.2f}% a.a. 
    rendeu ao todo {float(rentabilidade_igpm):,.2f}% sobre o nocional em {prazo_dias_uteis} dias úteis, 
    totalizando R$ {float(valor_atualizado_igpm):,.2f}.
    - **Ponta DI:** A taxa DI de {taxa_di:.2f}% a.a. gerou uma rentabilidade de {float(rentabilidade_di):,.2f}% 
    em {prazo_dias_uteis} dias úteis, totalizando R$ {float(valor_atualizado_di):,.2f}.
    - **Dinâmica:** {'O ganho veio da forte valorização do IGP-M e/ou do cupom superando a DI.' if resultado_swap > 0 
    else 'A perda reflete uma DI mais alta que o retorno combinado do IGP-M e cupom.'} O resultado depende do 
    comportamento relativo dessas variáveis no prazo escolhido.
    """)

    # Criar DataFrame para exportação
    df_resultado = pd.DataFrame({
        "Parâmetro": ["Nocional (R$)", "Prazo (dias úteis)", "Cupom IGP-M (% a.a.)",
                      "Variação IGP-M (% a.a.)", "Taxa DI (% a.a.)",
                      "Valor Atualizado IGP-M + Cupom (R$)", "Valor Atualizado DI (R$)",
                      "Resultado Líquido (R$)"],
        "Valor": [float(nocional), int(prazo_dias_uteis), float(cupom_igpm), float(igpm_variacao),
                  float(taxa_di), float(valor_atualizado_igpm), float(valor_atualizado_di),
                  float(resultado_swap)]
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_resultado.to_excel(writer, index=False, sheet_name="Resultado_Swap")
        writer.close()

    excel_data = output.getvalue()

    st.download_button(label="📥 Baixar resultado em Excel",
                       data=excel_data,
                       file_name="resultado_swap_igpm_di.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Informações adicionais
st.write("""
### Notas:
- Os cálculos utilizam 252 dias úteis como convenção de mercado no Brasil.
- A ponta IGP-M + Cupom soma a variação do IGP-M ao cupom antes de aplicar o fator de capitalização.
- O resultado reflete a diferença entre o recebimento (IGP-M + Cupom) e o pagamento (DI).
""")



st.markdown("""
Entre em contato comigo:  
📧 **E-mail:** william.paiva@outlook.com  
📱 **WhatsApp:** +55 11 98576-0234  
🔗 **LinkedIn:** [William Paiva](https://www.linkedin.com/in/william-paiva-fin/)  
""")

# Botão para redirecionar para o LinkedIn (opcional)
st.markdown("""
<a href="https://www.linkedin.com/in/william-paiva-fin/" target="_blank">
    <button style="background-color: #0A66C2; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        Conectar no LinkedIn
    </button>
</a>
""", unsafe_allow_html=True)
