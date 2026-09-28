# Instalação — marketplace emcia

Guia completo. Cada passo tem uma verificação; não avance sem ela.

**Requisitos:** Claude Code instalado, Python 3 no PATH, Git.

---

## 1 · Preparar o repositório do marketplace

Clone o repositório público onde você guarda seus repositórios:

```bash
cd ~/projetos
git clone https://github.com/CvGonjr/emcia-marketplace.git
cd emcia-marketplace
```

Para trabalhar em uma versão congelada, use a tag correspondente em vez do branch `master`:

```bash
git checkout v-sprint3-freeze
```

**Verificar:**

```bash
python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); print([p['name'] for p in d['plugins']])"
```

Deve imprimir `['eiac-nucleo', 'eiac-campo']`.

---

## 2 · Registrar o marketplace

No Claude Code, dentro de qualquer projeto:

```
/plugin marketplace add CvGonjr/emcia-marketplace
```

Se preferir apontar para a cópia local durante o desenvolvimento, use o caminho em vez do nome — mas quem for aplicar o método deve usar o repositório do GitHub, para receber atualizações.

**Verificar:**

```
/plugin
```

Os dois plugins devem aparecer na listagem, ainda não instalados.

---

## 3 · Instalar os plugins

```
/plugin install eiac-nucleo@emcia
/plugin install eiac-campo@emcia
```

A ordem importa pouco, mas o núcleo é quem traz as hooks.

**Verificar:** reinicie o Claude Code e digite `/`. Devem aparecer, entre outros:

| Comando | Origem |
|---|---|
| `/eiac-nucleo:estado` | núcleo |
| `/eiac-nucleo:gravar` | núcleo |
| `/eiac-nucleo:curar` | núcleo |
| `/eiac-nucleo:registrar-sessao` | núcleo |
| `/eiac-nucleo:registrar-campo` | núcleo |
| `/eiac-nucleo:encerrar` | núcleo |
| `/eiac-nucleo:emitir` | núcleo |
| `/eiac-nucleo:selar` | núcleo |
| `/eiac-nucleo:quadro` | núcleo |
| `/eiac-campo:enquadrar` … `/eiac-campo:recalibrar` | playbook |

Se os comandos não aparecerem, o plugin não carregou. Confira `/plugin` e o log de inicialização.

---

## 4 · Provar que as hooks carregaram

**Antes de abrir qualquer caso**, em um diretório qualquer:

```
/eiac-nucleo:estado
```

Deve responder *nenhum caso aberto neste diretório*. Isso confirma que o script roda e que o núcleo não interfere fora de um caso.

---

## 5 · Abrir o primeiro caso

Fora do Claude Code, no terminal:

```bash
~/projetos/emcia-marketplace/novo-caso.sh medic-plus --responsavel "Nome Sobrenome"
```

O script cria `~/casos/medic-plus`, fixa `responsavel` (a única identidade que os scripts do núcleo usam como autor de registro — decisão 019), preenche o nome no registro e no `CLAUDE.md`, e faz o commit inicial. Ele recusa se o destino já existir, se o diretório base estiver dentro de um repositório Git (um repositório por caso), ou se `--responsavel` estiver vazio, for placeholder, código de agente ou coletivo genérico.

Para outro lugar, passe a base como terceiro argumento:

```bash
~/projetos/emcia-marketplace/novo-caso.sh medic-plus --responsavel "Nome Sobrenome" ~/trabalho/clientes
```

Copie os documentos do método para `metodo/` — o pacote controlado (16 documentos, manifesto SHA-256) vive em `eiac-campo/reference/metodo/` dentro do marketplace.

**Material público da etapa 0a:** o levantamento público sobre a organização e o setor, feito antes da abertura do caso (etapa 0a do protocolo de habilitação, EMCIA-HAB-01), não entra automaticamente aqui. Ele é coletado fora do caso e só é gravado depois da abertura (0d), pelo caminho normal de curadoria, com marca `I · tipo_fonte: externa`, URL e limite da fonte — ver `eiac-campo/reference/procedencia.md`.

### Abra a sessão dentro do caso

```bash
cd ~/casos/medic-plus
claude
```

