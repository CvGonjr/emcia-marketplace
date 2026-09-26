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

O núcleo lê `registro/estado.json` do diretório corrente. De fora, a guarda não protege nada.

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

**Esperado:** bloqueio, com a mensagem sobre `EX4` e modalidade presencial.
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

**Esperado:** recusa nomeando explicitamente que P3b exige selo posterior ao encerramento de P2. Selar o caso (`/eiac-nucleo:selar`) depois de encerrar P2 e antes de tentar novamente resolve.

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
