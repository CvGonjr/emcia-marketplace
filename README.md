# emcia — marketplace de plugins

Dois plugins, e a separação entre eles é o argumento arquitetural do projeto.

| Plugin | Contém | Conhece o método |
|---|---|---|
| **eiac-nucleo** | Guarda de camada, validador de procedência, máquina de etapas, trilha | **Não** |
| **eiac-campo** | Habilidades por etapa, comandos, subagentes, template de caso | É o método |

O núcleo lê o playbook do caso e aplica o que ele declara. Trocar o playbook troca o método sem tocar em uma linha de código — é o que sustenta a afirmação de que o método é independente da ferramenta.

Repositório: [github.com/CvGonjr/emcia-marketplace](https://github.com/CvGonjr/emcia-marketplace)

## Instalação

```
/plugin marketplace add CvGonjr/emcia-marketplace
/plugin install eiac-nucleo@emcia
/plugin install eiac-campo@emcia
```

As hooks do núcleo registram automaticamente. A trava viaja com o plugin, não com o `settings.json` de cada operador.

## Habilitação anterior ao caso

O comando `/eiac-campo:habilitacao <expediente>` conduz a coleta administrativa
via Tally, rodadas de esclarecimentos, preparação dos três documentos HAB e
registro da conferência das assinaturas. A assinatura ocorre pelo painel da
ferramenta escolhida pelo cliente, sem integração.

Antes da sessão, o engenheiro inicializa o expediente fora de qualquer repositório:

```bash
python3 eiac-campo/scripts/habilitacao.py iniciar \
  --expediente "$HOME/habilitacoes/HAB-0001" --id HAB-0001 \
  --caso caso-0001 --responsavel "Nome Sobrenome"
```

A [referência de habilitação](eiac-campo/reference/habilitacao.md) descreve os
formatos de entrada, as condições prévias ao MCP, a geração dos PDFs com
Chrome/Chromium instalado e os registros de revisão humana. Os templates são
lidos do checkout canônico de `emcia-artefatos` e preservados com hash.
O expediente reserva o identificador do caso, mas não o abre nem libera F0.

## Abrir um caso

```bash
~/projetos/emcia-marketplace/novo-caso.sh medic-plus --responsavel "Nome Sobrenome"
cd ~/casos/medic-plus && claude
```

O script copia o template, fixa `responsavel` em `registro/estado.json` (a autoria de todo registro do caso vem daqui, nunca de um argumento informado durante a sessão — ver decisão 019), preenche o nome no registro e no `CLAUDE.md`, cria `metodo/`, `rascunho/` e `caso/`, e faz o commit inicial. Destino padrão é `~/casos/<nome>`; um segundo argumento posicional muda a base.

`--responsavel` é obrigatório e recusa nome vazio, placeholder, código de agente ou coletivo genérico ("equipe", "área" etc.). É a única identidade humana que os scripts do núcleo (`validar.py`, `curar.py`, `selar.py`) usam como autor — mesmo que outro valor seja informado a cada chamada.

Um alias deixa mais curto:

```bash
alias novocaso='~/projetos/emcia-marketplace/novo-caso.sh'
```

Antes de começar, copie os documentos do método para `metodo/` (o pacote controlado vive em `eiac-campo/reference/metodo/`, com manifesto SHA-256 — ver "Material público da etapa 0a" abaixo para o que **não** entra nessa cópia).

**A sessão precisa estar dentro do caso.** O núcleo lê `registro/estado.json` do diretório corrente — de fora, não há guarda nem validador.

## Percurso — 13 etapas, F0 a P10

| Comando | Etapa | Camada (N2) | Modalidade | Depende de |
|---|---|---|---|---|
| `/eiac-campo:enquadrar` | F0 | EX1 | assíncrono | — |
| `/eiac-campo:mapear-contexto` | P1 | EX2 | vídeo | — |
| `/eiac-campo:mapear-fontes` | P2 | EX2 | assíncrono | — |
| `/eiac-campo:medir` | P3a | EX3 | remoto | — |
| — | P3b | **EX4 · sem comando, por desenho** | presencial | selo posterior ao encerramento de P2* |
| `/eiac-campo:confrontar` | P3d | EX3 | remoto | P3b |
| `/eiac-campo:priorizar` | P4 | EX3 | vídeo | — |
| `/eiac-campo:classificar` | P5 | EX3 | vídeo | — |
| `/eiac-campo:operacionalizar` | P6 | EX3 | presencial ou remoto | P5 |
| `/eiac-campo:governar` | P7 | **EX4 · decisão humana registrada** | — | P6 |
| `/eiac-campo:pilotar` | P8 | EX3 | conforme nível | P7 |
| `/eiac-campo:medir-valor` | P9 | EX3 | conforme nível | P8 |
| `/eiac-campo:recalibrar` | P10 | **EX4 · decisão humana registrada, recorrente** | conforme nível | P9 |

\* P3b não abre nem encerra sem um evento `SeloAplicado` posterior ao encerramento de P2 — declarado no playbook (`"exige_selo_apos": "P2"` em P3b), aplicado genericamente pelo núcleo (`playbook.selo_apos_etapa()`, usado por `guarda.py` na abertura e por `avancar.py` no encerramento). Ver "Verificação por estados do caso" abaixo.

A camada de uma etapa desloca por nível (N1/N2/N3, CAT-01 §3.6) — a tabela acima mostra N2; `/eiac-nucleo:fronteira` mostra a camada real do caso aberto.

**Sessão antes de encerrar:** o playbook do caso declara a exigência por
camada em `encerramento_por_camada`. EX3 e EX4 exigem sessão humana
registrada da própria etapa; EX1 e EX2 não. Em N2, isso inclui P3a, P3d,
P4 e P5. Registre a sessão enquanto a etapa for a corrente, com
`/eiac-nucleo:registrar-sessao <etapa> <participantes>`, antes de chamar
`/eiac-nucleo:encerrar <etapa>`. Etapa futura ou já encerrada não aceita
sessão, e sessão de outra etapa não libera o encerramento.

O núcleo resolve a camada pelo nível apurado e aplica essa declaração,
mesmo se a habilidade nunca tiver sido carregada. A falta de sessão
produz `TentativaNegada`, nomeando etapa, camada, nível e modalidade.
Em P3b, a conferência da sessão vem antes da trava de selo de P2, que
permanece exigida (decisões 024 e 021).

E os comandos de núcleo, que valem em qualquer playbook:

`/eiac-nucleo:estado` · `/eiac-nucleo:apurar-nivel` · `/eiac-nucleo:gravar` · `/eiac-nucleo:curar` · `/eiac-nucleo:registrar-sessao` · `/eiac-nucleo:registrar-campo` · `/eiac-nucleo:registrar-recorrencia` · `/eiac-nucleo:satisfazer-inegociavel` · `/eiac-nucleo:encerrar` · `/eiac-nucleo:emitir` · `/eiac-nucleo:selar` · `/eiac-nucleo:consultar` · `/eiac-nucleo:quadro` · `/eiac-nucleo:esforco` · `/eiac-nucleo:fronteira`

## Campos da etapa e artefatos de emissão

Antes de encerrar P5, registre a classificação confirmada pela pessoa:

```text
/eiac-nucleo:registrar-campo P5 classificacao_tecnologica "agente"
```

O playbook declara os campos aceitos por etapa em `campos_registraveis` e a
taxonomia em `valores`. No passo 5: `agente`, `caso isolado` ou
`habilitador acoplado`. O registro só aceita a etapa corrente ainda aberta e
autor pessoa nomeada; produz `CampoRegistrado`. Campo não declarado, valor
fora da taxonomia, autor agente ou etapa incorreta produzem `TentativaNegada`.

Cada entregável declara `artefato` e `comando_materializacao`. O núcleo recusa
emissão sem o arquivo esperado, indicando seu caminho e `/eiac-campo:emitir`.
Esse comando materializa a partir dos registros reais do caso. E3-D/E3-E
compartilham `caso/entregaveis/E3.md`; `NAO_APLICAVEL` dispensa arquivo e fica
registrado. Toda emissão autorizada guarda arquivo, versão e pessoa autora.

Casos existentes atualizam explicitamente seu próprio playbook; não recebem
essas declarações do plugin automaticamente.

## Verificação por estados do caso

A comparação entre o que a organização declarou e o que o levantamento presencial confirma não roda como execução externa: é interna ao mesmo caso. O estado declarado é selado ao fim de P2 (antes do levantamento presencial); P3b/P3d produzem o estado verificado. `/eiac-nucleo:quadro` cruza os dois — célula crítica vazia no estado declarado selado é o resultado esperado quando o levantamento presencial ainda não confirmou as regras de baixa frequência e alta consequência que os documentos não registram (CTX-01 §8).

A trava de código dessa comparação é única: P3b não abre, nem encerra, sem o selo de P2. Sem selo, `/eiac-nucleo:estado` mostra a etapa presa em P3b e a mensagem nomeia exatamente qual selo falta.

## Material público da etapa 0a

O levantamento público sobre a organização e o setor, feito na etapa 0a do protocolo de habilitação (EMCIA-HAB-01, anterior a F0), **não entra no caso nesse momento**. Ele é coletado fora do repositório do caso e só é gravado depois da abertura (etapa 0d — caso aberto e selado), pelo caminho normal de curadoria (`/eiac-nucleo:curar` ou `/eiac-nucleo:gravar`, conforme o tipo de objeto), com marca `I · tipo_fonte: externa`, URL e limite da fonte explícitos — o mesmo formato que `eiac-campo/reference/procedencia.md` já define para qualquer inferência apoiada em fonte externa. Não há automatismo que grave esse material antes da abertura; é regra documental, não trava de código.

## As três travas

| Trava | Mecanismo | Onde |
|---|---|---|
| **T1 procedência** | Escrita direta em `caso/` negada; todo conteúdo passa pelo validador | `guarda.py` G2 + `validar.py` |
| **T2 camada** | Habilidade de etapa não delegável não carrega; etapa dependente não abre; encerramento confere sessão conforme a camada declarada | `guarda.py` G1 e G3 + `avancar.py` |
| **T3 selo** | Commits do repositório do caso | Git |

## Testes negativos — faça no primeiro dia

Antes de confiar em qualquer coisa, prove que ela recusa.

| # | Tente | Esperado |
|---|---|---|
| 1 | Ler `hb-levantar-regras/SKILL.md` durante um caso, sem sessão registrada | Bloqueio, `TentativaNegada` no log |
| 2 | Escrever direto em `caso/qualquer.md` | Bloqueio, com instrução de usar o validador |
| 3 | Gravar rascunho com asserção sem procedência D/I/V | Recusa, `AssercaoRecusada` no log |
| 4 | `/eiac-nucleo:encerrar P3b` sem sessão registrada | Recusa |
| 5 | `/eiac-nucleo:encerrar P3b` (ou ler `hb-levantar-regras/SKILL.md`) antes de selar após P2 | Recusa, nomeando o selo que falta |
| 6 | `/eiac-nucleo:emitir E2` com etapas pendentes | Recusa, nomeando as etapas |
| 7 | `--autor AG05` em qualquer script | Recusa (autoria efetiva vem de `responsavel`, não do argumento) |

**Se algum passar, a trava não existe.** Há relatos públicos de que o bloqueio por `exit 2` nem sempre funciona para `Write` e `Edit`, apenas para `Bash`. O teste 2 é o que confirma se isso afeta você — e se afetar, a regra G2 precisa ser reforçada por permissão `deny` além da hook.

## Portões de emissão — E1 a E5

Os cinco entregáveis ao cliente têm portão fixo, sem pendência aberta de correspondência:

| Entregável | Etapas exigidas |
|---|---|
| E1 — Ficha de enquadramento | F0 |
| E2 — Diagnóstico e oportunidade | P1, P2, P3a, P3b, P3d |
| E3 — Blueprint da solução (consolida E3-D + E3-E) | P4, P5 |
| E4 — Guia operacional | P6, P7 |
| E5 — Relatório de piloto e calibragem | P8, P9, P10 |

Cinco itens inegociáveis (um por entregável a partir de E2) bloqueiam emissão até estarem semanticamente satisfeitos — nunca por flag manual. Ver `eiac-campo/reference/gates.md` para o detalhamento completo, incluindo a distinção interna E3-D/E3-E.

---

## Requisitos

- Claude Code instalado
- Python 3 no PATH. Nenhuma biblioteca externa é obrigatória — `quadro.py` usa PyYAML quando existe e cai num leitor mínimo quando não
- Git, para o repositório do caso

## Verificação pós-instalação

Depois de instalar os dois plugins, rode em um caso recém-aberto:

```
/eiac-nucleo:estado          deve mostrar etapa F0, camada EX1
/eiac-nucleo:quadro          deve avisar que a célula crítica está vazia
```

E os sete testes negativos da seção anterior. **Se o teste 2 passar — escrita direta em `caso/` funcionando — a trava T1 não existe no seu ambiente**, e a saída é acrescentar uma regra de permissão `deny` sobre `caso/**` além da hook.

---

## Atualização

Com o marketplace no GitHub:

```bash
git commit -am "mensagem da mudança"
git push
```

Do lado de quem usa:

```
/plugin marketplace update emcia
```

Para atualizar sozinho a cada sessão, ligue `autoUpdate` no marketplace.

### Versionar é obrigatório

Suba a versão no `plugin.json` a cada mudança de comportamento. Com o playbook sendo o método, **versão de plugin e versão de método são a mesma coisa** — e é isso que permite dizer, no relatório, qual versão produziu qual entregável.

O CI recusa mudança em `eiac-nucleo/scripts/` sem que a versão do núcleo suba junto.

### Caso aberto não é afetado

O `playbook.json` vive no repositório do **caso**, copiado na abertura, não no plugin. Atualizar o plugin não muda o método de um caso em andamento.

**Isso é decisão, não acaso.** Se alguém "consertar" isso fazendo o caso ler o playbook do plugin, um caso no P3 pode acordar com outra camada na etapa corrente.

## Testes

```bash
bash testes/negativos.sh
```

Rodam no CI a cada push. Falha é regressão de trava — conserte a trava, não o teste. A suíte acumulada (regressão + pacotes por ação) soma centenas de verificações; ver `testes/README.md` para o detalhamento por pacote.
