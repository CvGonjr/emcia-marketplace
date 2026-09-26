# Ação 3.4 — Correção A9 e A10

## Base e escopo

Base: `v-sprint3-poc.2`, objeto anotado `339034ac7a09c1df847e5eb21a856e62a9908053`, commit `b53fb04bcf4d225080bfbd4a2c525d60fc60b6aa`.
Foram lidos CLAUDE.md, o índice de decisões e as decisões 022 e 023. A decisão 024 já registra A8, por confirmação humana anterior. Preservada essa decisão, **025 registra A9 e 026 registra A10**. O conflito de numeração foi apresentado ao usuário; adotados os próximos números livres sem renumerar o histórico.

Correções restritas aos caminhos de emissão e registro identificados em F2. Núcleo aplica dados do playbook do caso. Nenhum teste existente foi apagado. As edições locais anteriores em `3.1/suite-congelamento.txt` e `3.2/testes-f0.txt` permanecem fora destes commits.

## Lacunas e correções

### A9 — Emissão pelo núcleo sem artefato

Antes, arquivo só era conferido quando o chamador fornecia `--materializar`. O núcleo autorizava emissão com base nos portões, sem documento. Agora cada entregável declara `artefato` e `comando_materializacao`. Arquivo precisa existir, ser arquivo regular legível e conter texto não vazio. O caminho é relativo e interno ao caso; `--materializar` precisa corresponder ao caminho declarado e não permite substituir o documento.

| Portão | Caminho declarado | Comando declarado |
|---|---|---|
| E1 | caso/entregaveis/E1.md | /eiac-campo:emitir |
| E2 | caso/entregaveis/E2.md | /eiac-campo:emitir |
| E3-D | caso/entregaveis/E3.md | /eiac-campo:emitir |
| E3-E | caso/entregaveis/E3.md | /eiac-campo:emitir |
| E4 | caso/entregaveis/E4.md | /eiac-campo:emitir |
| E5 | caso/entregaveis/E5.md | /eiac-campo:emitir |

O código lê tanto o caminho quanto o comando declarado; não conhece o nome do comando do campo. Recusa indica o arquivo esperado e o comando para materializar. Emissões autorizadas sempre gravam arquivo, pessoa autora e versão em `EntregavelEmitido` e no estado. Reemissão incrementa versão. Recusa de emissão mantém `RecusaEmissao`, sem alterar o estado; contrato inválido deixa `TentativaNegada`. `NAO_APLICAVEL` continua produzindo `EntregavelNaoAplicavel`, sem exigir arquivo.

### A10 — Classificação sem caminho de registro

Criados `avancar.py --registrar-campo <etapa> --campo <nome> --valor <valor> --autor <pessoa>` e `/eiac-nucleo:registrar-campo`. As etapas declaram `campos_registraveis`, com `valores` quando houver taxonomia. Campo sem taxonomia aceita texto não vazio; campos internos da máquina são reservados.

O registro só aceita etapa corrente ainda aberta, campo declarado, valor válido e pessoa nomeada. Cada registro produz `CampoRegistrado` com etapa, campo, valor, valor anterior e autor. Cada recusa produz `TentativaNegada` com autoria nominal e preserva o estado. Tentativa de agente recebe como autor o responsável nominal do caso.

A declaração de P5 aceita exatamente:

- `agente`
- `caso isolado`
- `habilitador acoplado`

Fonte: EMCIA-MET-01 §3.4.5, passo 5, conferido com a cópia canônica local de emcia-artefatos (conteúdo idêntico ao empacotado). O documento conserva “Em revisão” e aprovação pendente; a implementação desta taxonomia atende à instrução expressa do usuário e não altera o estado de aprovação do documento.

`hb-classificar` instrui registrar a conclusão confirmada antes de encerrar P5; justificativa escrita permanece no artefato da etapa. A sessão obrigatória de A8 continua exigida. A classificação e suas categorias não aparecem como regra nova no código do núcleo.

## Auditoria de TODOS os campos lidos por entregaveis.py

Foram conferidas todas as leituras do estado, todas as leituras dos arquivos estruturados e os filtros usados na seleção desses arquivos. A única lacuna de caminho de registro era `cumprimentos.P5.classificacao_tecnologica`.

