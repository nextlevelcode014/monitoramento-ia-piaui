from src.data_collector import RSSCollector


def test_rss_collection():
    collector = RSSCollector()

    xml_content = collector.fetch_rss_feed("Inteligência Artificial Piauí")

    if xml_content:
        print("Requisição RSS funcionando!")
        print(f"Tamanho do conteúdo: {len(xml_content)} caracteres")

        news_data = collector.parse_xml_feed(xml_content)
        if news_data:
            print(f"Parsing XML funcionando! {len(news_data)} notícias encontradas")
            print("\nPrimeira notícia:")
            print(f"Título: {news_data[0]['title']}")
            print(f"Fonte: {news_data[0]['source']}")
        else:
            print("Nenhuma notícia encontrada no XML")
    else:
        print("Erro na requisição RSS")


if __name__ == "__main__":
    test_rss_collection()
