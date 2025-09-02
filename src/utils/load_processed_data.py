import streamlit as st
import pandas as pd
import json
import os


@st.cache_data
def load_processed_data():
    """
    Converte os dados processados de csv para json, pegando o mais atual
    """
    processed_dir = "data/processed"

    if not os.path.exists(processed_dir):
        return None, None

    csv_files = [
        f
        for f in os.listdir(processed_dir)
        if f.startswith("news_analyzed_") and f.endswith(".csv")
    ]

    if not csv_files:
        return None, None

    csv_files.sort(reverse=True)
    latest_csv = os.path.join(processed_dir, csv_files[0])

    df = pd.read_csv(latest_csv)

    summary_file = latest_csv.replace("news_analyzed_", "summary_").replace(
        ".csv", ".json"
    )
    summary = None
    if os.path.exists(summary_file):
        with open(summary_file, "r", encoding="utf-8") as f:
            summary = json.load(f)

    return df, summary
