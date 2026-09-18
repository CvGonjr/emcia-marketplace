# Procedência documental — referência obrigatória

Toda asserção gravada no repositório do caso carrega exatamente uma marca
de procedência:

| Código | Rótulo | Quando usar | Exige |
|---|---|---|---|
| `D` | Declarada | A organização forneceu a informação, ainda não verificada | Autor e data |
| `I` | Inferida | Pessoa ou ferramenta deduziu a informação | `premissa:` explícita |
| `V` | Verificada | Observação, documento-fonte ou leitura de volta confirmou a informação | Evidência identificada |

`D` não significa falsa. `I` não passa automaticamente a `V`. A marca não é
atribuída por modelo de linguagem: um agente pode propor e apontar evidência,
mas a confirmação segue a curadoria humana prevista pelo método.

## Dimensões separadas

Procedência não descreve meio de contato, local, braço de execução, tipo de
fonte nem técnica de apuração.

Quando houver número, a apuração pode ser registrada separadamente:

| Valor de `apuracao` | Exige |
|---|---|
| `medido` | Amostra e período |
| `calculado` | Fórmula e entradas |
| `estimado` | Base e margem |

Uma fonte externa usa `tipo_fonte: externa`, URL e limite da fonte. `externo`
não é procedência. Os antigos valores `campo`, `antitese`, `conversa`, `livre`
e `externo` não são aceitos como marca documental.

## Formato de linha

Declaração ainda não verificada:

```text
- [D · Helena · 2026-09-11]
  O volume informado é de 86 guias por mês.
```

Inferência com premissa:

```text
- [I · premissa: toda etapa presencial exige deslocamento · Celso]
  O custo de campo em N2 é dominado por transporte, não por horas.
```

Verificação por documento:

```text
- [V · documento: contrato-padrao.pdf p.3 · 2026-09-08 · Celso]
  O aceite do cliente precede a abertura do caso.
```

Verificação e apuração coexistindo como dimensões distintas:

```text
- [V · observacao: amostra de agosto · apuracao: medido · amostra: 86 guias · periodo: ago/2026 · Celso]
  Cinco de 86 guias exigiram retrabalho.
```

## Regra de ouro

**Se você não sabe se a marca é D, I ou V, a asserção não está pronta para
ser gravada.** Pergunte ao operador em vez de escolher.
