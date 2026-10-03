# A2 — selo confirmado após encerramento

Quatro negativas falharam contra o motor anterior; o controle positivo passou.
A correção compartilha `_confirmar_selo_posterior` com `exige_evento_selado`.
A regressão intermediária identificou duas fixtures em sessao_a8: uma esperava
o tipo antigo RecusaMaquina, agora TentativaNegada por requisito explícito;
a outra fabricava SeloAplicado sem Git. Foi preservada a recusa e substituída
a preparação do controle por selo real. A fixture A18 também passou a selar
realmente para continuar exercitando G1, sem ser mascarada por G7.

Regressão final Python 3.12.12: 899 verificações em 45 módulos, zero falhas.
`restricoes.py` foi excluído explicitamente desta execução porque pertence ao
A3 ainda em construção e não a este commit. Todos os módulos de A1/A2 rodaram.
Sem mudança do pacote do método nem de selar.py.
