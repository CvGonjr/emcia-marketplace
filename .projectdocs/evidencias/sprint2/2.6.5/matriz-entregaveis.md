# Matriz de entregáveis — pacote 2.6.5

Estado final, após implementação. Fonte: `eiac-campo/scripts/entregaveis.py`.

| Entregável | Autorização | Fonte | Arquivo material | Versão | Status |
|------------|-------------|-------|-------------------|--------|--------|
| E1 | E1 | Cumprimento de F0 (`eixos`, `nível`) | `caso/entregaveis/E1.md` | 1 (caso de controle) | MATERIALIZÁVEL |
| E2 | E2 | `registro/baseline/BL-*.yaml` (I1) | `caso/entregaveis/E2.md` | 1 | MATERIALIZÁVEL |
| E3 | E3-D + E3-E | Cumprimento de P5 (`classificacao_tecnologica`) | `caso/entregaveis/E3.md` | 1 | MATERIALIZÁVEL |
| E4 | E4 | `registro/operacional/OP-*.yaml` (P6) + `registro/governanca/autonomia/AUT-*.yaml` (P7, I2) | `caso/entregaveis/E4.md` | 1 | MATERIALIZÁVEL |
| E5 | E5 | `registro/piloto/CT-*.yaml` (I3) + `registro/metricas/MET-*.yaml` (I4) + `registro/calibragem/CAL-*.yaml` (I5) | `caso/entregaveis/E5.md` | 1→2 (reemissão testada em T42) | MATERIALIZÁVEL |

## Reemissão e versionamento (T41/T42)

Cada emissão bem-sucedida grava `st["entregaveis_emitidos"][ID] =
{arquivo, versao, autor}` em `registro/estado.json`, incrementando
`versao` a cada nova chamada — uma reemissão nunca sobrescreve
silenciosamente a anterior; o histórico de versão fica no próprio
estado do caso e no evento `EntregavelEmitido` (que carrega `arquivo` e
`versao`).

## Emissão sem arquivo (T40)

`avancar.py --emitir --materializar <caminho>` recusa registrar a
emissão se o caminho indicado não existir ou estiver vazio — testado
diretamente apontando para um arquivo que nunca foi renderizado
(`caso/entregaveis/E5-inexistente.md`).

## Nenhum entregável emitido inventa conteúdo ausente (T48/T49)

`entregaveis.py` levanta `NaoMaterializavel` e recusa renderizar
quando um campo obrigatório do modelo oficial não tem artefato real no
caso (T48: E2 sem nenhuma linha de base). Quando o dado existe, ele é
reproduzido literalmente do artefato-fonte, nunca reescrito ou
resumido por geração livre (T49: `valor_atual`/`apuracao` da baseline
aparecem letra por letra em `caso/entregaveis/E2.md`).
