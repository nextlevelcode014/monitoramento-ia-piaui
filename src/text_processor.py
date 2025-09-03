import re
import pandas as pd
from bs4 import BeautifulSoup
import html


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

    def clean_html(self, text):
        if not text:
            return ""

        text = html.unescape(text)

        text = re.sub(r"<.*?>", "", text)
        text = text.replace("&nbsp;", " ")
        text = re.sub(r"\s+", " ", text)
        soup = BeautifulSoup(text, "html.parser")

        return soup.get_text()

    def clean_special_characters(self, text):
        if not text:
            return ""

        text = text.lower()
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
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

        text = self.clean_html(text)
        text = self.clean_special_characters(text)
        text = self.remove_stopwords(text)
        return text

    def process_news_dataframe(self, df):
        df_processed = df.copy()

        df_processed["description"] = df_processed["description"].apply(self.clean_html)

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


# --- Demonstração com o seu exemplo ---
if __name__ == "__main__":
    processor = TextProcessor()

    problem_html = (
        '<a href="https://news.google.com/..." target="_blank">'
        "Piauí Instituto de Tecnologia (PIT) destina 25% das vagas exclusivamente para mulheres em cursos de IA"
        '</a>&nbsp;&nbsp;<font color="#6f6f6f">Assembleia Legislativa do Piauí</font>'
    )

    print(f"Texto Original com HTML:\n{problem_html}\n")

    cleaned_text = processor.process_text(problem_html)

    print(f"Resultado Final Limpo:\n{cleaned_text}")

    print("\n--- Exemplo com DataFrame ---\n")

    data = {"title": ["Notícia de IA no Piauí"], "description": [problem_html]}
    news_df = pd.DataFrame(data)

    processed_df = processor.process_news_dataframe(news_df)
    print(
        processed_df[
            ["title_clean", "description_clean", "full_text_clean", "word_count"]
        ].to_string()
    )
