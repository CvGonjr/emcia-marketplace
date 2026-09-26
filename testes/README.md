# Testes

O expediente administrativo de habilitação tem 19 testes próprios, com recusas
de assinatura parcial, versão obsoleta, fonte alterada, rodada incorreta e
coleta via MCP sem condições prévias, além do percurso de formalização e acessos:

```bash
python3 testes/habilitacao.py
```

```bash
bash testes/negativos.sh
```

São 51 verificações, incluindo as 26 do baseline, sete do contrato canônico
D/I/V e 18 acrescentadas posteriormente. Há negativas e controles positivos —
o que é bem formado precisa passar, senão a trava está apenas quebrada.

Os 11 testes estruturais dos quatro objetos CTX rodam separadamente:

```bash
python3 testes/contexto.py
```

Os 17 testes de curadoria, autoria e versionamento I→V rodam separadamente:

```bash
python3 testes/curadoria.py
```

Os 12 testes de integração CTX ↔ P3d rodam separadamente:

```bash
python3 testes/p3d.py
```

As 23 verificações da bateria formal CTX-V01–CTX-V11 rodam separadamente:

```bash
python3 testes/ctx_v.py
```

Os 17 testes de integração P2/P3 → CTX → P4/P5 rodam separadamente:

```bash
python3 testes/integracao.py
```

As 16 verificações consolidadas da Ação 2.5 (caso de controle único,
percurso ponta a ponta) rodam separadamente:

```bash
python3 testes/consolidado.py
```

As 29 verificações do contrato executável F0–P10 (pacote 2.6.0: 24
estruturais/positivas + 5 negativas por fixture temporária) rodam
separadamente:

```bash
python3 testes/playbook_2_6_0.py
```

As 39 verificações do núcleo genérico de protocolos (pacote 2.6.1: etapa
corrente, dependências, delegabilidade, camadas, critério de verificação,
recorrência, cadência, responsável nominal, inegociáveis por caminho
autorizado, proteção de `registro/`, integridade de portão/condição e
eventos de recusa) rodam separadamente:

```bash
python3 testes/nucleo_2_6_1.py
```

As 38 verificações operacionais de P6 e P7 (pacote 2.6.2: especificação
operacional, termo de autonomia, fronteira agente×humano em ambos,
dependência P7→P6, evidência para o inegociável 2, e a correção de G1
em `guarda.py` — sessão humana válida libera carregamento de skill
EX3/EX4) rodam separadamente:

```bash
python3 testes/campo_2_6_2.py
```

As 57 verificações operacionais de P8, P9 e P10 (pacote 2.6.3: casos de
teste com saída esperada, plano de medição com métrica de resultado,
rotina de recalibragem recorrente com detecção de drift e decisão
humana, dependências P8→P9→P10, evidência para os inegociáveis 3, 4 e
5, e a correção do ciclo de calibragem em duas fases em
`calibragem.py`) rodam separadamente:

```bash
python3 testes/campo_2_6_3.py
```

As 50 verificações do catálogo formal de HB/AG (pacote 2.6.4: 18
habilidades e 4 agentes lógicos, resolução genérica papel↔capacidade
via `eiac-nucleo/scripts/catalogo.py`, mapa canônico AG→HB de CAT-01
Anexo A, resolução playbook→HB, identidade rastreável nas skills
físicas, fronteira EX3/EX4 preservada) rodam separadamente:

```bash
python3 testes/campo_2_6_4.py
```

As 62 verificações da ativação dos seis portões, dos cinco inegociáveis
verificados semanticamente e da materialização de E1–E5 (pacote 2.6.5:
`inegociaveis.py`, `entregaveis.py`, novo domínio `registro/baseline/`,
`avancar.emitir` com NAO_APLICAVEL e `--materializar`) rodam
separadamente:

```bash
python3 testes/campo_2_6_5.py
```

As 43 verificações da verificação integral F0–P10 (pacote 2.6.6: caso de
controle novo, percurso completo, fronteira EX1–EX4, HB/AG, cinco
inegociáveis, seis portões, cinco entregáveis, proteção de registro/
contexto, não invenção, rastreabilidade ponta a ponta) rodam
separadamente:

```bash
python3 testes/campo_2_6_6.py
```

O total das suítes listadas de `negativos.sh` a `campo_2_6_6.py` é de 465
verificações. Com os módulos complementares (`autoria_responsavel.py`: 14,
`nucleo_yaml.py`: 7, `verificacao_por_estados.py`: 7, `esforco.py`: 1,
`metodo_empacotado.py`: 1) e `habilitacao.py` (19), a suíte completa soma
514 verificações. A correção A7 acrescenta 24 testes de apuração declarada,
elevando a suíte completa a 538 verificações:

```bash
python3 testes/triagem_a7.py
```

As recusas são verificadas **pela mensagem**, não só pelo código de saída. Num ponto em que várias travas recusam, conferir apenas o `exit` deixa o teste passar mesmo com a trava certa removida — foi o que aconteceu com o 18 até a mensagem entrar na asserção.

| # | Prova |
|---|---|
| 1 | Habilidade de camada não delegável não carrega |
| 2 | Escrita direta em `caso/` é negada |
| 2b | Redirecionamento de shell para `caso/` é negado |
| 3 | Asserção sem procedência é recusada |
| 4 | Asserção bem marcada é gravada |
| 5 | Etapa presencial não encerra sem sessão registrada |
| 6 | Autor agente é recusado |
| 7 | Entregável com portão fechado não emite |
| 8 | Playbook sem itens inegociáveis não carrega |
| 14 | Nível fora dos declarados no playbook é recusado |
| 15 | Nível apurado por agente é recusado |
| 16 | Nível válido grava e emite `NivelApurado` *(controle positivo)* |
| 17 | Com o nível apurado pelo comando, F0 encerra *(controle positivo)* |
| 18 | Selo por agente é recusado |
| 19 | Selo fora de repositório git é recusado |
| 20 | Selo grava commit com o autor nomeado e emite `SeloAplicado` *(controle positivo)* |
| 21 | Selo sem nada a selar é recusado |
| 22 | A fronteira anunciada acompanha o nível *(controle positivo)* |
| 23 | Etapa não delegável aparece como tal em qualquer nível *(controle positivo)* |
| 24 | Documento citado que não está em `fontes/` é recusado |
| 25 | Documento presente grava e registra o hash na trilha *(controle positivo)* |

