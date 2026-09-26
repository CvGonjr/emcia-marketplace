# Sprint 3 — Ação 3.2 — verificação da Fase F0

## Versão e escopo

Data: 26/09/2026. Responsável do caso sintético: **Celso do Vale**.

Execução após `git checkout v-sprint3-poc`, no commit
`737525a1c92a163bc375e80ae7a54a58f0a6d0be`.
Objeto da tag anotada: `de68c888c773bde7add2946600421d8464d68fe1`.
Repositório disponível neste ambiente:
`/home/netiv-dn-1/Projetos/emcia-marketplace`; o caminho `/home/netiv-ai/...`
informado no pedido não existe aqui.

Verificação por testes de fase e de fronteira, com caso sintético em
`/tmp/caso-f0`. Não houve aplicação em campo. Código e testes permaneceram
idênticos à tag. A alteração local pendente em `3.1/suite-congelamento.txt`
foi preservada fora deste registro.

## Contagens

| Módulo | Verificações executadas no módulo integral | Selecionadas para F0 | Falhas |
|---|---:|---:|---:|
| `negativos.sh` | 51 | 9 | 0 |
| `autoria_responsavel.py` | 14 | 7 | 0 |
| `campo_2_6_5.py` | 62 | 4 | 0 |
| `campo_2_6_6.py` | 43 | 3 | 0 |
| **Total** | **170** | **23** | **0** |

Os módulos foram executados integralmente; o arquivo
[testes-f0.txt](testes-f0.txt) contém os recortes solicitados e os códigos
de saída dos módulos. A pré-verificação `contexto.py`, exigida por
`AGENTS.md`, passou em mais 11 verificações: **181 verificações executadas
ao todo**, das quais **23 compõem o recorte desta ação**.

## Verificações de F0

Os identificadores AR-NC01–AR-NC07 abaixo são rótulos deste relatório para
as sete linhas de `autoria_responsavel.py` referentes a `novo-caso.sh`.

| ID | O que verifica | Resultado |
|---|---|---|
| negativos #11 | Etapa posterior a F0 sem nível apurado é negada | PASSOU |
| negativos #12 | F0 não encerra sem nível apurado | PASSOU |
| negativos #14 | Nível fora dos declarados no playbook é recusado | PASSOU |
| negativos #15 | Apuração por autor de agente é recusada | PASSOU |
| negativos #16 | Apuração válida grava o nível e emite evento | PASSOU |
| negativos #17 | F0 encerra após a apuração do nível | PASSOU |
| negativos #18 | Abertura com responsável de agente é recusada | PASSOU |
| negativos #22 | Fronteira acompanha o nível | PASSOU |
| negativos #23 | P3b permanece não delegável nos níveis exercitados pelo teste | PASSOU |
| AR-NC01 | Responsável `AG-01` é recusado na abertura | PASSOU |
| AR-NC02 | Responsável `agente` é recusado na abertura | PASSOU |
| AR-NC03 | Placeholder de responsável é recusado | PASSOU |
| AR-NC04 | Coletivo `equipe` é recusado como responsável | PASSOU |
| AR-NC05 | Responsável vazio é recusado | PASSOU |
| AR-NC06 | Responsável válido é gravado no estado do caso | PASSOU |
| AR-NC07 | Abertura emite `CasoAberto` com o responsável | PASSOU |
| 2.6.5-T13 | Emissão de E1 antes de F0 completo é negada | PASSOU |
| 2.6.5-T14 | Emissão de E1 após F0 é autorizada | PASSOU |
| 2.6.5-T15 | E1 é materializado em arquivo real não vazio | PASSOU |
| 2.6.5-T43 | E1 contém as seções exigidas pelo teste | PASSOU |
| 2.6.6-C02 | Caso novo inicia em F0 | PASSOU |
| 2.6.6-C03 | Encerramento de F0 avança o caso para P1 | PASSOU |
| 2.6.6-C28 | E1 é autorizado e materializado | PASSOU |

## Caso de controle

As 16 execuções de comandos estão enumeradas em
[execucoes.json](caso-controle/execucoes.json), com saídas individuais.
Quinze retornaram zero; a tentativa com autor `AG-01` retornou 1, como
esperado, com a mensagem `autor precisa ser pessoa nomeada`.

1. `novo-caso.sh` abriu `/tmp/caso-f0` com responsável `Celso do Vale`.
   [Estado inicial](caso-controle/estado-inicial.json): F0, nível não apurado.
2. A apuração por agente foi recusada, sem mudar o estado.
3. N2 foi aceito com `DAD 2, GOV 1, CRI 2`, conforme a entrada solicitada.
4. O nível foi reapurado em N1, N2 e N3 antes de cada execução de
   `fronteira.py`, mantendo os eixos solicitados. Essas entradas exercitam
   a seleção de fronteira; não constituem triagem válida segundo TRI-01.
