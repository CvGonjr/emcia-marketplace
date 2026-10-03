# 042 — Selo confirmado para a exigência após encerramento

**Data:** 03/10/2026 · **Estado:** aprovada pelo pedido da parte A · **Emenda:** 021

## Contexto

A decisão 039 corrigiu `exige_evento_selado`, mas preservou expressamente
`exige_selo_apos` até autorização específica. Um commit recusado deixava
SeloAplicado na trilha e podia satisfazer a exigência de P3b após P2.
Os testes negativos da parte A reproduzem isso.

## Decisão

`exige_selo_apos` exige selo confirmado no histórico Git após o último
EtapaEncerrada da etapa declarada. Usa a mesma função de confirmação da
039: autoria e nota do commit, posição do selo e prefixo exato da trilha
presente no snapshot. Commit comum não confirma tentativa de selo recusada.
Git inacessível recusa. A ordem continua sendo a posição dos eventos.

A guarda e o encerramento produzem TentativaNegada. O núcleo recebe apenas
identificadores e contratos do caso; não interpreta o significado das etapas.
A confirmação de selo não torna habilidade humana delegável.

## Consequência

A 021 recebe nota de emenda, preservando seu texto original. Fixtures que
pretendiam satisfazer o selo precisam de commit de selo real. Evidência:
`.projectdocs/evidencias/parte-a-operacional/A2/`. Núcleo 0.2.43.