## Contrato D/I/V — pacote 2.5.0

| ID | Prova |
|---|---|
| 2.5.0-T01 | `D` válido é aceito sem evidência de verificação |
| 2.5.0-T02 | `I` sem premissa é recusado |
| 2.5.0-T03 | `I` com premissa é aceito |
| 2.5.0-T04 | `V` sem evidência é recusado |
| 2.5.0-T05 | `V` com evidência é aceito |
| 2.5.0-T06 | `X`, `campo` e `externo` são recusados como procedência |
| 2.5.0-T07 | `V` coexiste com `apuracao: medido` em dimensão separada |

O teste 2.5.0-T08 é a execução acumulada desta suíte: os 26 cenários do
baseline permanecem presentes, com os marcadores por extenso atualizados para
os códigos canônicos.

## Objetos CTX — pacote 2.5.1

| ID | Prova |
|---|---|
| 2.5.1-T01 | Termo mínimo válido é aceito |
| 2.5.1-T02 | Entidade mínima válida é aceita |
| 2.5.1-T03 | Regra mínima válida é aceita |
| 2.5.1-T04 | Fonte mínima válida é aceita |
| 2.5.1-T05 | Termo sem `significado` é recusado |
| 2.5.1-T06 | Entidade sem `entidade` é recusada |
| 2.5.1-T07 | Regra sem `estabilidade` é recusada |
| 2.5.1-T08 | Fonte sem `contrato.significado` é recusada |
| 2.5.1-T09 | D/I/V é representável nos quatro objetos |
| 2.5.1-T10 | Taxonomias obsoletas são recusadas como procedência |
| 2.5.1-T11 | Os sete campos centrais da Regra são obrigatórios no schema |

Rodam contra uma cópia temporária do template, sem tocar em caso real.

**Falha aqui é regressão de trava, não de funcionalidade.** Não conserte o teste; conserte a trava.

## Curadoria, autoria e versionamento I→V — pacote 2.5.2

| ID | Prova |
|---|---|
| 2.5.2-T01 | `D` com autoria humana válida é curado |
| 2.5.2-T02 | `I` sem premissa é recusado |
| 2.5.2-T03 | `I` com premissa é curado |
| 2.5.2-T04 | `V` sem evidência é recusado |
| 2.5.2-T05 | `V` com evidência é curado |
| 2.5.2-T06 | Agente como `autoria_conteudo` é recusado |
| 2.5.2-T07 | Pessoa como `autoria_conteudo` é curada |
| 2.5.2-T08 | `registrado_por` distinto de `autoria_conteudo` é preservado |
| 2.5.2-T09 | Sobrescrever `I` por `V` sem nova versão/histórico é recusado |
| 2.5.2-T10 | `I` → `V` com nova versão e histórico é curado |
| 2.5.2-T11 | A versão anterior permanece legível dentro do histórico |
| 2.5.2-T12 | Escrita direta em `contexto/` é negada pela guarda |
| 2.5.2-T13 | Escrita pelo curador em `contexto/` é aceita *(controle positivo)* |
| 2.5.2-T14 | Conteúdo em `rascunho/` não é tratado como contexto curado |
| 2.5.2-T15 | Recusa de curadoria emite `CuradoriaRecusada` |
| 2.5.2-T16 | Curadoria válida emite `ObjetoContextoCurado` *(controle positivo)* |
| 2.5.2-T-baseline | `--registrado-por AG-01` (com hífen) não passa como autor humano |

Rodam contra uma cópia temporária do template, sem tocar em caso real.

## Integração CTX ↔ P3d — pacote 2.5.3

| ID | Prova |
|---|---|
| 2.5.3-T01 | Classificação oficial válida (`alinhada`) é curada |
| 2.5.3-T02 | Classificação fora da taxonomia de EMCIA-ROT-01 3.9 é recusada |
| 2.5.3-T03 | `divergente` sem `referencia_p3d` é recusado |
| 2.5.3-T04 | `divergente` com `referencia_p3d` inexistente é recusado |
| 2.5.3-T05 | `divergente` com `referencia_p3d` válida é curado |
| 2.5.3-T06 | A referência resolve para o registro `divergencia` correto |
| 2.5.3-T07 | A Regra curada não duplica `documento_diz`/`observado`/`justificativa` |
| 2.5.3-T08 | `estatuto`/`divergencia` (contrato antigo) não existem mais no schema desde o 2.5.1 |
| 2.5.3-T09 | Classificação que não exige `referencia_p3d` (`nao_documentada`) é curada sem ela |
| 2.5.3-T10 | Mudar `classificacao_confronto` sem versão/histórico é recusado; com versão nova é aceito |
| 2.5.3-T11 | Agente como `autor` do registro de confronto é recusado |
| 2.5.3-T12 | Pessoa nomeada como `autor` do registro de confronto é aceita *(controle positivo)* |

Rodam contra uma cópia temporária do template, sem tocar em caso real. A
taxonomia oficial usada nos testes (`alinhada`, `divergente`,
`nao_documentada`, `orfa`, `escrita_inacessivel`) vem de EMCIA-ROT-01 3.9 —
o CTX-01 não define códigos próprios para as classes.

