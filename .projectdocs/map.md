# Mapa de documentação — emcia-marketplace

Gerado em: 2026-09-12 (docs-mapper, Pipeline A)

> Atualizado em: 2026-09-18 — D/I/V normalizado no pacote 2.5.0; modelos
> Termo, Entidade, Regra e Fonte alinhados ao CTX-01 v0.4 no pacote 2.5.1.

## Atualização da Sprint 2

- `eiac-nucleo` 0.2.7: validador estrutural genérico orientado por schema.
- `eiac-campo` 0.3.4: quatro modelos CTX e
  `registro/contexto.schema.json`.
- Suíte acumulada: 44 verificações — 33 de regressão e 11 estruturais CTX.
- Evidências: `.projectdocs/evidencias/sprint2/2.5.0/` e `2.5.1/`.
- O conteúdo abaixo preserva o retrato original produzido em 12/09/2026;
  esta atualização registra somente a evolução diretamente relacionada.

## O que é o projeto

Marketplace de dois plugins Claude Code que instrumentam um método de engenharia
de IA aplicado a organizações-cliente ("Engenharia de IA de Campo"). O repositório
é a ferramenta; não contém caso nem dado de cliente — casos vivem em repositórios
próprios, abertos via `novo-caso.sh` a partir de `eiac-campo/template-caso/`.

## Separação estrutural

| Plugin | Versão | Papel | Conhece o método? |
|---|---|---|---|
| `eiac-nucleo` | 0.2.0 | guarda de camada, validador de procedência, máquina de etapas, trilha | Não |
| `eiac-campo` | 0.3.0 | habilidades por etapa, comandos, subagentes, template de caso | Sim |

O núcleo lê `registro/playbook.json` do caso e aplica o que ele declara — trocar o
playbook troca o método sem tocar em código. Nenhum vocabulário de base (preset,
plugin, capability, assistant) atravessa para o núcleo.

## Inventário de arquivos

### Raiz
- `README.md` — visão de instalação, percurso de etapas, as três travas, testes negativos
- `INSTALACAO.md` — guia passo a passo com verificação a cada etapa
- `CLAUDE.md` — regras invioláveis para quem edita o repositório (não para o método)
- `CTX-01-instrumento-camada-contexto.md` — instrumento de referência (camada de contexto)
- `novo-caso.sh` — abre um caso a partir do template, commit inicial não-fatal
- `.claude-plugin/marketplace.json` — registro dos dois plugins
- `decisoes/` — 12 decisões registradas, uma por arquivo (`README.md` é o índice)
- `testes/negativos.sh` — 7 testes negativos (hooks) + README

### eiac-nucleo/ (agnóstico de método)
- `scripts/`: `avancar.py`, `estado.py`, `guarda.py`, `playbook.py`, `quadro.py`, `validar.py` (508 linhas ao todo)
- `hooks/hooks.json` — registra as travas automaticamente com o plugin
- `commands/`: `emitir`, `encerrar`, `estado`, `gravar`, `quadro`, `registrar-sessao`

### eiac-campo/ (é o método)
- `commands/`: `classificar`, `confrontar`, `enquadrar`, `mapear-contexto`, `mapear-fontes`, `medir`, `priorizar`
- `agents/`: `classificador-tecnologico.md`, `extrator-documental.md`
- `skills/hb-*`: 13 habilidades (enquadrar, mapear-contexto, extrair-regras, levantar-regras, medir, confrontar, priorizar, classificar, emitir-e1..e5)
- `reference/`: `CTX-01-instrumento-camada-contexto.md`, `gates.md`, `procedencia.md`
- `template-caso/`: `CLAUDE.md`, `registro/{estado.json,playbook.json}`, `contexto/{entidades,fontes,regras,termos}` (modelos YAML)

## Playbook do caso (o método declarado em dados)

`registro/playbook.json` (v0.3.0, ref. EMCIA-MET-01/CAT-01) declara:
- Níveis N1–N3, três dimensões de procedência (contexto/origem/apuração)
- 8 etapas com habilidade, camada por nível e modalidade: F0, P1, P2, P3a, P3b
  (não delegável, EX4 por desenho), P3d (depende de P3b), P4, P5
