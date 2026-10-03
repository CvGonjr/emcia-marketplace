# Correspondência CAT-01 — evidência operacional

Data: 2026-10-03. Autor: Celso do Vale.

Linha de base marketplace: `ebb6bbda55ea7403bc0e09a0bc316f0a1071cf4f`, branch master.
Origem canônica final: `989e1e73796a356b660be8ed55b686ba716787ac`, emcia-artefatos.
Versões: núcleo 0.2.45, campo 0.8.23, playbook 0.4.19, manifesto 5.
Documentos reempacotados: CAT-01 v0.5, CAM-01 v0.4, GLO-01 v0.4 e MAN-01 v0.4.
Os 21 documentos provêm de objetos Git, com hashes SHA-256 conferidos; nenhum
texto do pacote foi editado manualmente. Estado e aprovação canônicos são preservados.

## Correção aprovada e retomada do item 3.2

A pré-validação inicial encontrou a célula de produto F0 como `—` no MAN-01
v0.3, incompatível com o produto obrigatório. O trabalho parou conforme item
3.2. `prevalidacao-manual.json`, `prevalidar-manual.py`, `diff-inicial.txt`
e `propostas-artefatos.md` preservam esse diagnóstico sobre a origem
`2cf4ebd913b7a4de2ca7f5a2322a991bc69c1cbe` e playbook anterior.

O engenheiro aprovou a expressão literal **Decisão de prosseguimento registrada**,
que cobre ambos os desfechos. Antes do commit canônico, a função original
`manual_a25.conferir()` retornou **[]** contra o rascunho MAN-01 v0.4 e contrato
em memória (`correcao-manual-precommit.json`). O commit canônico modificou
somente essa célula, versão e histórico solicitado, preservando Estado
Em revisão e Aprovação pendente. O histórico registra "produto de F0 alinhado
ao contrato de decidir-prosseguimento". A decisão 043 registra a aprovação e
a retomada. O playbook usa exatamente a mesma descrição.

O pacote foi reextraído desse novo commit. `metodo-empacotado.txt`,
`manual-final.txt`, `manual-conferir-final.json` e `citacoes-final.txt`
registram a retomada dos itens 3.2 e 3.3: inventário e bytes canônicos corretos,
`conferir() == []`, quatro negativas de A25 e remissões MET-01 §3.4.1/§3.4.3.

## Testes e execução

- Linha de base: Python 3.12.12, **926 verificações em 47 módulos**, zero falhas,
  nenhuma exclusão (`regressao-inicial.txt`).
- Regressão final: Python 3.12.12, **958 verificações em 49 módulos**, zero falhas,
  nenhuma exclusão (`regressao-final.txt`).
- Catálogo: 11 testes, incluindo negativa de cada regra solicitada
  (`catalogo-final.txt`). Todas as 21 HBs estão relacionadas às 13 etapas;
  P3b permanece sem HB por desenho. Anexo A reproduzido literalmente e
  relação do Anexo C conferida com playbook e frontmatter.
- Prosseguimento: 20 testes (`prosseguimento-final.txt`). Negativas do ato pela
  sessão, autoria, campos, desfecho, data, versão, integridade, ausência de
  produto e bloqueio das etapas seguintes precedem os controles positivos.
  Ambos os desfechos permitem encerrar F0. Nova decisão preserva as anteriores;
  E1 apresenta desfecho, decisor, data e motivo. Casos com playbook anterior
  conservam o comportamento anterior.
- `catalogo-antes.txt` e `prosseguimento-antes.txt` preservam as execuções
  vermelhas antes da implementação. O primeiro inclui uma falha inicial de
  montagem da negativa HB-09, corrigida antes de alterar o playbook.
- `regressao-desenvolvimento.txt`, `regressao-fixtures.txt` e
  `regressao-pre-final.txt` preservam resultados intermediários. As fixtures
  receberam a precondição explícita pelo script real; não se removeu teste,
  não se desativou guarda e não se mudou o contrato para fazê-las passar.
- A inspeção `grep-nucleo.txt` não encontrou vocabulário do método nos scripts
  do núcleo. Condições de continuidade, produtos e integridade são genéricos.

O executador descobre todos os módulos raiz de testes/ e negativos.sh.
Não soma reexecuções às contagens. Comando usado, sem argumentos de exclusão:

```bash
PATH=/home/netiv-dn-1/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin:$PATH \
  PYTHONDONTWRITEBYTECODE=1 python3 \
  .projectdocs/evidencias/correspondencia-cat01/reexecutar-suite.py \
  /tmp/emcia-cat01-regressao-final-958.txt
```

## Percursos congelados no Git

As duas variantes de percurso-completo.sh usaram a fonte imutável `5469ec2`,
com Python 3.12.12. Cada uma encerrou as 13 etapas até P10, registrou o ato
humano de F0 e materializou E1. A variante integral executou 72 invocações
diretas (68 do percurso, 3 de infraestrutura, 1 de resumo); a restrita executou
71 (67, 3, 1). Não houve erro ou TentativaNegada nesses controles positivos.

`demo-cat01-integral.txt` e `demo-cat01-restrita.txt` preservam a saída completa.
`percursos-verificados.json` registra a conferência do selo P2 citado no mapa,
dos bytes do estado declarado, dos candidatos I para P4 e da decisão em E1.
Comando da variante integral, acrescentando `com-restricao` na outra:

```bash
PATH=/home/netiv-dn-1/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/bin:$PATH \
  PYTHONDONTWRITEBYTECODE=1 EMCIA_DEMO_BASE=/tmp/emcia-cat01-demos-20261003 \
  bash .projectdocs/demos/percurso-completo.sh cat01-integral
```

Os worktrees temporários das demonstrações foram removidos pelo roteiro.
`diff.txt` cobre todas as alterações de implementação e documentação desde
a linha de base até `5469ec2`, antes desta pasta de evidência. `commits.txt`
lista os nove commits por item; `versoes.json` fixa versões, origem e contagens.
A suíte final foi executada sobre esses mesmos arquivos antes dos commits;
o HEAD impresso na saída identifica a linha de base do diretório de trabalho.

## Limites e divergências

A divergência inicial do MAN-01 foi resolvida pela correção autorizada.
A divergência de natureza de HB-16 entre CAT-01 e CAM-01 permanece descrita
no Anexo D.3 canônico; habilidades.json reproduz CAT-01 conforme instrução.
Nenhuma decisão documental foi tomada por semelhança. As sete atividades do
Anexo B seguem com o engenheiro, sem novas HBs inventadas.

D5 distingue quatro frentes de P1 e mapa de valor de P3d. O mapa usa o estado
declarado selado após P2 e prepara candidatos D/I para P4; não substitui a
observação nem realiza o confronto humano. D7 separa preparação de decisão.
A 043 supera explicitamente a autoria provisória da 020. AG é agrupamento;
a autoria de eventos permanece nominal.

Nenhum push foi realizado e nenhum dado real de cliente foi usado. A pasta
preexistente `.projectdocs/figuras/` foi preservada. As provas sintéticas não
autenticam conteúdo remoto nem demonstram hooks em clientes adicionais.
