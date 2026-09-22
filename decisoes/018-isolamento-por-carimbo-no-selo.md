# 018 — Isolamento verificado no selo por carimbo de componente, não por nome de plugin

**Data:** 21/09/2026 · **Estado:** firme · **Supersede parcialmente:** [[015-isolamento-esforco-calculo-compartilhado]] (só a parte de checagem por plugin habilitado; esforço e cálculo compartilhado da 015 continuam valendo)

## Contexto

A decisão 015 registrou que "o núcleo recusa qualquer ferramenta dentro de um caso quando encontra `eiac-contraste` habilitado nas configurações efetivas". A decisão 016, registrada na mesma leva, estabeleceu que o manifesto do `emcia-contraste` **também declara `name: eiac-nucleo`** — colisão deliberada, necessária para que as habilidades chamem `/eiac-nucleo:*` sem alteração nos dois braços.

As duas decisões, lidas juntas, se contradizem: se o plugin de contraste nunca aparece como `eiac-contraste` em `enabledPlugins` (porque seu nome real é `eiac-nucleo`), a checagem da 015 **nunca poderia disparar** — não é um caso extremo raro, é estrutural, válido desde o primeiro commit do `emcia-contraste`.

A implementação em `eiac-nucleo/scripts/guarda.py::_settings_contraste_habilitado()` de fato procurava por `nome == "eiac-contraste"`. O teste que deveria cobrir essa trava (`testes/negativos.sh`, caso `ISO1`) passava porque **fabricava** um `.claude/settings.json` com a chave `"eiac-contraste@pesquisa": true` — usando o nome que o plugin deveria ter segundo a decisão 006 original (antes de ela ser resolvida pela 008 do lado contraste), não o nome que ele de fato declara em `.claude-plugin/plugin.json`. O teste validava uma configuração hipotética consistente entre si, nunca o artefato real.

## Decisão

Remove `_settings_contraste_habilitado()` de `guarda.py`. A identidade de execução deixa de ser verificada por nome de plugin (que não pode distinguir os dois lados, por desenho) e passa a ser verificada de duas formas:

1. **Em tempo real, na guarda:** `registro/` já marcado com `execucao: contraste` continua recusado por `guarda.py` (isso não dependia do nome do plugin e permanece válido).
2. **No selo, pela trilha inteira:** `estado.evento()`, nos dois componentes, passa a gravar `componente: {variante, commit}` em todo evento — `variante` lida do campo `variante` do `plugin.json` do próprio componente (`campo` no `eiac-nucleo`, `contraste` no `emcia-contraste`), `commit` lido de `git rev-parse HEAD` no repositório do componente, ambos em tempo de execução, nunca digitados. `selar.py`, nos dois lados, recusa se qualquer evento da trilha estiver sem esse carimbo ou carregar variante diferente da esperada para aquele selo. O evento `SeloAplicado` do lado campo lista os commits de componente encontrados na trilha.

O teste `ISO1` (checagem por nome fabricado) foi removido. Em seu lugar, `testes/negativos.sh` ganhou os testes `ISO-selo-1`, `ISO-selo-2` e `ISO-selo-controle`, que operam contra os `plugin.json` **reais** dos dois repositórios — sem fabricar `settings.json`.

## Consequência

- A garantia de isolamento não depende mais de uma propriedade (nome de plugin) que a própria arquitetura de compartilhamento de comando torna impossível de diferenciar.
- Um caso de campo que acumule qualquer evento produzido pelo componente de contraste (ainda que por engano de configuração) não sela — o selo é o ponto de checagem definitivo, com a trilha inteira como evidência, não um hook que só vê uma chamada de ferramenta por vez.
- Registrado como defeito encontrado e corrigido nesta frente: teste de isolamento cobria uma configuração fabricada, não o comportamento real dos dois `plugin.json`.
