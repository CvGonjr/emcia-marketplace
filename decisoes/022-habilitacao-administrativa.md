# 022 — Expediente administrativo de habilitação anterior ao caso

**Data:** 25/09/2026 · **Estado:** firme quanto ao escopo aprovado nesta sessão

## Contexto

A habilitação precisa preservar respostas, esclarecimentos e os três documentos
assinados antes da abertura do caso. O protocolo anterior proibia processamento
de qualquer informação do cliente antes de 0d. O usuário decidiu expressamente
permitir processamento apenas administrativo em expediente separado e reservar o
identificador do futuro caso. Decidiu manter a carta atual, com revisão humana
obrigatória antes da emissão, e assinatura pelo painel escolhido pelo cliente.

## Decisão

- O expediente vive fora dos repositórios da ferramenta, do método e do caso.
  Sua criação é humana, anterior à sessão, fixando responsável e identificador.
- Informações administrativas podem ser processadas antes de 0d com origem e
  condições de tratamento previamente registradas. Dados operacionais aguardam
  abertura e registro de procedência; a exceção não abre o caso antecipadamente.
- O `eiac-campo` fornece comando e script de habilitação. O núcleo continua
  agnóstico; nenhuma regra de Tally ou de HAB entra nele.
- O identificador do futuro caso é reservado; os documentos deixam explícito
  que o caso ainda não foi aberto.
- A assinatura é externa, pelo painel escolhido pelo cliente, sem integração.
  O expediente registra documentos finais e a conferência humana das evidências.
- A carta canônica é mantida. Sua conferência humana é requisito de emissão;
  não se presume resolvida a divergência de conteúdo em relação ao protocolo.

## Consequência

`habilitacao.py` não cria caso, não escreve nele e não libera F0. A assinatura
registrada continua sendo testemunho da conferência humana, conforme 008.
Autoria fixa e ator de decisão permanecem separados conforme 019. O procedimento
vive nos documentos canônicos; o comando remete a eles conforme 009.

O expediente tem validação determinística e histórico, mas não as guardas de
sessão de um caso aberto nem autenticação de identidade. O disco do engenheiro
continua sendo a fronteira de confiança. Esta decisão não altera 003 ou 005.
