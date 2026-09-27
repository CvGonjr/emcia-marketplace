---
description: Encerra a etapa corrente, se o critério de encerramento estiver cumprido.
argument-hint: <etapa>
---
Antes de preparar o encerramento, releia o critério de encerramento da etapa no documento do método e confirme com o operador que ele foi cumprido.

Confira a etapa corrente e a camada resolvida para o nível do caso com
`/eiac-nucleo:estado` e `/eiac-nucleo:fronteira`. O encerramento obedece à
exigência de sessão declarada por camada no playbook do caso. No método
atual, EX3 e EX4 exigem sessão humana registrada da própria etapa; EX1 e
EX2 não exigem sessão para encerrar.

Quando exigida, peça ao engenheiro registrar a sessão da etapa corrente, na modalidade
declarada, com `/eiac-nucleo:registrar-sessao <etapa> <participantes>`.
Sessão de outra etapa não libera o encerramento. Etapas futuras ou já
encerradas não aceitam registro de sessão.

Prepare o comando abaixo. Se a camada da etapa está na lista humana do
playbook (EX3/EX4 no campo), entregue ao engenheiro: ele executa no próprio
terminal, fora da sessão do Claude Code, com caminho absoluto real do plugin.
O agente não executa esse encerramento, mesmo com nome humano. Em EX1/EX2,
o encerramento continua permitido à sessão quando o playbook assim declara:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --encerrar <etapa> --autor "<nome da pessoa>"`

Se o script recusar, apresente o motivo sem contorná-lo.

A falta de sessão produz `TentativaNegada`, com etapa, camada, nível e
modalidade na mensagem. Satisfeita a sessão, o núcleo confere as demais
condições; a exigência de selo posterior declarada no playbook permanece.

Depois da sessão e do selo, o núcleo confere os produtos declarados em
`produtos_encerramento` da etapa. Produto ausente gera TentativaNegada e
preserva o estado. Apresente a descrição, o caminho e os campos faltantes;
prepare o registro correspondente antes de pedir novo encerramento.
