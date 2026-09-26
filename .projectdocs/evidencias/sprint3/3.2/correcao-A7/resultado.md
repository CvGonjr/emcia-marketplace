# Sprint 3 — Ação 3.2 — correção A7

## Lacuna e referência

A apuração aceitava qualquer nível existente no playbook e eixos como texto
livre, inclusive `N2` com `DAD 2, GOV 1, CRI 2`. A correção implementa a
regra já definida em EMCIA-TRI-01 §3.4: somas de 3 a 9 por eixo, agregação
pelo máximo e faixas 3–4 → N1, 5–7 → N2, 8–9 → N3.

Foi consultado o documento controlado do pacote e sua fonte canônica em
`emcia-artefatos`. A versão anterior verificada é `v-sprint3-poc`, commit
`737525a1c92a163bc375e80ae7a54a58f0a6d0be`. O trabalho desta correção
partiu de `0d24e0f`, que acrescentava evidências de F1 sem alterar código.

## Correção

- O playbook do template passa de 0.4.2 a 0.4.3 e declara `apuracao_nivel`:
  eixos, mínimos, máximos, operador `maximo` e faixas de nível.
- `eiac-nucleo/scripts/apuracao.py` interpreta somente esses dados. Não
  contém siglas DAD/GOV/CRI, limites 3–9 ou correspondências N1–N3.
  Regra ausente, operador desconhecido e faixas sobrepostas ou incompletas
  são recusados; não existe opção para desativar a validação.
- `avancar.py --apurar-nivel` exige os eixos declarados, inteiros separados
  por vírgula, sem omissões ou duplicações. Calcula o nível e recusa a
  divergência com a conta, antes de gravar qualquer alteração de estado.
- Recusas de apuração em um caso aberto geram `TentativaNegada`, inclusive
  autor de agente e nível desconhecido. A autoria da negativa é atribuída
  ao responsável nominal do caso, preservando a proibição de identificador
  de agente como autor. As demais operações da máquina mantêm seus eventos.
- O caso continua lendo seu próprio `registro/playbook.json`. Casos antigos
  não são modificados automaticamente: precisam receber uma atualização
  explícita de sua declaração para reapurar. Sem a regra, a apuração recusa.
- Versões: núcleo 0.2.21 → 0.2.22; campo 0.8.0 → 0.8.1.
- O comando `apurar-nivel` e a habilidade `hb-enquadrar` foram atualizados
  para usar as somas corretas e remeter ao instrumento controlado. O
  procedimento completo continua no documento do método.
- O CI passa a executar o módulo `testes/triagem_a7.py`.

Nenhuma outra lacuna de F0/F1 ou comportamento de outras operações foi
corrigido. As alterações locais anteriores em `3.1/suite-congelamento.txt`
e `3.2/testes-f0.txt` foram preservadas fora dos commits desta correção.

## Testes novos — negativos primeiro

`testes/triagem_a7.py` contém **24 testes**: 15 negativos e 9 positivos.
Cada negativa confere saída 1, mensagem, estado inalterado e último evento
`TentativaNegada` com autoria nominal. Os positivos conferem o nível,
os eixos gravados e o evento `NivelApurado`.

| Grupo | Cobertura |
|---|---|
| Negativos solicitados | Eixo ausente; `DAD 2, GOV 1, CRI 2` fora da escala; N1 divergente de `DAD 5, GOV 3, CRI 6` |
| Demais negativos | Eixo desconhecido; duplicado; formato inválido; eixos não informados; regra ausente; operador não suportado; sobreposição e lacuna nas faixas; autor de agente; nível desconhecido; valor acima do máximo; valor fracionário |
| Positivos solicitados | N2 com `DAD 5, GOV 3, CRI 6`; N3 com `DAD 4, GOV 3, CRI 8` |
| Limites | Máximos 3, 4, 5, 7, 8 e 9, cobrindo as duas extremidades de cada faixa |
| Núcleo genérico | Outro playbook com X/Y/Z, escala 10–19 e faixas diferentes; aceita N2 com `X 14, Y 10, Z 11` |

