# Caso — ALTERE-ME

Este repositório é um caso do playbook **Engenharia de IA de Campo**.

## Regras que valem em toda conversa aqui

**Nunca escreva direto em `caso/`.** Escreva o conteúdo em `rascunho/` e grave com `/eiac-nucleo:gravar`. A guarda bloqueia a escrita direta e registra a tentativa.

**Toda asserção carrega marcação.** Formato:

```
- [origem · fonte · data · autor]  texto da asserção
- [inferido · premissa: <premissa> · Celso]  texto
- [externo · https://... · captura: 2026-09-10 · limite: amostra enviesada]  texto
- [declarado · Helena · 2026-09-11 · medido · amostra: 86 guias · periodo: ago/2026]  texto
```

**Autor é sempre pessoa nomeada.** Nunca identificador de agente.

**A etapa corrente decide o que pode ser feito.** Consulte com `/eiac-nucleo:estado`. Se a guarda recusar uma ação, apresente o motivo e pare — não contorne.

**Procedimento de cada etapa:** documento do método, em `metodo/`. As habilidades remetem a ele; não o reproduzem.

## Estrutura

```
registro/playbook.json    o método como arquivo — não editar durante o caso
registro/estado.json      etapa corrente e cumprimentos
registro/eventos.jsonl    trilha de auditoria
rascunho/                 conteúdo proposto, antes do validador
caso/                     asserções gravadas
metodo/                   documentos do método, só leitura
```