| Entregável/uso | Fonte e campos efetivamente lidos | Caminho de registro | Resultado |
|---|---|---|---|
| Cabeçalho de E1–E5; linha de caso E3 | estado: `caso` | novo-caso.sh | Existente |
| Cabeçalho de E1–E5; E1 | estado: `nivel` | avancar.py --apurar-nivel | Existente |
| Leitor de cumprimento E1/E3 | estado: `cumprimentos`, chaves F0 e P5 | Máquina de etapas; registros pelos comandos abaixo | Existente |
| E1 | `cumprimentos.F0.cumprido`, `autor` | avancar.py --encerrar F0 | Existente |
| E1 | `cumprimentos.F0.eixos` | avancar.py --apurar-nivel --eixos | Existente |
| E3 | `cumprimentos.P5.cumprido` | avancar.py --encerrar P5 | Existente |
| E3 e condição de E3-E | `cumprimentos.P5.classificacao_tecnologica` | avancar.py --registrar-campo P5 --campo classificacao_tecnologica | **Ausente antes; corrigido por A10** |
| E2 | registro/baseline: `indicador`, `valor_atual`, `apuracao`, `data`, `procedencia` | baseline.py --arquivo registro/baseline/BL-001.yaml --ator pessoa | Existente |
| E4 — seleção operacional | registro/operacional: `estado` = validado | operacional.py --arquivo registro/operacional/OP-001.yaml --ator pessoa | Existente |
| E4 — desenho operacional | registro/operacional: `ponto_insercao`, `momento`, `sistema`, `excecao`, `fallback`, `ator_humano` | operacional.py, candidato em rascunho, validação e gravação | Existente |
| E4 — seleção do termo | registro/governanca/autonomia: `estado` = decidido | governanca.py --arquivo registro/governanca/autonomia/AUT-001.yaml --ator pessoa | Existente |
| E4 — decisão de autonomia | registro/governanca/autonomia: `decisor`, `data_decisao`, `justificativa_decisao` | governanca.py, transições e decisão humana | Existente |
| E5 — seleção do piloto | registro/piloto: `estado` = revisado | piloto.py --arquivo registro/piloto/CT-001.yaml --ator pessoa | Existente |
| E5 — parâmetros do piloto | registro/piloto: `modo`, `duracao`, `criterio_aprovacao_escala`, `criterio_aprovacao_escala_definido_em` | piloto.py, candidato validado e gravado | Existente |
| E5 — seleção das métricas | registro/metricas: `tipo` = resultado, `estado` = apurada | metrica.py --arquivo registro/metricas/MET-001.yaml --ator pessoa | Existente |
| E5 — resultados | registro/metricas: `metrica`, `linha_base`, `resultado_apurado`, `resultado_apurado_procedencia` | metrica.py, candidato validado e gravado | Existente |
| E5 — rotina | registro/calibragem: `responsavel`, `cadencia`, `data_primeira_revisao` | calibragem.py --arquivo registro/calibragem/CAL-001.yaml --ator pessoa | Existente |

`Gerado em` vem do relógio, sem campo a registrar. Diretórios e nomes de arquivo são fontes de seleção, não campos de estado. A rotina de E5 exclui arquivos de ciclos pelo nome, preservando o registro existente de calibragem. Nenhum campo de E4 ou E5 precisa ser espelhado em estado.json; seus scripts já gravam os artefatos estruturados. Não foram acrescentados campos sem uso ao playbook.

## Testes novos — negativos primeiro

Antes de mudanças: negativos **51/51** e contexto **11/11**, verdes. Os dois módulos novos foram escritos e executados contra a versão anterior antes da implementação.

| Módulo | Quantidade | Antes | Depois |
|---|---:|---|---|
| testes/emissao_a9.py | 13 métodos | 14 falhas de asserção/subteste e 1 erro em 13 métodos | 13 passaram |
| testes/campos_a10.py | 18 métodos | 20 falhas de asserção/subteste em 18 métodos | 18 passaram |

Contagens da suíte são por método/verificação, não por asserção ou subteste. A9 cobre arquivo ausente, vazio, diretório, caminho divergente, declaração ausente/caminho externo, os demais portões, arquivo existente, materialização explícita, NAO_APLICAVEL sem arquivo, declaração alternativa, reemissão e template. O erro anterior foi a tentativa de ler a referência de arquivo que a emissão antiga gravava como nula.

A10 cobre campo não declarado, valor inválido, agente, etapa futura/passada/desconhecida/encerrada, valor vazio, autor genérico, campo omitido, campo interno reservado, taxonomia inválida e contrato ilegível. Positivos cobrem as três categorias, histórico de substituição, campo livre de outro método, declaração do template e E3 ponta a ponta.