## Bateria formal CTX-V01–CTX-V11 — pacote 2.5.4

Cada validação do EMCIA-CTX-01 3.13 tem um teste negativo e um controle
positivo, extraídos literalmente do documento oficial — a maioria já
implementada pelos pacotes 2.5.1–2.5.3; este pacote formaliza o vínculo
com o código `CTX-Vxx` e fecha as três genuinamente ausentes (V05–V07).

| ID | Regra oficial (EMCIA-CTX-01 3.13) |
|---|---|
| CTX-V01 | Regra possui os sete campos do bloco de decisão |
| CTX-V02 | Registro `I` possui premissa escrita |
| CTX-V03 | Registro `V` possui evidência identificada |
| CTX-V04 | Mudança `I` → `V` cria nova versão |
| CTX-V05 | Todo termo referenciado existe |
| CTX-V06 | Toda entidade referenciada existe |
| CTX-V07 | Toda fonte referenciada existe e possui contrato mínimo |
| CTX-V08 | Escrita em `contexto/` passa pela curadoria prevista |
| CTX-V09 | Autoria de conteúdo e registro são pessoas nomeadas |
| CTX-V10 | Toda nova versão possui data, responsável e motivo da mudança |
| CTX-V11 | `classificacao_confronto` completa e resolvível quando `divergente` |

Cada uma tem um teste `2.5.4-Vxx-N` (negativo) e `2.5.4-Vxx-P` (positivo) em
`testes/ctx_v.py` — 22 verificações — mais `2.5.4-multi`, que confirma a
política de validação acumulativa: um objeto com duas violações simultâneas
(`I` sem premissa e Fonte inexistente) é recusado com as duas causas
relatadas na mesma mensagem, não só a primeira encontrada. A matriz completa
está em `.projectdocs/evidencias/sprint2/2.5.4/matriz-ctx-validacoes.md`.

## Integração P2/P3 → CTX → P4/P5 — pacote 2.5.5

| ID | Prova |
|---|---|
| 2.5.5-T01 | P2 produz candidato CTX em `rascunho/`, sem virar contexto sozinho |
| 2.5.5-T02 | Candidato de P2 sem curadoria não é consumido (`consultar.py` recusa) |
| 2.5.5-T03 | Candidato de P2 curado entra no CTX |
| 2.5.5-T04 | P3b gera Regra candidata rastreável (referencia Termo) |
| 2.5.5-T05 | P3d atualiza vínculo de confronto sem sobrescrever histórico |
| 2.5.5-T05b | Mudança de confronto com histórico correto é aceita *(controle positivo)* |
| 2.5.5-T06 | P4 consome contexto válido via `quadro.py` |
| 2.5.5-T07 | P4 com `contexto/regras/` vazio ainda roda, sinaliza célula crítica vazia |
| 2.5.5-T08 | P4 não reinfere `frequencia`/`consequencia_do_erro` — lê direto do YAML curado |
| 2.5.5-T09 | P5 consome os sete campos centrais via `consultar.py --campo` |
| 2.5.5-T10 | P5 com Regra incompleta (nunca cura, logo nunca é consultável) |
| 2.5.5-T11 | P5 distingue `I` de `V` — `procedencia` exposta explicitamente, nunca mascarada |
| 2.5.5-T12 | P5 com `V` válida |
| 2.5.5-T13 | CTX inválido (referência quebrada) não é consumido |
| 2.5.5-T14 | Falha de curadoria/consumo emite `CuradoriaRecusada` |
| 2.5.5-T15 | Fluxo mínimo P2 → CTX → P4 |
| 2.5.5-T16 | Fluxo mínimo P3 → CTX → P5 |

Rodam contra uma cópia temporária do template, sem tocar em caso real.
Um defeito real de `quadro.py` foi corrigido durante este pacote: o script
tratava `entradas: []` e `excecoes_conhecidas: []` como campos "ausentes"
mesmo quando o schema já os considera válidos sem conteúdo (`required` sem
`nonempty`) — o mesmo tratamento que o script já dava a
`decisor_quando_nao_cobre`. Corrigido para usar a mesma semântica de
presença do schema, em vez de uma regra própria e mais restritiva.

## Verificação consolidada da Ação 2.5 — pacote 2.5.6

| ID | Prova |
|---|---|
| 2.5.6-C01 | D/I/V integrados: D aceita, I sem/com premissa, V sem/com evidência, X recusado |
| 2.5.6-C02 | Termo, Entidade, Regra e Fonte válidos aceitos; Termo inválido recusado |
| 2.5.6-C03 | `autoria_conteudo` ≠ `registrado_por` aceito; agente como autor recusado |
| 2.5.6-C04 | `rascunho/` isolado não é contexto; curado, materializa objeto |
| 2.5.6-C05 | Escrita direta em `contexto/` negada; curadoria autorizada aceita |
| 2.5.6-C06 | Sobrescrita de versão recusada; nova versão com histórico aceita |
| 2.5.6-C07 | P3d referenciado sem duplicar `documento_diz`/`observado`/`justificativa` |
| 2.5.6-C08 | 8 cenários de violação CTX-V (V01,V02,V03,V05,V06,V07,V09,V11) recusados neste caso novo |
| 2.5.6-C09 | Referência válida a Termo/Entidade/Fonte aceita; cada tipo inexistente recusado |
| 2.5.6-C10 | P2 → CTX: candidato em `rascunho/` não é contexto; curado, materializa |
| 2.5.6-C11 | P3 → CTX: Regra levantada (I) e confrontada (V) preservando histórico |
| 2.5.6-C12 | CTX → P4: `quadro.py` consome `contexto/regras/` do caso de controle |
| 2.5.6-C13 | CTX → P5: `consultar.py` retorna sete campos centrais e `procedencia` |
| 2.5.6-C14 | Não reinterpretação: valor lido literal do YAML, sem chamada a LLM |
| 2.5.6-C15 | Eventos: violação D/I/V, agente como autor, bypass e referência quebrada geram trilha |
| 2.5.6-C16 | Percurso integrado: T-100/E-100/F-100/RN-100/DIV-100, do P2 ao P5, um único objeto rastreável |

