# Ação 3.8 — Correção A23

## Lacuna e escopo

A evidência original em `../resumo-percurso.txt`, produzida sobre
v-sprint3-poc.6, registra CAL-001 com **Celso do Vale** e a recorrência de P10
com **Marina Prado**. As duas entradas nomeavam a mesma responsabilidade.
A máquina conferia apenas presença e validade lexical do nome informado.

Base do plugin: v-sprint3-poc.6, commit
`533391bb65fdd9735fa9d229d363f04f08bdff35`. A base de trabalho
`8e4e869fbbe66190cc04e8ee0e054924a4ed2cba` já incluía os auxiliares da ação 3.8; seu código dos plugins era
idêntico ao da tag .6. Evidências anteriores e outras mudanças locais do
usuário foram preservadas e excluídas destes commits.

## Correção

Decisão **036**, com índice atualizado. P10 declara no playbook do caso:

```json
{
  "coerencia_responsavel_recorrencia": {
    "padrao": "registro/calibragem/CAL-*.yaml",
    "excluir_padrao": "registro/calibragem/*-C*.yaml",
    "campo": "responsavel",
    "campo_versao": "versao",
    "selecao": "maior_versao",
    "orientacao_troca": "Para trocar o responsavel, grave uma nova versao da rotina pelo engenheiro no proprio terminal, antes da recorrencia."
  }
}
```

O avaliador genérico lê os arquivos do caso, exclui ciclos e seleciona a
maior versão inteira positiva. Não usa ordem lexical de identificadores,
data do arquivo ou vocabulário de método no código. Empate da maior versão
com pessoas distintas é recusado como ambíguo. Fonte ilegível, externa ao
caso, sem versão válida ou sem pessoa nomeada também não libera a operação.

A comparação antecede a alteração do estado. Divergência mostra os dois
nomes, arquivo, versão e a orientação do playbook. Recusas comuns geram
`RecusaMaquina`; contrato inválido gera `TentativaNegada`. O estado não é
regravado na recusa. A recorrência aceita guarda `fonte_responsavel`
(arquivo, versão, campo, valor) no estado e em `RecorrenciaRegistrada`.

A autoridade humana da decisão 027 permanece: o engenheiro grava a nova
versão da rotina e executa a recorrência no próprio terminal. A correção
não altera o validador de gravação de rotinas nem injeta playbook novo em
casos antigos. Versões: núcleo **0.2.33**, campo **0.8.7**, playbook **0.4.9**.

## Antes e depois

| Operação | Antes (.6) | Depois |
|---|---|---|
| CAL com Celso; recorrência com Marina | Aceita | Recusada, com os dois nomes e instrução de troca |
| Recorrência sem rotina registrada | Aceita se a etapa constava encerrada | Recusada, indicando o padrão esperado |
| CAL e recorrência com a mesma pessoa | Aceita sem vincular a fonte | Aceita, com fonte e versão rastreáveis |
| CAL v1/Celso → nova CAL v2/Marina gravada pelo engenheiro → recorrência/Marina | Aceita sem conferir a troca | Aceita após conferir v2; Celso fica no histórico do ciclo anterior |
| Maior versão numérica em arquivo de nome anterior | Ignora a fonte | Seleciona a maior versão numérica |
| Ciclo com versão superior à rotina | Ignora a fonte | Exclui o ciclo pelo contrato do playbook |

## Testes novos: `testes/recorrencia_a23.py`

| Teste | Verificação | Resultado |
|---|---|---|
| 01 | Responsável divergente; mensagem com nomes e orientação; evento e estado preservado | PASS |
| 02 | Ausência de rotina; evento e estado preservado | PASS |
| 03 | Versão 10 precede versão 2 independentemente do nome do arquivo | PASS |
| 04 | Ciclo v100 não substitui rotina v1 | PASS |
| 05 | Fonte com versão inválida não permite usar uma fonte antiga como escape | PASS |
| 06 | Empate na maior versão com responsáveis distintos | PASS |
| 07 | Link simbólico para fonte externa ao caso | PASS |
| 08 | Contrato com seleção desconhecida recusado com evento | PASS |
| 09 | Mesmo responsável, fonte registrada no estado e no evento | PASS |
| 10 | Troca por versão 2 via calibragem.py; recorrência anterior preservada | PASS |
| 11 | Outra etapa, diretório e campos declarados; sem nomes de método no avaliador | PASS |
| 12 | Fonte ilegível não ignorada em favor de outra rotina | PASS |

Negativos foram escritos e executados antes da alteração do núcleo
(`primeira-execucao.txt`). A preparação do teste de link foi corrigida para
criar seu diretório. A contraprova com o módulo final em cópia separada da
.6 (`testes-antes-v6.txt`) teve 11 falhas e 1 erro: o erro é a ausência da
nova chave `fonte_responsavel` no caminho positivo antigo. Após a correção,
os mesmos 12 testes passam (`testes-depois.txt`). Também passam com os
interpretadores dos scripts em `-S`, sem PyYAML (`testes-sem-pyyaml.txt`),
sem nova dependência externa.

## Testes existentes ajustados

Somente preparação; nenhuma asserção ou teste removido:

| Arquivo / testes | Ajuste |
|---|---|
| `testes/apoio/preparar.py` | Produto sintético aceita responsável opcional na preparação de P10; chamadas anteriores mantêm seu responsável padrão |
| `testes/nucleo_2_6_1.py`: 2.6.1-T11, T12, T12b, T13, T14 | Os dois casos que percorrem até P10 preparam CAL-999 com Marina Prado, o nome já usado nas recorrências positivas T12/T14. As negativas de ausência/coletivo/cadência continuam intactas |

