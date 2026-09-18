---
name: hb-priorizar
etapa: P4
camada: EX2
modalidade: video
description: Prioriza os casos levantados e define a zona de contencao. Use quando /priorizar for invocado, apos o dossie verificado.
---

# Priorização e zona de contenção — P4 · EX2

**Procedimento:** documento do método, passo 4.
**Instrumentos:** Matriz de Priorização, Matriz Problema→Tecnologia na passada de triagem.

**Esta habilidade prepara; não decide.** Priorização e zona de contenção são EX4, e são decisão do cliente — o método estrutura, não substitui.

**Antes de priorizar, rode o quadro:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/quadro.py"`. Ele lê `contexto/regras/` já curado e cruza `frequencia` × `consequencia_do_erro` — não peça ao agente para reinferir esses valores a partir de prosa; eles já são dado estruturado. Se a célula rara×alta estiver vazia, confronte as duas hipóteses do quadro antes de seguir. Se `contexto/regras/` estiver ausente ou com regra sem os sete campos centrais, o quadro recusa (`exit≠0`) — a priorização não continua sem isso resolvido.

**Cite os IDs de Regra (`RN-*`)** que sustentam cada caso priorizado — a matriz de priorização referencia o contexto curado, não reproduz o enunciado de novo.

**Saída:** `caso/P4-priorizacao.md`, com autor da decisão registrado.
**Encerramento:** critério do passo 4 no documento do método.
