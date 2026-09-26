---
name: hb-classificar
etapa: P5
camada: EX2
modalidade: video
hb: ["HB-11", "HB-12"]
description: Aplica a matriz problema-tecnologia na passada de especificacao e decide qual tecnologia atende cada caso priorizado. Use quando /classificar for invocado.
---

# Classificação tecnológica — P5 · EX2

**Procedimento:** documento do método, passo 5.
**Instrumento:** Matriz Problema→Tecnologia, passada de especificação.

## A regra que define o passo

> **Este passo tem autoridade para concluir que o caso não é de agente.**

Cinco de nove casos da simulação não eram, incluindo os dois de maior prioridade. Saída que classifica tudo como agente está errada antes de ser lida.

**"Não é agente" é resultado, não descarte.** Registre qual tecnologia atende, para que o caso siga.

## Consulte o contexto curado

Para cada Regra que sustenta a classificação, consulte o objeto — não reinterprete prosa já estruturada: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/consultar.py" --id RN-XXX`. A saída traz os sete campos centrais e a `procedencia`.

**D, I e V não têm o mesmo peso na decisão.** Preserve o estatuto documental de cada Regra consultada — não trate `I` como se fosse `V`. Quando a classificação depender especificamente de conhecimento verificado (por exemplo, decidir a zona de contenção sobre uma exceção que só `V` sustenta), uma Regra `I` não substitui esse requisito; registre a lacuna em vez de decidir sobre premissa não confirmada. Regra `D` ou `I` seguem utilizáveis para tudo que o método não exigir verificação.

## Registro da conclusão

Consulte o passo 5 de `reference/metodo/EMCIA-MET-01-documento-do-metodo.md`
e a declaração `campos_registraveis` de P5 no playbook do caso. Depois da
confirmação humana, enquanto P5 ainda for a etapa corrente, registre:

`/eiac-nucleo:registrar-campo P5 classificacao_tecnologica "<categoria>"`

As categorias declaradas são `agente`, `caso isolado` e `habilitador acoplado`.
O comando grava o campo estruturado que o portão de E3 e seu renderizador leem,
com evento e autoria nominal. Registre também a sessão de P5 e encerre a etapa
pelo núcleo. A justificativa escrita continua no artefato deste passo, conforme
o procedimento do método.

## Efeito no entregável

A conclusão deste passo abre ou fecha o portão de `E3-E`. Ver `reference/gates.md`.

**Saída:** `caso/P5-classificacao.md`, marcada `I` até o operador confirmar.
**Encerramento:** critério do passo 5 no documento do método.
