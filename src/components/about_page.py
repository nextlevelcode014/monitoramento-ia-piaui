import streamlit as st


def about_page():
    st.title("Sobre o Projeto")

    st.markdown("""
    ## Objetivo
    Este projeto monitora a percepção pública sobre Inteligência Artificial no estado do Piauí 
    através da análise de notícias coletadas do Google News.
    
    ## Metodologia
    1. **Coleta de Dados**: Feed RSS do Google News com palavras-chave específicas
    2. **Processamento**: Limpeza de textos e remoção de stopwords  
    3. **Análise de Sentimento**: Sistema baseado em regras com palavras-chave
    4. **Visualização**: Dashboard interativo com múltiplas perspectivas
    
    ## Métricas Utilizadas
    - **Score de Sentimento**: Valor de -1 (muito negativo) a +1 (muito positivo)
    - **Classificação**: Positivo (>0.1), Negativo (<-0.1), Neutro (-0.1 a 0.1)
    - **Frequência de Palavras**: Análise dos termos mais comuns por categoria
    
    ## Tecnologias
    - **Python**: Linguagem principal
    - **Streamlit**: Interface web interativa
    - **Plotly**: Gráficos interativos
    - **Pandas**: Manipulação de dados
    - **WordCloud**: Nuvem de palavras
    
    ## Limitações Reconhecidas
    - Análise baseada em regras simples
    - Não detecta sarcasmo ou ironia
    - Limitado às fontes do Google News
    - Dependente da qualidade das palavras-chave definidas
    
    ## Arquitetura do Projeto
    ```
    monitoramento-ia-piaui/
    ├── app.py                 # Dashboard principal (ESTE ARQUIVO)
    ├── src/
    │   ├── data_collector.py  # Coleta RSS
    │   ├── text_processor.py  # Limpeza de textos
    │   ├── sentiment_analyzer.py # Análise de sentimento
    │   ├── data_pipeline.py   # Pipeline completo
    │   └── dashboard_components.py # Componentes do dashboard
    ├── data/
    │   ├── raw/              # Dados brutos (JSON)
    │   └── processed/        # Dados processados (CSV)
    └── docs/                 # Documentação
    ```
    
    ## Desenvolvimento
    Projeto desenvolvido como case técnico para demonstrar habilidades em:
    - Coleta e processamento de dados
    - Análise de sentimento
    - Visualização interativa
    - Boas práticas de desenvolvimento
    """)
