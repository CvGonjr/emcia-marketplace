# 009 — Habilidades remetem ao método, não o reproduzem

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

O documento do método já traz cada passo com calibragem por nível, corte de viabilidade e critério de encerramento. Habilidade que repete isso cria segunda fonte de verdade, e quando uma mudar a outra fica errada em silêncio.

## Decisão

Cada habilidade acrescenta quatro coisas e nada mais:

| Item | Por que não está no método |
|---|---|
| Camada no cabeçalho | metadado de carregamento |
| Comportamento de recusa | o método diz que o passo é humano; a habilidade diz o que o agente faz ao ser chamado |
| Caminho e formato de saída | onde grava, com qual marcação |
| Ponteiro para o instrumento | qual ferramenta do quadro se aplica |

Exceção: `hb-levantar-regras` é quase toda recusa, e recusa não está no documento do método.

## Consequência

Habilidade de quinze linhas, não de cento e cinquenta.

**Lição aprendida:** converter método em habilidade tende a duplicar o método. O formato precisa da regra explícita contra isso.