Diferença em relação às suítes anteriores: `testes/consolidado.py`
constrói **um caso de controle único** (`CTX-TEST-2.5.6-001`) e faz a
Regra central (`RN-100`) atravessar D → tentativa de sobrescrita
recusada → V (v2) → V (v3, divergente, referenciando P3d) dentro do
mesmo teste, em vez de objetos isolados por cenário — é a prova de que a
camada funciona como sistema, não como travas independentes.

## Contrato executável F0–P10 — pacote 2.6.0

Este pacote não implementa P6–P10 operacionalmente. Verifica que o
playbook oficial declara o contrato completo das treze etapas e que o
carregador genérico do núcleo (`playbook.py`) aceita o contrato válido e
recusa fixtures estruturalmente inválidas — sem nunca escrever sobre o
playbook oficial.

| ID | Prova |
|---|---|
| 2.6.0-T01 | Playbook é JSON válido |
| 2.6.0-T02 | Exatamente 13 etapas canônicas |
| 2.6.0-T03 | Todos os IDs de etapa são únicos |
| 2.6.0-T04 | Conjunto esperado F0–P10 presente |
| 2.6.0-T05 | P3b permanece não delegável |
| 2.6.0-T06 | P7 declarada não delegável |
| 2.6.0-T07 | P7 na camada EX4 (humana) em todos os níveis |
| 2.6.0-T08 | P10 é recorrente |
| 2.6.0-T09 | P10 declara necessidade de cadência |
| 2.6.0-T10 | P10 declara necessidade de responsável |
| 2.6.0-T11 | Cinco inegociáveis declarados |
| 2.6.0-T12 | Mapeamento 1→P3a, 2→P7, 3→P8, 4→P9, 5→P10 |
| 2.6.0-T13 | Seis autorizações presentes (E1, E2, E3-D, E3-E, E4, E5) |
| 2.6.0-T14 | E1 = F0 |
| 2.6.0-T15 | E2 = P1/P2/P3a/P3b/P3d |
| 2.6.0-T16 | E3-D = P4/P5 |
| 2.6.0-T17 | E3-E = P5 + condição declarativa de solução agêntica |
| 2.6.0-T18 | E4 = P6/P7 + inegociável 2 |
| 2.6.0-T19 | E5 = P8/P9/P10 + inegociáveis 3/4/5 |
| 2.6.0-T20 | Nenhuma referência a etapa inexistente |
| 2.6.0-T21 | Nenhuma dependência órfã entre inegociáveis/entregáveis |
| 2.6.0-T22 | `portao_pendente` removido de E4/E5 |
| 2.6.0-T23 | D/I/V permanece inalterado |
| 2.6.0-T24 | `playbook.py` aceita o contrato oficial (regressão do carregador) |
| 2.6.0-N01 | Fixture sem P7 → recusado |
| 2.6.0-N02 | E5 só com P9/P10 → estrutura oficial já corrigida; validação semântica completa fica para 2.6.1 (capacidade declarativa OK, validador pendente) |
| 2.6.0-N03 | P10 recorrente sem cadência/responsável → recusado |
| 2.6.0-N04 | Inegociável apontando para etapa inexistente → recusado |
| 2.6.0-N05 | Camada fora de EX1–EX4 → recusada |

`playbook.py` ganhou, neste pacote, checagem genérica (sem vocabulário do
método) de: ID de etapa duplicado, camada fora de EX1–EX4, `depende_de`
referenciando etapa inexistente, portão/inegociável referenciando etapa
ou inegociável inexistente, e etapa recorrente exigindo cadência e
responsável declarados.

## Núcleo genérico de protocolos — pacote 2.6.1

Fortalece `avancar.py`, `guarda.py` e `playbook.py` para impor o contrato
declarado em 2.6.0 sem conhecer semântica EMCIA — nenhuma decisão usa
`if etapa == "P7"` ou equivalente; tudo lê campos genéricos do playbook
(`delegavel`, `depende_de`, `camada`, `recorrente`, `cadencia_obrigatoria`,
`responsavel_obrigatorio`, `condicao`) ou do estado.

