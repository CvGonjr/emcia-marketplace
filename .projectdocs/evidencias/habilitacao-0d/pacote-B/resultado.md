# Pacote B — evento com selo confirmado no Git

Núcleo 0.2.35, campo 0.8.10, playbook 0.4.11. A nova exigência é declarativa
por etapa e não conhece habilitação, Tally nem documentos administrativos.
A derivação de histórico da decisão 035 é compartilhada com a apresentação.
O commit precisa introduzir o selo com nota e autor correspondentes e conter
a linha do evento exigido e o prefixo exato da trilha. Usa ordem, não horário.

Negativas anteriores à implementação em regressao-inicial.txt; novas condições:
importação sem selo, encerramento sem selo, commit recusado, selo anterior,
Git inacessível, reimportação sem novo selo e commit comum que leva tentativa
recusada sem comprovar aplicação. Controle positivo valida, sela e carrega F0;
outro contrato com evento distinto também passa. Todas as negativas verificam evento.

As fixtures históricas foram atualizadas para usar expediente sintético real,
importador, validador e selo. Saídas intermediárias preservam os percursos que
falharam antes dessa atualização; as asserções originais não foram removidas.
A demonstração completa congela o HEAD commitado em worktree separado.

`exige_selo_apos` mantém a regra anterior de posições na trilha. A falha em P3b
foi registrada separadamente em 039; sua migração depende de pacote posterior.
`selar.py` permanece byte a byte inalterado. Por essa instrução, seu exemplo
histórico na docstring ainda aparece no grep literal de vocabulário. O grep
está anexado; a implementação das regras é genérica. Não houve alteração
dos documentos em reference/metodo/.
