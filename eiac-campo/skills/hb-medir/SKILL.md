---
name: hb-medir
etapa: P3a
camada: EX3
modalidade: remoto
description: Produz a medicao inicial a partir das amostras enviadas pela organizacao. Use quando /medir for invocado.
---

# Medição inicial — P3a · EX3

**Procedimento:** documento do método, passo 3, parte de medição.

**O cálculo é feito em código, não por leitura.** Apresente a conta.

**`apuracao = estimado` não satisfaz a medição inicial fora de N1.** Se não houver amostra em N2/N3, a medição não foi feita — diga isso em vez de estimar. É o item inegociável 1 e bloqueia o E2 (MET-01 3.4.3: estimada só é admitida em N1; N2 e N3 exigem cálculo ou medição).

**Saída narrativa:** `caso/P3a-medicao.md`, com `amostra` e `período` obrigatórios. A medição não é um dos quatro objetos de `contexto/` — o CTX-01 não define esse objeto, e nem toda medição precisa virar registro curado.

**Saída estruturada (linha de base, evidência do inegociável 1):** grave o indicador em `rascunho/BL-NNN.yaml` e registre com `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/baseline.py" --arquivo registro/baseline/BL-NNN.yaml --ator "<nome>"`. Este é o artefato que `inegociaveis.py --verificar 1` e a materialização de E2/E5 consomem — a narrativa em `caso/P3a-medicao.md` não substitui o registro estruturado.

**Quando esta medição sustentar uma Regra ou Fonte `V`,** dê à linha da medição um identificador estável dentro de `caso/P3a-medicao.md` (por exemplo, um cabeçalho ou âncora citável), para que `evidencia.referencia` daquele objeto CTX possa apontar para ela sem ambiguidade. Isso é vínculo rastreável, não duplicação — a medição continua vivendo só em `caso/P3a-medicao.md`.

**Encerramento:** critério do passo 3 no documento do método.
