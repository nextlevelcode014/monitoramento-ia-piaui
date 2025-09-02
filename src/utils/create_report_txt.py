from datetime import datetime


def create_report_text(stats):
    if not stats:
        return "Erro: Não foi possível gerar estatísticas."

    report = f"""
# RELATÓRIO DE MONITORAMENTO - IA NO PIAUÍ
**Gerado em:** {datetime.now().strftime("%d/%m/%Y às %H:%M")}

## RESUMO EXECUTIVO

Este relatório analisa **{stats["total_news"]} notícias** sobre Inteligência Artificial no estado do Piauí, 
coletadas entre {stats["date_range"]["start"]} e {stats["date_range"]["end"]}.

### PRINCIPAIS DESCOBERTAS:

- **Sentimento Geral:** Score médio de **{stats["average_score"]}** (escala -1 a +1)
- **Distribuição:** {stats["sentiment_percentages"].get("positivo", 0)}% positivas, {stats["sentiment_percentages"].get("negativo", 0)}% negativas, {stats["sentiment_percentages"].get("neutro", 0)}% neutras
- **Fontes Analisadas:** {stats["sources"]["total_sources"]} veículos de comunicação diferentes

## ANÁLISE DETALHADA

### Distribuição de Sentimentos:
"""

    for sentiment, count in stats["sentiment_distribution"].items():
        percentage = stats["sentiment_percentages"][sentiment]
        report += f"- **{sentiment.title()}:** {count} notícias ({percentage}%)\n"

    report += f"""
### Estatísticas de Score:
- **Mínimo:** {stats["score_stats"]["min"]}
- **Máximo:** {stats["score_stats"]["max"]}
- **Desvio Padrão:** {stats["score_stats"]["std"]}

### Top 5 Fontes de Notícias:
"""

    for source, count in stats["sources"]["top_sources"].items():
        report += f"- **{source}:** {count} notícias\n"

    report += f"""
### Análise de Palavras:
- **Média de palavras positivas por notícia:** {stats["word_analysis"]["avg_positive_words"]}
- **Média de palavras negativas por notícia:** {stats["word_analysis"]["avg_negative_words"]}

## DESTAQUES

### Notícia Mais Positiva:
**Título:** {stats["highlights"]["most_positive"]["title"]}
**Score:** {stats["highlights"]["most_positive"]["score"]}
**Fonte:** {stats["highlights"]["most_positive"]["source"]}

### Notícia Mais Negativa:
**Título:** {stats["highlights"]["most_negative"]["title"]}
**Score:** {stats["highlights"]["most_negative"]["score"]}
**Fonte:** {stats["highlights"]["most_negative"]["source"]}

## ANÁLISE POR FONTE

| Fonte | Score Médio | Qtd. Notícias |
|-------|-------------|---------------|"""

    for source in stats["source_analysis"]["mean"].keys():
        mean_score = stats["source_analysis"]["mean"][source]
        count = stats["source_analysis"]["count"][source]
        report += f"\n| {source} | {mean_score} | {count} |"

    report += f"""

## LIMITAÇÕES E METODOLOGIA

### Metodologia Utilizada:
- **Coleta:** Feed RSS do Google News
- **Processamento:** Limpeza de texto e remoção de stopwords
- **Análise:** Sistema baseado em regras com {len(["positivo", "negativo", "neutro"])} categorias
- **Score:** Escala de -1 (muito negativo) a +1 (muito positivo)

### Limitações Reconhecidas:
- Análise baseada em regras simples, não Machine Learning
- Não detecta sarcasmo, ironia ou contextos complexos
- Limitado às fontes indexadas pelo Google News
- Vocabulário de palavras-chave pode não cobrir todos os nuances

### Recomendações:
1. **Monitoramento Contínuo:** Atualizar dados semanalmente
2. **Expansão de Fontes:** Incluir redes sociais e blogs especializados
3. **Melhoria da Análise:** Considerar implementar modelos de ML no futuro
4. **Contextualização:** Cruzar dados com eventos locais e políticas públicas

## CONTATO

Para dúvidas sobre este relatório ou solicitação de análises customizadas, 
entre em contato com a equipe de monitoramento.

---
*Relatório gerado automaticamente pelo Sistema de Monitoramento de IA - Piauí*
"""

    return report
