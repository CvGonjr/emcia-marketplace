# 019 — Autoria de registro é atribuída pelo componente, nunca informada pelo agente

**Data:** 22/09/2026 · **Estado:** firme

## Contexto

`validar.py`, `curar.py` e `selar.py` aceitavam `--autor`/`--registrado-por` digitado a cada chamada, validado só por checagem léxica (`estado.autor_e_agente()`). Um achado documentado desde o baseline (`testes/curadoria.py::2.5.2-T-baseline`) mostrava que `"AG-01"` com hífen escapava dessa checagem e era aceito como autor humano — a garantia "autor é sempre pessoa nomeada" dependia de reconhecer o formato do valor recebido, não de uma propriedade estrutural do caso.

O `CLAUDE.md` do template de caso também dizia "Autor é sempre pessoa nomeada. Nunca identificador de agente." — uma instrução que o agente lê, mas cujo cumprimento dependia inteiramente dele mesmo, checado só depois do fato.

## Decisão

A autoria de registro (quem gravou uma asserção, curou um objeto de contexto, ou selou o caso) deixa de vir de argumento de linha de comando. `validar.py`, `curar.py` e `selar.py` leem sempre `responsavel` de `registro/estado.json`.

`responsavel` é fixado uma única vez, por `novo-caso.sh --responsavel "Nome Sobrenome"`, **fora da sessão do agente** — antes de o Claude Code ser aberto no diretório do caso. O script recusa nome vazio, placeholder (`<...>`), código de agente e coletivo genérico ("equipe", "área" etc.). Nenhum comando do plugin (`/eiac-nucleo:*`) grava ou altera esse campo — G5 já nega escrita direta em `registro/`, e não há comando dedicado a isso.

`--autor`/`--registrado-por` continuam aceitos como argumentos nos três scripts (para não quebrar chamadas existentes), mas são ignorados para fins de autoria — o valor informado é preservado em `autor_informado`/`registrado_por_informado` no evento, só para auditoria, nunca usado como autor gravado.

**Distinto disso, sem mudança:** o `--ator` que seis habilidades (`hb-operacionalizar`, `hb-governar`, `hb-pilotar`, `hb-medir`, `hb-medir-valor`, `hb-recalibrar`) instruem o agente a informar em scripts de `eiac-campo/scripts/` não é autoria de registro — é o ator de uma decisão de método (quem valida uma especificação, quem decide autonomia, quem decide recalibragem), dado que só o método sabe e que o componente não pode atribuir sem inventar quem decidiu. Esse `--ator` continua vindo do agente, validado como pessoa nomeada, nunca substituído.

## Consequência

- Um caso sem `responsavel` definido não grava, cura nem sela nada — a ausência é recusada, não um valor default silencioso.
- O agente não pode mais se tornar autor de registro por nenhum valor que informe — nem mesmo um formato que escape de checagem léxica, porque o valor informado nunca é usado para essa finalidade.
- `eiac-nucleo/commands/gravar.md`, `curar.md` e `selar.md` não instruem mais o operador/agente a informar autor — o texto agora diz que a autoria vem do responsável do caso.
- Teste dedicado em `testes/autoria_responsavel.py` (14 verificações) cobre `novo-caso.sh` (5 recusas + 2 controles positivos) e os três scripts (recusa sem responsável + controle positivo de atribuição correta, ignorando o valor informado).
- `testes/curadoria.py::2.5.2-T-baseline` reescrito: o achado original (autor por checagem léxica) está superado por uma garantia estrutural mais forte, testada diretamente.