O caso divergente usa média inferior a 5 e máximo 6: somente a regra de
máximo produz N2. O caso alternativo verifica que o núcleo obedece aos dados
do caso, sem incorporar os valores do método.

## Antes/depois

Os testes novos foram escritos antes da mudança de produção. O registro
[testes-antes.txt](testes-antes.txt) reproduz a execução contra a tag
antiga em checkout isolado, com somente o novo arquivo de teste copiado.

| Entrada ou bateria | Antes | Depois |
|---|---|---|
| N2, `DAD 2, GOV 1, CRI 2` | Aceita, saída 0 | Recusa: `DAD 2 fora da faixa 3 a 9`; `TentativaNegada` |
| N2, `DAD 5, GOV 3` | Aceita, saída 0 | Recusa: `eixos ausentes: CRI`; `TentativaNegada` |
| N1, `DAD 5, GOV 3, CRI 6` | Aceita, saída 0 | Recusa: `maior eixo CRI 6 -> N2; informado N1`; `TentativaNegada` |
| N2, `DAD 5, GOV 3, CRI 6` | Aceita sem conferir a conta | Aceita após calcular o máximo e conferir N2 |
| N3, `DAD 4, GOV 3, CRI 8` | Aceita sem conferir a conta | Aceita após calcular o máximo e conferir N3 |
| 24 testes novos contra a tag antiga | 11 falhas e 4 erros de preparação por ausência da declaração; 9 positivos passam | 24 aprovados |
| Pré-verificações negativas/CTX na versão anterior | 51 + 11 aprovadas | Contagens preservadas na suíte final |
| Suíte completa após a correção | — | **538 verificações em 21 módulos, zero falhas** |

As quatro falhas de preparação do teste na versão antiga decorrem da
ausência de `apuracao_nivel` no template; não são falhas de módulos antigos.
Saídas integrais: [negativos-inicial.txt](negativos-inicial.txt),
[contexto-inicial.txt](contexto-inicial.txt) e
[suite-final.txt](suite-final.txt). A suíte final inclui todos os módulos
Python de `testes/` e `negativos.sh`, com total por módulo.

## Preparações de testes existentes ajustadas

As mensagens, condições de aprovação e contagens das suítes existentes
foram preservadas. Eixos inválidos nos testes novos são intencionais.

| Arquivo / preparação | Antes | Depois | Motivo |
|---|---|---|---|
| `testes/nucleo_2_6_1.py`, comando de T22 | N1, `DAD 3` | N1, `DAD 3, GOV 3, CRI 3` | Completar o comando autorizado que a guarda inspeciona; T22 continua verificando a guarda |
| `testes/campo_2_6_5.py`, `apurar_e_encerrar_f0` | Eixos fixos `DAD 4, GOV 5, CRI 7` para qualquer nível | Eixos por nível: N1 `3,3,3`; N2 `5,3,6`; N3 `4,3,8`, sempre DAD/GOV/CRI | Manter a preparação coerente com o nível solicitado; 62 verificações preservadas |
| `testes/campo_2_6_6.py`, `apurar_e_encerrar_f0` | Eixos fixos `DAD 4, GOV 5, CRI 7` para qualquer nível | Mesmo mapa por nível | Manter a preparação coerente com o nível solicitado; 43 verificações preservadas |

Os eixos anteriores dos dois auxiliares estavam na escala e eram válidos
para N2; a inadequação era usá-los independentemente do parâmetro de nível.
As demais preparações que já forneciam somas completas e coerentes não
foram alteradas. Nenhuma expectativa de recusa foi afrouxada.

## Registro e publicação

Commit de implementação: `1b680e1` (`fix(A7)`).
Commit documental: `cf2fec0` (`docs`).

Por confirmação do usuário, A7 foi registrado como
[decisão 023](../../../../../decisoes/023-regra-leitura-triagem-A7.md).
A decisão 022 de habilitação administrativa permanece preservada.
O [diff.patch](diff.patch) registra a implementação e a documentação
desde `0d24e0f`, excluindo as alterações locais anteriores de evidência.

Tag anotada desta correção: `v-sprint3-poc.1`, criada após o commit
`docs(evidence)`. As tags anteriores não são movidas. O push de `master`
e da nova tag será tentado após a criação da tag.
