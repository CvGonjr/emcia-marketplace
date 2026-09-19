---
description: Materializa e emite um entregável (E1-E5) do playbook Engenharia de IA de Campo.
---
Uso: `/emitir <E1|E2|E3|E4|E5>`

Carregue a habilidade `hb-emitir-<entregavel em minúsculas>` e siga o modelo oficial referenciado nela.

Renderize o entregável a partir dos artefatos reais do caso e, se o portão autorizar, registre a emissão apontando para o arquivo real:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/entregaveis.py" --renderizar <E1|E2|E3|E4|E5> --autor "<nome>" --emitir`

Sem `--emitir`, o comando só renderiza `caso/entregaveis/<ID>.md` e recusa se algum campo obrigatório do modelo oficial não tiver evidência rastreável no caso — nenhum campo ausente é preenchido com texto genérico.

Com `--emitir`, a emissão só é registrada se o portão declarado em `reference/gates.md` estiver autorizado: etapas do portão encerradas, condição declarativa satisfeita (ou não aplicável, para `E3-E`) e, quando o entregável exigir, os itens inegociáveis correspondentes já satisfeitos via `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/inegociaveis.py" --verificar <N> --arquivo <artefato> --satisfazer --autor "<nome>"`.

**`E3` consolida duas autorizações internas (`E3-D`, sempre avaliado; `E3-E`, condicionado a P5 classificar como agente) em um único entregável ao cliente — nunca duas entregas separadas.**
