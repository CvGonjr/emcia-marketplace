# 038 — Manual de aplicação conferido contra o playbook

**Data:** 01/10/2026 · **Estado:** firme por instrução do usuário

## Contexto

O Guia do Engenheiro de Campo anterior envelheceu sem que a suíte conferisse sua correspondência com o playbook. Um guia desatualizado pode indicar etapas, camadas, comandos ou atos humanos diferentes dos que o Estúdio aplica.

## Decisão

O EMCIA-MAN-01 é empacotado no plugin de campo, com versão e hash no manifesto do método. `testes/manual_a25.py` confere a tabela da seção 3.3 e os atos transversais da seção 3.4 contra o playbook e os comandos de etapa existentes.

## Consequência

Mudar o playbook ou um comando de etapa sem atualizar o manual quebra a suíte. A entrada de MAN-01 no pacote amplia de 16 para 17 a lista de documentos esperados em `testes/metodo_empacotado.py`. O manual passa a ser a entrada para quem aplica o método, sem alterar a execução dos plugins nem atualizar o playbook de casos existentes.
