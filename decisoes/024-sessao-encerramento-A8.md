# 024 — Sessão exigida no encerramento das camadas EX3 e EX4 (A8)

**Data:** 26/09/2026 · **Estado:** firme, por instrução do usuário

## Contexto

A verificação de F1 da Sprint 3 demonstrou A8: a camada era conferida ao
carregar habilidades, mas etapas em EX3 podiam encerrar sem sessão
registrada. Em N2, isso afetava P3a, P3d, P4 e P5. O comando de registro
também aceitava sessão para etapa futura ou já encerrada.

Foram lidos CLAUDE.md, o índice de decisões e a decisão 022. A decisão
023 já registra A7. O usuário confirmou 024 para A8, preservando 022 e
023. A exigência de selo da decisão 021 permanece vigente.

## Decisão

- O campo declara `encerramento_por_camada` no playbook do template:
  EX1 e EX2 não exigem sessão; EX3 e EX4 exigem.
- O núcleo resolve a camada da etapa pelo nível apurado e aplica o
  booleano declarado. A nova condição não contém nomes de camada, etapa
  ou nível no código; esses valores vêm do playbook do caso.
- Encerramento sem a sessão exigida da própria etapa recusa antes de
  alterar o estado, com etapa, camada, nível e modalidade na mensagem.
  A negativa gera `TentativaNegada`, com autoria nominal.
- Sessão só pode ser registrada para a etapa corrente ainda não
  encerrada. Tentativa para etapa futura ou já encerrada recusa sem
  alterar o estado e gera `TentativaNegada`.
- Sessão de outra etapa não satisfaz a condição de encerramento.
- A checagem de sessão precede a checagem do selo. A regra de selo e seu
  algoritmo de ordem na trilha não são modificados.
- Testes existentes recebem apenas preparação coerente de sessões e
  percurso. Nenhum teste ou expectativa de recusa é removido.

## Consequência

O núcleo passa a 0.2.23, o campo a 0.8.2 e o playbook a 0.4.4.
O comando de encerramento, o de registro de sessão e os guias refletem
a exigência. O CI executa os testes específicos de A8.

Casos existentes continuam lendo seu próprio playbook (decisão 002).
Precisam atualizar explicitamente essa declaração; não há leitura do
playbook do plugin nem atualização automática. Declaração ausente,
camada não coberta ou valor não booleano recusam o carregamento.

Recusas anteriores de dependência e selo mantêm seus eventos, permitindo
que os testes continuem distinguindo essas travas. Esta decisão não
introduz conferência por modelo de linguagem nem dispensa validação humana.

As evidências ficam em `.projectdocs/evidencias/sprint3/3.3/correcao-A8/`.
A versão corrigida recebe a tag anotada `v-sprint3-poc.2`, mantendo as
tags anteriores como referências históricas.