| ID | Prova |
|---|---|
| 2.6.1-T01/T01b | Encerrar etapa que não é a corrente → recusado, com evento `RecusaMaquina` |
| 2.6.1-T02 | Encerrar a etapa corrente válida → aceito |
| 2.6.1-T03/T03b | Dependência não satisfeita → recusada por `avancar.py` e por `guarda.py` (G3) |
| 2.6.1-T04 | Dependência satisfeita → prossegue |
| 2.6.1-T05 | Etapa delegável executada por ator permitido → aceito |
| 2.6.1-T06 | Etapa não delegável tentada por agente → recusada (G1) |
| 2.6.1-T07 | Mesma etapa, humano autorizado, sessão registrada → aceito |
| 2.6.1-T08 | Camada fora de EX1–EX4 (fixture) → contrato recusado |
| 2.6.1-T09/T10/T10b | Mecanismo isolado de critério de verificação (`playbook.capacidade_valida()`) — capacidade automatizada sem critério recusada, com critério aceita, não automatizada não exige critério |
| 2.6.1-T11/T12/T12b | Responsável obrigatório ausente ou genérico ("equipe") recusado; pessoa nomeada aceita |
| 2.6.1-T13/T14 | Cadência obrigatória ausente recusada; cadência válida aceita |
| 2.6.1-T15/T16 | Etapa recorrente sem cadência/responsável declarados recusada no carregamento; com o contrato completo aceita |
| 2.6.1-T17 | Inegociável sem satisfação mantém portão fechado |
| 2.6.1-T18 | Tentativa de satisfazer inegociável por escrita direta em `registro/estado.json` recusada |
| 2.6.1-T19/T20/T20b/T20c | Satisfação por caminho autorizado (`--satisfazer-inegociavel`) sem evidência recusada; com evidência aceita, gera evento `InegociavelSatisfeito`, e libera a emissão |
| 2.6.1-T21/T22 | Escrita direta em `registro/` recusada (G5); invocação autorizada dos scripts do núcleo via `Bash` continua funcional |
| 2.6.1-T23/T24 | Regressão da Ação 2.5: `contexto/` continua protegido e a curadoria continua funcional |
| 2.6.1-T25/T26 | Portão com etapa ou inegociável inexistente → contrato inválido |
| 2.6.1-T27/T27b | Condição declarativa suportada avaliada corretamente (satisfeita e não satisfeita) |
| 2.6.1-T28 | Condição com operador desconhecido → recusada explicitamente no carregamento, não ignorada |
| 2.6.1-T29/T30 | Recusa de `avancar`/`emitir` gera evento auditável (`RecusaMaquina`/`RecusaEmissao`) |
| 2.6.1-T31 | Proteção de `caso/` revalidada, sem regressão |
| 2.6.1-T32 | Selo Git revalidado, sem regressão |

Reproduz e corrige o defeito do baseline (2.6-BL12): antes deste pacote,
`avancar.py --encerrar <etapa>` aceitava qualquer etapa declarada no
playbook, não apenas a etapa corrente do caso — uma etapa em `P1` podia
"encerrar" `P5` e o estado pulava direto para `P6`. `2.6.1-T01`
reproduz esse cenário e confirma a recusa.

## P6 e P7 — pacote 2.6.2

Implementa operacionalmente P6 (especificação operacional) e P7 (termo
de autonomia), inteiramente em `eiac-campo/scripts/` — `operacional.py`
e `governanca.py` reaproveitam primitivas genéricas do núcleo
(`estrutura.validar`, `estado.evento`, `estado.autor_e_agente`) sem
introduzir semântica de método em `eiac-nucleo/`.

| ID | Prova |
|---|---|
| 2.6.2-T01/T02 | P6 com entradas válidas aceito; sem campo obrigatório recusado |
| 2.6.2-T03 | P6 não reexecuta P4/P5 (`operacional.py` não invoca outro script) |
| 2.6.2-T04/T05 | Desenho operacional estruturado; saída marcada `proposta`, distinta de validação |
| 2.6.2-T06 | P6 produz especificação (schema textual/lista), não aciona deployment |
| 2.6.2-T07/T08 | P7 com P6 validado aceito; sem P6 (`operacional_ref` não resolve) recusado |
| 2.6.2-T09/T10/T10b | Agente prepara minuta (rascunho→proposto) aceito; agente tenta decidir recusado, com evento `TermoAutonomiaRecusado` |
| 2.6.2-T11/T11b | Humano autorizado decide, evento `AutonomiaDecidida` |
| 2.6.2-T12/T13 | Decisor genérico ("equipe") recusado; pessoa nomeada aceita |
| 2.6.2-T14/T15 | Decisão sem justificativa recusada; decisão completa aceita |
| 2.6.2-T16/T17 | Termo com estrutura mínima; decisor nunca é agente |
| 2.6.2-T18/T19 | Escrita direta em `registro/governanca/` recusada (G5); caminho autorizado funcional |
| 2.6.2-T20–T24 | Fronteira: ação autônoma só após decisão humana; minuta ≠ autorização; `nunca_faz` preservado; gatilhos preservados; exceção/fallback presentes |
| 2.6.2-T25–T27 | Evidência para o inegociável 2: sem termo decidido insuficiente; termo decidido disponível; booleano solto não é o padrão de evidência deste pacote |
| 2.6.2-T28–T30 | Eventos de tentativa de agente, decisão inválida e decisão válida, todos rastreáveis |
| 2.6.2-T31 | Ausência de hard-code comportamental de P6/P7/autonomia/E4 no núcleo |
| 2.6.2-T32/T33 | Regressão da Ação 2.5 e do pacote 2.6.1 |
| 2.6.2-G1a/G1b/G1c | Achado corrigido: skill EX3/EX4 sem sessão bloqueada; com sessão válida da mesma etapa carrega; sessão de outra etapa não libera |

**Achado corrigido neste pacote:** `guarda.py` G1 bloqueava o
carregamento do próprio `SKILL.md` para qualquer etapa EX3/EX4,
independentemente de sessão humana registrada — comportamento
pré-existente (já afetava `hb-confrontar`, `hb-priorizar`,
`hb-classificar`), descoberto ao escrever `hb-operacionalizar`/
`hb-governar`. G1 agora libera o carregamento quando existe sessão
humana válida **para a etapa corrente** — não libera decisão, aprovação
ou fechamento de etapa por agente, que continuam bloqueados por outras
regras (`delegavel:false` em `avancar.encerrar()`,
`operacional.py`/`governanca.py` recusando agente em
`estado: validado`/`decidido`).

Objetos produzidos: `registro/operacional/OP-*.yaml` (estados
`proposta`→`validado`) e `registro/governanca/autonomia/AUT-*.yaml`
(estados `rascunho`→`proposto`→`decidido`) — dois domínios distintos de
`contexto/` (CTX-01, intocado) e de `registro/estado.json` (máquina de
etapas, também intocada em sua semântica).

