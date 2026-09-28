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

**Abra a sessão na raiz do caso.** A guarda conserva a raiz indicada por
`CLAUDE_PROJECT_DIR` e localiza o registro também nos ancestrais do cwd.
Os comandos de operação continuam sendo executados na raiz do caso.

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
P4 e P5. O engenheiro registra a sessão no próprio terminal, enquanto a
etapa for a corrente, usando o comando preparado por
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

Antes de encerrar P5, prepare o comando de classificação confirmada
pela pessoa e entregue ao engenheiro para executar no próprio terminal:

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

## Decisões humanas fora da sessão (A12)

Toda chamada que chega à guarda é da sessão do agente. Informar um nome
humano em `--autor` ou `--ator` não muda essa origem. O playbook declara
`decisoes_humanas`, com script, argumento e condição de cada operação:

| Operação | Quem executa |
|---|---|
| Apurar nível; registrar sessão/campo/recorrência; satisfazer inegociável | Engenheiro no próprio terminal |
| Encerrar etapa em camada humana (EX3/EX4 no campo) | Engenheiro no próprio terminal |
| Gravar autonomia decidida, operacional validado, piloto revisado, rotina ou decisão de recalibragem | Engenheiro no próprio terminal |
| Gravar minuta/proposta/recomendação sem decisão; ler; validar asserção; curar; emitir | Agente pela sessão |

O agente prepara os argumentos e entrega o comando com caminho absoluto
real do script. O engenheiro o executa **no diretório do caso, fora da
sessão do Claude Code**. Confirmação no chat não executa a decisão nem
autoriza o agente a executá-la. A guarda recusa a chamada, registra
`TentativaNegada` e devolve a operação e o comando exato.

`inegociaveis.py --verificar` pode ser usado pelo agente; adicionar
`--satisfazer` torna a operação humana. Os demais portões e exigências de
sessão/selo continuam aplicados no terminal. A decisão 027 substitui a
exceção de ator informado pelo agente da decisão 019.

### Demonstração por caso sintético

No próprio terminal:

```bash
.projectdocs/demos/preparar-caso.sh controle-a12 P7
cd /tmp/emcia-demos/controle-a12
~/Projetos/emcia-marketplace/.projectdocs/demos/como-agente.sh 'python3 ~/Projetos/emcia-marketplace/eiac-nucleo/scripts/avancar.py --registrar-sessao P7 --autor "Celso do Vale" --participantes "X"'
```

O auxiliar deixa a etapa pedida corrente e registra as sessões exigidas,
o selo, a classificação e os rascunhos conforme o percurso. OP-001 chega
validado a P7 e AUT-001 fica proposto. A base pode ser escolhida com
`EMCIA_DEMO_BASE`; o padrão é `/tmp/emcia-demos`. Um nome já existente é
recusado. O auxiliar é executado pelo engenheiro no terminal.

`como-agente.sh` envia a chamada simulada à guarda e imprime PERMITIDO ou
NEGADO com o motivo; não executa o comando. Não cria nova permissão.

## Verificação por estados do caso

A comparação entre o que a organização declarou e o que o levantamento presencial confirma não roda como execução externa: é interna ao mesmo caso. O estado declarado é selado ao fim de P2 (antes do levantamento presencial); P3b/P3d produzem o estado verificado. `/eiac-nucleo:quadro` cruza os dois — célula crítica vazia no estado declarado selado é o resultado esperado quando o levantamento presencial ainda não confirmou as regras de baixa frequência e alta consequência que os documentos não registram (CTX-01 §8).

P3b exige selo posterior ao encerramento de P2. O encerramento pelo
engenheiro nomeia o selo que falta. Sessão e selo não autorizam o agente
a carregar uma habilidade declarada não delegável (decisão 031).

## Material público da etapa 0a

O levantamento público sobre a organização e o setor, feito na etapa 0a do protocolo de habilitação (EMCIA-HAB-01, anterior a F0), **não entra no caso nesse momento**. Ele é coletado fora do repositório do caso e só é gravado depois da abertura (etapa 0d — caso aberto e selado), pelo caminho normal de curadoria (`/eiac-nucleo:curar` ou `/eiac-nucleo:gravar`, conforme o tipo de objeto), com marca `I · tipo_fonte: externa`, URL e limite da fonte explícitos — o mesmo formato que `eiac-campo/reference/procedencia.md` já define para qualquer inferência apoiada em fonte externa. Não há automatismo que grave esse material antes da abertura; é regra documental, não trava de código.

