import re
import pandas as pd
from bs4 import BeautifulSoup


class TextProcessor:
    def __init__(self):
        # fmt: off
        self.stopwords = {
            'a', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as',
            'até', 'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele', 'deles',
            'depois', 'do', 'dos', 'e', 'ela', 'elas', 'ele', 'eles', 'em', 'entre',
            'essa', 'essas', 'esse', 'esses', 'esta', 'estas', 'este', 'estes',
            'isto', 'na', 'nas', 'no', 'nos', 'nós', 'o', 'os', 'ou', 'para',
            'pela', 'pelas', 'pelo', 'pelos', 'que', 'se', 'seu', 'sua', 'suas',
            'seus', 'também', 'te', 'um', 'uma', 'umas', 'uns', 'você', 'vocês',
            'vos', 'à', 'às', 'é', 'foi', 'ser', 'ter', 'mais', 'muito', 'quando',
            'onde', 'por', 'sobre', 'mas', 'já', 'são', 'só', 'tem', 'vai', 'ainda'
        }
        # fmt: on

    def clean_html_tags(self, text):
        if not text:
            return ""

        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def clean_special_characters(self, text):
        if not text:
            return ""

        text = text.lower()

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"[^\w\s\-àáâãäéêëíîïóôõöúûüç]", " ", text)

        text = re.sub(r"\b\d+\b", "", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text

    def remove_stopwords(self, text):
        if not text:
            return ""

        words = text.split()
        filtered_words = [
            word for word in words if word not in self.stopwords and len(word) > 2
        ]

        return " ".join(filtered_words)

    def process_text(self, text):
        if not text:
            return ""

        text = self.clean_html_tags(text)

        text = self.clean_special_characters(text)

        text = self.remove_stopwords(text)

        return text

    def process_news_dataframe(self, df):
        df_processed = df.copy()

        df_processed["title_clean"] = df_processed["title"].apply(self.process_text)
        df_processed["description_clean"] = df_processed["description"].apply(
            self.process_text
        )

        df_processed["full_text_clean"] = (
            df_processed["title_clean"] + " " + df_processed["description_clean"]
        ).str.strip()

        df_processed["processed_at"] = pd.Timestamp.now()
        df_processed["word_count"] = (
            df_processed["full_text_clean"].str.split().str.len()
        )

        return df_processed


if __name__ == "__main__":
    processor = TextProcessor()

    test_text = (
        "<p>A <b>Inteligência Artificial</b> está revolucionando o Piauí! 🚀</p>"
    )
    cleaned = processor.process_text(test_text)
    print(f"Original: {test_text}")
    print(f"Limpo: {cleaned}")