## P8, P9 e P10 — pacote 2.6.3

Implementa operacionalmente P8 (casos de teste com saída esperada), P9
(métricas contra a linha de base) e P10 (rotina de recalibragem
recorrente), inteiramente em `eiac-campo/scripts/` — `piloto.py`,
`metrica.py` e `calibragem.py` reaproveitam primitivas genéricas do
núcleo (`estrutura.validar`, `estado.evento`, `estado.autor_e_agente`
e, para recorrência/inegociáveis, `avancar.registrar_recorrencia` e
`avancar.satisfazer_inegociavel`, já genéricos desde o 2.6.1) sem
alterar `eiac-nucleo/` — nenhum arquivo do núcleo foi tocado neste
pacote.

| ID | Prova |
|---|---|
| 2.6.3-T01/T02 | P8 com P7 encerrado corretamente aceito; sem sessão de P7 (não delegável) recusado |
| 2.6.3-T03/T04 | Caso de teste completo (Anexo B) aceito; caso sem saída esperada recusado |
| 2.6.3-T05/T05a | Ordem temporal correta (esperado antes de obtido) aceita; saída obtida antes de `esperado_definido_em` recusada (viés retrospectivo) |
| 2.6.3-T06 | Comparação esperado × obtido é determinística |
| 2.6.3-T07 | Caso com resultado divergente do esperado: FAIL do caso, saída esperada preservada |
| 2.6.3-T08 | Tentativa de forjar `resultado` sem a saída bater é recusada |
| 2.6.3-T09 | Casos com saída esperada produzem evidência real para o inegociável 3 |
| 2.6.3-T10/T11 | P9 com P8 revisado e baseline válidos aceito; sem `linha_base_data` recusado |
| 2.6.3-T12/T13 | Métrica de uso aceita como métrica (não satisfaz sozinha o inegociável 4); métrica de resultado válida gravada |
| 2.6.3-T14/T15 | Nota sobre insuficiência de métrica de uso isolada; ao menos uma de resultado disponível |
| 2.6.3-T16 | Cálculo baseline × piloto presente e correto |
| 2.6.3-T17 | Baseline com data posterior ao resultado apurado (inventada depois do piloto) é recusada |
| 2.6.3-T18/T18b | Resultado observado com fatores externos declarados; apuração sem essa declaração é recusada |
| 2.6.3-T19/T20 | Responsável genérico ("equipe") recusado; pessoa nomeada aceita |
| 2.6.3-T21/T22 | Rotina sem cadência recusada; com cadência válida aceita |
| 2.6.3-T23–T26 | Primeiro ciclo persistido; segundo ciclo não sobrescreve; histórico recuperável; ciclo já registrado (sem drift) não aceita sobrescrita |
| 2.6.3-T27–T29 | Ciclo sem drift é caminho positivo; agente detecta e descreve drift; agente recomenda sem decidir |
| 2.6.3-T29b/T29c | Ciclo pendente (drift sem decisão) complementado pela decisão humana no mesmo identificador aceito; segunda decisão sobre ciclo já decidido recusada |
| 2.6.3-T30/T30b | Agente tenta decidir recalibragem recusado, evento `CicloCalibragemRecusado` |
| 2.6.3-T31/T31b | Humano decide recalibragem aceito, evento `DecisaoRecalibragemRegistrada` |
| 2.6.3-T32 | Decisão fora do enum documental (`recalibrar`/`expandir`/`descontinuar`) recusada, não inventada |
| 2.6.3-T33 | Decisão humana possui justificativa, decisor e data rastreáveis |
| 2.6.3-T34 | Drift sem decisão humana permanece pendente, não tratado como resolvido |
| 2.6.3-T35–T40 | Booleano/evidência vazia não satisfaz os inegociáveis 3, 4 e 5; evidência real de P8/P9/P10 satisfaz cada um |
| 2.6.3-T41/T42 | P9 referencia P8 (`piloto_ref`); P10 referencia P9 (`metricas_ref`) |
| 2.6.3-T43/T44 | Insumos rastreáveis para E5 disponíveis; E5 não emite automaticamente neste pacote |
| 2.6.3-G5a–G5c | Escrita direta em `registro/piloto/`, `registro/metricas/`, `registro/calibragem/` recusada pela guarda (G5, genérica) |
| 2.6.3-T45 | Ausência de hard-code comportamental de P8/P9/P10/piloto/baseline/métrica/drift/calibragem no núcleo |
| 2.6.3-T46–T48 | Regressão da Ação 2.5, do 2.6.1 e de P6/P7 |

**Achado corrigido neste pacote:** `calibragem.py::gravar_ciclo`
inicialmente recusava qualquer segunda gravação do mesmo identificador
de ciclo, mesmo quando a primeira gravação era só a detecção de drift
(sem decisão) e a segunda era a decisão humana complementando o mesmo
evento de verificação — bloqueando o fluxo de duas fases que o próprio
caso de controle integrado exigiu (agente detecta e recomenda; humano
decide depois, sobre o mesmo ciclo). Corrigido para permitir
complementar um ciclo *pendente* (drift detectado, sem `decisao`) com a
decisão humana, mantendo a recusa de sobrescrever um ciclo já decidido
ou de alterar os fatos do drift (`drift_descricao`/
`drift_quantificacao`) na complementação — T29b/T29c cobrem os dois
lados.

Objetos produzidos: `registro/piloto/CT-*.yaml` (estados
`rascunho`→`revisado`), `registro/metricas/MET-*.yaml` (estados
`planejada`→`apurada`), `registro/calibragem/CAL-*.yaml` (rotina, sem
estado — Anexo D não define um) e `registro/calibragem/CAL-*-C*.yaml`
(ciclos, com `drift_detectado` e `decisao` opcional) — três domínios
distintos de `contexto/`, de `registro/governanca/` e de
`registro/operacional/` (2.6.2, intocados).

