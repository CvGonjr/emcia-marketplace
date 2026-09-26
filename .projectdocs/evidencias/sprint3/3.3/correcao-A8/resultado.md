# Ação 3.3 — Correção A8

## Lacuna e base

A camada de execução era cobrada ao carregar a habilidade, mas não impedia o encerramento sem sessão da própria etapa. O registro de sessão também aceitava etapas futuras ou já encerradas.

Base: `v-sprint3-poc.1`, commit `aa40832e9f8a1ab4350785a12739058a8c4ac40d`, objeto anotado `313bc12a2e955ecff63e3b76278212ea08c5781b`.
Foram lidos CLAUDE.md, o índice de decisões e a decisão 022. A numeração **024** foi confirmada pelo usuário, pois 023 já registra A7.

## Correção

O playbook declara `encerramento_por_camada`: EX1/EX2 = falso, EX3/EX4 = verdadeiro. O núcleo resolve a camada da etapa pelo nível apurado e exige a sessão da própria etapa quando o booleano declara essa exigência. A condição nova não contém siglas de camada, nomes de etapa ou níveis do método.

A recusa informa etapa, camada, nível e modalidade exigida; registra `TentativaNegada` com pessoa nomeada e preserva o estado. Registro de sessão aceita apenas a etapa corrente ainda não encerrada. Sessão histórica de outra etapa não libera o encerramento.

A conferência de sessão ocorre antes da trava de selo de P3b. A função `selo_apos_etapa` permanece idêntica à versão congelada; recusas anteriores de selo e dependência mantêm seus eventos. A7 permanece coberto pelos 24 testes existentes.

Versões: núcleo **0.2.23**, campo **0.8.2**, playbook **0.4.4**. Decisão: [024](../../../../../decisoes/024-sessao-encerramento-A8.md). Atualizados os comandos encerrar/registrar-sessao, README, INSTALACAO, índice das decisões, README de testes e CI.

Casos existentes precisam atualizar explicitamente seu próprio playbook. Declaração ausente, camada não coberta ou valor não booleano recusam o carregamento; o caso não lê o playbook do plugin.

## Testes novos e antes/depois

Os negativos foram escritos e executados antes da alteração do núcleo. `sessao_a8.py` tem **23 verificações**: 16 negativas e 7 positivas/declaração. Contra a versão anterior, houve **16 falhas**; após a correção, **23 passaram**. Os arquivos `testes-antes.txt` e `testes-depois.txt` preservam a saída.

| Cenário | Antes | Depois |
|---|---|---|
| P3a em N2 (EX3), sem sessão | Encerrava | TentativaNegada; etapa/camada/nível/modalidade na mensagem |
| Sessão de outra etapa | Não impedia encerrar P3a | Não libera P3a |
| Sessão para etapa futura | Aceitava | TentativaNegada |
| Sessão para etapa passada ou corrente já encerrada | Aceitava | TentativaNegada |
| P1 em N2 (EX2), sem sessão | Encerrava | Encerra |
| P3a em N2, com sessão própria | Encerrava | Encerra |
| P3a em N1 (EX2), sem sessão | Encerrava | Encerra |
| P3b sem sessão e sem selo | Recusa pelo selo | Recusa pela sessão, primeiro |
| P3b com sessão própria, sem selo | Recusa pelo selo | Continua recusando pelo selo |
| P3b com sessão própria e selo posterior a P2 | Encerrava | Encerra |

Também cobertos: EX1 sem sessão; declaração alternativa que exige sessão de EX2 ou dispensa em EX3; mapa ausente/incompleto/inválido; etapa desconhecida; cache de camada divergente; P3d, P4 e P5 em N2 sem sessão. Os testes conferem trilha e ausência de mutação nas recusas.

## Ajustes na preparação dos testes existentes

Nenhum teste foi apagado e nenhuma expectativa foi relaxada. Foram alterados somente os passos de preparação em sete arquivos:

