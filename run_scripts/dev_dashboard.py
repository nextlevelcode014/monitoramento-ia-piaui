import subprocess
import sys
import os


def create_sample_data():
    import pandas as pd
    import json
    from datetime import datetime, timedelta

    sample_news = [
        {
            "title": "Universidade Federal do Piauí lança curso de IA",
            "description": "Nova graduação em inteligência artificial promete formar profissionais qualificados",
            "source": "Portal da UFPI",
            "sentiment_class": "positivo",
            "sentiment_score": 0.45,
            "positive_words_count": 3,
            "negative_words_count": 0,
            "full_text_clean": "universidade federal piauí lança curso inteligência artificial nova graduação promete formar profissionais qualificados",
            "pub_date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "link": "https://ufpi.br/exemplo",
        },
        {
            "title": "Empresas do Piauí adotam automação com IA",
            "description": "Setor empresarial investe em tecnologia para otimizar processos",
            "source": "Jornal O Dia",
            "sentiment_class": "positivo",
            "sentiment_score": 0.32,
            "positive_words_count": 2,
            "negative_words_count": 0,
            "full_text_clean": "empresas piauí adotam automação inteligência artificial setor empresarial investe tecnologia otimizar processos",
            "pub_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "link": "https://odia.com/exemplo",
        },
        {
            "title": "Debates sobre regulamentação de IA crescem no estado",
            "description": "Especialistas discutem necessidade de marcos regulatórios",
            "source": "G1 Piauí",
            "sentiment_class": "neutro",
            "sentiment_score": 0.05,
            "positive_words_count": 1,
            "negative_words_count": 1,
            "full_text_clean": "debates regulamentação inteligência artificial crescem estado especialistas discutem necessidade marcos regulatórios",
            "pub_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "link": "https://g1.globo.com/exemplo",
        },
        {
            "title": "Preocupações com privacidade em sistemas de IA",
            "description": "Cidadãos expressam receios sobre coleta de dados pessoais",
            "source": "Meio Norte",
            "sentiment_class": "negativo",
            "sentiment_score": -0.28,
            "positive_words_count": 0,
            "negative_words_count": 2,
            "full_text_clean": "preocupações privacidade sistemas inteligência artificial cidadãos expressam receios coleta dados pessoais",
            "pub_date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
            "link": "https://meionorte.com/exemplo",
        },
    ]

    df = pd.DataFrame(sample_news)

    os.makedirs("data/processed", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"data/processed/news_analyzed_{timestamp}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")

    summary = {
        "total_news": len(df),
        "sentiment_distribution": df["sentiment_class"].value_counts().to_dict(),
        "sentiment_percentages": (df["sentiment_class"].value_counts() / len(df) * 100)
        .round(1)
        .to_dict(),
        "average_score": df["sentiment_score"].mean().round(3),
    }

    summary_path = f"data/processed/summary_{timestamp}.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("Dados de exemplo criados:")
    print(f"   CSV: {csv_path}")
    print(f"   Resumo: {summary_path}")


def run_dev_dashboard():
    if not os.path.exists("data/processed") or not os.listdir("data/processed"):
        print("Criando dados de exemplo para teste...")
        create_sample_data()

    print("🚀 Iniciando dashboard em modo desenvolvimento...")
    print("🌐 URL: http://localhost:8501")
    print("🔄 Hot reload ativado - modificações serão atualizadas automaticamente")
    print("🛑 Para parar: Ctrl+C")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.runOnSave=true",
            "--server.headless=false",
        ]
    )


if __name__ == "__main__":
    run_dev_dashboard()
