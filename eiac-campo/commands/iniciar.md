---
description: Conduz a habilitação simplificada até F0 liberado, com formulário permanente, dois depósitos e três confirmações registradas.
---
Uso: `/eiac-campo:iniciar [id-da-habilitacao] [id-do-caso]`

Carregue somente `reference/cartao-habilitacao.md` para o percurso normal.
Execute `scripts/iniciar.py proximo --entrada <json-local>` uma vez por avanço;
apresente resumo, próximo passo, os artefatos para conferir e os hashes pertinentes.
Não carregue referências completas a cada retomada nem apresente JSON do expediente.

Quando faltar preparação ou houver recusa, abra somente a referência necessária:
`reference/habilitacao.md` para entradas/alternativa manual, `reference/canais.md`
para inventário/perfil/conferência dos formulários e P2. Configuração, aceitação ou
ratificação jurídica e conferência do formulário são preparação reutilizável.
O inventário fornecido é a única fonte de ferramentas/parâmetros. Não execute
API ampla de submissões; não envie mensagens por ferramentas sem autorização.

O engenheiro envia o link, deposita o CSV e depois os PDFs assinados em
`~/emcia-op/entrada/`, cola esclarecimentos e confirma os três conjuntos apresentados.
Capture o trecho real e a indicação explícita de aprovação; não deduza aprovação
de silêncio, timeout ou resposta negativa. Registre a matriz numa mensagem.
Nenhuma linha de outro caso pode ser copiada para entrada de script, fonte,
rascunho ou saída da sessão; use somente o filtrado produzido pelo script.

A decisão 047 emenda a 045. APR-01 rege os três templates separados por hash;
o pacote do método não é editado. Drive só em P2, com aprovação de criação e
compartilhamento. Métodos e decisões continuam no terminal, sem migração de
playbook de caso existente. Retorno de conector interrompido exige conferir o
objeto remoto por id antes de repetir a chamada; script não executa APIs.
