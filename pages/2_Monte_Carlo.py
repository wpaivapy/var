import streamlit as st
import numpy as np
import locale

# Configurar layout wide
st.set_page_config(page_title="Simulação de VaR Monte Carlo", layout="wide")

# Definir local para formatação monetária brasileira
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

# Título do app
st.title("Simulação de VaR Monte Carlo")

# Entrada do valor da exposição sem formatação (internamente)
valor_exposicao = st.number_input("Valor da Exposição (R$)", min_value=1_000_000, value=100_000_000, step=1_000_000)

# Entrada de outros parâmetros
media_retorno = st.number_input("Média de Retorno Diário (%)", value=0.05) / 100
desvio_padrao = st.number_input("Volatilidade Diária (%)", value=2.0) / 100
num_simulacoes = st.number_input("Número de Simulações", min_value=1_000, value=100_000, step=1_000)
nivel_confianca = st.slider("Nível de Confiança (%)", min_value=90, max_value=99, value=95) / 100

# Botão para calcular
if st.button("Calcular VaR"):
    # Gerar simulação de retornos aleatórios
    retornos_simulados = np.random.normal(media_retorno, desvio_padrao, num_simulacoes)

    # Calcular perdas simuladas
    perdas = valor_exposicao * retornos_simulados

    # Determinar o percentil do VaR
    var_monte_carlo = np.percentile(perdas, (1 - nivel_confianca) * 100)

    # Exibir resultado formatado
    st.markdown(f"### Resultado da Simulação:")
    st.metric("Valor da Exposição", locale.currency(valor_exposicao, grouping=True))
    st.metric(f"VaR Monte Carlo ({int(nivel_confianca * 100)}% de confiança)",
              locale.currency(abs(var_monte_carlo), grouping=True))

    # Explicação do VaR
    st.markdown(
        f"🔹 **O que significa esse resultado?**\n\n"
        f"O **VaR Monte Carlo ({int(nivel_confianca * 100)}% de confiança)** indica que, em **{int(nivel_confianca * 100)}% dos casos**, "
        f"a perda **não deve ultrapassar** {locale.currency(abs(var_monte_carlo), grouping=True)} em um único dia, considerando as premissas de volatilidade e retorno médio."
    )
