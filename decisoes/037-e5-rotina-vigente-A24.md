# 037 — E5 usa a rotina de calibragem vigente (A24)

**Data:** 29/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

A decisão 036 define a fonte vigente da recorrência pela maior versão
inteira positiva. `render_e5` escolhia a última rotina pela ordem lexical
do nome do arquivo. Com `CAL-001` v10/Marina Prado e `CAL-999`
v2/Celso do Vale, a recorrência e o E5 apresentavam pessoas diferentes
para a mesma responsabilidade.

## Decisão

O E5 lê do playbook do próprio caso o contrato
`coerencia_responsavel_recorrencia` de P10 e chama a mesma seleção
genérica usada pela recorrência. A função compartilhada valida fontes,
exclui ciclos pelo padrão declarado, exige versão inteira positiva e
pessoa nomeada, e recusa empate da maior versão com responsáveis
distintos. O E5 não escolhe por nome ou data do arquivo. Ausência ou
invalidade do contrato impede sua materialização; nenhum playbook é
injetado em casos existentes.

## Consequência e verificação

`testes/e5_rotina_a24.py` verifica seleção v10/v2, coerência com a
recorrência, recusa de empate e versão inválida, e exclusão de ciclos.
As seleções de piloto, métricas e linha de base são auditadas na
evidência da ação 4.3. Esta decisão não altera guarda, selo, playbook
nem fronteiras e não cria etiqueta de versão.
