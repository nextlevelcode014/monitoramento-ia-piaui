from datetime import datetime
import streamlit as st
import json
from src.utils.create_report_txt import create_report_text


def report_modal(stats, df):
    st.subheader("Relatório Gerado com Sucesso!")

    tab_texto, tab_download = st.tabs(["Texto", "Download"])
    with tab_texto:
        report_text = create_report_text(stats)
        st.markdown(report_text)

        st.download_button(
            label="Download Relatório (TXT)",
            data=report_text.encode("utf-8"),
            file_name=f"relatorio_ia_piaui_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )

    with tab_download:
        st.info("**Formatos Disponíveis:**")

        col1, col2 = st.columns(2)

        with col1:
            txt_data = create_report_text(stats).encode("utf-8")
            st.download_button(
                "Relatório Completo (TXT)",
                txt_data,
                file_name=f"relatorio_completo_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
            )

            csv_data = df.to_csv(index=False, encoding="utf-8")
            st.download_button(
                "Dados Brutos (CSV)",
                csv_data,
                file_name=f"dados_ia_piaui_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
            )

        with col2:
            json_data = stats

            json_str = json.dumps(json_data, ensure_ascii=False, indent=2, default=str)
            st.download_button(
                "Estatísticas (JSON)",
                json_str.encode("utf-8"),
                file_name=f"stats_ia_piaui_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
            )
