# Procedência — referência obrigatória

Toda asserção gravada no repositório do caso carrega três marcações. Duas sempre, a terceira só quando houver número.

## Contexto — quem produziu

Atribuído pela etapa, nunca escolhido.

| Valor | Quando |
|---|---|
| `campo` | Percurso real do método |
| `antitese` | Braço de controle, sem humano |
| `conversa` | Fora de caso |

## Origem — como foi obtido

| Valor | Exige | Entra em entregável |
|---|---|---|
| `verificado` | Observação direta ou documento interno, com fonte e data | Sim |
| `declarado` | Autor nomeado e data | Sim, marcado |
| `inferido` | Premissa explícita | Sim, marcado, requer confirmação |
| `externo` | URL, data de captura e limite da fonte | Sim, marcado, requer confirmação |

## Apuração — só para número

| Valor | Exige |
|---|---|
| `medido` | Amostra e período |
| `calculado` | Fórmula e entradas |
| `estimado` | Base e margem |

**Medição inicial não aceita `estimado`.**

## Formato de linha

```
- [verificado · documento: contrato-padrao.pdf p.3 · 2026-09-08 · Celso]
  O aceite do cliente precede a abertura do caso.
```

```
- [inferido · premissa: toda etapa presencial exige deslocamento · Celso]
  O custo de campo em N2 é dominado por transporte, não por horas.
```

```
- [declarado · Celso · 2026-09-11 · medido · amostra: 9 casos simulados · periodo: ago/2026]
  Cinco de nove casos nao eram caso de agente. valor: 5 unidade: casos
```

## Regra de ouro

**Se você não sabe qual marcação usar, a asserção não está pronta para ser gravada.** Pergunte ao operador em vez de escolher.
