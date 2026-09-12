# 001 — Dois plugins: núcleo e playbook

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

O estúdio precisa travar a fronteira de delegação e, ao mesmo tempo, sustentar a afirmação de que o método é independente da ferramenta. Empacotar tudo junto torna a afirmação não verificável.

## Decisão

Dois plugins no mesmo marketplace:

- `eiac-nucleo` — guarda de camada, validador, máquina de etapas, trilha. **Não conhece método nenhum.**
- `eiac-campo` — habilidades, comandos, subagentes, template de caso. É o método.

O núcleo lê o playbook do caso e aplica o que ele declara. O que exige de qualquer playbook: toda etapa declara camada por nível e modalidade; todo entregável declara um portão; existe lista de itens inegociáveis não vazia; existem rótulos de procedência.

## Consequência

Trocar o playbook troca o método sem tocar em código. Um segundo playbook, ainda que nunca executado, prova a genericidade sem que ninguém precise acreditar.

O núcleo recusa carregar playbook incompleto — omissão é erro de carga, não de execução.
