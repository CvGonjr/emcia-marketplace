# Passagem da habilitação ao caso — resultado

Decisão humana aprovada registrada em `decisoes/039-passagem-habilitacao-caso.md`.
Implementação em quatro pacotes, com dados exclusivamente sintéticos.

| Pacote | Resultado | Regressão completa |
|---|---|---|
| A (`f708a95`) | Importação humana, registro estruturado, arquivos conferidos e rascunho marcado | 804 verificações aprovadas |
| B (`692e1be`) | Pré-condição declarativa de evento seguido de selo confirmado no Git | 814 verificações aprovadas |
| C (`c8edc16`) | Abertura com expediente opcional e pacote conferido; diagnóstico somente leitura | 819 verificações aprovadas |
| D (commit deste relatório) | Recusa com evento das restrições sem destino nos entregáveis; parcial | 822 verificações aprovadas |

A suíte final contém 37 módulos; os 31 testes novos estão em
`testes/habilitacao_0d.py`. Cada pacote preserva suas saídas, regressão inicial,
regressão final, propostas canônicas e diff nas respectivas subpastas.

F0 permanece bloqueado quando o commit de selo falha depois da importação,
quando só há selo confirmado anterior ou quando o histórico Git não está
acessível. O controle com selo confirmado posterior permite carregar e
encerrar a etapa. Reimportação exige decisão explícita e novo selo.

O percurso sintético completo, executado no HEAD congelado do pacote C,
chegou às 13 etapas e cinco entregáveis, com sete selos e nenhuma negativa.
Os testes da árvore atual verificam separadamente a mudança D.

## Limites preservados

O pacote D não insere restrições por inferência. Falta um contrato que associe
o item da matriz ao ponto do entregável; E1–E5 com restrições ficam bloqueados,
nomeando os RH-xx sem destino e preservando arquivos anteriores.

O achado em P3b permanece para pacote posterior com decisão específica.
`exige_selo_apos` e `selar.py` foram preservados. Por essa exigência expressa,
o grep literal ainda encontra F0/E1 no exemplo histórico da docstring de
`selar.py`; não existe uso desses nomes na nova regra do núcleo.

O pacote `eiac-campo/reference/metodo/` não foi alterado. Propostas para
MAN-01 e ESP-01 estão nas evidências, sem tratar proposta como aprovação.
Versões finais: núcleo 0.2.36, campo 0.8.12, playbook 0.4.12.
Nenhum push ou alteração em dados reais de cliente foi realizado.
