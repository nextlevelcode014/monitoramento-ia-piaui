import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
from datetime import datetime
from src.components.dashboard_styles import create_section_header
from src.utils.load_processed_data import load_processed_data
from bs4 import BeautifulSoup
from src.utils.safe_dataframe_display import safe_dataframe_display


def main_dashboard():
    st.markdown(
        """
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🤖 Monitoramento de IA no Piauí</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            Análise de percepção pública sobre Inteligência Artificial
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    df, summary = load_processed_data()

    if df is None:
        st.markdown(
            """
        <div class="custom-alert-warning">
            <h4>Dados não encontrados</h4>
            <p>Execute os seguintes comandos para gerar os dados:</p>
            <pre>
python src/data_collector.py
python src/data_pipeline.py
            </pre>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.stop()

    if len(df) == 0:
        st.warning("Nenhum dado foi encontrado no arquivo carregado.")
        st.stop()

    with st.sidebar:
        st.markdown("### 🔍 Filtros e Controles")

        st.info(f"**{len(df)}** notícias analisadas")

        if summary:
            try:
                avg_score = summary.get("average_score", "N/A")
                st.success(f"Score médio: **{avg_score}**")
            except Exception:
                pass

        st.markdown("---")

        try:
            sentiment_options = ["Todos"]
            if "sentiment_class" in df.columns:
                unique_sentiments = df["sentiment_class"].dropna().unique()
                sentiment_options.extend(sorted([str(s) for s in unique_sentiments]))
            selected_sentiment = st.selectbox("Sentimento:", sentiment_options)
        except Exception:
            selected_sentiment = "Todos"

        try:
            source_options = ["Todas"]
            if "source" in df.columns:
                unique_sources = df["source"].dropna().unique()
                source_options.extend(sorted([str(s) for s in unique_sources]))
            selected_source = st.selectbox("Fonte:", source_options)
        except Exception:
            selected_source = "Todas"

        keyword_filter = st.text_input(
            "Palavra-chave:", placeholder="Digite para buscar..."
        )

        st.markdown("### Configurações")
        show_raw_data = st.checkbox("Mostrar dados brutos", False)
        auto_refresh = st.checkbox("Atualização automática", False)

        if auto_refresh:
            st.rerun()

    df_filtered = df.copy()

    try:
        if selected_sentiment != "Todos" and "sentiment_class" in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered["sentiment_class"] == selected_sentiment
            ]

        if selected_source != "Todas" and "source" in df_filtered.columns:
            df_filtered = df_filtered[df_filtered["source"] == selected_source]

        if keyword_filter and "title" in df_filtered.columns:
            mask = df_filtered["title"].str.contains(
                keyword_filter, case=False, na=False
            )
            df_filtered = df_filtered[mask]
    except Exception as e:
        st.error(f"Erro ao aplicar filtros: {str(e)}")
        df_filtered = df.copy()

    if len(df_filtered) == 0:
        st.warning("Nenhuma notícia encontrada com os filtros aplicados.")
        st.stop()

    create_section_header("Visão Geral", "Métricas principais do monitoramento")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total", len(df_filtered))

    with col2:
        try:
            if "sentiment_score" in df_filtered.columns:
                avg_score = df_filtered["sentiment_score"].mean()
                st.metric("Score Médio", f"{avg_score:.3f}")
            else:
                st.metric("Score Médio", "N/A")
        except Exception:
            st.metric("Score Médio", "N/A")

    with col3:
        try:
            if "sentiment_class" in df_filtered.columns:
                positive_count = len(
                    df_filtered[df_filtered["sentiment_class"] == "positivo"]
                )
                positive_pct = (
                    (positive_count / len(df_filtered) * 100)
                    if len(df_filtered) > 0
                    else 0
                )
                st.metric("😊 Positivas", f"{positive_count} ({positive_pct:.1f}%)")
            else:
                st.metric("😊 Positivas", "N/A")
        except Exception:
            st.metric("😊 Positivas", "N/A")

    with col4:
        try:
            if "sentiment_class" in df_filtered.columns:
                negative_count = len(
                    df_filtered[df_filtered["sentiment_class"] == "negativo"]
                )
                negative_pct = (
                    (negative_count / len(df_filtered) * 100)
                    if len(df_filtered) > 0
                    else 0
                )
                st.metric("😟 Negativas", f"{negative_count} ({negative_pct:.1f}%)")
            else:
                st.metric("😟 Negativas", "N/A")
        except Exception:
            st.metric("😟 Negativas", "N/A")

    with col5:
        try:
            if "sentiment_class" in df_filtered.columns:
                neutral_count = len(
                    df_filtered[df_filtered["sentiment_class"] == "neutro"]
                )
                neutral_pct = (
                    (neutral_count / len(df_filtered) * 100)
                    if len(df_filtered) > 0
                    else 0
                )
                st.metric("😐 Neutras", f"{neutral_count} ({neutral_pct:.1f}%)")
            else:
                st.metric("😐 Neutras", "N/A")
        except Exception:
            st.metric("😐 Neutras", "N/A")

    create_section_header("Análises Visuais", "Gráficos e visualizações dos dados")

    tab1, tab2, tab3 = st.tabs(["Distribuição", "Palavras", "Detalhes"])

    with tab1:
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            try:
                if "sentiment_class" in df_filtered.columns:
                    sentiment_counts = df_filtered["sentiment_class"].value_counts()
                    colors = {
                        "positivo": "#2ecc71",
                        "negativo": "#e74c3c",
                        "neutro": "#95a5a6",
                    }

                    fig_pie = px.pie(
                        values=sentiment_counts.values,
                        names=sentiment_counts.index,
                        title="Distribuição de Sentimentos",
                        color=sentiment_counts.index,
                        color_discrete_map=colors,
                        height=400,
                    )
                    fig_pie.update_traces(
                        textposition="inside", textinfo="percent+label"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("Coluna 'sentiment_class' não encontrada")
            except Exception as e:
                st.error(f"Erro ao gerar gráfico de pizza: {str(e)}")

        with col_chart2:
            try:
                if "sentiment_score" in df_filtered.columns:
                    fig_hist = px.histogram(
                        df_filtered,
                        x="sentiment_score",
                        nbins=15,
                        title="Distribuição dos Scores",
                        color_discrete_sequence=["#3498db"],
                        height=400,
                    )
                    fig_hist.add_vline(x=-0.1, line_dash="dash", line_color="red")
                    fig_hist.add_vline(x=0.1, line_dash="dash", line_color="green")
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.info("Coluna 'sentiment_score' não encontrada")
            except Exception as e:
                st.error(f"Erro ao gerar histograma: {str(e)}")

    with tab2:
        try:
            text_column = None
            for col in ["full_text_clean", "text", "description", "title"]:
                if col in df_filtered.columns:
                    text_column = col
                    break

            if text_column:
                all_text = " ".join(df_filtered[text_column].dropna().astype(str))

                if all_text.strip():
                    wordcloud = WordCloud(
                        width=800,
                        height=400,
                        background_color="white",
                        max_words=80,
                        colormap="plasma",
                        relative_scaling=0.5,
                    ).generate(all_text)

                    fig_wc, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.axis("off")
                    ax.set_title(
                        "Nuvem de Palavras - Termos Mais Frequentes",
                        fontsize=16,
                        pad=20,
                    )

                    st.pyplot(fig_wc)
                else:
                    st.info("Não há texto suficiente para gerar a nuvem de palavras.")
            else:
                st.info("Nenhuma coluna de texto encontrada para a nuvem de palavras.")
        except Exception as e:
            st.error(f"Erro ao gerar nuvem de palavras: {str(e)}")

    with tab3:
        st.markdown("#### Notícias Analisadas")

        try:
            col_sort, col_items = st.columns([2, 1])

            with col_sort:
                sort_options = {}
                if "sentiment_score" in df_filtered.columns:
                    sort_options.update(
                        {
                            "Score (Maior)": ("sentiment_score", False),
                            "Score (Menor)": ("sentiment_score", True),
                        }
                    )
                if "pub_date" in df_filtered.columns:
                    sort_options["Data (Recente)"] = ("pub_date", False)
                if "title" in df_filtered.columns:
                    sort_options["Título (A-Z)"] = ("title", True)

                if not sort_options:
                    sort_options = {"Ordem original": (df_filtered.columns[0], True)}

                sort_choice = st.selectbox("Ordenar por:", list(sort_options.keys()))

            with col_items:
                items_per_page = st.selectbox(
                    "Itens por página:", [5, 10, 15, 20], index=1
                )

            sort_column, ascending = sort_options[sort_choice]
            df_sorted = df_filtered.sort_values(by=sort_column, ascending=ascending)

            total_items = len(df_sorted)
            total_pages = (total_items - 1) // items_per_page + 1

            if total_pages > 1:
                page_num = st.selectbox("Página:", range(1, total_pages + 1))
                start_idx = (page_num - 1) * items_per_page
                end_idx = start_idx + items_per_page
                df_page = df_sorted.iloc[start_idx:end_idx]
            else:
                df_page = df_sorted

            for idx, row in df_page.iterrows():
                with st.container():
                    col_content, col_metrics = st.columns([3, 1])

                    with col_content:
                        sentiment = str(row.get("sentiment_class", "neutro")).lower()
                        emoji = (
                            "😊"
                            if sentiment == "positivo"
                            else "😟"
                            if sentiment == "negativo"
                            else "😐"
                        )

                        title = str(row.get("title", "Sem título"))
                        source = str(row.get("source", "Fonte não informada"))
                        pub_date = str(row.get("pub_date", "Data não informada"))

                        st.markdown(f"**{emoji} {title}**")
                        st.caption(f"{source} | {pub_date}")

                        if st.button("Ver detalhes", key=f"detail_{idx}"):
                            description = str(
                                row.get("description", "Descrição não disponível")
                            )
                            description = BeautifulSoup(description, "html.parser")

                            link = str(row.get("link", "Link não disponível"))
                            st.info(f"**Descrição:** {description.get_text()}")
                            st.info(f"**Link:** {link}")

                    with col_metrics:
                        try:
                            score = float(row.get("sentiment_score", 0))
                            sentiment_color = (
                                "#2ecc71"
                                if sentiment == "positivo"
                                else "#e74c3c"
                                if sentiment == "negativo"
                                else "#95a5a6"
                            )

                            st.markdown(
                                f"""
                            <div style="text-align: center; padding: 0.5rem; background-color: {sentiment_color}20; border-radius: 5px;">
                                <strong style="color: {sentiment_color};">{sentiment.upper()}</strong><br>
                                <span style="font-size: 1.2rem;">{score:.3f}</span>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        except Exception:
                            st.markdown("Score: N/A")

                    st.markdown("---")

        except Exception as e:
            st.error(f"Erro ao exibir tabela: {str(e)}")
            st.markdown("**Tentando exibição alternativa:**")
            safe_dataframe_display(df_filtered, "main")

    create_section_header("Exportar Dados", "Download dos dados analisados")

    col_download1, col_download2, col_download3 = st.columns(3)

    with col_download1:
        try:
            csv_data = df_filtered.to_csv(index=False, encoding="utf-8")
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"ia_piaui_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                help="Baixar dados filtrados em formato CSV",
            )
        except Exception as e:
            st.error(f"Erro ao gerar CSV: {str(e)}")

    with col_download2:
        try:
            df_dict = df_filtered.copy()
            for col in df_dict.columns:
                if df_dict[col].dtype == "object":
                    df_dict[col] = df_dict[col].astype(str)

            json_data = df_dict.to_json(orient="records", force_ascii=False, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"ia_piaui_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                help="Baixar dados filtrados em formato JSON",
            )
        except Exception as e:
            st.error(f"Erro ao gerar JSON: {str(e)}")

    with col_download3:
        if summary:
            try:
                summary_data = json.dumps(summary, ensure_ascii=False, indent=2)
                st.download_button(
                    label="Download Resumo",
                    data=summary_data,
                    file_name=f"resumo_ia_piaui_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json",
                    help="Baixar resumo estatístico",
                )
            except Exception as e:
                st.error(f"Erro ao gerar resumo: {str(e)}")

    if len(df_filtered) > 0:
        create_section_header("Destaque da Análise", "Notícia com análise mais extrema")

        try:
            if "sentiment_score" in df_filtered.columns:
                most_positive = df_filtered.loc[df_filtered["sentiment_score"].idxmax()]
                most_negative = df_filtered.loc[df_filtered["sentiment_score"].idxmin()]

                col_pos, col_neg = st.columns(2)

                with col_pos:
                    st.markdown(
                        """
                    <div class="custom-alert-success">
                        <h4>😊 Mais Positiva</h4>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    st.write(f"**Título:** {str(most_positive.get('title', 'N/A'))}")
                    st.write(
                        f"**Score:** {float(most_positive.get('sentiment_score', 0)):.3f}"
                    )
                    st.write(f"**Fonte:** {str(most_positive.get('source', 'N/A'))}")

                with col_neg:
                    st.markdown(
                        """
                    <div class="custom-alert-warning">
                        <h4>😟 Mais Negativa</h4>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    st.write(f"**Título:** {str(most_negative.get('title', 'N/A'))}")
                    st.write(
                        f"**Score:** {float(most_negative.get('sentiment_score', 0)):.3f}"
                    )
                    st.write(f"**Fonte:** {str(most_negative.get('source', 'N/A'))}")
            else:
                st.info(
                    "Coluna 'sentiment_score' não encontrada para análise de extremos"
                )
        except Exception as e:
            st.error(f"Erro ao gerar análise de destaques: {str(e)}")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background-color: #F5F5F5; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #667eea;">
            <h4 style="color: #292929; margin-top: 0;">⚠️ Limitações da Análise</h4>
            <p style="margin-bottom: 0; color: #292929;">
                Esta análise de sentimento é baseada em <strong>regras simples</strong> e pode não capturar 
                sarcasmo, ironia ou contextos complexos. Os resultados devem ser interpretados como uma 
                <strong>aproximação</strong> e não como uma análise definitiva da percepção pública sobre IA no Piauí.
            </p>
            <br>
            <p style="margin-bottom: 0; font-size: 0.9rem; color: #292929;">
                <strong>Metodologia:</strong> Contagem de palavras-chave positivas e negativas, 
    normalizada pelo tamanho do texto. Última atualização: {datetime.now().strftime("%d/%m/%Y às %H:%M")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if show_raw_data:
        create_section_header(
            "🔧 Dados Técnicos", "Informações detalhadas para debugging"
        )

        with st.expander("Ver estrutura dos dados"):
            st.write("**Colunas disponíveis:**")
            st.write(list(df.columns))
            st.write("**Tipos de dados:**")
            st.write(df.dtypes.to_dict())
            st.write("**Informações gerais:**")
            st.write(f"Shape: {df.shape}")

            st.write("**Amostra dos dados:**")
            try:
                sample_df = df.head(3).copy()
                for col in sample_df.columns:
                    sample_df[col] = sample_df[col].astype(str).str[:50]

                st.dataframe(sample_df, key="debug_sample")

            except Exception as e:
                st.error(f"Erro ao exibir amostra: {str(e)}")
                st.write("**Dados em formato texto:**")
                for i, (idx, row) in enumerate(df.head(2).iterrows()):
                    st.write(f"**Linha {i + 1}:**")
                    for col, val in row.items():
                        st.write(f"  - {col}: {str(val)[:100]}")


if __name__ == "__main__":
    main_dashboard()
