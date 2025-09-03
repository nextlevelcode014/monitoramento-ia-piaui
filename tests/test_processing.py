from src.text_processor import TextProcessor
from src.sentiment_analyzer import SentimentAnalyzer
import pandas as pd


def test_text_processing():
    print("TESTE 1: Processamento de Texto")
    print("=" * 50)

    processor = TextProcessor()

    test_cases = [
        "<p>A <b>IA</b> está mudando o Piauí!</p>",
        "   INTELIGÊNCIA ARTIFICIAL    revoluciona    educação   ",
        "Sistema de IA pode causar problemas sérios de privacidade...",
        "",
    ]

    for i, text in enumerate(test_cases, 1):
        cleaned = processor.process_text(text)
        print(f"{i}. Original: '{text}'")
        print(f"   Limpo: '{cleaned}'\n")


def test_sentiment_analysis():
    print("TESTE 2: Análise de Sentimento")
    print("=" * 50)

    analyzer = SentimentAnalyzer()

    test_cases = [
        "Excelente inovação em inteligência artificial revoluciona Piauí",
        "IA causa muito desemprego e sérios problemas de privacidade",
        "Universidade desenvolve projeto de inteligência artificial",
        "Sistema inteligente otimiza processos com eficiência incrível",
        "Riscos enormes da automação para trabalhadores",
    ]

    for i, text in enumerate(test_cases, 1):
        result = analyzer.analyze_text(text)
        print(f"{i}. Texto: '{text}'")
        print(
            f"   Score: {result['sentiment_score']} | Classe: {result['sentiment_class']}"
        )
        print(
            f"   Positivas: {result['positive_words_count']} | Negativas: {result['negative_words_count']}\n"
        )


def test_complete_pipeline():
    print("TESTE 3: Pipeline Completo")
    print("=" * 50)

    test_data = [
        {
            "title": "IA revoluciona educação no Piauí",
            "description": "Nova tecnologia de inteligência artificial está transformando o ensino",
            "link": "https://example.com/1",
            "source": "Portal de Notícias",
            "pub_date": "2024-03-01",
            "collected_at": "2024-03-01T10:00:00",
        },
        {
            "title": "Preocupações com IA no mercado de trabalho",
            "description": "Especialistas alertam sobre riscos do desemprego causado pela automação",
            "link": "https://example.com/2",
            "source": "Jornal Local",
            "pub_date": "2024-03-01",
            "collected_at": "2024-03-01T11:00:00",
        },
    ]

    df_test = pd.DataFrame(test_data)

    processor = TextProcessor()
    df_processed = processor.process_news_dataframe(df_test)

    analyzer = SentimentAnalyzer()
    df_final = analyzer.analyze_dataframe(df_processed)

    print("Pipeline testado com sucesso!")
    print(f"Colunas finais: {list(df_final.columns)}")
    print("\n Resultados:")
    for _, row in df_final.iterrows():
        print(f"• {row['title']} → {row['sentiment_class']} ({row['sentiment_score']})")


if __name__ == "__main__":
    test_text_processing()
    print("\n")
    test_sentiment_analysis()
    print("\n")
    test_complete_pipeline()
