import streamlit as st
from src.components.dashboard_styles import create_section_header
from src.components.dashboard_components import DashboardComponents
from src.utils.load_processed_data import load_processed_data


def advanced_analysis():
    st.title("Análises Avançadas")

    df, _ = load_processed_data()

    if df is None:
        st.error("Dados não encontrados!")
        return

    create_section_header(
        "Análise por Fonte", "Comparação entre diferentes veículos de notícias"
    )

    col1, col2 = st.columns(2)

    with col1:
        bar_chart = DashboardComponents.create_sentiment_bar_chart(df)
        if bar_chart:
            st.plotly_chart(bar_chart, use_container_width=True)
        else:
            st.info("Gráfico por fonte não disponível")

    with col2:
        score_dist = DashboardComponents.create_score_distribution(df)
        if score_dist:
            st.plotly_chart(score_dist, use_container_width=True)
        else:
            st.info("Distribuição de scores não disponível")

    create_section_header(
        "Análise de Vocabulário", "Palavras mais frequentes por categoria"
    )

    tab_pos, tab_neg, tab_neu = st.tabs(["😊 Positivas", "😟 Negativas", "😐 Neutras"])

    with tab_pos:
        pos_chart = DashboardComponents.create_top_words_chart(df, "positivo")
        if pos_chart:
            st.plotly_chart(pos_chart, use_container_width=True)
        else:
            st.info("Dados insuficientes para análise de palavras positivas")

    with tab_neg:
        neg_chart = DashboardComponents.create_top_words_chart(df, "negativo")
        if neg_chart:
            st.plotly_chart(neg_chart, use_container_width=True)
        else:
            st.info("Dados insuficientes para análise de palavras negativas")

    with tab_neu:
        neu_chart = DashboardComponents.create_top_words_chart(df, "neutro")
        if neu_chart:
            st.plotly_chart(neu_chart, use_container_width=True)
        else:
            st.info("Dados insuficientes para análise de palavras neutras")
