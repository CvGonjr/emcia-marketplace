# 038 — Manual de aplicação conferido contra o playbook

> Atualização de 04/10/2026: a decisão 044 supera as declarações de aprovação pendente deste registro histórico. A linha de base vigente metodo-v1.0 foi aprovada por Celso do Vale no APR-01. Os commits e estados descritos abaixo permanecem como evidência histórica.

**Data:** 01/10/2026 · **Estado:** firme por instrução do usuário

## Contexto

O Guia do Engenheiro de Campo anterior envelheceu sem que a suíte conferisse sua correspondência com o playbook. Um guia desatualizado pode indicar etapas, camadas, comandos ou atos humanos diferentes dos que o Estúdio aplica.

## Decisão

O EMCIA-MAN-01 é empacotado no plugin de campo, com versão e hash no manifesto do método. `testes/manual_a25.py` confere a tabela da seção 3.3 e os atos transversais da seção 3.4 contra o playbook e os comandos de etapa existentes.

## Consequência

Mudar o playbook ou um comando de etapa sem atualizar o manual quebra a suíte. A entrada de MAN-01 no pacote amplia de 16 para 17 a lista de documentos esperados em `testes/metodo_empacotado.py`. O manual passa a ser a entrada para quem aplica o método, sem alterar a execução dos plugins nem atualizar o playbook de casos existentes.

## Emenda de 03/10/2026 — manual operacional v0.2

Por instrução do engenheiro, o MAN-01 passa a acompanhar a versão operacional
do Estúdio. O pacote é extraído do commit canônico
`1d6d1e8bfc1739594ea7a119257ecae28c8e5af4`, com MAN-01 v0.2 e playbook 0.4.18.
O A25 exige conferir() vazio diretamente para o manual empacotado; a emenda
local da decisão 041 é retirada. Os quatro testes negativos mantêm seu
comportamento. A v0.1 conferida na ação 4.5 permanece recuperável pelo commit
canônico `968281c`. O texto original acima é preservado como registro histórico.
A revisão canônica permanece Em revisão, com aprovação pendente; empacotamento
não lhe atribui aprovação.
