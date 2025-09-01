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
- **O que deixei de lado**:  
  - Tenho que fazer um requiriment.txt, para pessoas que optam por usar o pip

