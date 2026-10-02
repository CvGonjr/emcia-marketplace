# Complemento das verificações finais

A execução integral em `saida-suite.txt` aprovou 889 verificações em 44
módulos. Depois foram acrescentados dois controles de canais (autoria fixa
e documentação da fronteira) e três verificações de importação (workspace
alheio, ausência de canais e migração com vínculo). As suítes foram
reexecutadas por pacote: canais passou de 17 para 19 e habilitacao_0d de
31 para 34. As saídas estão em `../pacote-E1/saida-suite.txt` e
`../pacote-E2/saida-suite.txt`. Total distinto final: 894 verificações em
44 módulos, todas aprovadas.

Cada commit também foi preparado como árvore Git isolada, inicializada com
histórico sintético para os testes que o exigem, e validado antes de commitar.
As saídas desses testes ficam em `../pacote-E*/arvore-isolada.txt`.
Nenhum teste negativo anterior foi removido ou dispensado. Fixtures declaram
canais sintéticos e, para o controle documental, fazem o recebimento real.
