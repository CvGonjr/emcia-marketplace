# emcia-marketplace

Dois plugins do Claude Code que instrumentam um método de engenharia de IA aplicado a organizações clientes.

**Este repositório é a ferramenta. Ele não contém caso nem dado de cliente.**

---

## A separação que organiza tudo

| Plugin | Contém | Conhece o método |
|---|---|---|
| `eiac-nucleo` | Guarda de camada, validador de procedência, máquina de etapas, trilha | **Não** |
| `eiac-campo` | Habilidades, comandos, subagentes, template de caso | É o método |

O núcleo lê o `playbook.json` do caso e aplica o que ele declara. Trocar o playbook troca o método sem tocar em código.

**Nenhum vocabulário de base atravessa para o núcleo.** Ele conhece caso, etapa, camada, asserção, papel — não `preset`, `plugin`, `capability` nem `assistant`.

---

## Regras invioláveis

**Nenhuma decisão de camada ou de procedência passa por modelo de linguagem.** São funções determinísticas sobre dados estruturados. Instrução em texto natural para resolver uma regra significa que a regra virou preferência.

**Autor é sempre pessoa nomeada.** Nenhum evento, asserção ou registro aceita identificador de agente.

**Toda negativa produz evento.** Recusar em silêncio é pior que permitir — não deixa rastro.

**O comportamento de recusa é a funcionalidade.** Testes negativos vêm antes do caminho feliz. Falha na suíte é regressão de trava: conserte a trava, não o teste.

---

## Antes de mudar qualquer coisa

```bash
bash testes/negativos.sh
```

Trinta e três verificações. Se alguma falhar, não commite.

Ao mudar scripts do núcleo, **suba a versão** em `eiac-nucleo/.claude-plugin/plugin.json`. O CI recusa o contrário — com o playbook sendo o método, versão de plugin e versão de método são a mesma coisa.

---

## O que não fazer

**Não faça o caso ler o playbook do plugin.** Parece duplicação e não é. Ver `decisoes/002`.

**Não crie sinalizador que desative a guarda**, nem modo de depuração que a contorne.

**Não resolva as pendências marcadas no `playbook.json`.** Duas estão em aberto por decisão: a correspondência entre entregáveis e passos, e o conflito de procedência com CAT-01. São decisões de método, não de código.

**Não reproduza o conteúdo do método nas habilidades.** Elas remetem; o procedimento vive no documento do método. Ver `decisoes/009`.

**Não acrescente dependência externa** sem necessidade. `quadro.py` usa PyYAML quando existe e cai num leitor mínimo quando não.

---

## Estrutura

```
.claude-plugin/marketplace.json   registro dos dois plugins
eiac-nucleo/                      scripts, hooks, comandos de núcleo
eiac-campo/                       habilidades, comandos, template de caso
testes/negativos.sh               a suíte
decisoes/                         registro de decisões, uma por arquivo
novo-caso.sh                      abre um caso a partir do template
```

---

## Decisões registradas

Leia `decisoes/README.md` antes de propor mudança estrutural. Decisão registrada não se desfaz por esquecimento — se precisar mudar, escreva uma nova que a supersede.

As mais consequentes: dois plugins (001), playbook no caso (002), chat sem autoridade de escrita (003), camada resolvida por nível (005).

A 006 está **em conflito com documento controlado** e precisa de decisão humana.

---

## Vocabulário

`EX1`–`EX4` são camadas de execução: conversacional, analítica, verificação, julgamento.
`CA1`–`CA5` são camadas de arquitetura: controle, agente, protocolos, contexto, dados.
`HB-01`–`HB-18` são habilidades. `AG-01`–`AG-04` são agentes internos.

**Harness** designa exclusivamente infraestrutura de orquestração como commodity. Não nomeia produto, serviço nem componente construído.

**Levantamento**, nunca "elicitação". **Regras não documentadas**, nunca "regras tácitas".
