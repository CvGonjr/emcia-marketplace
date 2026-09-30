# Ação 4.3 — Correção A24: rotina vigente no E5

## Problema e correção

Na base `v-sprint3-poc.7`, `render_e5` lia `rotinas[-1]` após ordenação
lexical dos arquivos. A decisão 036 já fazia a recorrência selecionar
a maior `versao` inteira positiva do contrato declarado em P10. Assim,
`CAL-001` v10/Marina Prado e `CAL-999` v2/Celso do Vale produziam E5
com Celso e recorrência com Marina.

A seleção genérica foi extraída de `recorrencia.conferir` para
`recorrencia.selecionar_fonte`. A recorrência e o E5 chamam a mesma
função. O E5 obtém a regra do playbook **do caso** e carrega o arquivo
escolhido; contrato ausente/inválido ou fonte ambígua/ilegível/inválida
impede a materialização e, portanto, a emissão. A regra continua no
playbook, que não foi alterado nem injetado em casos antigos.

| Cenário | Antes | Depois |
|---|---|---|
| CAL-001 v10/Marina e CAL-999 v2/Celso | E5: Celso; recorrência: Marina | E5 e recorrência: Marina |
| Maior versão empatada, responsáveis distintos | E5 escolhia último nome lexical | E5 recusa fonte ambígua; não emite |
| Versão inválida em outra rotina | E5 podia ignorá-la pela ordem lexical | E5 recusa, como a recorrência |
| Ciclo `*-C*` com versão superior | Ignorado por filtro local | Ignorado pelo mesmo contrato da recorrência |

## Auditoria das outras seleções

| Fonte em `entregaveis.py` | Forma atual | Resultado e ação |
|---|---|---|
| Piloto revisado, E5 | `pilotos[-1]` lexical | Pode escolher outro conjunto revisado quando há vários IDs; a versão de cada CT não define, por si, um único piloto vigente entre IDs. As métricas têm `piloto_ref`, mas pode haver mais de uma métrica. Falta regra de seleção de conjunto; não substituir ordem lexical por uma suposta vigência global nesta correção. |
| Métricas de resultado apuradas, E5 | Itera **todas** as métricas filtradas | Não usa `[-1]`; nenhuma escolha lexical de um único registro. |
| Linhas de base, E2 | Itera **todas** as linhas de base | Não usa `[-1]`; nenhuma escolha lexical de um único registro. |
| Especificação operacional validada e termo decidido, E4 | `operacionais[-1]` e `termos[-1]` lexicais | Mesmo risco de escolha arbitrária entre IDs, mas sem contrato de fonte vigente comparável ao da decisão 036. Registrado para decisão própria; não alterado por A24. |

## Testes

`testes/e5_rotina_a24.py` foi escrito e executado antes da correção;
reproduziu a seleção incorreta. Na versão corrigida, suas **5 verificações**
passam:

| Teste | Verificação |
|---|---|
| 01 | Empate de maior versão com nomes distintos bloqueia emissão de E5 |
| 02 | Versão inválida não permite escape pela rotina antiga |
| 03 | v10 precede v2 apesar do nome lexical; E5 emitido mostra Marina |
| 04 | E5 e recorrência apontam a mesma pessoa e fonte no mesmo caso |
| 05 | Ciclo `*-C*` não substitui rotina vigente |

`testes/recorrencia_a23.py` também passou após a extração da função.
A suíte completa terminou verde: **786 verificações em 35 módulos**, sem
falhas (base: 781 em 34). A saída integral e a contagem por módulo estão
em `saida-suite.txt`.

## Versões e limite

Base: `v-sprint3-poc.7`; núcleo **0.2.34**; campo **0.8.8**;
playbook do template **0.4.9**. Guarda, selo, playbook, fronteiras e
aparato inativo do contraste não foram alterados. Nenhuma tag foi criada.
