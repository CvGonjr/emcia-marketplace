# 035 — Selo exibido pelo histórico confirmado do caso (A17)

**Data:** 28/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

O selo era registrado na trilha e no Git, mas estado.py exibia o campo
selo do arquivo, ainda vazio. SeloAplicado entra antes do commit para que
seu registro integre o conteúdo selado.

## Decisão

A apresentação JSON e o resumo do estado derivam o último selo do histórico
Git de registro/eventos.jsonl. Identificam a primeira introdução do evento
em commit com a nota e a pessoa autora correspondentes; exibem hash completo,
data do evento e nota. Eventos ainda não commitados não comprovam aplicação.

A leitura não regrava estado.json nem suja o caso depois do selo. A trilha
de trabalho não substitui o histórico confirmado. Sem selo confirmado,
ou sem histórico Git acessível, a apresentação não inventa um hash.
A máquina de etapas e a checagem G7 não são alteradas por esta correção.

## Consequência e verificação

`testes/selo_a17.py` cobre ausência de selo, commit recusado, último de dois
selos, resumo, commit posterior comum, tentativa frustrada após selo e
limpeza do caso imediatamente após aplicação. A apresentação é derivada;
o campo bruto no arquivo não é uma segunda fonte de verdade.
