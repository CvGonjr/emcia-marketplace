# Instalação — marketplace emcia

Guia completo. Cada passo tem uma verificação; não avance sem ela.

**Requisitos:** Claude Code instalado, Python 3 no PATH, Git.

---

## 1 · Preparar o repositório do marketplace

Descompacte `emcia-marketplace.zip` onde você guarda seus repositórios.

```bash
cd ~/projetos
unzip emcia-marketplace.zip
cd emcia-marketplace
git init -q
git add -A
git commit -qm "marketplace emcia: nucleo e playbook de campo"
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
/plugin marketplace add <seu-usuario>/emcia-marketplace
```

Para repositório privado, o Claude Code usa as credenciais do seu Git. Se preferir apontar para a cópia local durante o desenvolvimento, use o caminho em vez do nome — mas quem for aplicar o método deve usar o repositório.

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

**Verificar:** reinicie o Claude Code e digite `/`. Devem aparecer:

| Comando | Origem |
|---|---|
| `/eiac-nucleo:estado` | núcleo |
| `/eiac-nucleo:gravar` | núcleo |
| `/eiac-nucleo:registrar-sessao` | núcleo |
| `/eiac-nucleo:encerrar` | núcleo |
| `/eiac-nucleo:emitir` | núcleo |
| `/eiac-nucleo:quadro` | núcleo |
| `/eiac-campo:abrir-caso` | playbook |
| `/eiac-campo:enquadrar` … `/eiac-campo:classificar` | playbook |

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

**Onde o caso nasce importa.** Um repositório Git por caso, fora do repositório do marketplace e fora de qualquer outro caso. O selo, a trilha de eventos e o isolamento entre organizações dependem disso.

```bash
mkdir -p ~/casos
cd ~/casos
claude
```

Dentro da sessão:

```
/eiac-campo:abrir-caso ~/casos/medic-plus
```

O comando recusa se o destino já existir ou se o diretório pai estiver dentro de um repositório Git.

Depois:

1. Edite `registro/estado.json` e troque `ALTERE-ME` pelo nome do caso.
2. Copie os documentos do método para `metodo/` — documento do método, glossário, catálogo de delegação, quadro de ferramentas, instrumento de triagem, modelos E1–E5, plano de verificação, CTX-01.
3. Ajuste o título de `CLAUDE.md`.

**Não altere `registro/playbook.json`.** Ele é o método como arquivo.

### Entre no caso antes de seguir

O núcleo procura `registro/estado.json` no diretório corrente. De fora, a guarda não protege nada.

```bash
cd ~/casos/medic-plus
claude
```

**Verificar:**

```
/eiac-nucleo:estado
```

Deve mostrar: caso medic-plus, etapa F0, camada EX1, modalidade assíncrono.

Se responder *Nenhum caso aberto AQUI, mas existe caso em…*, a sessão está no diretório errado — entre na pasta do caso.

## 6 · Os seis testes negativos

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

**Esperado:** recusa com *origem ausente*, e `AssercaoRecusada` no log.

### Teste 4 — asserção válida

```bash
echo '- [inferido · premissa: documento reflete a pratica · Celso] guias seguem fila unica' > rascunho/P2.md
python3 ~/.claude/plugins/eiac-nucleo/scripts/validar.py --arquivo caso/P2.md --autor "Celso"
```

**Esperado:** *1 assercoes gravadas em caso/P2.md*.

### Teste 5 — encerrar etapa presencial sem sessão

```
/eiac-nucleo:encerrar P3b
```

**Esperado:** recusa, exigindo registro de sessão.

### Teste 6 — autor agente

```bash
python3 ~/.claude/plugins/eiac-nucleo/scripts/avancar.py --encerrar F0 --autor "AG05"
```

**Esperado:** *autor precisa ser pessoa nomeada*.

### Teste 7 — emitir com portão fechado

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

Cada linha é um evento de domínio com data e autor. `TentativaNegada` e `AssercaoRecusada` são a prova de que as travas operam — e um print disso vale mais que qualquer descrição.

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

---

## O que ainda não existe

| Item | Estado |
|---|---|
| Habilidades de P6 a P10 | Ausentes — instrumentos ainda não escritos |
| Portão de E4 e E5 | Pendente — divergência entre o PFC e os documentos internos |
| Base de referência curada | Ausente — esforço de curadoria |
| Servidores MCP | Ausentes — decisão entre MCP e sistema de arquivos em aberto |
| Geração de documento dos entregáveis | Ausente — `--emitir` autoriza, não gera |
| Zona `sugestoes/` para copilotagem | Ausente |
| Formulário F0 para o cliente | Ausente |

Nenhum deles impede o percurso F0 a P5, que é o que a ação 1.9 exercita.
