import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np


# Configurar layout wide
st.set_page_config(page_title="Consulta de Cotações de Ativos e Cálculo do VaR Histórico", layout="wide")

# Título do aplicativo
st.title('Consulta de Cotações de Ativos e Cálculo do VaR Histórico')

# Instruções para o usuário
st.markdown('''
**Instruções:**
- Digite o código do ativo no campo acima.
- Insira o nível de confiança desejado (ex: 95 para 95%).
- Escolha o período em dias para o cálculo.
- Clique em "Buscar Cotação e Calcular VaR" para ver os dados e o VaR.
- Exemplos de códigos: `AAPL` (Apple), `PETR4.SA` (Petrobras), `BTC-USD` (Bitcoin).
''')

# Campo de entrada para o usuário inserir o código do ativo
ticker = st.text_input('Digite o código do ativo (ex: AAPL para Apple, PETR4.SA para Petrobras):', 'AAPL')

# Campo de entrada para o nível de confiança
confidence_level = st.number_input('Nível de confiança (ex: 95 para 95%):', min_value=90, max_value=99, value=95)

# Campo para o período
period = st.number_input('Digite o número de dias para o período (ex: 60):', min_value=1, value=60)

# Botão para buscar a cotação e calcular o VaR
if st.button('Buscar Cotação e Calcular VaR'):
    # Coletar os dados do Yahoo Finance
    dados = yf.download(ticker, period=f'{period}d', interval='1d')

    # Verificar se os dados foram coletados corretamente
    if not dados.empty:
        # Calcular os retornos logarítmicos diários
        dados['Retorno Diário'] = np.log(dados['Close'] / dados['Close'].shift(1))

        # Remover a primeira linha (NaN)
        dados = dados.dropna()

        # Exibir o dataframe com os dados de cotação e retornos
        st.write(f'Cotação do ativo {ticker}:')
        st.data_editor(dados)

        # Calcular o VaR histórico
        retornos = dados['Retorno Diário'].sort_values().values  # Ordenar retornos
        var_index = int(np.ceil((1 - confidence_level / 100) * len(retornos)) - 1)  # Índice do percentil
        var = retornos[var_index]  # VaR histórico

        # Exibir o VaR
        st.write(f'VaR Histórico ({confidence_level}%): {var:.4f} (ou {var * 100:.2f}%)')

        # Explicação do VaR
        st.markdown(f'''
        **Interpretação do VaR Histórico:**

        O **VaR Histórico de {var * 100:.2f}%** significa que, com **{confidence_level}% de confiança**, a maior perda esperada para o ativo em um único dia não será maior do que **{var * 100:.2f}%** do valor atual do ativo.

        Em outras palavras, em **{confidence_level}% das vezes**, a perda no ativo não ultrapassará **{var * 100:.2f}%** em um único dia. Para os **{100 - confidence_level}% restantes**, o risco de perda pode ser superior a esse valor.

        
        Isso indica a **exposição ao risco diário** do ativo e pode ser útil para estratégias de **mitigação de risco**.
        ''')

    else:
        st.error('Ativo não encontrado ou código inválido.')


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
