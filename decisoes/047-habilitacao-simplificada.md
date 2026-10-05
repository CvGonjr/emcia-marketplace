# 047 — Habilitação simplificada e abertura sem Drive

**Data:** 05/10/2026 · **Autor:** Celso do Vale · **Estado:** firme por instrução do engenheiro

## Contexto

O engenheiro aprovou simplificar os atos administrativos anteriores ao percurso:
cliente responde um formulário permanente e assina três documentos separados;
engenheiro envia o link, deposita uma exportação e os PDFs assinados e confirma
três conjuntos de atos. Esta decisão emenda a 045. F0 a P10, decisões de método,
camadas, procedência e autoria nominal conservam suas regras.

## Decisão

1. Um formulário Tally permanente por tipo fica em `~/.emcia/config.json`, com
   formId, versão/hash do contrato, data e hash do relatório conferido. O link
   acrescenta `?caso=<caso>`. Alteração do contrato ou nova leitura do formulário
   invalida a conferência até novo relatório sem divergência e “conferido”.
2. O engenheiro deposita o CSV em `~/emcia-op/entrada/`. A leitura local filtra
   pelo caso reservado antes de qualquer persistência. Preserva somente linhas
   desse caso, hash do filtrado e hash do original, sem copiar o original.
   Zero ou várias submissões aguardam indicação humana; não há escolha automática.
   A fonte usa `tally-exportacao`. A API ampla continua recusada.
3. Lacunas geram perguntas; resposta colada vira fonte `manual`, com rodada,
   sem exigir formulário novo ou operações pendencia/resolver/reabrir. Essas
   operações permanecem na alternativa manual.
4. As condições administrativas configuradas são aplicadas automaticamente,
   com referência e hash. Só condição diferente exige esclarecimento específico.
5. Três confirmações, sem frase obrigatória, conservam resumo, trecho literal,
   data, pessoa e hashes: revisão conjunta dos três documentos, cobrindo revisar/
   gerar/liberar; conferência dos três PDFs assinados e evidências; abertura,
   importação, validação de 00-habilitacao e selo. Silêncio não é aprovação.
6. A matriz deriva das respostas 0c e é apresentada para confirmar/corrigir em
   mensagem; restrições conservam o mecanismo vigente. Não se presume acesso
   concedido, disponibilidade ou agenda a partir de resposta ambígua.
7. A abertura declara Tally e calendário, sem pastas Drive. O provisionamento
   ocorre em P2, com aprovação da criação e compartilhamento. P2 continua
   bloqueada sem os canais que exige; nenhum caso existente migra automaticamente.
8. `/eiac-campo:iniciar` carrega somente o cartão operacional de uma página e
   usa `iniciar.py proximo`: uma chamada por avanço, saída curta, retomada pelo
   estado e parada na próxima informação ou aprovação humana necessária.

## Limites e documentação

APR-01 continua resolvendo os três templates por código e hash. Não há edição
ou reempacotamento do método. Ratificação/aceitação revogável seguem a 045.
A configuração inicial do ambiente, conferência dos formulários, perfil e
situação jurídica são preparação reutilizável, fora das três confirmações por
caso. Compartilhamento em P2 é aprovação posterior, fora da abertura.

A conferência de PDF e assinatura continua testemunho humano, sem autenticação
criptográfica. Hash fixa bytes, não identidade nem mérito. Decidir-prosseguimento,
apuração de nível, sessões e demais decisões de método continuam no terminal.
F0 liberado não significa F0 encerrado. Nenhuma mensagem é enviada automaticamente.

Mudanças de HAB-01, ROT-02, CAN-01 e MAN-01 são propostas no arquivo correspondente.
A25 conserva exatamente a falha conhecida da 045:
`ato humano selar-apos-P2 ausente das seções 3.3 e 3.4`, em test_01; quatro
negativas passam. A lista exata é conferida, sem ocultar saída do teste.
Qualquer divergência nova interrompe a regressão e os commits.

## Verificação

Linha de base no commit 70702c6: 1109 verificações em 53 módulos em Python
3.12.12; 1111 em 3.14.4. Uma falha conhecida A25, zero falhas inesperadas.
As duas verificações adicionais correspondem à disponibilidade de PyYAML.
Evidência: `.projectdocs/evidencias/habilitacao-simplificada/`.