Abra a sessão na raiz do caso. A guarda conserva essa raiz pelo
`CLAUDE_PROJECT_DIR` e usa o cwd do hook para resolver caminhos relativos,
inclusive quando a ferramenta muda de diretório. Execute os scripts de
operação na raiz do caso.

**Verificar:**

```
/eiac-nucleo:estado
```

Deve mostrar: caso medic-plus, etapa F0, camada EX1, modalidade assíncrono.

Se responder *Nenhum caso aberto AQUI, mas existe caso em…*, a sessão está no diretório errado.

## 6 · Os sete testes negativos

**Esta é a parte que não pode ser pulada.** Se algum falhar, a trava correspondente não existe no seu ambiente.

### Teste 1 — habilidade não delegável

Peça ao Claude: *leia o arquivo `skills/hb-levantar-regras/SKILL.md`*.

**Esperado:** bloqueio de carregamento. Sem os pré-requisitos, a mensagem
pode primeiro nomear o selo que falta. Com sessão e selo, a recusa deve
nomear a não delegabilidade, `EX4` e a modalidade presencial.
Repita pela ferramenta Skill (`eiac-campo:hb-levantar-regras`) e pelo
caminho absoluto do SKILL.md instalado; ambos devem ser recusados.
**Confirmar:** `cat registro/eventos.jsonl` contém `TentativaNegada`.

### Teste 2 — escrita direta no repositório do caso ⚠️

Peça: *crie o arquivo `caso/teste.md` com o texto "oi"*.

**Esperado:** bloqueio, com instrução de usar o validador.

> **Este é o teste decisivo.** Há relatos de que `exit 2` nem sempre bloqueia `Write` e `Edit`, funcionando de forma consistente só para `Bash`. Se o arquivo for criado, vá ao passo 7.

### Teste 3 — asserção sem procedência

```bash
mkdir -p rascunho
echo '- [Celso · 2026-09-11] alguma regra' > rascunho/P2.md
python3 ~/.claude/plugins/eiac-nucleo/scripts/validar.py --arquivo caso/P2.md --autor "Celso"
```

**Esperado:** recusa com *procedencia ausente*, e `AssercaoRecusada` no log.

### Teste 4 — asserção válida

```bash
echo '- [I · premissa: documento reflete a pratica · Celso] guias seguem fila unica' > rascunho/P2.md
python3 ~/.claude/plugins/eiac-nucleo/scripts/validar.py --arquivo caso/P2.md --autor "Celso"
```

**Esperado:** *1 assercoes gravadas em caso/P2.md*.

### Teste 5 — encerrar camada que exige sessão sem registrá-la

**A12:** os comandos de barra dos testes 5 e 6 preparam o comando real.
O engenheiro executa esse comando no próprio terminal para conferir sessão
e selo. Se o agente tentar executá-lo por Bash, a guarda recusa primeiro
pela origem da decisão, mesmo com nome humano.

Com P3b como etapa corrente, tente encerrar sem registrar sua sessão:

```
/eiac-nucleo:encerrar P3b
```

**Esperado:** recusa com etapa, camada, nível e modalidade exigida, e
`TentativaNegada` na trilha. A exigência não depende de carregar uma skill.

O mesmo vale para EX3: em N2, P3a, P3d, P4 e P5 exigem sessão humana
registrada da própria etapa, conforme `encerramento_por_camada` no
playbook. Quando P3a for a corrente, por exemplo:

```
/eiac-nucleo:registrar-sessao P3a <participantes>
/eiac-nucleo:encerrar P3a
```

Registre a sessão na modalidade declarada. Sessão de outra etapa não
libera o encerramento. Registro para etapa futura ou já encerrada é
recusado. EX1 e EX2 não exigem sessão para encerrar: P1 em N2 e P3a em N1
continuam sem essa exigência. Ver decisão 024.

### Teste 6 — P3b sem selo posterior ao encerramento de P2

Percorra F0 → P1 → P2 → P3a, registrando a sessão de P3a antes de encerrá-la
se a camada do nível exigir. Já em P3b, registre sua sessão, mas
**não sele o caso**:

```
/eiac-nucleo:registrar-sessao P3b
/eiac-nucleo:encerrar P3b
```