## Catálogo HB/AG — pacote 2.6.4

Formaliza as 18 habilidades (HB) e os 4 agentes lógicos (AG) do
método, materializados como catálogo declarativo em
`eiac-campo/reference/habilidades.json` e `agentes.json`. A resolução
genérica (capacidade↔papel, sem conhecer HB/AG/EMCIA) fica em
`eiac-nucleo/scripts/catalogo.py`, reaproveitando
`playbook.capacidade_valida()` (ESP-01 G6, já genérico desde o 2.6.1).

| ID | Prova |
|---|---|
| 2.6.4-T01–T06 | Catálogo de HB estruturalmente válido; exatamente 18 IDs; conjunto HB-01–18 completo; IDs únicos; nomes presentes; camada válida em todas |
| 2.6.4-T07/T08 | `skill_ref` resolve para as 14 HB com implementação; skill inexistente (fixture) confirmaria recusa |
| 2.6.4-T09/T10 | HB automatizada sem critério recusada; com critério aceita |
| 2.6.4-T11/T12 | Critérios não vagos (extraídos literalmente de CAT-01 Anexo A); toda HB declara `estado_relacao_etapa` |
| 2.6.4-T13–T15 | Exatamente 4 AG; conjunto AG-01–04 completo; IDs únicos |
| 2.6.4-T16/T17 | Todo AG referencia só HB existentes; toda HB automatizada tem ao menos um AG autorizado |
| 2.6.4-T18/T19 | AG tenta HB não autorizada (AG-01×HB-17) recusado; AG executa HB autorizada (AG-04×HB-17) aceito |
| 2.6.4-T20 | Nenhum AG do catálogo recebe camada EX3/EX4 |
| 2.6.4-T21–T24 | Cada AG (01–04) resolve exatamente o conjunto de HB do mapa canônico de CAT-01 Anexo A |
| 2.6.4-T25/T26 | Todas as referências HB do playbook oficial resolvem; referência a HB inexistente recusada |
| 2.6.4-T27/T28 | Catálogo com HB automatizada sem critério bloqueia antes do playbook; cadeia etapa→HB→skill→AG íntegra (P9→HB-17→hb-medir-valor→AG-04) |
| 2.6.4-T29/T30 | Skills com HB no catálogo declaram `hb:` no frontmatter; skills sem HB estão classificadas como infraestrutura (emissão de entregável, etapa humana não delegável) — nenhuma sem classificação |
| 2.6.4-T31 | Skills que materializam mais de uma HB preservam critério individual por HB |
| 2.6.4-T32–T35 | Mecanismo genérico do 2.6.1 recebe HB real sem/com critério; critério recuperável em runtime; não duplicado na etapa do playbook |
| 2.6.4-T36–T38 | Nenhum AG tem autoridade sobre a decisão humana de P7 (HB-14) nem de recalibragem em P10 (HB-18); nenhum AG substitui a sessão de P3b |
| 2.6.4-T39/T40 | Regressão G1: skill EX3/EX4 sem sessão bloqueada; com sessão válida carrega |
| 2.6.4-T41–T43 | Os 4 AG lógicos resolvem sem exigir 4 arquivos físicos; agentes físicos existentes preservam identidade 1:1; implementação física resolve para arquivo real |
| 2.6.4-T44/T45 | `catalogo.py` não expõe caminho de auto-ampliação em runtime; catálogo só muda por edição de arquivo versionado |
| 2.6.4-T46 | Ausência de hard-code HB/AG no núcleo |
| 2.6.4-T47–T50 | Regressão da Ação 2.5, do 2.6.1, de P6/P7 e de P8/P9/P10 |

**Achado registrado, não defeito:** 4 das 18 HB (HB-04, HB-05, HB-06,
HB-13) existem no catálogo formal (CAT-01) mas não são referenciadas
por nenhuma etapa do playbook — o campo `estado_relacao_etapa:
"nao_referenciada_no_playbook"` documenta isso explicitamente, sem
forçar uma associação textual entre HB e etapa que os documentos não
sustentam (a correspondência entregável×passo continua pendência aberta
por decisão, `decisoes/002`). A relação HB→etapa neste catálogo vem
exclusivamente de `playbook.json`, nunca de inferência entre CAT-01 e
MET-01/CAM-01.

## Portões e inegociáveis — pacote 2.6.5

Torna semanticamente verificáveis os cinco inegociáveis (I1–I5, a
partir de artefato real, nunca de flag solta), operacionaliza os seis
portões de emissão (E1, E2, E3-D, E3-E, E4, E5) e materializa os cinco
entregáveis ao cliente em `caso/entregaveis/*.md`.

