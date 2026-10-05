---
description: Consulta ou retoma a habilitação administrativa, com conferências humanas registradas e templates aprovados pelo APR-01.
---
Uso: `/eiac-campo:habilitacao <expediente> [ação]`

Para o percurso completo, use `/eiac-campo:iniciar`. Leia `reference/habilitacao.md`,
`reference/canais.md` e os instrumentos HAB-01, ROT-02, CAN-01 e APR-01 do pacote
aprovado. Diferenças operacionais são autorizadas pelas decisões 045 e 047; não edite o pacote.

Consulte o estado antes de executar. Prepare JSON fora dos repositórios da ferramenta
e do método. Atos administrativos podem ser executados pela sessão depois de
aprovação explícita registrada: operação, resumo, trecho literal, data e responsável,
com entrada e hashes. Use `iniciar.py aprovar` e `executar` conforme a referência;
não escreva diretamente no expediente ou no caso. Aprovação é testemunho, não autenticação.

Tratamento administrativo precede a coleta. Preserve respostas, perguntas, ids,
versões e esclarecimentos, com campos consolidados vinculados a fontes. Carta,
qualificação, PDFs, signatários e evidências de assinatura exigem conferência humana.
Assinatura permanece externa no painel escolhido pelo cliente. Aguarde os PDFs
devolvidos e comprovantes indicados pelo engenheiro; não invente retorno ou autenticação.

Localize HAB-01/02/03 pelo código no APR-01, exatamente um arquivo por código;
confira seus hashes, tanto no pacote quanto se usar checkout canônico na tag.
`revisao-juridica` exige resultado exato `aprovado`, hashes e evidência; ciclo é texto
opcional. Parecer condicionado não vira revisão autorizadora. Revisão aprovada
prevalece sobre a aceitação explícita “uso as minutas sem ratificação jurídica”,
registrada uma vez na configuração e revogável. Sem revisão ou aceitação ativa,
a geração recusa; não transforme condição em aprovação nem invente dispensa.

Controle do modelo, aviso e histórico internos e registros de aceitação/situação
jurídica ficam no expediente, nunca no MD/PDF do cliente. A emissão mostra
“Para assinatura”. O checklist mostra “Minutas sem ratificação jurídica” sem bloquear.

Na decisão 047, item 9, Tally/Drive/Calendar operam sem perfil ou escopo por id
antes da abertura. Leituras, listagens, rascunhos e comparação não têm aprovação
própria; efeitos externos exigem “ok” com resumo/data. fetch_submissions entrega
o retorno ao script, que registra só a submissão do campo oculto caso; CSV é
alternativa. load_form admite qualquer formId. A confirmação de abertura cobre
aprovar o perfil/escopo apresentados e declarar Tally/calendário,
importar, validar 00-habilitacao e selar. Drive é provisionado em P2, com
aprovação do plano de criação/compartilhamento. Os comandos daqui são a
alternativa manual; o percurso normal usa o cartão e iniciar.py proximo.
Apuração, decidir-prosseguimento, sessões, restrições, autonomia, recalibragem,
encerramentos EX3/EX4 e selo após P2 continuam no terminal humano. Caso antigo
conserva o playbook; uma atualização do plugin não altera essa fronteira.
