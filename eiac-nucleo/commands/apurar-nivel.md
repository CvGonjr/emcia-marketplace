---
description: Grava o nível de complexidade apurado pela triagem no Registro do caso.
argument-hint: <nível> <eixos>
---

**Decisão humana fora da sessão (A12).** O agente prepara os argumentos e
entrega o comando pronto ao engenheiro. Não o execute por Bash na sessão,
mesmo usando nome humano. O engenheiro executa no próprio terminal, fora
do Claude Code, no diretório do caso. Resolva o caminho do plugin antes de
entregar: use o caminho absoluto real, sem variável de sessão no comando.

Confirme com o operador as somas dos eixos do instrumento de triagem
(EMCIA-TRI-01, seção 3.4). Informe todos os eixos declarados no playbook:
cada soma está na faixa de 3 a 9. O script calcula o nível pela regra
declarada de máximo e confere o nível informado. Não use a média.

Prepare e entregue ao engenheiro este comando:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --apurar-nivel <nivel> --autor "<nome da pessoa>" --eixos "<DAD n, GOV n, CRI n>"`

Exemplo válido: nível `N2`, eixos `DAD 5, GOV 3, CRI 6`.
O maior eixo é CRI 6, que corresponde a N2 segundo o playbook do caso.
Eixos ausentes, desconhecidos, duplicados, fora da faixa ou em formato
inválido e nível divergente são recusados com `TentativaNegada` na trilha.

Se o script recusar, apresente o motivo sem contorná-lo.

O nível decide a camada de todas as etapas seguintes (CAT-01 3.6). Reapuração é permitida e fica na trilha com o valor anterior — não edite `registro/estado.json` à mão para corrigir.
