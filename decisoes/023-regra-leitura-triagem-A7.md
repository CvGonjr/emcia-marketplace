# 023 — Regra de leitura da triagem declarada e conferida (A7)

**Data:** 26/09/2026 · **Estado:** firme, por instrução do usuário

## Contexto

A verificação de F0 na Sprint 3 demonstrou A7: `avancar.py --apurar-nivel`
aceitava eixos como texto livre e gravava o nível informado sem conferir
a conta. N2 com `DAD 2, GOV 1, CRI 2` foi aceito, embora as somas estejam
fora da escala de EMCIA-TRI-01 §3.4.

O instrumento controlado define somas de 3 a 9 por eixo e nível pela maior
soma: 3–4 → N1, 5–7 → N2, 8–9 → N3. Essa regra é determinística e deve
ser conferida pelo sistema, preservando a separação núcleo × método.

O usuário confirmou o número 023 para esta decisão, pois a decisão 022
já registra a habilitação administrativa. A 022 permanece preservada.

## Decisão

- O campo declara a regra em `apuracao_nivel` no playbook do template:
  siglas DAD/GOV/CRI, mínimos e máximos, agregação `maximo` e faixas de nível.
- O núcleo interpreta os eixos, limites, operador e faixas do playbook
  do caso. Nenhum valor da escala ou sigla do método entra em seu código.
- A apuração exige todos os eixos declarados, como inteiros separados
  por vírgula. Eixos ausentes, desconhecidos, duplicados, malformados ou
  fora da faixa são recusados.
- O nível é calculado pela regra declarada. Divergência com o nível
  informado é recusada com a conta na mensagem, sem alterar o estado.
- Regra ausente, operador não suportado ou faixas inválidas também
  recusam. Não há modo de desativar essa conferência.
- Recusas de apuração em caso aberto produzem `TentativaNegada` com
  autoria nominal. Tentativa por agente é atribuída ao responsável do
  caso, sem registrar identificador de agente como autor.
- As expectativas dos testes anteriores são preservadas. Ajustes se
  limitam à preparação de eixos completos e coerentes com o nível.

## Consequência

O template passa a playbook 0.4.3, o núcleo a 0.2.22 e o campo a 0.8.1.
O comando de apuração e `hb-enquadrar` remetem à escala do instrumento e
à conferência determinística, sem reproduzir o procedimento completo.

Casos existentes continuam lendo sua própria declaração (decisão 002).
Não recebem atualização automática nem leem o playbook do plugin. Sem
`apuracao_nivel`, a reapuração recusa até atualização explícita do caso.

As evidências ficam em `.projectdocs/evidencias/sprint3/3.2/correcao-A7/`.
A versão verificada da correção recebe a tag anotada `v-sprint3-poc.1`;
`v-sprint3-poc` permanece como referência do comportamento anterior.
