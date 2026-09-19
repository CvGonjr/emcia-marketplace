# Caso de controle — HB/AG

ID: `caso-controle-2-6-4` (execução direta dos comandos de resolução, sem caso de campo aberto — o catálogo é dado de método, não dado de caso)

HEAD: `418a91635b96742a443e36ad4976146c4b04894a` (HEAD_INICIAL_2.6.4)

Data: 2026-09-19

## 1. Etapa selecionada

Duas etapas, cobrindo os dois intervalos pedidos pela seção 52 do
pacote: **P4** (dentro de P1–P5) e **P9** (dentro de P6–P10).

## 2. HB referenciada

P4 → `HB-10` (Montagem da matriz de priorização).
P9 → `HB-17` (Consolidação de indicadores).

Ambas resolvem via `playbook.json`: `P4.hb == ["HB-10"]`,
`P9.hb == ["HB-17"]`.

## 3. Definição no catálogo

`HB-10`: camada EX2, automatizada, insumo "Casos candidatos", saída
"Matriz preenchida, sem escolha", critério "Todos os candidatos
presentes, inclusive os descartados".

`HB-17`: camada EX2, automatizada, insumo "Medições do piloto e linha
de base", saída "Comparativo contra a linha de base", critério
"Apuração determinística e documentada".

## 4. Skill física

`HB-10` → `eiac-campo/skills/hb-priorizar/SKILL.md` (frontmatter
`hb: ["HB-10"]`).
`HB-17` → `eiac-campo/skills/hb-medir-valor/SKILL.md` (frontmatter
`hb: ["HB-17"]`).

## 5. AG autorizado

`HB-10` → `AG-02` (Agente de análise documental).
`HB-17` → `AG-04` (Agente de avaliação).

## 6. Critério de verificação

`HB-10`: "Todos os candidatos presentes, inclusive os descartados" —
verificável (compara o conjunto declarado contra o conjunto na matriz).
`HB-17`: "Apuração determinística e documentada" — verificável (mesmo
método de cálculo reproduz o mesmo resultado).

## 7. Execução autorizada

```
$ python3 eiac-nucleo/scripts/catalogo.py --capacidades eiac-campo/reference/habilidades.json \
    --papeis eiac-campo/reference/agentes.json --chave-capacidades habilidades \
    --chave-papeis agentes --chave-autorizadas hb_autorizadas \
    --resolver-papel-capacidade AG-02 HB-10
ok | AG-02 autorizado para HB-10

$ python3 eiac-nucleo/scripts/catalogo.py --capacidades eiac-campo/reference/habilidades.json \
    --papeis eiac-campo/reference/agentes.json --chave-capacidades habilidades \
    --chave-papeis agentes --chave-autorizadas hb_autorizadas \
    --resolver-papel-capacidade AG-04 HB-17
ok | AG-04 autorizado para HB-17
```

Saída completa em `caso-controle-comandos.txt`.

## 8. Evidência produzida

`ok | catalogo valido: 18 capacidades` (ambas as consultas de resolução
de HB partem de um catálogo estruturalmente válido — 18/18, todas as
automatizadas com critério).

## 9. Verificação

`ok | todas as referencias 'hb' do playbook resolvem` — confirma que a
cadeia completa etapa→HB-ID→catálogo→critério funciona para as 14
HB atualmente referenciadas pelo playbook, incluindo HB-10 e HB-17.

## 10. Execução não autorizada

```
$ python3 eiac-nucleo/scripts/catalogo.py ... --resolver-papel-capacidade AG-01 HB-10
papel 'AG-01' nao esta autorizado a executar 'HB-10'

$ python3 eiac-nucleo/scripts/catalogo.py ... --resolver-papel-capacidade AG-03 HB-17
papel 'AG-03' nao esta autorizado a executar 'HB-17'
```

Ambas recusadas com `exit 1` e mensagem explícita — nunca falha
silenciosa.

## 11. Evento de recusa

Este mecanismo (`catalogo.py`) opera fora de um caso de campo aberto —
é resolução de catálogo, não ação de execução dentro de `registro/` —
portanto não produz `eventos.jsonl` (que é exclusivo do caso). A
"recusa" aqui é o `exit 1` + mensagem no `stderr`, análogo ao padrão de
`estrutura.validar()`. Nenhum evento de trilha é esperado nem
necessário neste nível — a trilha de eventos entra quando uma HB é de
fato executada dentro de um caso (por exemplo, via `metrica.py`, que já
produz `MetricaRegistrada`/`MetricaRecusada`).

## 12. Fronteira humana

Nenhuma das quatro consultas acima envolveu decisão humana de P7 ou
P10 — propositalmente, porque HB-14 (P7) e HB-18 (P10) são híbridas: o
catálogo as marca `automatizada: false`/`true` respectivamente mas
ambas têm skills físicas que recusam estruturalmente a decisão final
por agente (`hb-governar`/`hb-recalibrar`, já testado nos pacotes
2.6.2/2.6.3). O catálogo deste pacote não reabre nem enfraquece essa
fronteira — apenas confirma, por T36/T38, que nenhum AG do catálogo
adquire autoridade sobre ela.

## 13. Resultado

Cadeia completa demonstrada para dois pontos do percurso (P4 e P9):
etapa → HB-ID (via playbook) → definição no catálogo → AG autorizado →
skill física → critério de verificação → execução autorizada (PASS) →
execução não autorizada (RECUSA determinística, sem hard-code —
resolução por associação de conjunto em `eiac-campo/reference/agentes.json`).
