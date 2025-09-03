# Monitoramento de Percepção Pública sobre IA no Piauí

Sistema automatizado para coletar, processar e analisar notícias sobre Inteligência Artificial no estado do Piauí, utilizando análise de sentimento e visualizações interativas.

## Objetivo

Criar um painel simplificado para monitorar menções sobre "Inteligência Artificial no Piauí" em fontes de notícias públicas, com foco em análise de sentimento e identificação de temas recorrentes.

## Arquitetura do Projeto

```bash
    monitoramento-ia-piaui/
    ├── app.py # Dashboard principal (Streamlit)
    ├── SCHEDULE.md 
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
---

## **Instalação e Configuração**

### **Pré-requisitos**
- Python 3.8+  
- Git  
- Conexão com internet (para coleta RSS)  
- pip ou uv (recomendado)
---

### **Passo a Passo**

#### **Clone o repositório**
```bash
git clone https://github.com/nextlevelcode014/monitoramento-ia-piaui.git
cd monitoramento-ia-piaui
```

#### **Crie e ative o ambiente virtual**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### **Instale as dependências**
```bash
pip install -r requirements.txt
```

---

### **Execução dos scripts**

#### **Coleta inicial de dados**
```bash
# Usando Python diretamente
python -m src.data_collector

# Usando uv
uv run -m src.data_collector
```

#### **Processamento dos dados coletados**
```bash
# Usando Python diretamente
python -m src.data_pipeline

# Usando uv
uv run -m src.data_pipeline
```

#### **Iniciar o dashboard**
```bash
# Usando Streamlit diretamente
streamlit run app.py

# Usando uv
uv run streamlit run app.py
```

#### **Acesse no navegador**
```bash
http://localhost:8501
```

---

### **Como Usar**

#### **Atualização Automática (Recomendado)**
```bash
# Usando Python
python -m run_scripts.quick_update

# Usando uv
uv run -m run_scripts.quick_update
```
> Executa coleta → processamento → dashboard em sequência  

#### **Apenas Dashboard**
```bash
streamlit run app.py

uv run streamlit run app.py
```

#### **Modo Desenvolvimento**
```bash
python -m run_scripts.dev_dashboard

uv run -m run_scripts.dev_dashboard
```

## Testes rapídos
```bash
# Usando python
python -m tests.test_endpoint 
python -m tests.test_collector
python -m tests.test_processing

# Usando uv
uv run -m tests.test_endpoint 
uv run -m tests.test_collector
uv run -m tests.test_processing
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

## Mais informações
**Sobre o objetivo do projeto leia:** [ABOUT.md](ABOUT.md)
**Cronograma e estrutura dos commits:** [SSCHEDULE.md](SCHEDULE.md)
