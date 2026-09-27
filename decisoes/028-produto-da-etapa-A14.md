# 028 — Produto próprio exigido no encerramento (A14)

**Data:** 27/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

Sobre v-sprint3-poc.4, etapas podiam encerrar sem seu produto, embora o
portão de emissão recusasse depois. 027 já registra A12 e é preservada.

## Decisão

O campo declara `produtos_encerramento` em cada etapa. O núcleo interpreta
predicados genéricos: arquivo por padrão relativo ao caso, igualdade de
campos e campos preenchidos no mesmo arquivo; ou campo registrado na etapa.
Não há nomes de etapas, caminhos de método ou estados do campo no avaliador.

| Etapa | Produto mínimo para encerrar |
|---|---|
| P3a | Linha de base com indicador, valor atual e data |
| P5 | Classificação tecnológica registrada, na taxonomia declarada |
| P6 | OP em estado validado |
| P7 | AUT em estado decidido |
| P8 | Conjunto em estado revisado |
| P9 | Métrica tipo resultado em estado apurada |
| P10 | Rotina com responsável nomeado e cadência |

A sessão é conferida primeiro; dependências e selo continuam exigidos.
Sem produto: TentativaNegada, descrição/caminho/campos faltantes e nenhum
avanço do estado. Arquivo vazio, ilegível ou symlink externo não satisfaz.
Condições de arquivo são satisfeitas por um mesmo candidato; campos de
arquivos diferentes não se somam. Os validadores de campo continuam
responsáveis pela estrutura e referências de cada artefato.

## Verificação

`testes/produtos_a14.py`: negativas por etapa, estados/tipos errados, YAML
ilegível, caminho externo e contrato alternativo. Percursos anteriores
recebem produtos sintéticos somente na preparação; nenhuma asserção removida.
Casos existentes exigem atualização explícita do próprio playbook.