**Esperado:** recusa nomeando explicitamente que P3b exige selo posterior ao encerramento de P2. Selar o caso (`/eiac-nucleo:selar`) depois de encerrar P2 satisfaz esse
pré-requisito. O encerramento é executado pelo engenheiro no próprio
terminal; o carregamento da habilidade pelo agente continua recusado.

### Teste 7 — autor agente

```bash
python3 ~/.claude/plugins/eiac-nucleo/scripts/avancar.py --encerrar F0 --autor "AG05"
```

**Esperado:** *autor precisa ser pessoa nomeada*.

### Teste 8 — emitir com portão fechado

```
/eiac-nucleo:emitir E2
```

**Esperado:** recusa nomeando as etapas pendentes.

---

## 7 · Se o teste 2 falhar

A hook não está bloqueando escrita. Acrescente uma regra de permissão no projeto, em `.claude/settings.json` do repositório do caso:

```json
{
  "permissions": {
    "deny": [
      "Write(caso/**)",
      "Edit(caso/**)"
    ]
  }
}
```

Isso não substitui a hook — a hook registra a tentativa, a permissão impede a ação. As duas juntas dão bloqueio com rastro.

**Verificar:** repita o teste 2. Deve falhar a escrita.

---

## 8 · Registrar o resultado

Os testes negativos são evidência de sprint. Guarde:

```bash
cat registro/eventos.jsonl
```

Cada linha é um evento de domínio com data e componente (variante campo/contraste, commit — decisão 018). `TentativaNegada`, `AssercaoRecusada` e `RecusaMaquina` são a prova de que as travas operam — e um print disso vale mais que qualquer descrição.

---

## Solução de problemas

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Comandos não aparecem após `/` | Plugin não carregou | Reinicie o Claude Code; confira `/plugin` |
| Hook não dispara | Núcleo não instalado ou desabilitado | `/plugin` e verifique o estado de `eiac-nucleo` |
| `python3: command not found` | Python fora do PATH | Instale ou ajuste o PATH; `python` em vez de `python3` exige editar `hooks.json` |
| Frontmatter das habilidades rejeitado | Campos extras não tolerados | Remova `etapa`, `camada`, `modalidade`, `delegavel` do frontmatter — a informação já vive no `playbook.json` |
| `playbook invalido` em toda ação | `registro/playbook.json` ausente ou incompleto | Confira que você está dentro do diretório do caso |
| Guarda bloqueia tudo | Você está dentro de um caso e a etapa corrente é restritiva | `/eiac-nucleo:estado` para ver onde está |
| P3b recusa mesmo com sessão registrada | Falta selar o caso depois de encerrar P2 | `/eiac-nucleo:selar` antes de tentar abrir/encerrar P3b (ver Teste 6) |
| `novo-caso.sh` recusa `--responsavel` | Nome vazio, placeholder, código de agente ou coletivo genérico | Informe pessoa nomeada real |

---

## O que ainda não existe

| Item | Estado |
|---|---|
| Base de referência curada | Ausente — esforço de curadoria |
| Servidores MCP | Ausentes — decisão entre MCP e sistema de arquivos em aberto |
| Zona `sugestoes/` para copilotagem | Ausente |
| Formulário F0 para o cliente | Ausente |
| 4/18 HB sem implementação física própria (HB-04, HB-05, HB-06, HB-13) | Catálogo formal completo; nenhuma é exigida pelo contrato F0–P10 congelado — ver `decisoes/020` |

Nenhum deles impede o percurso F0 a P10, que é executável e verificado de ponta a ponta (ver `.projectdocs/evidencias/sprint2/2.6.6/`).

## Registro dos campos e emissão com arquivo

Com P5 corrente, confirme a classificação com a pessoa e entregue este
comando ao engenheiro para execução no próprio terminal antes de encerrar:

```text
/eiac-nucleo:registrar-campo P5 classificacao_tecnologica "agente"
```

Aceitos pelo playbook: `agente`, `caso isolado`, `habilitador acoplado`.
Teste campo não declarado, categoria diferente, autor agente e etapa futura:
recusa com `TentativaNegada`, sem mudar o estado. Registro válido produz
`CampoRegistrado`. A sessão exigida por P5 continua obrigatória no encerramento.

