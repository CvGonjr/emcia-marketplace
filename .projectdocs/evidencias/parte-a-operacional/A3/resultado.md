# A3 — restrições vinculadas a fontes

Negativas foram registradas antes do contrato e da materialização novos.
A primeira execução tinha fixtures com JSON como documento YAML completo,
fora do subconjunto do leitor mínimo; elas foram corrigidas para YAML com
valores JSON inline, sem alterar nenhuma condição de recusa. A execução
`testes-contratos-antes.txt` demonstra a ausência da trava humana e do
produto de P2. As implementações e correções intermediárias estão registradas.

`restricoes.py` fixa autoria no responsável e registra vínculo/dispensa,
versão, importação, data e decisão. Preserva anteriores e confere o hash do
registro contra a trilha. Exige fonte com contrato CTX e curadoria registrada.
O produto genérico do núcleo confere cobertura de ids e integridade de origem
e destino. A habilitação com desfecho prosseguir satisfaz cobertura vazia.

Renderização recebe os vínculos íntegros e insere marcas no próprio valor.
REC só resolve por relação explícita no objeto F curado e por recebimento
íntegro. Falta de relação produz TentativaNegada com o id da asserção.
O teste por campo confere que valores não afetados não recebem a marca.
RH pendente mantém bloqueio anterior e preserva a versão já existente.

A regressão intermediária encontrou a lista humana histórica e a conferência
do MAN-01 base defasadas pela mudança aprovada em 041. A lista mantém todos
os atos anteriores e inclui o novo. O teste do manual conserva a detecção
das duas divergências base e confere a emenda local explícita, em separado.
O pacote do método fica intacto; a revisão v0.2 continua proposta documental.

Final em Python 3.12.12, sem PyYAML: **919 verificações em 46 módulos,
zero falhas**, sem exclusões. Inclui negativos.sh, contexto.py e todos os
módulos na raiz de testes/. JSON válido e scripts compilam em 3.12.

As duas demonstrações integrais passam a partir do snapshot temporário
registrado em snapshot-demo.txt, fora da branch: percurso sem restrição e
percurso com restrição. Ambos emitem E1–E5 e completam F0–P10. O restrito
adia E1 até P2; não dispensa RH automaticamente. E2 materializado está na
própria evidência. A variante do preparador também é exercitada pelo teste
ponta a ponta que efetivamente emite E2 após os portões.

Busca no núcleo alterado não encontra vocabulário administrativo. O único
resultado da busca ampla `restri` é “mais restritiva”, texto genérico antigo.
A referência histórica F0/E1 da docstring de selar.py permanece, conforme
limite previamente registrado na 039; nenhuma nova regra usa esse vocabulário.
Versões: núcleo 0.2.44, campo 0.8.21, playbook **0.4.18**.
