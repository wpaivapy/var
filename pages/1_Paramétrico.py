import streamlit as st
import numpy as np
from scipy.stats import norm
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Cálculo de VaR Paramétrico", layout="wide")
st.title("Cálculo de VaR Paramétrico")

st.write("""
O **Value at Risk (VaR) Paramétrico** estima a perda máxima potencial de um portfólio com base em sua volatilidade 
diária e um nível de confiança, assumindo que os retornos seguem uma distribuição normal. Insira os dados abaixo 
para calcular o VaR do seu portfólio em um horizonte de tempo específico!
""")

# Entrada do usuário
st.subheader("Insira os dados do portfólio")
valor_portfolio = st.number_input("💰 Valor do portfólio (R$)", min_value=0.0, value=1000000.0, format="%.2f")
volatilidade_diaria = st.number_input("📉 Volatilidade diária (% por dia)", min_value=0.0, value=1.26, format="%.2f")
nivel_confianca = st.selectbox("🔍 Nível de confiança", options=[0.90, 0.95, 0.99], index=1)
horizonte_tempo = st.number_input("📅 Horizonte de tempo (dias)", min_value=1, value=1, format="%d")

# Botão para calcular
if st.button("🚀 Calcular VaR"):
    # Conversão dos inputs
    volatilidade_horizonte = (volatilidade_diaria / 100) * np.sqrt(horizonte_tempo)  # Ajusta para o horizonte de tempo
    z_score = norm.ppf(nivel_confianca)  # Z-score correspondente ao nível de confiança

    # Cálculo do VaR
    var = valor_portfolio * volatilidade_horizonte * z_score
    var_percentual = (var / valor_portfolio) * 100

    # Exibição dos resultados
    st.subheader("📊 Resultado do VaR")
    st.success(f"✅ **VaR ({nivel_confianca*100:.0f}% de confiança):** R$ {var:,.2f}")
    st.write(f"**VaR percentual:** {var_percentual:.2f}% do valor do portfólio")

    # Interpretação do resultado
    st.write("🔍 **O que isso significa?**")
    st.write(f"""
    Com {nivel_confianca*100:.0f}% de confiança, a perda máxima esperada do portfólio em {horizonte_tempo} 
    dia(s) é de R$ {var:,.2f}. Isso significa que há uma chance de {100 - nivel_confianca*100:.0f}% de as perdas 
    excederem esse valor, considerando a volatilidade diária de {volatilidade_diaria:.2f}% e a distribuição normal 
    dos retornos.
    """)
    st.write(f"""
    - **Volatilidade no horizonte:** {(volatilidade_horizonte*100):.2f}%  
    - **Z-score usado:** {z_score:.2f}
    """)

    # Gráfico simples da distribuição
    st.subheader("📈 Visualização da Distribuição")
    x = np.linspace(-4, 4, 100)  # Z-scores para a curva normal
    y = norm.pdf(x, 0, 1)  # Densidade da normal padrão
    df = pd.DataFrame({"Z-score": x, "Densidade": y}).set_index("Z-score")
    st.line_chart(df)
    st.write(f"A linha vertical seria em {z_score:.2f}, delimitando o VaR na cauda esquerda.")

# Informações adicionais
st.markdown("""
### Como o VaR é calculado?
O VaR paramétrico usa a fórmula:  
**VaR = Valor do Portfólio × Volatilidade no Horizonte × Z-score**  
- **Volatilidade no horizonte** = Volatilidade diária × √(dias)  
- **Z-score** = Percentil da distribuição normal para o nível de confiança (ex.: 1,65 para 95%).  
""")

# Contato
st.markdown("""
Entre em contato comigo:  
📧 **E-mail:** william.paiva@outlook.com  
📱 **WhatsApp:** +55 11 98576-0234  
🔗 **LinkedIn:** [William Paiva](https://www.linkedin.com/in/william-paiva-fin/)  
""")