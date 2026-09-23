# Mapa de documentação — emcia-marketplace

Gerado em: 2026-09-12 (docs-mapper, Pipeline A)

> Atualizado em: 2026-09-23 — pacote 3.2 (decisão 021): retirada da
> execução de contraste, verificação por estados do caso (selo de P2
> exigido por P3b), documentação de etapa 0a e reescrita integral de
> `README.md`/`INSTALACAO.md`. Substitui integralmente o retrato de
> 2026-09-18 abaixo, que já estava defasado em relação ao estado real do
> repositório (Ações 2.5 e 2.6 inteiras, decisões 007–021, Sprint 3 em
> curso).

## O que é o projeto

Marketplace de dois plugins Claude Code que instrumentam um método de engenharia
de IA aplicado a organizações-cliente ("Engenharia de IA de Campo"). O repositório
é a ferramenta; não contém caso nem dado de cliente — casos vivem em repositórios
próprios, abertos via `novo-caso.sh` a partir de `eiac-campo/template-caso/`.

Repositório público: `CvGonjr/emcia-marketplace` (GitHub).

## Separação estrutural

| Plugin | Versão | Papel | Conhece o método? |
|---|---|---|---|
| `eiac-nucleo` | 0.2.21 | guarda de camada, validador de procedência, máquina de etapas, trilha | Não |
| `eiac-campo` | 0.7.2 | habilidades por etapa, comandos, subagentes, template de caso | Sim |

O núcleo lê `registro/playbook.json` do caso e aplica o que ele declara — trocar o
playbook troca o método sem tocar em código. Nenhum vocabulário de base (preset,
plugin, capability, assistant) atravessa para o núcleo.

## O método declarado em dados — playbook v0.4.2

`registro/playbook.json` declara:

- Níveis N1–N3
- Procedência em uma dimensão de três valores: `D` declarado, `I` inferido, `V`
  verificado (conforme CAT-01/GLO-01 — a antiga divergência de três dimensões
  independentes foi resolvida, decisão 006)
- **13 etapas** (contrato completo, congelado em 2.6.0): F0, P1, P2, P3a, P3b
  (não delegável, EX4 por desenho, exige selo posterior ao encerramento de
  P2 — decisão 021), P3d (depende de P3b), P4, P5, P6 (depende de P5), P7
  (depende de P6, não delegável), P8 (depende de P7), P9 (depende de P8),
  P10 (depende de P9, não delegável, recorrente)
- Deslocamento por nível (CAT-01 §3.6): a camada de execução de cada etapa varia
  por N1/N2/N3
- 6 autorizações de emissão (E1, E2, E3-D, E3-E, E4, E5) e 5 itens inegociáveis,
  todos com portão fixo — a correspondência entregável×passo foi resolvida
  (decisões 012/013): E4 = P6/P7, E5 = P8/P9/P10
- Uma pendência de método aberta por decisão (020): cruzamento completo entre
  CAT-01 Anexo A, `reference/habilidades.json` e o playbook

## As três travas (o que o núcleo aplica)

| Trava | Mecanismo | Onde |
|---|---|---|
| T1 procedência | escrita direta em `caso/` negada; tudo passa pelo validador | `guarda.py` G2 + `validar.py` |
| T2 camada | habilidade não delegável não carrega; etapa dependente não abre; etapa sem selo exigido não abre nem encerra | `guarda.py` G1/G3/G7 + `avancar.py` |
| T3 selo | commits do repositório do caso | Git |

Regra de ouro do repositório: nenhuma decisão de camada/procedência passa por
modelo de linguagem — são funções determinísticas sobre dados estruturados.

## Verificação por estados do caso (decisão 021, pacote 3.2)

A execução de contraste (antes: `emcia-contraste`/`eiac-contraste`, uma
execução completa e independente do playbook em repositório próprio,
decisões 014–020) foi retirada do projeto por decisão metodológica. A
comparação entre o que a organização declara e o que o levantamento
presencial confirma passou a ser **interna ao mesmo caso de campo**: o
estado declarado é selado ao fim de P2; P3b/P3d produzem o estado
verificado.

Mecanismo de código: `playbook.json` marca `{"exige_selo_apos": "P2"}`
em P3b. O núcleo aplica isso genericamente, sem citar "P2" nem "P3b" em
código — `playbook.selo_apos_etapa()` compara a ordem de eventos
`EtapaEncerrada`/`SeloAplicado` na trilha (`estado.eventos()`), chamada
por `guarda.py` (G7, bloqueia abertura da skill) e por
`avancar.py::encerrar()` (bloqueia fechamento).

O código de isolamento núcleo × contraste em `guarda.py` (marcador
`execucao: contraste`) e `selar.py` (carimbo `componente.variante`) não
foi removido nesta rodada — permanece funcional, mas passou a proteger
contra uma execução que não é mais parte do fluxo declarado do projeto.
Fica registrado como candidato a remoção em decisão futura.

## Material público da etapa 0a (regra documental, sem trava de código)

O levantamento público sobre a organização e o setor, feito na etapa 0a
do protocolo de habilitação (EMCIA-HAB-01, anterior a F0), não entra no
caso nesse momento — é coletado fora do repositório e só é gravado
depois da abertura (etapa 0d), com marca `I · tipo_fonte: externa`, URL
e limite da fonte. Documentado em `README.md` e `INSTALACAO.md`; não há
mecanismo automatizado que force isso, por design (regra de processo,
não de código).

## Inventário de arquivos (atualizado)

### Raiz