## As três travas

| Trava | Mecanismo | Onde |
|---|---|---|
| **T1 procedência** | Escrita direta em `caso/` negada; todo conteúdo passa pelo validador | `guarda.py` G2 + `validar.py` |
| **T2 camada** | Habilidade de etapa não delegável não carrega; etapa dependente não abre; encerramento confere sessão conforme a camada declarada; decisão humana não executa pela sessão | `guarda.py` G1, G3 e G8 + `avancar.py` |
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

## Encerramento com produto e revisão humana (A14–A16)

O encerramento confere sessão, dependências e selo, depois os produtos
`produtos_encerramento` do playbook do caso: linha de base (P3a), classificação
registrada (P5), OP validado (P6), AUT decidido (P7), conjunto revisado (P8),
métrica de resultado apurada (P9) e rotina com responsável e cadência (P10).
Produto ausente gera `TentativaNegada`, informa o que falta e preserva o estado.
O portão do entregável continua sendo conferido na emissão.

A revisão do piloto e a definição da rotina de calibragem também são atos
humanos da lista `decisoes_humanas`. O agente prepara os rascunhos; o
engenheiro os registra no próprio terminal, fora da sessão. Rascunho de
piloto, medição de baseline/métrica e ciclo com recomendação sem decisão
continuam permitidos. Um nome humano informado não libera a guarda.

Pessoas exigem nome e sobrenome e nenhuma palavra coletiva, conforme
`pessoa_nomeada` do playbook: equipe de TI, Time Comercial, Área de Vendas
e Marina são recusados; Marina Prado é aceito. A regra vale também para
campos nominais dos artefatos. Atualize explicitamente o playbook de casos
existentes; o núcleo não consulta o template como alternativa.

### Demonstração até P10

Execute no terminal do engenheiro:

```bash
cd ~/Projetos/emcia-marketplace
bash .projectdocs/demos/preparar-caso.sh controle-p10 P10
```

O caso fica em `/tmp/emcia-demos/controle-p10`, P10 corrente e N2. O auxiliar
imprime o caminho e os rascunhos. Ao parar em P6/P7/P8, o rascunho da etapa
tem versão incrementada e campos de decisão preenchidos: o engenheiro muda
apenas estado para validado/decidido/revisado e executa o script indicado.
As decisões das etapas anteriores são executadas no percurso sintético.
Em P10, CAL-001 já está registrada; CAL-001-C01 tem drift e recomendação,
sem decisão. O rascunho do ciclo tem versão 2 e campos humanos preenchidos:
o engenheiro informa apenas decisao (recalibrar/expandir/descontinuar).

## Fronteira da sessão e caminhos — Sprint 3, ação 3.7

A guarda alcança Read, Skill, leitura de conteúdo por Bash/Grep e a invocação
direta de habilidades pelo evento UserPromptExpansion. Uma habilidade com
`delegavel: false` no playbook não carrega, mesmo após sessão humana e selo.
O nome da habilidade identifica a etapa; a pasta da instalação não autoriza
seu uso. Nas etapas delegáveis de camada humana, mantém-se o apoio após a
sessão da própria etapa. Toda recusa produz TentativaNegada.

Absolutos, relativos, `..` e links simbólicos passam pela mesma proteção de
caso/, contexto/, registro/ e fontes/. Redirecionamentos de Bash são
conferidos pelo destino: leitura com `2>/dev/null` e escrita em rascunho/
continuam permitidas. A tentativa de carregar hb-levantar-regras é evento
da guarda; não se escreve uma marca inválida de procedência em caso/.

`/eiac-nucleo:estado` exibe o último selo confirmado pelo Git do caso, com
hash, data e nota, inclusive no resumo. Essa apresentação não altera o
arquivo de estado nem cria uma mudança após o selo.

Versão desta correção: `v-sprint3-poc.6` (núcleo 0.2.32, campo 0.8.6).
Decisões 031–035 e evidência em
[correcao-A17-A21](.projectdocs/evidencias/sprint3/3.7/correcao-A17-A21/resultado.md).
