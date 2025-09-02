# DECISIONS.md

Documento explicativo sobre **como pensei, quais caminhos considerei e por que escolhi determinada solução**.

---

## 1. Coleta de Dados
- **Pensamento inicial**: 
  - Possíveis problemas com dependencias indiretas diferentes.
  - Requisições com queries semelhantes poderiam retornar notícias repetidas.
  - Chance de `403 Forbidden` ao acessar o feed RSS.
  - Mensagens de commits simples e padronizadas.
- **Decisão tomada**:  
  - Optei por usar o **uv** ao invés do **pip** como package manager, para evitar conflito de dependências.
  - Implementei um filtrar de noticias repetidas por link.
  - Evitar possíveis erros nas requisições, adicionei um **User-Agent** para simular a requisição de um navegador.
  - Vou separar os commits por etapas do projeto, seguindo a estrutura descrita no arquivo `CRONOGRAMA.md`.
- **Por que escolhi isso**:  
  - Rápido, fácil de usar, melhora o trabalho em equipe, multiplataforma, entre outros beneficios.
  - Prevenir a duplicação de noticies, assim deixando os processo de análise dos dados mais precisos.
  - Prevenção simples para potenciais erros.
  - Mensagens tem correlação direta com a proposta do case, melhor auditoria.

## 2: Processamento e Análise
- Pensamento inicial
  - Agrupar palavras que demonstram sentimentos e eliminar palavras e caracteres inúteis.
  - Para melhorar a precisão dos cálculos, acredito que será útil adicionar identificadores.
  - Salvar os dados brutos por data, para poder saber quais são os mais recentes e aplicar uma lógica posteriormente.
  - Calcular as palavras mais frequentes para criar uma nuvem de palavras.
  - Normalizar a pontuação das palavras, de modo a tender para positivo ou negativo.
- Decisão tomada.
  - Pesquisar ou pedir a uma IA várias palavras que demonstrem sentimentos ou intensidade e, depois, usá-las para medir as notícias.
  - Multiplicar a palavra de intensidade por `0.5`, aumentando **50%** a cada intensificador.
  - Prefixo para nomes de arquivos processados com timestamp.
  - Usar o `Counter` para calcular as palavras frequentes.
  - Subtrair as negativas das positivas e, depois, dividir pelo número de palavras (`(positivos - negativos) / número de palavras`).
- Por que escolhi isto?
  - É mais prático do que tentar lembrar de várias palavras.
  - As frases do tipo "bom" ou "muito bom" podem ser melhor calculadas.
  - Com timestamp no nome dos arquivos, posso fazer uma atualização em tempo real e obter os mais recentes por data.
  - O `Counter` mostra quantas vezes um elemento apareceu sem ser necessário escrever um loop.
  - É a melhor forma de calcular o `core`, por isso, optei por restringir entre -1.0 e 1.0.

