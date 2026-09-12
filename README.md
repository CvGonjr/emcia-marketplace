# emcia — marketplace de plugins

Dois plugins, e a separação entre eles é o argumento arquitetural do projeto.

| Plugin | Contém | Conhece o método |
|---|---|---|
| **eiac-nucleo** | Guarda de camada, validador de procedência, máquina de etapas, trilha | **Não** |
| **eiac-campo** | Habilidades por etapa, comandos, subagentes, template de caso | É o método |

O núcleo lê o playbook do caso e aplica o que ele declara. Trocar o playbook troca o método sem tocar em uma linha de código — é o que sustenta a afirmação de que o método é independente da ferramenta.

## Instalação

```
/plugin marketplace add <url-do-repositorio>
/plugin install eiac-nucleo@emcia
/plugin install eiac-campo@emcia
```

As hooks do núcleo registram automaticamente. A trava viaja com o plugin, não com o `settings.json` de cada operador.

## Abrir um caso

```
cp -r <plugin>/eiac-campo/template-caso caso-medic-plus
cd caso-medic-plus
git init && git add -A && git commit -m "abertura do caso"
```

Edite `registro/estado.json` com o nome do caso. Copie os documentos do método para `metodo/`.

## Percurso

| Comando | Etapa | Camada |
|---|---|---|
| `/eiac-campo:enquadrar` | F0 | EX1 |
| `/eiac-campo:mapear-contexto` | P1 | EX2 |
| `/eiac-campo:mapear-fontes` | P2 | EX2 |
| `/eiac-campo:medir` | P3a | EX3 |
| — | P3b | **EX4 · sem comando, por desenho** |
| `/eiac-campo:confrontar` | P3d | EX3 |
| `/eiac-campo:priorizar` | P4 | EX2 |
| `/eiac-campo:classificar` | P5 | EX2 |

E os comandos de núcleo, que valem em qualquer playbook:

`/eiac-nucleo:estado` · `/eiac-nucleo:gravar` · `/eiac-nucleo:registrar-sessao` · `/eiac-nucleo:encerrar` · `/eiac-nucleo:emitir`

## As três travas

| Trava | Mecanismo | Onde |
|---|---|---|
| **T1 procedência** | Escrita direta em `caso/` negada; todo conteúdo passa pelo validador | `guarda.py` G2 + `validar.py` |
| **T2 camada** | Habilidade de etapa não delegável não carrega; etapa dependente não abre | `guarda.py` G1 e G3 |
| **T3 selo** | Commits do repositório do caso | Git |

## Testes negativos — faça no primeiro dia

Antes de confiar em qualquer coisa, prove que ela recusa.

| # | Tente | Esperado |
|---|---|---|
| 1 | Ler `hb-levantar-regras/SKILL.md` durante um caso | Bloqueio, `TentativaNegada` no log |
| 2 | Escrever direto em `caso/qualquer.md` | Bloqueio, com instrução de usar o validador |
| 3 | Gravar rascunho com asserção sem origem | Recusa, `AssercaoRecusada` no log |
| 4 | `/eiac-nucleo:encerrar P3b` sem sessão registrada | Recusa |
| 5 | `/eiac-nucleo:emitir E2` com etapas pendentes | Recusa, nomeando as etapas |
| 6 | `--autor AG05` em qualquer script | Recusa |

**Se algum passar, a trava não existe.** Há relatos públicos de que o bloqueio por `exit 2` nem sempre funciona para `Write` e `Edit`, apenas para `Bash`. O teste 2 é o que confirma se isso afeta você — e se afetar, a regra G2 precisa ser reforçada por permissão `deny` além da hook.

## Pendências que o playbook declara e o núcleo respeita

O `registro/playbook.json` marca `E4` e `E5` com `portao_pendente: true`, porque a correspondência entre entregáveis e passos ainda diverge entre o relatório do PFC e os documentos internos. A emissão recusa até a decisão. **O agente não deve resolver isso.**

P6 a P10 não têm habilidade: os instrumentos que elas exigem — roteiro de levantamento, instrumento da camada de contexto, protocolo de campo — ainda não existem.

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

E os seis testes negativos da seção anterior. **Se o teste 2 passar — escrita direta em `caso/` funcionando — a trava T1 não existe no seu ambiente**, e a saída é acrescentar uma regra de permissão `deny` sobre `caso/**` além da hook.

---

## Atualização

Com o marketplace no GitHub:

```bash
git commit -am "hb-medir: exige amostra e periodo"
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

Rodam no CI a cada push. Falha é regressão de trava — conserte a trava, não o teste.
