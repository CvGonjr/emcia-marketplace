---
description: Grava o nível de complexidade apurado pela triagem no Registro do caso.
argument-hint: <nível> [eixos]
---
O nível é apurado pelo instrumento de triagem, não por você. Antes de executar, confirme com o operador qual foi o resultado e a conta dos três eixos — **o nível é o maior dos três, nunca a média.**

Execute:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --apurar-nivel <nivel> --autor "<nome da pessoa>" --eixos "<DAD n, GOV n, CRI n>"`

Se o script recusar, apresente o motivo sem contorná-lo.

O nível decide a camada de todas as etapas seguintes (CAT-01 3.6). Reapuração é permitida e fica na trilha com o valor anterior — não edite `registro/estado.json` à mão para corrigir.