| Arquivo | Cada ajuste |
|---|---|
| `nucleo_2_6_1.py` | `percorrer_ate` registra sessão conforme camada resolvida e política; sessão de P3d antes de T03 (dependência negativa), T04 (dependência positiva) e preparação de T17–T20 (inegociável/E2). |
| `campo_2_6_2.py` | Percurso registra sessão quando exigida; caso sintético recebe Git, identidade e responsável nominal; aplica selo após a etapa declarada para chegar realmente a P5 na preparação de G1a/G1b/G1c. |
| `campo_2_6_3.py` | Percurso registra sessão quando exigida; sessões próprias de P8 e P9 antes de encerrar, tanto no caso principal quanto no caso de recalibração pendente (quatro chamadas explícitas). |
| `campo_2_6_4.py` | Percurso registra sessão quando exigida; Git, identidade, responsável e selo após a etapa declarada permitem chegar realmente a P5 em G1 T39/T40. |
| `campo_2_6_5.py` | Percurso registra sessão conforme camada e política declaradas, preservando a preparação existente de selo. |
| `campo_2_6_6.py` | Treze sessões antes de encerramentos EX3: C04 P3a/P3d/P4; preparação C05 P3a; caso P6 P3a/P3d/P4/P6/P8/P9; caso E1/E2/E3 P3a/P3d/P4. |
| `verificacao_por_estados.py` | Sessão de P3a em `levar_ate_p3b` e T03 (duas chamadas), para isolar as verificações de selo. |

A primeira execução integral expôs preparações que paravam em P3b por falta de selo e depois registravam sessão futura de P5, além de encerramentos EX3 sem sessão. A saída foi preservada em `suite-primeira.txt`. Corrigidos os percursos, sem alterar as asserções. O módulo campo_2_6_5 pode devolver código zero mesmo imprimindo falhas; a conferência da suíte final verifica também mensagens de falha, sem alterar esse comportamento fora do escopo de A8.

## Suíte completa

Antes de modificar o núcleo: negativos **51/51** e contexto **11/11**, sem falhas. Saídas preservadas nos respectivos arquivos iniciais.

| Módulo | Verificações | Falhas |
|---|---:|---:|
| negativos.sh | 51 | 0 |
| autoria_responsavel.py | 14 | 0 |
| campo_2_6_2.py | 38 | 0 |
| campo_2_6_3.py | 57 | 0 |
| campo_2_6_4.py | 50 | 0 |
| campo_2_6_5.py | 62 | 0 |
| campo_2_6_6.py | 43 | 0 |
| consolidado.py | 16 | 0 |
| contexto.py | 11 | 0 |
| ctx_v.py | 23 | 0 |
| curadoria.py | 17 | 0 |
| esforco.py | 1 | 0 |
| habilitacao.py | 19 | 0 |
| integracao.py | 17 | 0 |
| metodo_empacotado.py | 1 | 0 |
| nucleo_2_6_1.py | 39 | 0 |
| nucleo_yaml.py | 7 | 0 |
| p3d.py | 12 | 0 |
| playbook_2_6_0.py | 29 | 0 |
| sessao_a8.py | 23 | 0 |
| triagem_a7.py | 24 | 0 |
| verificacao_por_estados.py | 7 | 0 |
| **Total (22 módulos)** | **561** | **0** |

Saída integral em `suite.txt`, com comandos, contagens por módulo e conferência de códigos de saída/mensagens de falha. Comparação: **538 antes + 23 novos = 561 depois**; contagens dos módulos existentes preservadas.

## Artefatos e commits

- `diff.patch`: diferença exata de `v-sprint3-poc.1` até os commits de correção e documentação.
- `2ba34b8ed0ff35b7cf115b48f4dede41d8e8dc22`: fix(A8).
- `daeec86`: docs, decisão 024 e orientações.
- Este pacote recebe commit separado docs(evidence); a tag anotada `v-sprint3-poc.2` aponta para o pacote completo.

As duas edições locais anteriores em `3.1/suite-congelamento.txt` e `3.2/testes-f0.txt` foram preservadas fora dos commits desta correção. As tags anteriores permanecem intactas. Esta verificação é por testes; não houve aplicação em campo.
