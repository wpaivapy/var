import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Configuração inicial do Streamlit
st.set_page_config(page_title="Dashboard Câmbio", layout="wide")
st.title("Panorama Econômico: Câmbio, Reservas, SELIC e Inflação em Tempo Real")

# Dicionário de moedas disponíveis no Banco Central
moedas = {
    "Dólar (USD/BRL)": 1,
    "Euro (EUR/BRL)": 21619,
    "Libra (GBP/BRL)": 21623,
    "Iene (JPY/BRL)": 21621
}

# Selecionar moeda
moeda_selecionada = st.sidebar.selectbox("Selecione a moeda", list(moedas.keys()), index=0)
codigo_cambio = moedas[moeda_selecionada]


# Função para buscar dados do Banco Central do Brasil
def get_bacen_data(endpoint):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{endpoint}/dados?formato=json"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return None


# Buscar dados do câmbio
df = get_bacen_data(codigo_cambio)
if df is not None:
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["valor"] = pd.to_numeric(df["valor"], errors='coerce')
    df = df[df["data"] >= "2020-01-01"]

    # Criar filtro de data
    st.sidebar.header("Filtro de Data")
    data_inicio = st.sidebar.date_input("Data Início", df["data"].min())
    data_fim = st.sidebar.date_input("Data Fim", df["data"].max())

    df_filtrado = df[(df["data"] >= pd.to_datetime(data_inicio)) & (df["data"] <= pd.to_datetime(data_fim))]

    df_filtrado = df_filtrado.set_index("data")
    modelo = ExponentialSmoothing(df_filtrado["valor"], trend="add", seasonal=None).fit()
    previsao_periodo = 6 * 30
    previsao = modelo.forecast(steps=previsao_periodo)

    ult_data = df_filtrado.index[-1]
    datas_futuras = pd.date_range(start=ult_data + pd.Timedelta(days=1), periods=previsao_periodo, freq='D')
    df_previsao = pd.DataFrame({"data": datas_futuras, "valor": previsao})

    df_filtrado = df_filtrado.reset_index()
    df_previsao = df_previsao.reset_index(drop=True)
    df_completo = pd.concat([df_filtrado, df_previsao])
    df_completo["tipo"] = ["Histórico"] * len(df_filtrado) + ["Previsão"] * len(df_previsao)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{moeda_selecionada} e Previsão para os Próximos 6 Meses")
        fig = px.line(df_completo, x="data", y="valor", color="tipo",
                      labels={"valor": "Cotação", "tipo": "Legenda"},
                      title=f"Variação do {moeda_selecionada} e Projeção para os Próximos 6 Meses")
        st.plotly_chart(fig, use_container_width=True)

# Buscar dados das reservas internacionais
df_reservas = get_bacen_data(13621)
if df_reservas is not None:
    df_reservas["data"] = pd.to_datetime(df_reservas["data"], dayfirst=True)
    df_reservas["valor"] = pd.to_numeric(df_reservas["valor"], errors='coerce')
    df_reservas = df_reservas[df_reservas["data"] >= "2020-01-01"]
    df_reservas_filtrado = df_reservas[
        (df_reservas["data"] >= pd.to_datetime(data_inicio)) & (df_reservas["data"] <= pd.to_datetime(data_fim))]
    with col2:
        st.subheader("Reservas Internacionais")
        fig_reservas = px.line(df_reservas_filtrado, x="data", y="valor",
                               labels={"valor": "Reservas (USD Milhões)"},
                               title="Evolução das Reservas Internacionais")
        st.plotly_chart(fig_reservas, use_container_width=True)

# Criar gráficos adicionais para Taxa SELIC e Inflação Acumulada
col3, col4 = st.columns(2)

# Buscar dados da Taxa SELIC
df_selic = get_bacen_data(432)
if df_selic is not None:
    df_selic["data"] = pd.to_datetime(df_selic["data"], dayfirst=True)
    df_selic["valor"] = pd.to_numeric(df_selic["valor"], errors='coerce')
    df_selic = df_selic[df_selic["data"] >= "2020-01-01"]
    df_selic_filtrado = df_selic[
        (df_selic["data"] >= pd.to_datetime(data_inicio)) & (df_selic["data"] <= pd.to_datetime(data_fim))]
    with col3:
        st.subheader("Taxa SELIC")
        fig_selic = px.line(df_selic_filtrado, x="data", y="valor",
                            labels={"valor": "Taxa (%)"},
                            title="Evolução da Taxa SELIC")
        st.plotly_chart(fig_selic, use_container_width=True)

# Buscar dados da Inflação Acumulada dos Últimos 12 Meses
df_ipca = get_bacen_data(433)
if df_ipca is not None:
    df_ipca["data"] = pd.to_datetime(df_ipca["data"], dayfirst=True)
    df_ipca["valor"] = pd.to_numeric(df_ipca["valor"], errors='coerce')
    df_ipca = df_ipca[df_ipca["data"] >= "2020-01-01"]
    df_ipca["acumulado_12m"] = df_ipca["valor"].rolling(window=12).sum()
    df_ipca_filtrado = df_ipca[
        (df_ipca["data"] >= pd.to_datetime(data_inicio)) & (df_ipca["data"] <= pd.to_datetime(data_fim))]
    with col4:
        st.subheader("Inflação Acumulada (Últimos 12 Meses)")
        fig_ipca = px.line(df_ipca_filtrado, x="data", y="acumulado_12m",
                           labels={"acumulado_12m": "Inflação (%)"},
                           title="Evolução da Inflação Acumulada 12M")
        st.plotly_chart(fig_ipca, use_container_width=True)

st.write(
    "📌 Dados atualizados em tempo real via API do Banco Central do Brasil, incluindo previsão baseada no modelo Holt-Winters.")


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
