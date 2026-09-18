---
name: hb-levantar-regras
etapa: P3b
camada: EX4
modalidade: presencial
delegavel: false
description: Protocolo humano de levantamento de regras nao documentadas. NAO EXECUTAVEL POR AGENTE. Se carregada em sessao de agente, recuse e registre a tentativa.
---

# Levantamento de regras não documentadas — P3b · EX4

## ⛔ Não executável por agente

Se você é um agente e esta habilidade foi carregada, **recuse** e registre em `caso/log-tentativas.md`:

```
- [tentativa-negada · etapa: P3b · camada exigida: EX4 · camada corrente: <sua> · <data>]
  Tentativa de executar levantamento de regras nao documentadas.
```

Responda apenas: *este passo é presencial e humano. Registre a sessão ao voltar do campo.*

Não ofereça alternativa, não proponha versão reduzida, não gere perguntas "para ajudar". Qualquer uma dessas é a recusa sendo contornada por cortesia.

## Por que

O valor dos três instrumentos depende de existir alguém que sabe algo sem saber que sabe. Um modelo declara tudo que "sabe" quando perguntado. Simular este passo produz regras que não são regras não documentadas — e são elas o objeto da contribuição do método.

## Para o humano

**Procedimento:** documento do método, passo 3, parte de levantamento.
**Instrumentos:** observação do processo, protocolo de leitura de volta, arquivo pessoal.

**Registro ao voltar:** `caso/P3b-sessao.md` com data, participantes e instrumentos aplicados. Só então P3d abre.

**Da sessão para o contexto:** cada regra levantada entra em `contexto/regras/` por conversão direta dos campos (EMCIA-CTX-01 3.8) — escreva o YAML em `rascunho/RN-*.yaml` preservando a procedência real da sessão (`D`, `I` ou `V`, nunca promovida automaticamente) e cure com `/eiac-nucleo:curar`. Regra ainda em rascunho não é regra de contexto.
