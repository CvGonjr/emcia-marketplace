# Documentação operacional — resultado

Data: 03/10/2026. Marketplace de partida: d5924c0e6b4771ac4b8fc8fb35d0a50775ce10c9.
Origem canônica: 1d6d1e8bfc1739594ea7a119257ecae28c8e5af4.
Versões finais: núcleo 0.2.44, campo 0.8.22, playbook 0.4.18, manifesto v4.

## Validação

| Execução | Resultado | Evidência |
|---|---|---|
| Inicial, Python 3.12.12 | 919 verificações, 46 módulos; sem falhas ou exclusões | regressao-inicial-3.12.txt |
| Final, Python 3.12.12 | 926 verificações, 47 módulos; sem falhas ou exclusões | regressao-final-3.12.txt |
| Pacote | 21 documentos iguais byte a byte ao objeto Git canônico; SHA-256 correto | metodo_empacotado.txt, comparacao-canonica.txt |
| Manual | conferir() vazio contra 0.4.18; cinco testes passam sem emenda | manual_a25.txt, conferir-manual.json |
| Citações | Sete testes, incluindo negativos, auxiliares, TRI real e retirada CTX | citacoes.txt, citacoes-conferidas.txt |
| Preservação | Núcleo/scripts de campo/contratos inalterados; negativos A25 e algoritmo com AST preservada | preservacao.txt |
| Grep | Sem remissão operacional ao roteiro antigo ou resumo CTX | grep-roteiro-operacional.txt, grep-ctx-operacional.txt |
| Histórico | As ocorrências antigas restantes são contexto da 039 e notas canônicas de renomeação | grep-roteiro-historico.txt |
| Diff | Sem erro de whitespace; alteração operacional completa | diff-check.txt, diff-operacional.patch, diff-stat.txt |

O executador reexecutar-suite.py descobre todos os módulos e preserva o PATH
Python 3.12 dos subprocessos. A regressão final confere o conjunto completo
do working tree antes dos seis commits interdependentes; os commits separam
os itens do pedido. O HEAD no log é o ponto de partida, e o diff registra o
conteúdo validado. Nos logs preservados, foi removido somente o espaço final
do cabeçalho vazio de exclusões para passar diff --check; não houve alteração
de resultado ou exclusão. O levantamento do histórico CTX também teve
seus espaços finais de apresentação normalizados. O executador agora imprime “nenhum” nesse campo.
Nenhum teste foi excluído, dispensado ou alterado para
acomodar divergência canônica.

## Entrega por item

1. build(metodo): reempacotar origem canônica e conferir manifesto v4.
2. test(manual): conferir MAN-01 v0.2 sem emenda local.
3. docs(habilitacao): remeter ao roteiro ROT-02 sem alterar templates.
4. test(citacoes): conferir seções e retirar resumos CTX anteriores.
5. docs(operacao): alinhar guias, interfaces, mapa e inventário de testes.
6. docs(limites): consolidar fronteiras e evidência da documentação operacional.

HAB-01 e os dois auxiliares foram incluídos junto com CAN-01 para que as citações
resolvam offline por arquivo e seção, com caminho canônico fixado no manifesto.
O nome real manifesto.json foi preservado; o pedido o chamava manifest.json.
Nenhum documento canônico foi editado à mão. O README local antigo do pacote,
com origem ultrapassada e execução de contraste retirada, foi removido.

O engenheiro decidiu retirar os resumos CTX anteriores: a nota da 021 registra
que não eram controlados pelo manifesto, e o mapa e o teste refletem a retirada.
O histórico da consulta está em pendencia-ctx.md e levantamento-ctx.txt.
A nota da 038 mantém v0.1 recuperável pelo commit canônico 968281c e registra
a passagem ao manual operacional sem sobreposição local.

Interfaces foram conferidas contra scripts existentes; detalhes em auditoria.md.
Assinatura integrada, aceite, gravação e transcrição permanecem fora do escopo;
coerência local não autentica origem, e a demonstração E7 cobre apenas Claude
Code 2.1.283 com MCP stdio sintético. Nenhum dado real de cliente foi usado.

O repositório canônico permaneceu limpo e no mesmo commit. A pasta preexistente
.projectdocs/figuras/ não foi alterada nem adicionada. Nenhum push realizado.