- Deslocamento por nível (CAT-01 §3.6): até onde a preparação é automatizada e a
  partir de onde a verificação é obrigatória, varia por N1/N2/N3
- 6 entregáveis (E1–E5, com E3 dividido em D/E) e 5 inegociáveis
- 3 pendências abertas **por decisão**, não por falta de tempo: correspondência
  entregável×passo, conflito de procedência com CAT-01/GLO-01, P6–P10 sem habilidade

## As três travas (o que o núcleo aplica)

| Trava | Mecanismo | Onde |
|---|---|---|
| T1 procedência | escrita direta em `caso/` negada; tudo passa pelo validador | `guarda.py` G2 + `validar.py` |
| T2 camada | habilidade não delegável não carrega; etapa dependente não abre | `guarda.py` G1/G3 |
| T3 selo | commits do repositório do caso | Git |

Regra de ouro do repositório: nenhuma decisão de camada/procedência passa por
modelo de linguagem — são funções determinísticas sobre dados estruturados.

## Decisões registradas (decisoes/)

12 decisões, formato contexto→decisão→consequência. Estado atual:
- **Firmes (10):** 001 dois plugins, 002 playbook no caso, 003 chat sem
  autoridade de escrita, 004 antítese entre P2/P3a, 005 camada por nível,
  007 um repo Git por caso, 008 cliente nunca fala com agente, 009 habilidades
  remetem (não reproduzem) o método, 011 testes negativos primeiro, 012 E3
  dividido + termo de autonomia no E4
- **Em conflito (1):** 006 procedência em três dimensões — conflita com CAT-01,
  precisa de decisão humana
- **Proposta (1):** 010 três zonas de escrita

## Testes

`testes/negativos.sh` — 7 testes que prova que cada trava recusa (leitura de
skill não-delegável durante caso, escrita direta em `caso/`, mesma coisa via
Bash, asserção sem origem, `encerrar` sem sessão registrada, `emitir` com
etapas pendentes, `--autor` de agente). Regra do projeto: falha na suíte é
regressão de trava — conserta-se a trava, não o teste. Roda no CI a cada push.

## Histórico (git log)

1. `b83610b` marketplace emcia: núcleo e playbook de campo (inicial)
2. `93ac18c` testes negativos, CI, correção do abrir-caso, aviso de diretório
3. `b96a7e0` novo-caso.sh substitui abrir-caso; commit inicial não-fatal
4. `60a69c1` camada resolvida por nível (CAT-01 3.6); núcleo 0.2.0, campo 0.3.0
5. `26b06e4` marca scripts como executáveis
6. `8df9d81` registro de decisões e CLAUDE.md da raiz (HEAD)

Projeto jovem (6 commits), em consolidação da arquitetura de travas.

## Cobertura Diátaxis (avaliação)

| Tipo | Estado | Onde |
|---|---|---|
| Tutorial | ✅ | `INSTALACAO.md` (passo a passo com verificação) |
| How-to | ✅ | `README.md` (abrir caso, percurso, atualização) |
| Referência | ✅ | `decisoes/`, `eiac-campo/reference/`, `playbook.json`, `plugin.json` |
| Explicação | ⚠️ parcial | a razão de cada trava está espalhada entre README e decisões; não há um documento único de arquitetura/"por quê" |

## Documentos canônicos do método (docs/)

Chegaram depois do primeiro mapeamento — não estão sob controle de versão ainda
(`docs/` aparece como não rastreado no `git status`). São os documentos
controlados que o playbook e as decisões do repositório citam por sigla; até
agora só existiam como referência textual, sem o conteúdo presente no repo.

