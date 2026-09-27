# 029 — Revisão humana do piloto declarada na guarda (A15)

**Data:** 27/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

A lista de A12 (027) não incluía piloto revisado. O nome revisado_por podia
ser informado pelo agente. A auditoria também identificou a definição da
rotina de calibragem: responsável e cadência são decisão de governança,
conforme o contrato já aplicado por calibragem.py.

## Decisão

O playbook acrescenta duas condições de arquivo à lista `decisoes_humanas`:
`piloto.py` quando estado=revisado; `calibragem.py` quando responsável está
preenchido (rotina). A guarda interpreta o contrato existente, sem nomes
novos no núcleo. Toda chamada Bash vem da sessão do agente; nome humano
informado não autoriza. A recusa gera TentativaNegada, operação e comando.

Rascunho de piloto e ciclo com drift/recomendação sem decisão continuam
permitidos. O engenheiro registra revisão e rotina no próprio terminal.
O agente prepara rascunhos e entrega comandos com caminhos absolutos.

## Auditoria de eiac-campo/scripts

| Script | Transição/ato humano | Declaração na guarda | Preparação permitida |
|---|---|---|---|
| baseline.py | Não há transição de decisão: registro de medição/estimativa | Não se acrescenta decisão por nome de autor de conteúdo | Medição, com autoria nominal no artefato |
| metrica.py | Não há transição de julgamento: planejada/apurada registra medição | Não se acrescenta decisão por autoria nominal | Plano e cálculo, com responsável nominal |
| piloto.py | Revisão do conjunto | revisar-piloto, estado=revisado (nova) | estado=rascunho |
| operacional.py | Validar especificação | validar-operacional, estado=validado (027) | estado=proposta |
| governanca.py | Decidir autonomia | decidir-autonomia, estado=decidido (027) | rascunho/proposto |
| calibragem.py | Definir rotina; decidir recalibragem | definir-rotina, responsável preenchido (nova); decidir-recalibragem, decisão preenchida (027) | Ciclo sem decisão, com drift e recomendação |

A autoria do conteúdo não autentica origem nem transforma registro de fato
em decisão. A inspeção de invocações preserva os limites da decisão 027;
ela não é uma autenticação de sistema operacional para shell arbitrário.

## Verificação

`testes/revisao_a15.py`: piloto revisado e rotina negados pela guarda com nome
humano; rascunho, baseline, métrica e ciclo sem decisão permitidos.
