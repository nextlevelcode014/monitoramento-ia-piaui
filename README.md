# Monitoramento de Percepção Pública sobre IA no Piauí

Sistema automatizado para coletar, processar e analisar notícias sobre Inteligência Artificial no estado do Piauí, utilizando análise de sentimento e visualizações interativas.

## Objetivo

Criar um painel simplificado para monitorar menções sobre "Inteligência Artificial no Piauí" em fontes de notícias públicas, com foco em análise de sentimento e identificação de temas recorrentes.

## Arquitetura do Projeto

```bash
    monitoramento-ia-piaui/
    ├── app.py # Dashboard principal (Streamlit)
    ├── CRONOGRAMA.md 
    ├── DECISIONS.md # Por que?
    ├── requirements.txt 
    ├── README.md
    ├── pyproject.toml
    ├── data/ # Dados do sistema
    │   ├── raw/ # XML e JSON brutos do RSS
    │   └── processed/ # CSV e JSON processados
    ├── src/ # Módulos do sistema
    │   ├── components/ # Componentes visuais reutilizáveis
    │   │   ├── about_page.py
    │   │   ├── dashboard_components.py
    │   │   ├── dashboard_styles.py #  Estilos CSS customizados
    │   │   ├── main_dashboard.py
    │   │   └── report_modal.py
    │   ├── utils/ # Lógicas auxiliares
    │   │   ├── advanced_analysis.py
    │   │   ├── create_report_txt.py
    │   │   ├── generate_statistical_report.py
    │   │   ├── load_processed_data.py
    │   │   └── safe_dataframe_display.py
    │   ├── data_collector.py # Coleta de dados RSS
    │   ├── data_pipeline.py # Pipeline completo de processamento
    │   ├── sentiment_analyzer.py # Análise de sentimento por regras
    │   └── text_processor.py # Limpeza e processamento de textos
    ├── run_scripts/ # Scripts auxiliares
    │   ├── run_dashboard.py
    │   ├── run_dashboard.py
    │   └── quick_update.py
    └── tests/
        ├── test_collector.py
        ├── test_endpoint.py
        └── test_processing.py

```
## **Instalação e Configuração**

### **Pré-requisitos**
- Python 3.8+ 
- Git
- Conexão com internet (para coleta RSS)

### **Passo a Passo**

1. **Clone o repositório:**
```bash
    git clone https://github.com/nextlevelcode014/monitoramento-ia-piaui.git
    cd monitoramento-ia-piaui
```

1. **Crie e ative o ambiente virtual**
```bash
    # Criar ambiente virtual
    python -m venv venv

    # Ativar ambiente virtual
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
```

3. **Instale as dependências**
```bash
    pip install -r requirements.txt
```

4. **Execute a coleta inicial de dados**
```bash
    python src/data_collector.py
```

5. **Processe os dados coletados**
```bash
    python src/data_pipeline.py
```

6. **Inicie o dashboard**
```bash 
    streamlit run app.py
```

7. **Acesse no navegador**
```bash
    http://localhost:8501
```

## Como Usar
**Atualização Automática (Recomendado):**
```bash
    python quick_update.py
```
Executa coleta → processamento → dashboard em sequência

**Apenas Dashboard**
```bash
    streamlit run app.py
```

**Modo Desenvolvimento**
```bash
    python dev_dashboard.py
```

## Estrutura de Dados
**Dados Brutos (JSON):**
```json
    {
        "title": "string",
        "description": "string", 
        "link": "string",
        "source": "string",
        "pub_date": "string",
        "search_query": "string",
        "collected_at": "ISO datetime"
    }
```
**Dados Processados (CSV):**
```csv
    title, description, source, link, pub_date, 
    title_clean, description_clean, full_text_clean,
    sentiment_score, sentiment_class, positive_words_count, negative_words_count,
    processed_at, word_count
```