| ID | Prova |
|---|---|
| 2.6.5-T01/T02/T02b | I1 sem baseline recusado; com baseline válida aceito; apuração `estimado` fora de N1 recusada (MET-01 3.4.3) |
| 2.6.5-T03/T04 | I2 com termo apenas proposto recusado; termo decidido por humano aceito |
| 2.6.5-T05/T06 | I3 sem saída esperada recusado; casos válidos revisados aceito |
| 2.6.5-T07/T08 | I4 só com métrica de uso recusado; métrica de resultado aceito |
| 2.6.5-T09/T09b/T10 | I5 com `responsavel: equipe` recusado em `calibragem.py`; `equipe de TI` (frase composta) recusado no verificador semântico; pessoa nominal aceito |
| 2.6.5-T11/T12 | Flags manuais sem artefato real nunca produzem satisfação; evidência real produz registro rastreável ao verificador |
| 2.6.5-T13–T19 | Portão E1 (par negativo/positivo + materialização) |
| 2.6.5-T20–T27 | Portões E3-D (par) e E3-E (não aplicável / autorizado / negado, materialização consolidada em um único E3) |
| 2.6.5-T28–T31 | Portão E4 (par negativo/positivo + materialização) |
| 2.6.5-T32–T37 | Portão E5 (quatro negativos, um por requisito faltando, + positivo + materialização) |
| 2.6.5-T38–T42 | Emissão sempre aponta para arquivo real; arquivo inexistente recusado; reemissão versiona sem sobrescrever |
| 2.6.5-T43–T47 | E1–E5 materializados contêm as seções obrigatórias do modelo oficial |
| 2.6.5-T48/T49 | Campo obrigatório sem evidência não inventa valor; dado presente é reproduzido literalmente da fonte |
| 2.6.5-T50–T53 | Portão negado gera evento; portão autorizado gera trilha; emissão material referencia arquivo+versão; E3-E não aplicável fica registrado |
| 2.6.5-T54 | Ausência de hard-code de portão/inegociável no núcleo |
| 2.6.5-T55–T60 | Regressão da Ação 2.5, do 2.6.1, de P6/P7, de P8/P9/P10, do catálogo HB/AG e suíte completa |

Objeto novo: `registro/baseline/BL-*.yaml` (linha de base, inegociável
1) — sem schema/ID dedicado em nenhuma fonte oficial (MET-01 3.4.3 só
exige "registrada e datada"; o formato concreto é a tabela de EMCIA-E2
Parte A.3). `BL-nnn` é convenção técnica do Estúdio para
rastreabilidade, não terminologia do método.

## Verificação integral F0–P10 — pacote 2.6.6

Demonstra, em um caso de controle inteiramente novo (nenhum estado
reaproveitado de casos anteriores), o percurso F0→P10 completo: 13/13
etapas, fronteira EX1–EX4 nos quatro pontos críticos (P3b, validação de
P6, decisão de P7, decisão de recalibragem em P10), cinco inegociáveis
satisfeitos a partir de artefato real, seis portões avaliados
corretamente (cenário agêntico, E3-E AUTORIZADO), cinco entregáveis
materializados, proteção de `registro/`/`contexto/` reconfirmada,
ausência de bypass manual e rastreabilidade ponta a ponta de um elemento
central do caso (RN-101 → P4 → P5 → E3 → P6/P7 → P8/P9 → P10 → E5).

| ID | Prova |
|---|---|
| 2.6.6-C01–C04 | Contrato com 13 etapas; caso novo inicia em F0; F0→P1 válido; percurso P1–P5 executa sem falha |
| 2.6.6-C05 | P3b permanece não delegável a agente |
| 2.6.6-C06/C07 | Escrita direta em `contexto/` e em `registro/` continuam recusadas |
| 2.6.6-C08/C09 | P6 é etapa operacional executável; validação exige humano (agente recusado, humano aceito) |
| 2.6.6-C10–C12 | P7 é etapa operacional executável; agente não decide autonomia; humano nominal decide |
| 2.6.6-C13/C14 | P8 produz casos com saída esperada; P9 produz métrica de resultado apurada |
| 2.6.6-C15/C16 | P10 é recorrente; dois ciclos preservados sem sobrescrita |
| 2.6.6-C17/C18 | Agente (AG-04) detecta e registra drift; decisão de recalibragem exige humano |
| 2.6.6-C19–C22 | 18/18 HB resolvíveis; 4/4 AG resolvíveis; fronteira formal AG×HB (negativo/positivo); critérios de verificação presentes nas HB automatizadas |
| 2.6.6-C23–C27 | Cinco inegociáveis (I1–I5) satisfeitos |
| 2.6.6-C28–C35 | Seis autorizações (E1, E2, E3-D, E3-E AUTORIZADO, E4, E5) e cinco entregáveis materiais confirmados |
| 2.6.6-C36/C37 | Recusa de etapa incorreta e de escrita direta geram evento |
| 2.6.6-C38 | Nenhum AG declarado em camada EX3/EX4 |
| 2.6.6-C39 | Trilha integral recuperável (categorias mínimas de evento presentes) |
| 2.6.6-C40 | Log do caso de controle preservado para auditoria de bypass |
| 2.6.6-C41 | Materialização sem evidência (portão fechado) recusada, não inventa conteúdo |
| 2.6.6-C42 | Rastreabilidade ponta a ponta com IDs preservados sem reinvenção |
| 2.6.6-C43 | Regressão completa sem falha inexplicada |

Defeito encontrado e corrigido durante a construção do caso de controle
(não pré-existente à leitura, surgiu ao exercitar pela primeira vez um
ciclo de calibragem com autoria de agente ponta a ponta):
`calibragem.py::checar_autoria()` recusava indevidamente
`declarado_por`/`registrado_por` de agente também para
`ciclo_calibragem`, quando o próprio módulo já documentava que "o agente
pode preparar um ciclo inteiro". Corrigido com uma função dedicada
(`checar_autoria_ciclo()`), sem alterar a autoria da rotina (sempre
humana) nem a vedação de `decisao` a agente.

## Deslocamento da fronteira por nível

Cinco testes cobrem o que CAT-01 seção 3.6 estabelece: **a camada de uma etapa depende do nível do caso.**

| # | Prova |
|---|---|
| 9 | P1 em N3 é `EX3` — habilidade não carrega |
| 10 | A mesma P1 em N1 é `EX2` — carrega |
| 11 | Sem nível apurado, nenhuma etapa após F0 opera |
| 12 | F0 não encerra sem o nível |
| 13 | Playbook com camada plana, sem mapa por nível, é recusado |

O par 9 e 10 é o mais importante do conjunto: mesma etapa, mesma habilidade, resultado oposto conforme o nível. Se os dois passarem juntos, a fronteira desloca.