- `README.md` — instalação, percurso de 13 etapas, verificação por estados do caso, as três travas, portões E1–E5, testes negativos
- `INSTALACAO.md` — guia passo a passo com verificação a cada etapa, oito testes negativos
- `CLAUDE.md` — regras invioláveis para quem edita o repositório
- `CTX-01-instrumento-camada-contexto.md` — instrumento de referência (camada de contexto), idêntico à cópia em `eiac-campo/reference/`
- `novo-caso.sh` — abre um caso a partir do template, exige `--responsavel`, commit inicial não-fatal
- `.claude-plugin/marketplace.json` — registro dos dois plugins
- `decisoes/` — 21 decisões registradas (README.md é o índice)
- `testes/` — suíte acumulada (`negativos.sh` + ~18 módulos Python por pacote/frente), README com detalhamento

### eiac-nucleo/ (agnóstico de método) — v0.2.21

- `scripts/`: `avancar.py`, `estado.py`, `guarda.py`, `playbook.py`, `curar.py`, `validar.py`, `selar.py`, `consultar.py`, `catalogo.py`, `estrutura.py`, `fronteira.py`, `quadro.py`, `esforco.py`
- `hooks/hooks.json` — registra as travas automaticamente com o plugin
- `commands/`: `estado`, `apurar-nivel`, `gravar`, `curar`, `registrar-sessao`, `registrar-recorrencia`, `satisfazer-inegociavel`, `encerrar`, `emitir`, `selar`, `consultar`, `quadro`, `esforco`, `fronteira`

### eiac-campo/ (é o método) — v0.7.2

- `commands/`: `enquadrar`, `mapear-contexto`, `mapear-fontes`, `medir`, `confrontar`, `priorizar`, `classificar`, `operacionalizar`, `governar`, `pilotar`, `medir-valor`, `recalibrar`, `emitir`
- `agents/`: `classificador-tecnologico.md`, `extrator-documental.md`
- `skills/hb-*`: 18 habilidades (F0–P10 completo, incluindo `hb-emitir-e1..e5`)
- `scripts/`: `operacional.py`, `governanca.py`, `piloto.py`, `metrica.py`, `calibragem.py`, `baseline.py`, `inegociaveis.py`, `entregaveis.py`
- `reference/`: `CTX-01-instrumento-camada-contexto.md`, `gates.md`, `procedencia.md`, `habilidades.json`, `agentes.json`, `metodo/` (16 documentos controlados, pacote versionado com manifesto SHA-256)
- `template-caso/`: `CLAUDE.md`, `registro/{estado.json,playbook.json,*.schema.json}`, `contexto/{entidades,fontes,regras,termos}` (modelos YAML)

## Decisões registradas (decisoes/) — 21 decisões

Estado atual (ver `decisoes/README.md` para o índice completo):

- **Firmes:** 001 dois plugins, 002 playbook no caso, 003 chat sem autoridade
  de escrita, 005 camada por nível, 007 um repo Git por caso, 008 cliente
  nunca fala com agente, 009 habilidades remetem (não reproduzem) o método,
  011 testes negativos primeiro, 012 E3 dividido, 013 correspondência
  entregável×passo fixada, **021 retirada da execução de contraste e
  verificação por estados do caso**
- **Resolvida:** 006 procedência — D/I/V, conforme CAT-01
- **Substituídas:** 004 (janela da antítese, por 021), 014–020 (execução de
  contraste e seu aparato de isolamento, todas por 021)
- **Proposta:** 010 três zonas de escrita
- **Pendente de decisão de método:** 020 (pendência única de correspondência
  CAT-01/catálogo/playbook)

## Testes

`testes/negativos.sh` — suíte acumulada de travas e controles positivos
(regressão completa desde o baseline, incluindo G1–G7, ISO-selo,
verificação por estados do caso). Cada pacote/frente de trabalho também
tem um módulo Python dedicado em `testes/` (`nucleo_2_6_1.py`,
`campo_2_6_2.py` … `campo_2_6_6.py`, `autoria_responsavel.py`,
`esforco.py`, `metodo_empacotado.py`, `verificacao_por_estados.py`
entre outros). Regra do projeto: falha na suíte é regressão de trava —
conserta-se a trava, não o teste. Roda no CI a cada push.

## Cobertura Diátaxis (avaliação)

| Tipo | Estado | Onde |
|---|---|---|
| Tutorial | ✅ | `INSTALACAO.md` (passo a passo com verificação) |
| How-to | ✅ | `README.md` (abrir caso, percurso, atualização) |
| Referência | ✅ | `decisoes/`, `eiac-campo/reference/`, `playbook.json`, `plugin.json` |
| Explicação | ⚠️ parcial | a razão de cada trava está espalhada entre README e decisões; não há um documento único de arquitetura/"por quê" |

## Documentos canônicos do método

`eiac-campo/reference/metodo/` contém o pacote operacional versionado dos
16 documentos controlados usados na execução (decisão 017), com manifesto
SHA-256 — cópia read-only consumida pelo campo; nenhum documento é
duplicado para fora do marketplace.

## Lacunas identificadas (revisão 2026-09-23)

- Não há doc de arquitetura consolidada ligando guarda→validador→playbook→selo
  num só lugar (hoje é preciso ler `guarda.py`, `avancar.py`, `selar.py` e o
  README juntos).
- Decisão 020 (cruzamento CAT-01 Anexo A × catálogo × playbook) segue aberta,
  aguardando decisão humana de método.
- O aparato de isolamento núcleo×contraste (`guarda.py`, `selar.py`) não foi
  removido nesta rodada apesar de a execução de contraste ter sido retirada
  do projeto — candidato explícito a decisão de remoção futura (ver seção
  acima).
- 4/18 HB (HB-04, HB-05, HB-06, HB-13) seguem sem implementação física
  própria — catálogo completo e resolvível, mas sem skill dedicada; nenhuma
  é exigida pelo contrato F0–P10 congelado.
