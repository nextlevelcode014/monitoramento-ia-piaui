from src.components.dashboard_styles import apply_custom_css
from src.components.main_dashboard import main_dashboard
from src.components.report_modal import report_modal
from src.utils.generate_statistical_report import (
    generate_statistical_report,
)
from src.utils.advanced_analysis import advanced_analysis
from src.utils.load_processed_data import load_processed_data
from src.components.about_page import about_page

import streamlit as st


st.set_page_config(
    page_title="Monitoramento IA Piauí",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()


def main():
    st.sidebar.title("🤖 Navegação")

    pages = {
        "🏠 Dashboard Principal": main_dashboard,
        "📈 Análises Avançadas": advanced_analysis,
        "ℹ️ Sobre o Projeto": about_page,
    }

    selected_page = st.sidebar.radio("Selecione a página:", list(pages.keys()))

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Status do Sistema")

    df, summary = load_processed_data()
    if df is not None:
        st.sidebar.success(f"{len(df)} notícias carregadas")
        if summary:
            st.sidebar.info(f"Score médio: {summary['average_score']}")
    else:
        st.sidebar.error("Dados não encontrados :(")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Ações Rápidas")

    if st.sidebar.button("Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

    if st.sidebar.button("Gerar Relatório"):
        if df is not None and len(df) > 0:
            with st.spinner("Gerando relatório completo..."):
                stats = generate_statistical_report(df, summary)
                if stats:
                    st.session_state.show_report = True
                    st.session_state.report_stats = stats
                    st.session_state.report_df = df
                else:
                    st.sidebar.error("Erro ao gerar estatísticas")
        else:
            st.sidebar.error("Carregue os dados primeiro!")

    if st.session_state.get("show_report", False):
        st.markdown("---")
        report_modal(st.session_state.report_stats, st.session_state.report_df)

        if st.button("❌ Fechar Relatório"):
            st.session_state.show_report = False
            st.rerun()

    pages[selected_page]()


if __name__ == "__main__":
    main()
