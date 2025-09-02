import pandas as pd


class SentimentAnalyzer:
    def __init__(self):
        # fmt: off
        self.positive_words = {
            'inovação', 'inovador', 'inovadora', 'revolucionário', 'revolucionária',
            'avanço', 'progresso', 'desenvolvimento', 'crescimento', 'sucesso',
            'excelente', 'ótimo', 'bom', 'boa', 'positivo', 'positiva',
            'eficiente', 'eficaz', 'inteligente', 'moderno', 'moderna',
            'futuro', 'oportunidade', 'benefício', 'vantagem', 'solução',
            'melhoria', 'otimização', 'automatização', 'facilitação',
            'transformação', 'evolução', 'pioneiro', 'pioneira', 'líder',
            'competitivo', 'competitiva', 'promissor', 'promissora',
            'qualidade', 'precisão', 'rapidez', 'eficiência', 'produtividade'
        }

        self.negative_words = {
            'problema', 'risco', 'perigo', 'ameaça', 'preocupação',
            'dificuldade', 'desafio', 'obstáculo', 'limitação', 'erro',
            'falha', 'ruim', 'péssimo', 'péssima', 'negativo', 'negativa',
            'desemprego', 'substituição', 'eliminação', 'redução',
            'custo', 'caro', 'cara', 'complexo', 'complicado', 'complicada',
            'invasão', 'privacidade', 'segurança', 'vulnerabilidade',
            'bias', 'viés', 'discriminação', 'exclusão', 'dependência',
            'controle', 'manipulação', 'ética', 'responsabilidade',
            'transparência', 'accountability', 'regulamentação'
        }

        self.intensifiers = {
            'muito', 'bastante', 'extremamente', 'super', 'altamente',
            'completamente', 'totalmente', 'absolutamente', 'definitivamente'
        }
        # fml: on

    def count_sentiment_words(self, text):
        if not text:
            return {"positive": 0, "negative": 0, "intensifiers": 0}

        words = text.lower().split()

        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        intensifier_count = sum(1 for word in words if word in self.intensifiers)

        return {
            "positive": positive_count,
            "negative": negative_count,
            "intensifiers": intensifier_count,
        }

    def calculate_sentiment_score(self, text):
        if not text:
            return 0.0

        counts = self.count_sentiment_words(text)
        total_words = len(text.split())

        if total_words == 0:
            return 0.0

        positive_score = counts["positive"]
        negative_score = counts["negative"]

        if counts["intensifiers"] > 0:
            intensifier_multiplier = 1 + (counts["intensifiers"] * 0.5)
            positive_score *= intensifier_multiplier
            negative_score *= intensifier_multiplier

        raw_score = (positive_score - negative_score) / total_words

        normalized_score = max(-1, min(1, raw_score * 10))

        return round(normalized_score, 3)

    def classify_sentiment(self, score):
        if score > 0.1:
            return "positivo"
        elif score < -0.1:
            return "negativo"
        else:
            return "neutro"

    def analyze_text(self, text):
        score = self.calculate_sentiment_score(text)
        classification = self.classify_sentiment(score)
        counts = self.count_sentiment_words(text)

        return {
            "sentiment_score": score,
            "sentiment_class": classification,
            "positive_words_count": counts["positive"],
            "negative_words_count": counts["negative"],
            "intensifiers_count": counts["intensifiers"],
        }

    def analyze_dataframe(self, df, text_column="full_text_clean"):
        df_analyzed = df.copy()

        sentiment_results = df_analyzed[text_column].apply(self.analyze_text)

        sentiment_df = pd.json_normalize(sentiment_results)

        for col in sentiment_df.columns:
            df_analyzed[col] = sentiment_df[col]

        return df_analyzed

    def get_sentiment_summary(self, df):
        if "sentiment_class" not in df.columns:
            return "DataFrame não contém análise de sentimento"

        sentiment_counts = df["sentiment_class"].value_counts()
        total = len(df)

        summary = {
            "total_news": total,
            "sentiment_distribution": sentiment_counts.to_dict(),
            "sentiment_percentages": (sentiment_counts / total * 100)
            .round(1)
            .to_dict(),
            "average_score": df["sentiment_score"].mean().round(3),
            "most_positive": df.loc[df["sentiment_score"].idxmax()]["title"]
            if total > 0
            else None,
            "most_negative": df.loc[df["sentiment_score"].idxmin()]["title"]
            if total > 0
            else None,
        }

        return summary


if __name__ == "__main__":
    analyzer = SentimentAnalyzer()

    test_texts = [
        "A inteligência artificial está revolucionando o Piauí com inovações incríveis!",
        "IA pode causar desemprego e riscos para a privacidade dos dados",
        "Universidade no Piauí desenvolve projeto de inteligência artificial",
    ]

    print("Testando Análise de Sentimento:\n")
    for text in test_texts:
        result = analyzer.analyze_text(text)
        print(f"Texto: {text}")
        print(
            f"Score: {result['sentiment_score']} | Classe: {result['sentiment_class']}"
        )
        print(
            f"Palavras +: {result['positive_words_count']} | Palavras -: {result['negative_words_count']}\n"
        )
