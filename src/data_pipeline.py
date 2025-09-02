import json
import pandas as pd
import os
from datetime import datetime
from src.text_processor import TextProcessor
from src.sentiment_analyzer import SentimentAnalyzer
from collections import Counter


class DataPipeline:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.sentiment_analyzer = SentimentAnalyzer()

    def load_raw_data(self, filepath=None):
        if filepath is None:
            raw_dir = "data/raw"
            json_files = [f for f in os.listdir(raw_dir) if f.endswith(".json")]

            if not json_files:
                raise FileNotFoundError("Nenhum arquivo JSON encontrado em data/raw/")

            json_files.sort(
                key=lambda x: os.path.getmtime(os.path.join(raw_dir, x)), reverse=True
            )
            filepath = os.path.join(raw_dir, json_files[0])

        print(f"Carregando dados de: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return pd.DataFrame(data)

    def process_complete_pipeline(self, save_processed=True):
        print("Iniciando pipeline de processamento...\n")

        print("1. Carregando dados brutos...")
        df_raw = self.load_raw_data()
        print(f"   {len(df_raw)} notícias carregadas\n")

        print("2. Limpando e processando textos...")
        df_processed = self.text_processor.process_news_dataframe(df_raw)
        print("   Textos processados\n")

        print("3. Analisando sentimentos...")
        df_analyzed = self.sentiment_analyzer.analyze_dataframe(df_processed)
        print("   Análise de sentimento concluída\n")

        print("4. Gerando resumo estatístico...")
        summary = self.sentiment_analyzer.get_sentiment_summary(df_analyzed)
        print("   Resumo dos Sentimentos:")
        print(f"   • Total de notícias: {summary['total_news']}")
        print(f"   • Distribuição: {summary['sentiment_distribution']}")
        print(f"   • Percentuais: {summary['sentiment_percentages']}")
        print(f"   • Score médio: {summary['average_score']}\n")

        if save_processed:
            print("5. Salvando dados processados...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            csv_path = f"data/processed/news_analyzed_{timestamp}.csv"
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df_analyzed.to_csv(csv_path, index=False, encoding="utf-8")

            summary_path = f"data/processed/summary_{timestamp}.json"
            with open(summary_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)

            print(f"   Dados salvos em: {csv_path}")
            print(f"   Resumo salvo em: {summary_path}\n")

        return df_analyzed, summary

    def get_word_frequency(self, df, text_column="full_text_clean", top_n=50):
        all_text = " ".join(df[text_column].dropna())
        words = all_text.split()

        words = [word for word in words if len(word) > 3]

        word_freq = Counter(words)
        return dict(word_freq.most_common(top_n))


if __name__ == "__main__":
    pipeline = DataPipeline()

    try:
        df_final, summary = pipeline.process_complete_pipeline()

        print("Pipeline executado com sucesso!")
        print(
            f"DataFrame final tem {len(df_final)} linhas e {len(df_final.columns)} colunas"
        )

        print("\nColunas do DataFrame final:")
        for col in df_final.columns:
            print(f"   • {col}")

        if len(df_final) > 0:
            print("\nExemplo de notícia processada:")
            example = df_final.iloc[0]
            print(f"Título: {example['title']}")
            print(
                f"Sentimento: {example['sentiment_class']} (score: {example['sentiment_score']})"
            )
            print(f"Texto limpo: {example['full_text_clean'][:100]}...")

    except Exception as e:
        print(f"Erro no pipeline: {e}")
