# 033 — Redirecionamento inspecionado pelo alvo de escrita (A20)

**Data:** 28/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

A presença de `>` em leituras com `2>/dev/null` disparava a proteção de
escrita, mesmo quando a saída não ia para o caso.

## Decisão

A análise shlex distingue operadores de caracteres entre aspas/escapados,
separa argumentos dos redirecionamentos e identifica os arquivos de saída.
A proteção usa o destino normalizado: `>`, `>>`, `2>`, `&>` e variantes
para área protegida são recusados. Duplicação de descritor não é arquivo.
`/dev/null`, saída externa e rascunho continuam permitidos nessas regras.

Comandos de escrita conhecidos também têm seus alvos inspecionados. A trava
anterior para código arbitrário que menciona fontes permanece: reconhecer
redirecionamento de leitura não autoriza remoção por Python ou outro código.

## Consequência e verificação

`testes/redirecionamentos_a20.py` cobre negativas de stdout/stderr/append,
caminho com espaço, leituras com descarte, duplicação de FD, cópia para
rascunho, saída externa e caracteres literais. `negativos.sh` mantém todos
os controles de imutabilidade de fontes, inclusive G6k.