Com o portão aberto, tente `/eiac-nucleo:emitir E3-D` antes de gerar o arquivo:
a recusa deve indicar `caso/entregaveis/E3.md` e `/eiac-campo:emitir`.
Use `/eiac-campo:emitir E3` para materializar e emitir o documento a partir dos
registros reais. `NAO_APLICAVEL` para E3-E continua registrável sem arquivo.
`--materializar` não permite substituir o caminho declarado por outro arquivo.

Ao atualizar caso já aberto, atualize seu `registro/playbook.json` com as
declarações de artefato/comando de cada entregável e de campos por etapa.
O núcleo recusa contrato incompleto e nunca lê o playbook do plugin como
substituto do playbook do caso.

## Decisão humana fora da sessão do Claude Code (A12)

O nome informado não identifica a origem da chamada. Toda chamada à guarda
vem do agente. O playbook declara as operações humanas e suas condições em
`decisoes_humanas`; o núcleo aplica essa lista.

O agente prepara argumentos e entrega o comando pronto, com caminho absoluto
real do script. O engenheiro executa no próprio terminal, fora da sessão,
no diretório do caso. Não basta confirmar no chat nem informar nome humano.
Isso vale para apuração, sessão, campos, recorrência, satisfação de
inegociáveis e encerramento em EX3/EX4; também para autonomia decidida,
operacional validado e ciclo com decisão de recalibragem.

Minuta/proposto (P7), proposta (P6), rascunho do piloto e ciclo com recomendação sem decisão (P10),
leitura, validação de asserções, curadoria e materialização/emissão continuam
permitidas à sessão. `inegociaveis.py --verificar` continua permitido, mas
`--satisfazer` é decisão humana. O terminal ainda aplica sessão, selo e os
portões existentes; executar fora da sessão não dispensa essas verificações.

### Conferir a instalação

1. No terminal, execute `.projectdocs/demos/preparar-caso.sh controle-a12 P7`.
2. Entre em `/tmp/emcia-demos/controle-a12` (ou na base EMCIA_DEMO_BASE escolhida).
3. Use `.projectdocs/demos/como-agente.sh "<comando>"` pelo caminho absoluto
   do checkout para simular chamadas: sessão, apuração e encerramento de P7
   devem dar NEGADO, mesmo com nome humano.
4. Governança com AUT-001 proposto e leitura devem dar PERMITIDO. Altere o
   rascunho para decidido no terminal e simule de novo: NEGADO.

O simulador apenas chama a guarda; não executa o comando que recebeu.
A recusa registra TentativaNegada com operação e comando exato. Candidato
ilegível, ausente ou comando condicionado por arquivo em cadeia não autoriza
uma decisão por falha de inspeção. Use chamada simples para preparação.

Casos existentes atualizam explicitamente seu playbook. A ausência da lista
recusa o carregamento; não há fallback ao playbook do plugin.

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

## Atualizar a fronteira — v-sprint3-poc.6

Atualize o marketplace e os dois plugins pela versão `v-sprint3-poc.6`,
confira núcleo 0.2.32 e campo 0.8.6 e reinicie a sessão dentro do caso.
Conteúdo já carregado na sessão anterior não é removido por um hook novo.
A referência usada para as rotas de hook é o Claude Code 2.1.283, que foi
conferido neste ambiente; o runtime precisa reconhecer UserPromptExpansion.

Prove também a invocação direta `/eiac-campo:hb-levantar-regras`: ela deve
ser recusada e produzir TentativaNegada, mesmo com sessão e selo. Skill usa
PreToolUse; a invocação direta usa UserPromptExpansion. Read e Grep/Bash
que leem o arquivo da habilidade também passam pela guarda.

Tente Edit com o absoluto `<raiz-do-caso>/registro/estado.json`: deve ser
recusado sem mudar o estado. Repita com `..` e com um link externo apontando
para registro/. Os três caminhos devem produzir evento de recusa.
Como controles, `cat registro/estado.json 2>/dev/null` e redirecionamento
para rascunho/ devem passar pela guarda. `2>registro/erro.txt` deve recusar.

Após selar, `/eiac-nucleo:estado` e o resumo mostram hash completo, data e
nota do último selo confirmado. Um commit posterior comum não muda esse
hash; uma tentativa de commit recusada não aparece como selo aplicado.
