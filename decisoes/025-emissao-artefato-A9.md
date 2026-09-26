# 025 — Emissão exige artefato declarado no playbook (A9)

**Data:** 26/09/2026 · **Estado:** firme quanto à correção solicitada

## Contexto

A verificação de F2 demonstrou que o comando de emissão do núcleo autorizava
E3-D apenas pelo cumprimento das etapas. A conferência de arquivo dependia
de `--materializar` e podia ser omitida. A versão de base é v-sprint3-poc.2.

Foram lidos CLAUDE.md, o índice e as decisões 022 e 023. A decisão 024 já
registra A8, por confirmação humana anterior; permanece preservada. Usa-se
o próximo número livre, 025 para A9, sem renumerar o histórico.

## Decisão

- Cada entregável declara `artefato` e `comando_materializacao` no playbook
  do caso. No campo, E3-D e E3-E apontam para o mesmo E3.md.
- O núcleo exige arquivo existente e não vazio no caminho declarado,
  relativo e interno ao caso. Diretório, caminho fora do caso ou
  materialização apontando para outro arquivo não satisfazem a regra.
- A recusa indica o caminho esperado e o comando declarado para gerar o
  artefato. O núcleo não contém o nome de comando do campo como regra.
- Etapas, condições e inegociáveis continuam conferidos. `NAO_APLICAVEL`
  continua registrável sem arquivo, como `EntregavelNaoAplicavel`.
- Emissão autorizada sempre grava arquivo, pessoa autora e versão no
  estado e em `EntregavelEmitido`; reemissão incrementa a versão. Emissão
  negada continua deixando evento, sem mutação no estado.

## Consequência

A9 sobe o núcleo a 0.2.24, campo a 0.8.3 e playbook a 0.4.5; A10, no
mesmo pacote de entrega, avança núcleo/playbook novamente.

Casos existentes precisam atualizar seu playbook explicitamente; ausência
de declaração de artefato/comando recusa o carregamento, sem ler o plugin.
O núcleo confere existência e conteúdo não vazio, sem julgar a qualidade
metodológica do documento. O campo mantém a materialização do conteúdo.

Os testes negativos precederam a implementação. Preparações de testes de
portão agora fornecem artefato; expectativas de versão contabilizam também
a emissão pelo núcleo. Nenhum teste anterior é removido.

Evidências: `.projectdocs/evidencias/sprint3/3.4/correcao-A9-A10/`.
