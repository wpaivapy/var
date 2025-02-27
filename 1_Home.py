import streamlit as st

# Configuração da página
st.set_page_config(page_title="Plataforma de Riscos e Hedge", page_icon="📊", layout="wide")

# Título da página
st.title("📊 Plataforma de Riscos e Hedge")

# Seção de Introdução
st.write("""
## Bem-vindo à Plataforma de Gestão de Riscos e Hedge Cambial! 💰📈

Esta plataforma permite simular e calcular diferentes operações financeiras, auxiliando na **gestão de riscos**, **tomada de decisões estratégicas** e **proteção contra variações do mercado**.

Aqui você pode calcular desde o **Value at Risk (VaR)** até diferentes operações de **hedge** e **swaps**.

### 🔹 O que você pode calcular nesta plataforma?
✅ **Value at Risk (VaR)** – Estime o risco de perdas financeiras com os métodos:
   - **Paramétrico** (Distribuição Normal)
   - **Histórico** (Baseado em dados reais)
   - **Monte Carlo** (Simulação Estatística)

✅ **Cálculo de Hedge Cambial** – Simule operações para minimizar riscos:
   - **NDF (Non-Deliverable Forward)**: Proteja-se contra flutuações cambiais.
   - **Swap Pré x Dólar**: Firme uma taxa pré-fixada para operações de exportação.
   - **Swap Dólar x Selic**: Converta dívidas ou investimentos entre diferentes indexadores.
   - **Swap IGP-M x DI**: Troque indexadores para otimizar passivos atrelados ao IGP-M.

✅ **Mapeamento de Exposição Cambial**:
   - Insira suas posições em diversas moedas.
   - Calcule sua **exposição total por moeda e prazo**.
   - Prepare-se para definir a melhor estratégia de hedge.

---

### 📌 **Como utilizar?**
1️⃣ **Escolha a funcionalidade desejada no menu lateral** 🏦  
2️⃣ **Insira os parâmetros da operação ou risco que deseja calcular** ✍️  
3️⃣ **Visualize os cálculos e gráficos interativos** 📊  
4️⃣ **Exporte os resultados para Excel para análise detalhada** 📥  

💡 **Transforme seus dados financeiros em decisões estratégicas!**

---



📧 **E-mail:** william.paiva@outlook.com  
📱 **WhatsApp:** +55 11 98576-0234  
🔗 **LinkedIn:** [William Paiva](https://www.linkedin.com/in/william-paiva-fin/)  

<a href="https://www.linkedin.com/in/william-paiva-fin/" target="_blank">
    <button style="background-color: #0A66C2; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        Conectar no LinkedIn
    </button>
</a>
""", unsafe_allow_html=True)