O teste `test_17_e3_partes_a_b_sem_escrita_direta_no_estado` abre caso com novo-caso.sh, apura N2, percorre as etapas com sessão e selo reais, registra a classificação e encerra P5 por comandos. Materializa E3 e confere Partes A/B e os dois eventos E3-D/E3-E. Desde a abertura, o teste apenas lê estado.json; não injeta nenhum campo nesse percurso.

## Antes/depois

| Cenário | Antes | Depois |
|---|---|---|
| Núcleo emite E3-D sem arquivo com portão aberto | Autorizava | Recusa com caminho e comando |
| --materializar aponta para arquivo diferente | Aceitava arquivo informado | Recusa divergência com declaração |
| Emissão autorizada pelo núcleo sem --materializar | Evento sem arquivo/versão | Evento e estado com arquivo/versão |
| E3-E não aplicável, arquivo ausente | NAO_APLICAVEL registrado | Preservado |
| P5 recebe classificação pelo núcleo | Não havia comando | CampoRegistrado por comando validado |
| Campo desconhecido, valor inválido, autor agente, etapa incorreta | Não havia esse registro validado | TentativaNegada; estado preservado |
| E3 com agente, Partes A e B | Preparação dependia de injeção no estado | Percurso inteiro por comandos |

## Ajustes em testes existentes

| Arquivo | Ajustes, sem apagar testes |
|---|---|
| nucleo_2_6_1.py | Artefatos sintéticos explícitos para os testes do motor T20c (E2) e T27 (E3). T27/T27b usam percurso até P4, registrar-campo, sessão e encerramento de P5, sem injeção de classificação. T27b usa outro caso, pois P5 encerrada não admite reclassificação; categoria passa a habilitador acoplado. |
| campo_2_6_5.py | Pré-renderização antes dos portões positivos T14 (E1), T18 (E2), T21/T24 (E3), T30 (E4), T36 (E5). Preparações T21/T22/T24 registram classificação, sessão e encerramento via CLI; isolado passa a caso isolado. T25 lê a classificação resultante. T41 espera versão 2 porque núcleo e campo emitiram; T42 exige precisamente versão anterior + 1, mantendo a conferência de incremento. |
| campo_2_6_6.py | gravar_p5_agentico registra campo, sessão e encerramento por comandos nos dois casos (P6 e E1/E2/E3). Removida a escrita direta para forçar P6 e seu helper sem uso; nenhum teste removido. Pré-renderiza E3 para C30 antes da emissão direta pelo núcleo. |

A primeira suíte integral identificou T42 esperando versão absoluta 2 após três emissões. Corrigida a expectativa para incremento exato da anterior; `suite-primeira.txt` preserva esse achado. A saída final abaixo está verde. O executor confere mensagens de falha além do código, pois campo_2_6_5 pode imprimir falha e devolver zero. Esse comportamento fora do escopo não foi modificado.

## Suíte completa

| Módulo | Verificações | Falhas |
|---|---:|---:|
| negativos.sh | 51 | 0 |
| autoria_responsavel.py | 14 | 0 |
| campo_2_6_2.py | 38 | 0 |
| campo_2_6_3.py | 57 | 0 |
| campo_2_6_4.py | 50 | 0 |
| campo_2_6_5.py | 62 | 0 |
| campo_2_6_6.py | 43 | 0 |
| campos_a10.py | 18 | 0 |
| consolidado.py | 16 | 0 |
| contexto.py | 11 | 0 |
| ctx_v.py | 23 | 0 |
| curadoria.py | 17 | 0 |
| emissao_a9.py | 13 | 0 |
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
| **Total (24 módulos)** | **592** | **0** |

Comparação: **561 anteriores + 13 A9 + 18 A10 = 592**. Nenhuma verificação anterior perdida. `suite.txt` contém comandos, saída integral e contagens por módulo; saídas de antes/depois dos novos módulos e dos testes iniciais estão neste diretório.

## Entrega

- fix(A9): `44b2b5f`.
- fix(A10): `a0f1a50`.
- docs: `8932715` (decisões 025/026, índice, comandos, habilidade e guias).
- docs(evidence): pacote de evidências em commit separado.
- `diff.patch`: diferença exata de v-sprint3-poc.2 até os três commits acima.
- Tag anotada prevista: `v-sprint3-poc.3`, sobre a evidência completa.

Versões finais: núcleo **0.2.25**, campo **0.8.3**, playbook **0.4.6**. Casos existentes precisam atualizar explicitamente seu próprio playbook; não há leitura do playbook do plugin como substituto. As tags anteriores permanecem intactas. Verificação por testes, sem aplicação em campo.
