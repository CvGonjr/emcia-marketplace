# Matriz de contrato — F0 a P10

**Pacote:** 2.6.0
**HEAD inicial:** `667c0212e81721b67b3dcf866b3eb3333a7d60d4`
**Playbook antes:** `eiac-campo/template-caso/registro/playbook.json` v0.3.1, 8 etapas

Fontes primárias, por precedência declarada no pacote: EMCIA-MET-01
(fases/passos/sequência/entregáveis), EMCIA-CAT-01 (delegação/EX/fronteira),
EMCIA-ESP-01 (forma executável/estados/protocolo), EMCIA-CAM-01
(protocolo de campo P6–P10, entrada/saída/encerramento/fronteira), EMCIA-E1
a EMCIA-E5 (composição dos entregáveis), EMCIA-ROT-01 (P3d).

## 1. Playbook atual → método oficial → diferenças

| Item | Playbook atual (v0.3.1) | Método oficial | Diferença |
|---|---|---|---|
| Etapas declaradas | F0, P1, P2, P3a, P3b, P3d, P4, P5 (8) | F0, P1, P2, P3a, P3b, P3d, P4, P5, P6, P7, P8, P9, P10 (13) — ESP-01 §3.3 | Faltam P6–P10 (D-07) |
| E3 | `E3-D` e `E3-E` já presentes, com `condicao` em texto livre | ESP-01 §3.8: E3-D sempre emite (P4,P5); E3-E só quando P5 classifica caso como agente | Condição existe só como string, motor não a interpreta — CAPACIDADE DECLARATIVA a resolver aqui, execução em 2.6.1/2.6.5 |
| E4 | `portao: [P6,P7]`, `inegociavel: [2]`, **`portao_pendente: true`** | ESP-01 §3.8: E4 = P6,P7 + inegociável 2, sem bloqueio artificial | `portao_pendente` é resíduo da ausência estrutural de P6/P7, não de uma decisão de método vigente — remover |
| E5 | `portao: [P9,P10]`, `inegociavel: [4,5]`, **`portao_pendente: true`**, **sem P8, sem inegociável 3** | ESP-01 §3.8: E5 = P8,P9,P10 + inegociáveis 3,4,5 | E5 incompleto — faltam P8 e inegociável 3; corrigir |
| Inegociável 1 | `"Linha de base registrada, apuracao diferente de estimado"` | MET-01 §3.4.3: linha de base é "obrigatória nos três níveis. Estimada em N1, medida em N2 e N3" | Texto do playbook proíbe estimativa em qualquer nível — mais restritivo que o método. Corrigir (item 19 do pacote) |
| P3b | `delegavel: false`, EX4, presencial, sem comando de agente | CAT-01 §3.5.2/§3.5.3, ESP-01 §3.5: humano, EX4, não delegável | JÁ IMPLEMENTADO E CONFORME — preservar sem alteração |
| Pendências do playbook | "Correspondência entregável x passos diverge..."; "P6 a P10 sem habilidade" | Decisão 012 tinha isso como pendência aberta; CAM-01/ESP-01 (17/09/2026) resolvem a correspondência: E4=P6/P7, E5=P8/P9/P10 | Pendência de correspondência **documentalmente resolvida** — remover e registrar decisão 013. Pendência "P6 a P10 sem habilidade" permanece real para as skills (parcialmente resolvida aqui como declaração de passo; skill completa é 2.6.2/2.6.3) |
| P3d | `depende_de: "P3b"` | CAM-01 refs; ROT-01 confirma P3d como confronto pós-levantamento | JÁ IMPLEMENTADO E CONFORME |
| Recorrência | Nenhum campo — não existe `recorrente` no schema do playbook | CAM-01 §3.6, ESP-01 §3.7/§3.10 G5: P10 é recorrente, exige cadência e responsável | AUSENTE — adicionar `recorrente`, `cadencia_obrigatoria`, `responsavel_obrigatorio` (ou equivalente) em P10 |

## 2. Classificação por requisito do pacote (AUSENTE / PARCIAL / CONFORME / DIVERGENTE)

