---
description: Registra a satisfação de um item inegociável do playbook, com evidência rastreável.
argument-hint: <número do inegociável> <evidência>
---

**Decisão humana fora da sessão (A12).** O agente prepara os argumentos e
entrega o comando pronto ao engenheiro. Não o execute por Bash na sessão,
mesmo usando nome humano. O engenheiro executa no próprio terminal, fora
do Claude Code, no diretório do caso. Resolva o caminho do plugin antes de
entregar: use o caminho absoluto real, sem variável de sessão no comando.

Este é o único caminho autorizado para satisfazer um item inegociável — uma flag manual no estado não é aceita e é bloqueada pela guarda (`registro/` não aceita escrita direta).

Pergunte ao operador, se não vierem nos argumentos: qual item inegociável e qual evidência sustenta a satisfação (documento, sessão, referência).

Prepare e entregue ao engenheiro este comando:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --satisfazer-inegociavel <n> --autor "<nome da pessoa>" --evidencia "<descrição ou caminho>"`

O núcleo não julga se a evidência de fato comprova o item — isso é decisão humana/metodológica. Ele exige apenas que evidência e autor estejam presentes e rastreáveis. Se o script recusar, apresente o motivo sem contorná-lo.
