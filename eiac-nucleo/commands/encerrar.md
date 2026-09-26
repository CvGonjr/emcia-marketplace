---
description: Encerra a etapa corrente, se o critério de encerramento estiver cumprido.
argument-hint: <etapa>
---
Antes de executar, releia o critério de encerramento da etapa no documento do método e confirme com o operador que ele foi cumprido.

Confira a etapa corrente e a camada resolvida para o nível do caso com
`/eiac-nucleo:estado` e `/eiac-nucleo:fronteira`. O encerramento obedece à
exigência de sessão declarada por camada no playbook do caso. No método
atual, EX3 e EX4 exigem sessão humana registrada da própria etapa; EX1 e
EX2 não exigem sessão para encerrar.

Quando exigida, registre a sessão da etapa corrente, na modalidade
declarada, com `/eiac-nucleo:registrar-sessao <etapa> <participantes>`.
Sessão de outra etapa não libera o encerramento. Etapas futuras ou já
encerradas não aceitam registro de sessão.

Depois execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --encerrar <etapa> --autor "<nome da pessoa>"`

Se o script recusar, apresente o motivo sem contorná-lo.

A falta de sessão produz `TentativaNegada`, com etapa, camada, nível e
modalidade na mensagem. Satisfeita a sessão, o núcleo confere as demais
condições; a exigência de selo posterior declarada no playbook permanece.