| Requisito | Classificação |
|---|---|
| 13 etapas canônicas F0–P10 | AUSENTE (8/13) → implementar P6–P10 |
| P6 declarado (sem skill) | AUSENTE → implementar |
| P7 declarado, não delegável, EX4 | AUSENTE → implementar |
| P8 declarado, relação com inegociável 3 | AUSENTE → implementar |
| P9 declarado, relação com inegociável 4 | AUSENTE → implementar |
| P10 declarado, recorrente, cadência, responsável | AUSENTE → implementar |
| P3b não delegável | JÁ IMPLEMENTADO E CONFORME → preservar |
| Cinco inegociáveis declarados | PARCIAL (5 declarados, mas inegociável 1 mais restritivo que o método, 2–5 sem etapa alvo existente para 2,3,4,5 antes deste pacote) → completar |
| Seis autorizações de emissão | PARCIAL (E1,E2,E3-D,E3-E,E4,E5 todos presentes; E4/E5 com `portao_pendente` e E5 incompleto) → corrigir |
| E3-E condição declarativa | IMPLEMENTADO MAS DIVERGENTE (existe como string livre, não como estrutura interpretável) → corrigir forma, não motor |
| E4 = P6/P7 + inegociável 2 | PARCIAL (portão correto, `portao_pendente` bloqueando) → corrigir |
| E5 = P8/P9/P10 + inegociáveis 3/4/5 | IMPLEMENTADO MAS DIVERGENTE (faltava P8 e inegociável 3) → corrigir |
| Correspondência entregável×passo (pendência) | PARCIAL, resolvível com CAM-01/ESP-01 → remover pendência, registrar decisão 013 |
| D/I/V | JÁ IMPLEMENTADO E CONFORME (Ação 2.5) → não tocar |
| CTX-V01–V11 / objetos CTX | JÁ IMPLEMENTADO E CONFORME (Ação 2.5) → não tocar |

## 3. Matriz F0–P10

| Etapa | Fase | Camada (N1/N2/N3) | Delegável | Modalidade | Recorrente | Dependências | Inegociável |
|---|---|---|---|---|---|---|---|
| F0 | F0 | EX1/EX1/EX1 | sim | assíncrono | não | — | — |
| P1 | F1 | EX2/EX2/EX3 | sim | vídeo | não | — | — |
| P2 | F1 | EX2/EX2/EX3 | sim | assíncrono | não | — | — |
| P3a | F1 | EX2/EX3/EX3 | sim | remoto | não | — | 1 |
| P3b | F1 | EX4/EX4/EX4 | **não** | presencial | não | — | — |
| P3d | F1 | EX3/EX3/EX3 | sim | remoto | não | P3b | — |
| P4 | F2 | EX2/EX3/EX3 | sim | vídeo | não | — | — |
| P5 | F2 | EX3/EX3/EX3 | sim | vídeo | não | — | — |
| P6 | F3 | EX3/EX3/EX3 | sim (preparação); ponto de inserção e nomeação são humanos | presencial/remoto conforme nível | não | E3-E emitido; P5 classificou caso como agente | — |
| P7 | F3 | EX4/EX4/EX4 | **não** | conforme nível (CAM-01: decisão humana registrada) | não | P6 | 2 |
| P8 | F4 | EX3/EX3/EX3 | sim (geração de casos é híbrida; revisão é humana) | conforme nível | não | P7 | 3 |
| P9 | F4 | EX3/EX3/EX3 | sim (apuração determinística; interpretação é humana) | conforme nível | não | P8 | 4 |
| P10 | F4 | EX4 (decisão) / EX2 (monitoramento) | **não** (decisão de recalibrar é humana) | conforme nível | **sim** | P9 | 5 |

Fonte de camada/fase/dependência: EMCIA-CAM-01 §3.2–3.6 para P6–P10; playbook
atual para F0–P5 (preservado, já conforme).

## 4. Matriz de emissões (entregáveis)

| Emissão | Etapas | Condição | Inegociáveis |
|---|---|---|---|
| E1 | F0 | F0 encerrada | — |
| E2 | P1, P2, P3a, P3b, P3d | todas encerradas | 1 |
| E3-D | P4, P5 | sempre emite quando P4/P5 encerrados (ESP-01 §3.8) | — |
| E3-E | P5 | somente quando P5 classificou ao menos um caso como agente (condição declarativa nova) | — |
| E4 | P6, P7 | P6/P7 encerrados; `portao_pendente` removido | 2 |
| E5 | P8, P9, P10 | P8/P9/P10 encerrados/especificados conforme PoC; `portao_pendente` removido | 3, 4, 5 |

## 5. Nota sobre a pendência de correspondência (decisão 012)

A decisão 012 registrou como pendência aberta a divergência entre o
relatório do PFC (P6–P7 em E4, P8–P10 em E5) e "os documentos internos"
(que a decisão descrevia como P6–P8 em E4, P9–P10 em E5). Os documentos
publicados em 17/09/2026 — EMCIA-CAM-01 e EMCIA-ESP-01 v0.2 — fixam
formalmente E4 = P6/P7 e E5 = P8/P9/P10, coincidindo com o relatório do
PFC. Isso resolve a pendência por precedência documental, não por escolha
de implementação. Ver decisão 013.

## 6. Escopo negativo confirmado

Este pacote não implementa: lógica completa da máquina F0–P10 além do que
`avancar.py`/`guarda.py` já fazem genericamente; proteção de `registro/`
(D-08); eventos para toda recusa de `avancar.py` (D-09); verificação
semântica dos cinco inegociáveis; P6–P10 operacionais; 18 HB completas;
4 AG mapeados; geração material de E4/E5; percurso end-to-end F0–P10
(D-13).
