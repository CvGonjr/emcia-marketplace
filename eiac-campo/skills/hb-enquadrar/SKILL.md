---
name: hb-enquadrar
etapa: F0
camada: EX1
modalidade: assincrono
hb: ["HB-01", "HB-02", "HB-03"]
description: Estrutura a dor declarada e calcula o nivel de complexidade da organizacao. Use quando /enquadrar for invocado ou quando um caso novo nao tiver ficha.
---

# Enquadramento e triagem — F0 · EX1

**Procedimento:** documento do método, Fase 0. Não reproduza aqui.
**Instrumento:** EMCIA-TRI-01, seção 3.3 para as perguntas e seção 3.4 para
a pontuação, no pacote controlado em `reference/metodo/`.
As nove perguntas têm redação fixa e não podem ser reformuladas.

Registre as somas dos eixos na escala de 3 a 9 indicada pelo instrumento.
Escreva a conta antes do resultado e prepare o comando de
`/eiac-nucleo:apurar-nivel` para o engenheiro conferir e executar no próprio
terminal, fora da sessão. Se houver recusa, apresente o motivo
ao operador; não edite o estado para contorná-la.

**Pare e pergunte** se o custo do problema exigir cálculo e a premissa admitir mais de uma base. Não escolha; registre quem escolheu.

**Saída:** `caso/E1-ficha.md`, toda asserção marcada conforme `reference/procedencia.md`.
**Encerramento:** critério da Fase 0 no documento do método.

## Execução das decisões humanas (A12)

O agente prepara a proposta e os comandos; o engenheiro executa as decisões
no próprio terminal, fora da sessão do Claude Code, no diretório do caso.
Nome humano informado não autoriza o agente. Resolva o caminho do plugin e
entregue comandos com caminho absoluto real e argumentos confirmados.

Apuração de nível, sessão, campos de decisão, recorrência e satisfação de
inegociáveis são operações humanas declaradas no playbook. A verificação de
inegociável sem `--satisfazer` continua permitida; com `--satisfazer`, entregue
o comando ao engenheiro. Encerramento em EX3/EX4 também é feito por ele.
O agente pode ler, gravar preparação pelos scripts, validar asserções, curar
contexto e materializar/emitir entregáveis. A recusa da guarda registra
`TentativaNegada` com operação e comando exato.
