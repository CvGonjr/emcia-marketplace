---
description: Registra a emissão de um entregável com portão aberto e artefato existente.
argument-hint: <entregável>
---
Execute no diretório do caso:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/avancar.py" --emitir <entregavel> --autor "<nome da pessoa>"`

O playbook do caso declara `artefato` e `comando_materializacao` para cada
entregável. O núcleo confere etapas, condição, inegociáveis e o arquivo
esperado; não produz o documento. Arquivo ausente, vazio ou caminho divergente
recusa a emissão. A mensagem indica o caminho esperado e o comando declarado
para materializar (no playbook de campo: `/eiac-campo:emitir`).

Use esse comando de campo para gerar o artefato a partir dos registros reais;
depois confira a emissão. `--materializar` precisa apontar para o mesmo caminho
declarado no playbook. A emissão guarda arquivo, versão e pessoa autora na
trilha e no estado. Nova emissão incrementa a versão.

O resultado `NAO_APLICAVEL` registra `EntregavelNaoAplicavel` e dispensa arquivo.
Se houver recusa por item inegociável ou portão pendente, apresente o motivo e
pare. Portão pendente é decisão do operador.