Os demais módulos já usavam rotina e recorrência com o mesmo responsável e
não precisaram de alteração. O módulo 2.6.1 mantém suas 39 verificações.

## Auditoria de responsabilidades (item 3; sem correções adicionais)

Inspecionados os scripts de campo, schemas, referências entre registros,
consumidores de entregáveis/inegociáveis e campos da máquina. Consultada a
fonte local canônica EMCIA-CAM-01, em revisão/aprovação pendente; a nova
coerência é autorizada pela solicitação A23. Nenhuma igualdade entre papéis
distintos foi inferida a partir de proposta documental.

| Par / origem | Conferência atual | Resultado da auditoria |
|---|---|---|
| CAL.responsavel × P10.estado_recorrente.responsavel | Comparação com fonte de maior versão declarada | **A23 corrigido** |
| CAL.responsavel × `estado.inegociaveis["5"].evidencia` | `inegociaveis.py:verificar_i5` copia o nome na evidência textual; o portão só exige satisfação/evidência/autor, sem rever a fonte | **Duplicação da mesma responsabilidade sem revalidação**: trocar a rotina depois pode deixar o nome antigo na evidência de I5. Não corrigido |
| CAL vigente / recorrência × responsável apresentado por E5 | `entregaveis.py:render_e5` lê a última rotina pela ordem lexical de `_listar`, não por versão; não compara com a recorrência | **Mesma responsabilidade, seleção diferente**: com CAL-001 v10/Marina e CAL-999 v2/Celso, a recorrência seleciona Marina, mas a renderização atual de E5 selecionaria Celso. Não corrigido |
| P6.responsavel_operacional × P9.responsavel_apuracao | Nomes válidos, sem igualdade entre os registros; a métrica referencia piloto/linha de base, não OP | Papéis declarados diferentes: operação e apuração. Não há contrato que estabeleça serem a mesma responsabilidade; potencial vínculo a decidir pelo método, sem correção |
| P9.responsavel_apuracao × CAL.responsavel | `metricas_ref` confere existência das métricas, não igualdade de responsáveis | Papéis diferentes: apuração e manutenção/recalibragem. Nenhuma igualdade imposta |
| OP.ator_humano × OP.responsavel_operacional × OP.validado_por | Validação individual de pessoa, sem comparação dos nomes | Executor, responsável operacional e validador são papéis diferentes; nenhuma igualdade inferida |
| Piloto: revisor de caso × revisado_por do conjunto × esperado_definido_por | Validações individuais, sem igualdade | Revisor do item, revisão do conjunto e definição do esperado são atos distintos; nenhuma igualdade inferida |
| AUT.decisor / ciclo.decisor × responsáveis operacionais/de apuração/calibragem | Pessoa nomeada e decisão humana; sem igualdade dos papéis | Decidir não implica ser dono da execução/manutenção; sem novo vínculo |
| Contexto: responsável da fonte de dado × responsável da métrica | `contexto.schema.json` declara dono da fonte; métrica usa fonte_dado textual | Papéis diferentes; não há referência estruturada que declare a mesma responsabilidade |
| Responsável do caso × autores/declarantes/registradores | Autoria de registro atribuída ao responsável do caso; scripts de campo validam os papéis declarados | Identidade/autoria não é automaticamente responsabilidade operacional ou pela calibragem |
| Habilitação: responsável EMCIA / signatários × liberação/assinatura | habilitacao.py compara responsável EMCIA e signatário da organização com o documento, e assinaturas com a liberação | Coerência já existente no expediente administrativo; nenhuma alteração |

Ainda há também cadência repetida em CAL e recorrência sem igualdade
entre valores; não é uma segunda pessoa responsável e permanece fora de A23.
Emissão histórica já feita é um retrato da versão de sua fonte; a observação
sobre E5 diz respeito à **nova renderização** escolhendo uma fonte distinta.

## Auxiliares

`preparar-caso.sh` e `percurso-completo.sh` usam **Marina Prado** na CAL-001;
a recorrência do percurso já usava esse nome. O percurso passa a resolver
a tag **v-sprint3-poc.7**, para executar a versão com o novo contrato.
Conferidos com `bash -n`. `preparar-caso.sh controle-a23 P10` foi executado
num diretório temporário: chegou a P10/N2, CAL-001 com Marina Prado e
rascunhos de decisão prontos. O caso foi removido após a conferência
(`preparar-caso-P10.txt`).

## Suíte e entrega

**781 verificações em 34 módulos; 0 módulos com falhas.** São 769
verificações existentes e 12 novas, sem contar a repetição das mesmas
verificações como testes extras. `negativos.sh`: 51; `contexto.py`: 11.
`saida-suite.txt` contém totais por módulo, códigos de saída e saída
integral. `reexecutar-suite.py` executa todos os módulos de raiz de testes/
e negativos.sh, conferindo retorno e mensagens FALHA/FAILED/FAIL:.

A suíte foi executada sobre a árvore com as alterações depois gravadas em
`fdb64365984be054dcf3506a7bb8291723088deb` (`fix(A23)`). Auxiliares em `e1f2e73ebc91a49410ba74824d79dde3924d5f34`
(`docs(demos)`). `diff.patch` compara a base de trabalho com esses dois
commits e inclui código, playbook, versões, comando, decisão, índice,
testes e auxiliares. Este pacote será registrado por `docs(evidence)`;
a tag anotada v-sprint3-poc.7 aponta para o pacote completo.
