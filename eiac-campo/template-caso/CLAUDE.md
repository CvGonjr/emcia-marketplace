# Caso — ALTERE-ME

Este repositório é um caso do playbook **Engenharia de IA de Campo**.

## Regras que valem em toda conversa aqui

**Nunca escreva direto em `caso/`.** Escreva o conteúdo em `rascunho/` e grave com `/eiac-nucleo:gravar`. A guarda bloqueia a escrita direta e registra a tentativa.

**Nunca escreva direto em `contexto/`.** Escreva o objeto (termo, entidade, regra, fonte ou registro de confronto P3d) em `rascunho/` e cure com `/eiac-nucleo:curar`. A guarda bloqueia a escrita direta do mesmo modo que bloqueia `caso/`. Mudança de procedência (por exemplo `I` → `V`) ou de classificação de confronto exige versão nova com histórico — nunca sobrescrita.

**Toda asserção carrega marcação.** Formato:

```
- [D · Helena · 2026-09-11]  texto declarado
- [I · premissa: <premissa> · Celso]  texto inferido
- [V · observacao: <referencia> · Celso]  texto verificado
- [I · premissa: referência externa aplicável · tipo_fonte: externa · https://... · limite: amostra enviesada · Celso]  inferência apoiada em fonte externa
- [V · observacao: <referencia> · apuracao: medido · amostra: 86 guias · periodo: ago/2026 · Celso]  número medido
```

`D`, `I` e `V` são as únicas marcas de procedência. `apuracao` e
`tipo_fonte` são dimensões separadas. Agente pode propor a marca, mas não
confirmar autonomamente que uma informação é `V`.

**Autor é sempre pessoa nomeada.** Nunca identificador de agente.

**A etapa corrente decide o que pode ser feito.** Consulte com `/eiac-nucleo:estado`. Se a guarda recusar uma ação, apresente o motivo e pare — não contorne.

**Procedimento de cada etapa:** documento do método, em `metodo/`. As habilidades remetem a ele; não o reproduzem.

## Estrutura

```
registro/playbook.json    o método como arquivo — não editar durante o caso
registro/estado.json      etapa corrente e cumprimentos
registro/eventos.jsonl    trilha de auditoria
fontes/                   artefatos da organização, só leitura
rascunho/                 conteúdo proposto, antes do validador ou curador
caso/                     asserções gravadas
contexto/                 termos, entidades, regras, fontes e confrontos P3d curados (CA4)
metodo/                   documentos do método, só leitura
```
