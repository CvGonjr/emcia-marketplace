# 031 — Habilidade não delegável bloqueada nas rotas de carregamento (A18)

**Data:** 28/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

A sessão de controle da ação 3.7 carregou `eiac-campo:hb-levantar-regras`
por `Skill`. O matcher só alcançava Read/Write/Edit/Bash. Além disso, G1
aceitava carregar uma habilidade não delegável quando havia sessão registrada.

## Decisão

A guarda identifica a habilidade pelo nome declarado no playbook, incluindo
nome qualificado, componentes de caminho e destino de link simbólico.
Read, leitura de conteúdo por Grep/Bash e Skill passam pela mesma G1/G7.
`UserPromptExpansion` cobre a invocação direta `/nome`, que não dispara
PreToolUse. Hooks permanecem determinísticos, sem avaliação por modelo.

`delegavel: false` impede o carregamento mesmo com sessão e selo. O nível
continua resolvendo a camada pelo playbook. Nas etapas delegáveis de camada
humana, a sessão da própria etapa mantém o uso instrumental anterior, sem
autorizar decisão pelo agente. Esta decisão substitui a exceção histórica
de carregamento com sessão somente quanto às etapas não delegáveis.

Cada bloqueio grava TentativaNegada com responsável, etapa e motivo; G1
inclui habilidade, camada, nível e evento de hook. G7 continua exigindo selo.

## Consequência e verificação

`testes/habilidades_a18.py` cobre instalação, absolutos, relativos, `..`,
link, Skill, expansão direta, Bash/Grep e níveis N1/N2/N3. Os parâmetros de
Skill vêm do transcript do caso sintético controle-37. T04 de
`verificacao_por_estados.py` mantém o controle de encerramento com selo,
mas agora exige recusa do carregamento pelo agente. Nenhum teste é apagado.

Referências: [hooks do Claude Code](https://code.claude.com/docs/en/hooks#userpromptexpansion)
e [habilidades](https://code.claude.com/docs/en/skills#restrict-claudes-skill-access).
