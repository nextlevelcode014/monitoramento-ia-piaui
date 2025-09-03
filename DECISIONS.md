# DECISIONS.md

Documento explicativo sobre **como pensei, quais caminhos considerei e por que escolhi determinada solução**.

---

## Etapa 1: Coleta de Dados
- **Pensamento inicial**  
  - Usar o **Google News RSS** como principal fonte de dados.  
  - Possíveis problemas com dependências indiretas diferentes.  
  - Requisições com queries semelhantes poderiam retornar notícias repetidas.  
  - Risco de `403 Forbidden` ao acessar o feed RSS.  
  - Uso de mensagens de commit simples e padronizadas.  

- **Decisão tomada**  
  - Optei por usar apenas o **Google News RSS** pela simplicidade, formato estruturado e menor complexidade em relação a múltiplas fontes.  
  - Utilizar o **uv** como package manager no lugar do **pip**, para evitar conflitos de dependências.  
  - Implementar filtro para remoção de notícias repetidas (baseado no link).  
  - Adicionar um **User-Agent** para reduzir chances de bloqueio nas requisições.  
  - Organizar os commits por etapas, seguindo a estrutura definida em `SCHEDULE.md`.  

- **Por que escolhi isso**  
  - O RSS do Google News é rápido, padronizado e multiplataforma.  
  - Evitar duplicação melhora a precisão da análise de dados.  
  - O uso de `User-Agent` reduz falhas simples de rede.  
  - Estrutura de commits clara facilita a auditoria e o trabalho em equipe.  

## Etapa 2: Processamento e Análise
- **Pensamento inicial**  
  - Implementar análise de sentimento baseada em **regras (word counting)**, evitando dependência de modelos de Machine Learning.  
  - Agrupar palavras que representem sentimentos e remover termos irrelevantes.  
  - Salvar os dados brutos com referência de data para controle de atualizações.  
  - Calcular palavras mais frequentes para gerar nuvem de palavras.  
  - Normalizar a pontuação entre negativo e positivo.  

- **Decisão tomada**  
  - Criar lista de palavras associadas a sentimentos e intensificadores.  
  - Multiplicar palavras intensificadoras por `0.5`, aumentando em 50% a cada ocorrência.  
  - Salvar arquivos processados com **timestamp no prefixo**, para facilitar ordenação cronológica.  
  - Usar `collections.Counter` para medir frequência de palavras por categoria.  
  - Calcular o **sentiment score** com a fórmula:  
  $$
  \text{score} = \frac{(\text{positivos} - \text{negativos})}{\text{número de palavras}}
  $$
  - Restringir o escore ao intervalo entre **-1.0 e 1.0**.  

- **Por que escolhi isso**  
  - Método transparente, de baixo custo e fácil personalização.  
  - Intensificadores permitem captar nuances como “bom” vs. “muito bom”.  
  - Timestamps garantem acesso aos dados mais recentes em tempo real.  
  - O `Counter` simplifica a contagem sem necessidade de laços manuais.  
  - A fórmula escolhida é simples e mantém consistência estatística.  


## Etapa 3: Dashboard e Visualização
- **Pensamento inicial**  
  - Desenvolver o dashboard em **Streamlit** pela facilidade de integração.  
  - Exibir distribuição de sentimentos em **gráfico de pizza**.  
  - Implementar filtros para notícias e opção de download.  
  - Usar **WordCloud** para visualização das palavras mais frequentes.  
  - Exibir métricas principais logo na abertura.  
  - Implementar paginação para navegação entre notícias.  
  - Garantir tratamento de erros sem quebra da aplicação.  

- **Decisão tomada**  
  - Utilizar **Streamlit**, com suporte a cache, layout responsivo e navegação multipágina.  
  - Integrar `Plotly` para gráficos de pizza (sentimentos) e histograma (escore).  
  - Usar `WordCloud` junto ao `matplotlib` para gerar a nuvem de palavras.  
  - Disponibilizar opção de download dos dados já processados.  
  - Utilizar suporte de IA como auxílio em layout e estilização.  
  - Implementar tratamento de exceções personalizadas, como a função `safe_dataframe_display`, para evitar erros relacionados à **Arrow serialization**.  
  - Limpa o DataFrame para compatibilidade com Arrow/Streamlit

- **Por que escolhi isso**  
  - Integrações nativas com `Plotly` e `WordCloud` torna o processo mais escalavel.  
  - Tratamento de exceções melhora a robustez e experiência do usuário.  

## Etapa 4: Documentação e Finalização
- **Pontos finais**  
  - Pelo prazo de entrega usei AI para agilizar na documentação e revisão do código.
  - Documentação básica com estrutura do projeto e comandos uteis.
  - Arquitetura simples e sem muita padronização.
  - Resolvi adicionar o arquivo [ABOUT.md](ABOUT.md) sobre o objetivo do projeto.
  - Relatório de monitoramento por escrito para download e opção de baixa relatório, dados brutos e estatísticas.