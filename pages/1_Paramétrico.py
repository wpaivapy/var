import streamlit as st
import numpy as np

# Configuração para layout wide
st.set_page_config(page_title="VaR - Método Paramétrico", layout="wide")

st.title("Calculadora de Value at Risk - VaR - Método Paramétrico ")

st.markdown("""
### Explicação do Método Paramétrico para Cálculo do Value at Risk (VaR)

O **método paramétrico** para calcular o Value at Risk (VaR) é baseado na premissa de que os retornos dos ativos seguem uma distribuição normal. Este método utiliza a média e o desvio padrão dos retornos históricos para estimar o risco de perda. Os passos básicos incluem:

- **Coleta de Dados**: Obter uma série de retornos históricos do ativo.
- **Cálculo da Média e Desvio Padrão**: Calcular a média (μ) e o desvio padrão (σ) dos retornos.
- **Escolha do Nível de Confiança**: Definir um nível de confiança (por exemplo, 95% ou 99%) que determina o valor crítico (z) da distribuição normal.


### Explicação Customizada para Cálculo do VaR para Notas do Tesouro Nacional (NTN)

Para NTN, uma abordagem mais precisa leva em consideração que estes são títulos de renda fixa, cuja sensibilidade ao risco de taxa de juros pode ser medida pela **duração modificada**. Adaptamos o método paramétrico da seguinte forma:

- **Duração Modificada**: Consideramos a duração modificada para ajustar a volatilidade dos retornos do título, já que ela reflete a sensibilidade do preço do título às mudanças nas taxas de juro.
- **Volatilidade das Taxas de Juro**: Utilizamos a volatilidade das taxas de juro ao invés dos retornos diretos do título, para refletir melhor o risco de mercado para títulos de renda fixa.
- **Yield to Maturity (YTM)**: Levamos em conta o YTM para calcular corretamente a duração modificada, pois isso afeta a sensibilidade do preço do título à variação das taxas.
- **Delta Value de 1bp (DV01)**: Calculamos o DV01 para mostrar a sensibilidade do preço do título a uma mudança de 1 ponto base na taxa de juro.

""")


# Função para calcular VaR ajustado por duração modificada
def calculate_var_adjusted(current_value, macaulay_duration, ytm, rate_volatility, confidence_level, time_horizon):
    # Calculando duração modificada
    modified_duration = macaulay_duration / (1 + ytm)

    z = {95: 1.645, 99: 2.326}[confidence_level]
    daily_std = modified_duration * rate_volatility / np.sqrt(252)  # Assumindo 252 dias de negociação no ano
    var = current_value * (z * daily_std * np.sqrt(time_horizon))
    return var, modified_duration


# Função para calcular DV01
def calculate_dv01(present_value, modified_duration):
    return -modified_duration * present_value * 0.0001


# Interface Streamlit


# Usando um container para agrupar entradas de dados
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        current_value = st.number_input("Valor atual da NTN (PU)", value=1000.00, step=100.00, format="%.2f")
        macaulay_duration = st.number_input("Duração Macaulay do Título", value=5.0, step=0.1)
        ytm = st.number_input("Yield to Maturity (YTM) como fração decimal", value=0.05, step=0.01)  # Ex: 0.05 para 5%

    with col2:
        rate_volatility = st.number_input("Volatilidade das Taxas de Juro (em %) por ano", value=1.0,
                                          step=0.1) / 100  # Convertendo para fração decimal
        confidence_level = st.selectbox("Nível de confiança", [95, 99])
        time_horizon = st.number_input("Horizonte de tempo (dias)", value=1, min_value=1, step=1)

if st.button("Calcular VaR"):
    var, modified_duration = calculate_var_adjusted(current_value, macaulay_duration, ytm, rate_volatility,
                                                    confidence_level, time_horizon)
    dv01 = calculate_dv01(current_value, modified_duration)

    st.write(f"**VaR:** R$ {var:.2f}")
    st.write(f"**DV01:** R$ {dv01:.2f}")
    st.write("**Interpretação:**")
    st.write(
        f"- Há {confidence_level}% de chance de que a perda não exceda R$ {var:.2f} em {time_horizon} dia(s), assumindo a duração modificada e a volatilidade das taxas de juro fornecidas.")
    st.write(
        f"- O DV01 (Delta Value de 1bp) indica que um aumento de 1 ponto base nas taxas de juro resultaria em uma perda aproximada de R$ {abs(dv01):.2f} no valor do título.")

st.markdown(
    "**Nota**: O YTM deve ser fornecido como uma fração decimal. A volatilidade das taxas de juro deve ser em termos anuais. Ela é convertida para diária para o cálculo.")
