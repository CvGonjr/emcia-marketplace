---
description: Registra a satisfação de um item inegociável do playbook, com evidência rastreável.
argument-hint: <número do inegociável> <evidência>
---
Este é o único caminho autorizado para satisfazer um item inegociável — uma flag manual no estado não é aceita e é bloqueada pela guarda (`registro/` não aceita escrita direta).

Pergunte ao operador, se não vierem nos argumentos: qual item inegociável e qual evidência sustenta a satisfação (documento, sessão, referência).

Depois execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --satisfazer-inegociavel <n> --autor "<nome da pessoa>" --evidencia "<descrição ou caminho>"`

O núcleo não julga se a evidência de fato comprova o item — isso é decisão humana/metodológica. Ele exige apenas que evidência e autor estejam presentes e rastreáveis. Se o script recusar, apresente o motivo sem contorná-lo.
