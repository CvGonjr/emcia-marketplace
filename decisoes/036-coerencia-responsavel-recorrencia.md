# 036 — Responsável da recorrência conferido com a fonte vigente (A23)

**Data:** 28/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

No percurso da ação 3.8 sobre v-sprint3-poc.6, CAL-001 foi registrada com
Celso do Vale e a recorrência de P10 com Marina Prado. Ambos os nomes eram
válidos, mas designavam a mesma responsabilidade. A máquina aceitava a
recorrência sem consultar a rotina registrada.

## Decisão

A etapa declara `coerencia_responsavel_recorrencia` no playbook do caso:
padrão dos arquivos, padrão a excluir, campo da pessoa, campo da versão,
seleção `maior_versao` e orientação de troca. No método de campo, P10 aponta
para `registro/calibragem/CAL-*.yaml`, excluindo `*-C*.yaml` (ciclos), e
compara `responsavel` na maior `versao` inteira positiva.

O núcleo aplica esse contrato genérico antes de alterar o estado: recusa
ausência de fonte, divergência de responsável, fonte ilegível ou externa
ao caso, versão inválida e empate na maior versão com responsáveis
diferentes. Não decide por nome de arquivo nem por data do arquivo. A
recusa de divergência mostra ambos os nomes e a orientação: nova versão
da rotina, gravada pelo engenheiro no próprio terminal antes da recorrência.

A fonte comparada (arquivo, versão, campo e valor) fica registrada junto
à recorrência e ao evento. Toda recusa gera evento e preserva o estado.
Nenhum identificador de etapa nem diretório de método entra no avaliador.
Casos anteriores não recebem implicitamente o playbook do plugin.

## Consequência e verificação

`testes/recorrencia_a23.py` cobre negativas antes do caminho positivo,
mesmo responsável, troca por nova versão gravada por calibragem.py,
seleção numérica, exclusão de ciclos, empates, fonte externa, fonte
ilegível, contrato inválido e uso do contrato com outra etapa/campo/caminho.

Os auxiliares sintéticos usam Marina Prado na rotina e na recorrência.
A auditoria de outras responsabilidades está na evidência da ação 3.8;
nenhuma outra coerência é imposta nesta correção.
