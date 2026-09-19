# 013 — E4 = P6/P7, E5 = P8/P9/P10, fixado por EMCIA-CAM-01/ESP-01

**Data:** 18/09/2026 · **Estado:** firme

## Contexto

A decisão 012 registrou como pendência aberta uma divergência na
correspondência entre entregáveis e passos: o relatório do PFC associava
P6–P7 a E4 e P8–P10 a E5; a decisão descrevia "os documentos internos"
associando P6–P8 a E4 e P9–P10 a E5. O playbook marcava `E4` e `E5` com
`portao_pendente: true` e o `E5` nem sequer incluía `P8` no portão.

Em 17/09/2026, dois documentos controlados novos fixaram formalmente essa
correspondência: EMCIA-CAM-01 (Protocolo de Campo por Passo — P6 a P10) e
EMCIA-ESP-01 v0.2 (Especificação Executável do Estúdio de Trabalho). Ambos
descrevem P6/P7 na Fase F3 associados a E4, e P8/P9/P10 na Fase F4
associados a E5 (EMCIA-ESP-01 §3.3, §3.8; EMCIA-CAM-01 §3.2–3.6).

## Decisão

**A correspondência oficial é a do relatório do PFC:**

- `E4` depende de `P6` e `P7`, condicionado ao inegociável 2 (termo de
  autonomia escrito em P7).
- `E5` depende de `P8`, `P9` e `P10`, condicionado aos inegociáveis 3, 4
  e 5.

A pendência de correspondência registrada em 012 está resolvida por
precedência documental. `portao_pendente` em `E4`/`E5` foi removido do
playbook no pacote 2.6.0 — a remoção reflete a resolução da pendência
estrutural, não uma afirmação de que P6–P10 já estão operacionalmente
implementados.

## Consequência

O playbook (`eiac-campo/template-caso/registro/playbook.json`, a partir da
v0.4.0) declara `E4: {"portao": ["P6","P7"], "inegociavel": [2]}` e
`E5: {"portao": ["P8","P9","P10"], "inegociavel": [3,4,5]}`, sem bloqueio
artificial.

A decisão 012 permanece válida quanto à divisão E3-D/E3-E e à localização
do termo de autonomia em E4 — apenas sua seção "Pendência" está superada
por esta decisão.
