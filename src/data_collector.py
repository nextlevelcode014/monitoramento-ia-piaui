import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import os


class RSSCollector:
    def __init__(self):
        self.base_url = "https://news.google.com/rss/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def build_search_url(self, query, language="pt-BR", country="BR"):
        params = {
            "q": query,
            "hl": language,
            "gl": country,
            "ceid": f"{country}:{language.split('-')[0]}-419",
        }

        url = f"{self.base_url}?"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    def fetch_rss_feed(self, search_query):
        try:
            url = self.build_search_url(search_query)
            print(f"Buscando: {url}")

            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            print(f"Status: {response.status_code}")
            return response.text

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None

    def parse_xml_feed(self, xml_content):
        try:
            root = ET.fromstring(xml_content)

            items = root.findall(".//item")

            news_data = []

            for item in items:
                title = item.find("title")
                link = item.find("link")
                description = item.find("description")
                pub_date = item.find("pubDate")
                source = item.find("source")

                news_item = {
                    "title": title.text if title is not None else "Sem título",
                    "link": link.text if link is not None else "",
                    "description": description.text
                    if description is not None
                    else "Sem descrição",
                    "pub_date": pub_date.text if pub_date is not None else "",
                    "source": source.text
                    if source is not None
                    else "Fonte desconhecida",
                    "collected_at": datetime.now().isoformat(),
                }

                news_data.append(news_item)

            print(f"Coletadas {len(news_data)} notícias")
            return news_data

        except ET.ParseError as e:
            print(f"Erro ao processar XML: {e}")
            return []

    def collect_news(self, search_queries, max_news=15):
        all_news = []

        for query in search_queries:
            print(f"\n--- Coletando para: {query} ---")

            xml_content = self.fetch_rss_feed(query)

            if xml_content:
                news_items = self.parse_xml_feed(xml_content)

                for item in news_items:
                    item["search_query"] = query

                all_news.extend(news_items)

        unique_news = []
        seen_links = set()

        for news in all_news:
            if news["link"] not in seen_links:
                unique_news.append(news)
                seen_links.add(news["link"])

        return unique_news[:max_news]

    def save_raw_data(self, news_data, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_raw_{timestamp}.json"

        filepath = os.path.join("data", "raw", filename)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)

        print(f"Dados salvos em: {filepath}")
        return filepath


if __name__ == "__main__":
    collector = RSSCollector()

    search_queries = [
        "Inteligência Artificial Piauí",
        "IA Piauí",
        "SIA Piauí",
        "Inteligência Artificial Teresina",
    ]

    print(collector.build_search_url(search_queries))

    # news_data = collector.collect_news(search_queries, max_news=15)

    # if news_data:
    # filepath = collector.save_raw_data(news_data)
    # print(f"\nColetadas {len(news_data)} notícias únicas")
    # else:
    # print("Nenhuma notícia foi coletada")
