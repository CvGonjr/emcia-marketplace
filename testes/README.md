# Testes

```bash
bash testes/negativos.sh
```

Trinta e três verificações: as 26 do baseline e sete verificações do contrato
canônico D/I/V. Há negativas e controles positivos — o que é bem formado
precisa passar, senão a trava está apenas quebrada.

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

O total acumulado é de 129 verificações.

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
