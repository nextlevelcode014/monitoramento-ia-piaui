from src.data_collector import RSSCollector
from src.data_pipeline import DataPipeline
import subprocess
import sys


def update_and_run():
    print("Atualizando dados...")

    print("1. Coletando notícias...")
    collector = RSSCollector()
    search_queries = [
        "Inteligência Artificial Piauí",
        "IA Piauí",
        "SIA Piauí",
        "Inteligência Artificial Teresina",
    ]

    news_data = collector.collect_news(search_queries, max_news=15)

    if news_data:
        collector.save_raw_data(news_data)
        print(f"   {len(news_data)} notícias coletadas")
    else:
        print("   Nenhuma notícia nova coletada")

    print("2. Processando e analisando...")
    pipeline = DataPipeline()
    df_final, summary = pipeline.process_complete_pipeline()
    print(f"   {len(df_final)} notícias processadas")

    print("3. Abrindo dashboard...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])


if __name__ == "__main__":
    update_and_run()
