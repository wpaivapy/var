import streamlit as st

# Configuração da página
st.set_page_config(page_title="Cálculo do VaR", page_icon="📊", layout="wide")

# Título da página
st.title("Projeto de Cálculo do Value at Risk (VaR)")



# Página inicial

st.write("""
## Bem-vindo ao Projeto de Cálculo do VaR!

Este projeto tem como objetivo apresentar diferentes métodos para calcular o **Value at Risk (VaR)**, uma métrica amplamente utilizada para medir o risco financeiro. Abaixo estão os métodos disponíveis:

### Métodos de Cálculo do VaR:
1. **Método Paramétrico**:
   - Assume que os retornos seguem uma distribuição normal.
   - Veja o exemplo no Excel: [Clique aqui para visualizar](https://docs.google.com/spreadsheets/d/1dzqBfpH18qMkjlTLS8hYHwKHgPz2YFSg/edit?usp=sharing&ouid=100076090908713606520&rtpof=true&sd=true)

2. **Simulação de Monte Carlo**:
   - Utiliza simulações aleatórias para estimar o VaR.
   - Acesse a página **Simulação de Monte Carlo** para ver um exemplo.

3. **Método Histórico**:
   - Utiliza dados históricos de retornos para estimar o VaR.
   - Acesse a página **Método Histórico** para ver um exemplo.

### Como usar:
- Utilize o menu lateral para navegar entre as páginas e explorar cada método.
""")

# Seção de colaboração

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

