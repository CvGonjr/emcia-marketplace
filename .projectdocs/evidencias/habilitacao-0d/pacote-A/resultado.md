# Pacote A — importação humana do expediente

Decisão 039 aprovada em 02/10/2026. Núcleo e selar.py não alterados neste pacote.
Campo 0.8.9; playbook 0.4.10. A pré-condição de F0 pertence ao pacote B.

O importador exige expediente íntegro e pronto, identidade reservada e autoria
coincidentes, ausência de etapa encerrada e decisão explícita para reimportação.
Copia somente PDFs assinados, evidências e matriz; hashes conferidos na origem
e após cópia. Preserva versões anteriores, prepara rascunho marcado para validar.py
e registra HabilitacaoImportada. Cada recusa testada registra TentativaNegada.
A matriz deriva da entrada com hash registrada no expediente; não da resposta Tally.

Negativas escritas e executadas antes da implementação: regressao-inicial.txt.
Controles positivos posteriores: importação, validação, hashes e reimportação.
A regressão intermediária encontrou a lista de atos esperados em decisao_a12;
a expectativa foi ampliada com o novo ato, preservando as regras anteriores.
O teste do manual mantém o alcance de §3.3/3.4 (percurso); o ato anterior ao
percurso tem escopo declarado e a alteração de §3.2 vai como proposta canônica.
Saída da suíte completa em saida-suite.txt e do módulo em regressao-final.txt.

Limites: autoria não autentica identidade no SO; o expediente é uma fronteira
local de confiança, conforme 022. Os PDFs das fixtures são controles sintéticos,
sem assinaturas reais. Retomada durante percurso não é reimportação deste pacote.