5. N2 foi restabelecido antes de encerrar F0. O encerramento avançou para
   P1; `entregaveis.py --renderizar E1 --emitir` materializou e emitiu
   [E1.md](caso-controle/E1.md), versão 1, com nível N2.
6. O [estado após F0](caso-controle/estado-apos-f0.json) foi preservado
   antes de demonstrar A7. A trilha final
   [eventos.jsonl](caso-controle/eventos.jsonl) contém nove eventos,
   incluindo a reapuração usada na demonstração de A7. Todos identificam
   o commit congelado do componente.

Observação de procedência da evidência: a recusa ao autor de agente está
em [03-recusa-autor-agente.txt](caso-controle/03-recusa-autor-agente.txt),
mas não consta como evento no JSONL. O comando encerra na validação de
autor antes de chamar a rotina que registra recusas. Essa limitação foi
registrada para avaliação na ação 3.9; não houve correção nesta ação.

## Fronteira por nível

Cada célula informa **camada / preparação delegável**. “Sim” reproduz
`preparacao delegavel`; “não” abrange `exige verificacao humana` e
`nao delegavel`. A tabela não concede autoridade de apuração ou escrita
a agentes.

| Etapa | N1 | N2 | N3 |
|---|---|---|---|
| F0 | EX1 / sim | EX1 / sim | EX1 / sim |
| P1 | EX2 / sim | EX2 / sim | EX3 / não |
| P2 | EX2 / sim | EX2 / sim | EX3 / não |
| P3a | EX2 / sim | EX3 / não | EX3 / não |
| P3b | EX4 / não | EX4 / não | EX4 / não |
| P3d | EX3 / não | EX3 / não | EX3 / não |
| P4 | EX2 / sim | EX3 / não | EX3 / não |
| P5 | EX3 / não | EX3 / não | EX3 / não |
| P6 | EX3 / não | EX3 / não | EX3 / não |
| P7 | EX4 / não | EX4 / não | EX4 / não |
| P8 | EX3 / não | EX3 / não | EX3 / não |
| P9 | EX3 / não | EX3 / não | EX3 / não |
| P10 | EX4 / não | EX4 / não | EX4 / não |

São **13 etapas × 3 níveis = 39 células observadas**, nas saídas
[N1](caso-controle/fronteira-N1.txt),
[N2](caso-controle/fronteira-N2.txt) e
[N3](caso-controle/fronteira-N3.txt).
A primeira fronteira humana anunciada é P3b em N1, P3a em N2 e P1 em N3.
P3b, P7 e P10 permanecem explicitamente não delegáveis nos três níveis.

## Achado A7 — nível não calculado a partir dos eixos

**Reprodução:** no mesmo caso, após a emissão de E1, executou-se
`avancar.py --apurar-nivel N1 --autor "Celso do Vale" --eixos "DAD 3, GOV 1, CRI 1"`.
O comando retornou **0**, gravou **N1**, preservou a etapa P1 e emitiu
`NivelApurado`. A saída está em
[09-achado-A7.txt](caso-controle/09-achado-A7.txt); o estado efetivamente
gravado está em [estado-apos-A7.json](caso-controle/estado-apos-A7.json).

**Causa:** `avancar.py::apurar_nivel()` verifica se o nível informado
existe no playbook, atribui esse nível diretamente ao estado e guarda
`eixos` como texto. Não analisa os eixos, não valida suas faixas e não
calcula nem confronta o nível com a pontuação.

**Referência e limite da demonstração:** TRI-01 §3.4, tanto no pacote
congelado quanto no documento canônico consultado em `emcia-artefatos`,
define somas de 3 a 9 por eixo e usa a maior soma: 3–4 → N1, 5–7 → N2,
8–9 → N3. `GOV 1` e `CRI 1` estão fora desse domínio. Logo, o experimento
demonstra aceitação de eixos inválidos e ausência de cálculo/confronto;
essa entrada não fundamenta afirmar que o nível correto seria N3.
Os eixos `DAD 2, GOV 1, CRI 2` do percurso inicial também estão fora da
faixa de somas e foram mantidos por serem a entrada pedida nesta ação.

**Efeito:** o nível selecionado pela pessoa governa as camadas posteriores
mesmo sem pontuação válida ou coerência verificada com os eixos. Isso
permite uma fronteira mais permissiva do que uma triagem válida poderia
determinar. Nesta execução houve reapuração após F0: o estado passou a
N1, enquanto o E1 já materializado continuou registrando N2. Ambos os
estados foram preservados para tornar a sequência verificável.

**Destino:** ação **3.9**, para análise e decisão sobre o achado. Nenhum
código, teste ou regra do playbook foi alterado nesta ação.

## Resultado

**23 verificações selecionadas aprovadas**, percurso de F0 e emissão de
E1 executados, **39 células de fronteira registradas** e **A7 reproduzido**.
O resultado confirma o comportamento observado da versão congelada;
as limitações documentadas seguem para a ação 3.9.
