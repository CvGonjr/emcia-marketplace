# 034 — Recusa de habilidade registrada como evento (A21)

**Data:** 28/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

hb-levantar-regras sugeria uma marca de tentativa negada em caso/ que o
validador recusava por ausência de procedência D/I/V.

## Decisão

A habilidade remete ao evento TentativaNegada da guarda. Não propõe uma
asserção de caso, não escreve diretamente na trilha e não inventa marca
D/I/V para fazer uma tentativa do agente passar como evidência de método.
Se o conteúdo chegar sem hook, recusa o protocolo e informa ao engenheiro
a falha para investigação e registro. As asserções humanas continuam
passando pelo validador com sua procedência real.

## Consequência e verificação

`testes/recusa_a21.py` confere a instrução e executa a guarda: a recusa
produz evento e não cria asserção em caso/. O procedimento do método
continua referenciado, sem reprodução na habilidade.
