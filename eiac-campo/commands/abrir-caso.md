---
description: Cria o repositório de um caso novo a partir do template do playbook, em caminho explícito.
argument-hint: <caminho-de-destino>
---
## Antes de executar

O caso **não pode nascer dentro do repositório do marketplace nem dentro de outro caso**. Um repositório Git por caso — é disso que dependem o selo, a trilha de eventos e o isolamento entre organizações.

Confira onde a sessão está:

```bash
pwd
git rev-parse --show-toplevel 2>/dev/null || echo "fora de repositorio"
```

Se `pwd` estiver dentro de um repositório existente, **pare e peça ao operador o caminho de destino**. Não assuma o diretório corrente.

## Executar

Use o caminho que o operador forneceu como argumento. Se não vier argumento, pergunte — não invente.

```bash
DESTINO="<caminho-absoluto-informado>"

test -e "$DESTINO" && { echo "ja existe: $DESTINO"; exit 1; }
git -C "$(dirname "$DESTINO")" rev-parse --show-toplevel 2>/dev/null \
  && { echo "o diretorio pai esta dentro de um repositorio git — escolha outro lugar"; exit 1; }

cp -r "${CLAUDE_PLUGIN_ROOT}/template-caso" "$DESTINO"
cd "$DESTINO"
git init -q && git add -A && git commit -qm "abertura do caso"
echo "caso criado em $DESTINO"
```

## Depois

1. Edite `registro/estado.json` e troque `ALTERE-ME` pelo nome do caso.
2. Copie os documentos do método para `metodo/`.
3. Ajuste o título de `CLAUDE.md`.

**Não altere `registro/playbook.json`.** Ele é o método como arquivo, e mudá-lo durante o caso invalida o percurso.

## Por fim, avise o operador

O núcleo procura `registro/estado.json` no diretório corrente. Enquanto a sessão não estiver **dentro** do caso, `/eiac-nucleo:estado` responde que não há caso aberto e a guarda não protege nada.

Diga, com estas palavras:

> Caso criado. Encerre esta sessão, entre no diretório do caso e abra o Claude Code lá dentro. Depois confirme com `/eiac-nucleo:estado`.