| Sigla | Arquivo | Fase/Passo | Estado |
|---|---|---|---|
| EMCIA-MET-01 | `EMCIA-MET-01-documento-do-metodo.md` | F0–F4, todos os passos | Em revisão |
| EMCIA-CAT-01 | `EMCIA-CAT-01-fronteira-de-delegacao.md` | F0–F4, todos os passos | Em revisão |
| EMCIA-GLO-01 | `EMCIA-GLO-01-glossario-do-metodo.md` | Todas | Em revisão |
| EMCIA-HAB-01 | `EMCIA-HAB-01-protocolo-de-habilitacao.md` | Anterior a F0 | Em revisão |
| EMCIA-TRI-01 | `EMCIA-TRI-01-instrumento-de-triagem.md` | F0 — Triagem | Em revisão |
| EMCIA-FER-01 | `EMCIA-FER-01-quadro-de-ferramentas.md` | F0–F4, todos | Em revisão |
| EMCIA-VER-01 | `EMCIA-VER-01-plano-de-verificacao.md` | N/A (verificação do método em si) | Em revisão |
| EMCIA-E1 | `EMCIA-E1-ficha-de-enquadramento.md` | F0 | Em revisão |
| EMCIA-E2 | `EMCIA-E2-diagnostico-e-oportunidade.md` | F1, passos 1–3 | Em revisão |
| EMCIA-E3 | `EMCIA-E3-blueprint-da-solucao.md` | F2, passos 4–5 | Em revisão |
| EMCIA-E4 | `EMCIA-E4-guia-operacional.md` | F3, passos 6–7 | Em revisão |
| EMCIA-E5 | `EMCIA-E5-relatorio-de-piloto.md` | F4, passos 8–10 | Em revisão |

Todos os 12 têm responsável único (Celso do Vale) e aprovação pendente.

### O que esses documentos confirmam sobre as pendências abertas

- **CAT-01 §3.6 "Deslocamento da fronteira por nível"** é a fonte que o
  `playbook.json` cita (`deslocamento_por_nivel.referencia`). Conteúdo real:
  N1 automatiza até o passo 4 (verificação a partir do 5), N2 até o passo 2
  (verificação a partir do 3), N3 só na fase F0 (verificação a partir do
  passo 1). Isso bate com o que o playbook implementa — a referência é válida.
- **decisoes/006 (procedência) está mesmo em conflito, agora confirmado com
  texto em mãos:** CAT-01 §3.5.4 e GLO-01 §3.4 fixam procedência como
  **uma** dimensão de três valores — `[D]` declarado, `[I]` inferido, `[V]`
  verificado. O `playbook.json` deste repo implementa **três dimensões
  independentes** (contexto/origem/apuração), cada uma com seu próprio
  vocabulário, incluindo valores que não existem em CAT-01/GLO-01 (`externo`,
  `antitese`, `campo`, `livre`, `medido/calculado/estimado`). Não é
  divergência cosmética — são dois modelos de dados incompatíveis para o
  mesmo conceito. Continua exigindo decisão humana, como já registrado; o
  código não deve resolver isso silenciosamente.
- **CAT-01 Anexo A (catálogo de agentes e habilidades)** é candidato a
  conferir contra as 13 skills `hb-*` e os 2 agentes de `eiac-campo/` —
  não conferido neste mapeamento, ver lacunas abaixo.
- O método canônico tem **5 fases (F0–F4) e 10 passos**; o playbook do
  template de caso só declara **8 etapas (F0, P1, P2, P3a, P3b, P3d, P4,
  P5)** — isso é exatamente a pendência já registrada no `playbook.json`
  ("P6 a P10 sem habilidade: instrumentos ausentes") e agora tem contraparte
  documental: E4 e E5 (guia operacional e relatório de piloto) descrevem os
  passos 6–10 que ainda não têm habilidade no plugin.

## Lacunas identificadas

- Não há doc de arquitetura consolidada ligando guarda→validador→playbook num
  só lugar (hoje é preciso ler `guarda.py`, `validar.py` e o README juntos).
- `eiac-nucleo/README.md` e `testes/README.md` existem mas não foram lidos
  neste mapeamento — candidatos a checar na próxima passada.
- Duas pendências de método seguem abertas por decisão (não é lacuna de doc,
  é lacuna de método aguardando decisão humana — ver decisoes/006 e README).
- `docs/` (os 12 documentos canônicos EMCIA-*) ainda não está sob controle de
  versão (`git status` mostra como não rastreado) — vale decidir se entra no
  repositório do marketplace ou fica fora dele por design (o README diz "este
  repositório é a ferramenta, não contém caso nem dado de cliente"; os
  documentos do método não são dado de cliente, então a exclusão não parece
  intencional, mas não commitei nada — decisão do usuário).
- CAT-01 Anexo A (catálogo de agentes/habilidades) não foi conferido contra
  as 13 skills `hb-*` reais de `eiac-campo/skills/` — checar se cobertura
  bate 1:1 ou se há desvio.
