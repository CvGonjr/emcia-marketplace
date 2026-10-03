# A3 — propostas aos artefatos canônicos

## MAN-01 v0.2

Usar playbook **0.4.18** como referência. Em §3.3, P2 exige:
“Todos os RH-xx vinculados a fontes ou dispensados com motivo”.
Ato do engenheiro: `vincular-restricao`, que cobre vincular e dispensar;
execução fora da sessão, comando exato devolvido pela guarda. Descrever a
revisão com decisão explícita e histórico após P2. Em §3.2, informar que
E1 de caso restrito aguarda a resolução dos RH em P2 antes de materializar.

A emenda executável local está em
`eiac-campo/reference/manual-emenda-041.json`. Ela não edita o manual
empacotado nem aprova automaticamente uma revisão do documento canônico.
O teste mantém a detecção das duas divergências do manual base e confere
que a emenda corresponde ao playbook, sem dispensar produtos ou atos.

## ESP-01 e TST-01

Declarar o registro versionado de vínculos RH → F e dispensas motivadas.
A cobertura no encerramento é genérica, com origem/destino e estados
validáveis declarados no playbook, incluindo integridade pelos eventos.
Testar RH pendente no encerramento e na emissão, fonte não curada, autoria,
sessão, revisão sem decisão e relação de fonte ausente. Incluir o percurso
sintético restrito com E2 marcado junto à asserção, sem ressalva ao final.

## CTX-01 e modelos de entregáveis

Propor metadado opcional `recebimentos` no objeto Fonte para declarar a
relação entre ids REC e F. Os ids só resolvem com curadoria e recebimento
íntegros; a decisão humana do vínculo não decorre de nomes parecidos.
Nos artefatos renderizados, `fontes` declara a origem do registro e
`fontes_por_campo` declara a de uma asserção específica. Nenhum novo
metadado atribui procedência ou verdade por julgamento de modelo.

HAB-01 §3.4 permanece a regra de marca localizada. Não há mudança em seu
conteúdo. Nenhum arquivo em `eiac-campo/reference/metodo/` foi alterado.
