import plotly.express as px
from collections import Counter


class DashboardComponents:
    @staticmethod
    def create_sentiment_bar_chart(df):
        if "source" not in df.columns:
            return None

        source_sentiment = (
            df.groupby(["source", "sentiment_class"]).size().unstack(fill_value=0)
        )

        fig = px.bar(
            source_sentiment,
            title="Sentimentos por Fonte de Notícia",
            color_discrete_map={
                "positivo": "#2ecc71",
                "negativo": "#e74c3c",
                "neutro": "#95a5a6",
            },
        )

        fig.update_layout(
            xaxis_title="Fonte",
            yaxis_title="Número de Notícias",
            title_font_size=18,
            height=400,
        )

        return fig

    @staticmethod
    def create_score_distribution(df):
        fig = px.histogram(
            df,
            x="sentiment_score",
            nbins=20,
            title="Distribuição dos Scores de Sentimento",
            color_discrete_sequence=["#3498db"],
        )

        fig.update_layout(
            xaxis_title="Score de Sentimento",
            yaxis_title="Frequência",
            title_font_size=18,
            height=400,
        )

        fig.add_vline(
            x=-0.1,
            line_dash="dash",
            line_color="red",
            annotation_text="Limite Negativo",
        )
        fig.add_vline(
            x=0.1,
            line_dash="dash",
            line_color="green",
            annotation_text="Limite Positivo",
        )

        return fig

    @staticmethod
    def create_top_words_chart(df, sentiment_type="positivo", top_n=10):
        df_sentiment = df[df["sentiment_class"] == sentiment_type]

        if len(df_sentiment) == 0:
            return None

        all_text = " ".join(df_sentiment["full_text_clean"].dropna())
        words = all_text.split()

        words = [w for w in words if len(w) > 3]

        word_freq = Counter(words).most_common(top_n)

        if not word_freq:
            return None

        words_list, counts_list = zip(*word_freq)

        color = (
            "#2ecc71"
            if sentiment_type == "positivo"
            else "#e74c3c"
            if sentiment_type == "negativo"
            else "#95a5a6"
        )

        fig = px.bar(
            x=counts_list,
            y=words_list,
            orientation="h",
            title=f"Top {top_n} Palavras - Notícias {sentiment_type.title()}",
            color_discrete_sequence=[color],
        )

        fig.update_layout(
            xaxis_title="Frequência",
            yaxis_title="Palavras",
            title_font_size=16,
            height=400,
            yaxis={"categoryorder": "total ascending"},
        )

        return fig
