# Sprint 3 — ação 3.6: correção A14, A15 e A16

Base: `v-sprint3-poc.4`, commit `c3d02dc7825e342992640a9e69459f2e74a2806b`.
Versão de entrega: `v-sprint3-poc.5`. Núcleo 0.2.28, campo 0.8.5,
playbook 0.4.8. Decisões 028, 029 e 030: 027 já registra A12 e é preservada.
Não há aplicação em campo nem dado de cliente: apenas casos sintéticos.

## Lacunas e correções — antes e depois

| Lacuna | Antes (.4) | Depois (.5) |
|---|---|---|
| A14 | Etapa concluída sem seu produto; entregável recusava depois | Encerramento exige os produtos declarados, gera TentativaNegada e preserva estado quando faltam |
| A15 | Piloto revisado passava pela sessão com nome humano; definição da rotina ausente da lista | Ambos estão declarados como decisão humana e negados pela guarda; engenheiro registra no próprio terminal |
| A16 | Valor inteiro equipe recusado, frase equipe de TI aceita; primeiro nome suficiente | Palavras normalizadas são conferidas contra lista do playbook; mínimo de duas partes de nome; mesma função em todos os pontos nominais |

O núcleo interpreta dados: nenhum nome de etapa, estado/categoria de método,
padrão de artefato ou termo coletivo novo foi colocado nos avaliadores.
Os produtos são conferidos depois da sessão, dependências e selo; os portões
de emissão continuam presentes. Etapas sem produto declarado têm lista vazia.

### Produtos por etapa

| Etapa | Produto declarado | Sem produto | Com produto |
|---|---|---|---|
| P3a | registro/baseline/*.yaml com indicador, valor_atual e data | NEGADO | PASS |
| P5 | Campo classificacao_tecnologica registrado na etapa, taxonomia válida | NEGADO | PASS |
| P6 | registro/operacional/*.yaml, estado=validado | NEGADO | PASS |
| P7 | registro/governanca/autonomia/*.yaml, estado=decidido | NEGADO | PASS |
| P8 | registro/piloto/*.yaml, estado=revisado | NEGADO | PASS |
| P9 | registro/metricas/*.yaml, tipo=resultado e estado=apurada no mesmo arquivo | NEGADO | PASS |
| P10 | registro/calibragem/CAL-*.yaml com responsável nominal e cadência no mesmo arquivo | NEGADO | PASS |

Arquivos ilegíveis/vazios e symlink externo não satisfazem. Campos separados
em arquivos diferentes não completam um produto. Os scripts de campo
continuam validando estrutura, autoria, referências e transições; o novo
motor de encerramento confere os predicados declarados, sem substituir esses
validadores. O mínimo autorizado pelo usuário é aplicado; não se incorpora
por inferência todo critério adicional dos documentos em revisão do método.

## Auditoria A15 — todos os seis scripts solicitados

| Script | Ato/transição humana | Cobertura na lista do playbook | Preparação permitida |
|---|---|---|---|
| baseline.py | Não há transição de decisão: artefato de medição/estimativa | Sem operação de decisão adicional; autoria nominal do conteúdo não muda origem da chamada | Registro de baseline, com autoria nominal no artefato |
| metrica.py | Planejada/apurada registra medição, sem decisão de julgamento | Sem operação de decisão adicional; responsabilidade nominal é checada | Plano e cálculo/apuração |
| piloto.py | Revisão do conjunto | revisar-piloto: estado=revisado (NOVA) | estado=rascunho |
| operacional.py | Validação operacional | validar-operacional: estado=validado (027, mantida) | estado=proposta |
| governanca.py | Decisão de autonomia | decidir-autonomia: estado=decidido (027, mantida) | rascunho/proposto |
| calibragem.py | Definição de rotina; decisão do ciclo | definir-rotina: responsável preenchido (NOVA); decidir-recalibragem: decisão preenchida (027, mantida) | Ciclo com drift/recomendação, sem decisão |

Chamadas à guarda com tool_name Bash são sempre da sessão do agente. Nome
humano informado não libera decisões. A guarda registra TentativaNegada,
operação e comando exato. Definição de rotina é governança de responsável e
cadência, conforme o contrato já descrito pelo próprio calibragem.py.
A inspeção determinística continua com os limites documentados na 027:
não autentica identidade de sistema operacional nem shell arbitrário.

## A16 — pontos com a mesma checagem

Abertura por novo-caso.sh; autores do avanço, sessão, campos, recorrência e
satisfação de inegociável; responsável da recorrência; autores das asserções;
autoria de curadoria e histórico; responsável fixo de validar/curar/selar;
autor do esforço; declarado_por/registrado_por e campos de pessoa em
baseline, métrica, piloto, operacional, governança e calibragem, inclusive
revisor/esperado_definido_por/revisado_por, validado_por/ator_humano,
responsavel_operacional, decisor e responsavel_apuracao. Curadoria lê
campos_pessoa declarados no playbook. O produto de P10 declara pessoas=[responsavel].

Habilitação administrativa anterior ao caso também usa a função comum:
regra copiada do template à abertura do expediente, depois lida da cópia.
Expedientes antigos sem regra usam explicitamente o template da habilitação;
nenhum caso lê o playbook do plugin como alternativa. A lista lexical não é
prova civil de identidade: a barreira de origem continua na guarda.
Equipe de TI, Time Comercial, Área de Vendas e Marina são negados;
Marina Prado é aceito. Caixa/acentos são normalizados; há plurais e
termos equivalentes no playbook. Ciclo sem decisão mantém autoria de
preparação do agente; seus campos de decisão exigem pessoa.

## Testes novos e antes/depois

Os negativos principais foram escritos e executados contra .4 antes de
alterar o código. As saídas iniciais estão preservadas. Houve um erro do
harness inicial em pessoa_a16 (helper chamado testar, confundido com teste);
ele foi renomeado para conferir. Para comparação limpa, os três módulos
finais foram também executados em uma cópia isolada obtida com git archive
da tag .4, sem alterar o checkout do usuário.

| Módulo novo | Verificações | Na .4, testes finais | Na correção |
|---|---:|---|---|
| produtos_a14.py | 21 | 14 falhas: negativas eram aceitas | 21 PASS |
| revisao_a15.py | 6 | 2 falhas: revisão e rotina permitidas | 6 PASS |
| pessoa_a16.py | 17 | 16 falhas: coletivos/incompletos aceitos | 17 PASS |

A14 cobre sete pares sem/com produto, estado errado, campos distribuídos,
symlink externo, regra alternativa do caso, YAML ilegível, métrica de uso e
contrato desconhecido. A15 cobre as duas decisões e quatro preparações
permitidas. A16 cobre os nomes pedidos, comitê, acentos, regra alternativa,
registros pelos seis scripts com controle positivo após a recusa, abertura,
asserção e responsável coletivo no produto de P10.

## Cada ajuste nos testes anteriores

Nenhum teste foi apagado. Permanecem as mesmas 629 verificações anteriores;
somam-se 44. O único teste de lacuna convertido é T09b, conforme solicitado.
O auxílio testes/apoio/preparar.py fornece fixtures sintéticas de produtos
com IDs 999 para os percursos anteriores, sem sobrescrever os IDs sob teste.
Só a classificação altera estado, pelo comando oficial; o auxílio não escreve
estado.json. Ele não é chamado no wrapper de encerramento sob teste.

| Arquivo / testes | Ajuste |
|---|---|
| campo_2_6_2.py — preparar percurso de T25 e G1a/G1b/G1c | Produtos durante percorrer_ate (baseline, classificação, OP nos passos percorridos) |
| campo_2_6_3.py — T01/T02 e preparação de T03–T36 | Produtos durante percorrer_ate; preparar_ate_p7 herda o mesmo percurso; demais cenários acumulam esse caso |
| campo_2_6_4.py — T39/T40 | Linha de base durante percurso até P4; cenário de sessão permanece igual |
| campo_2_6_5.py — percursos de T17–T42 e cenários derivados T43–T52 | Produtos durante percorrer_ate: P3a/P5/P6/P7/P8/P9 conforme o destino; portões/condições/negativas permanecem |
| campo_2_6_5.py — T09b | Agora exige recusa na gravação e inexistência do arquivo para equipe de TI |
| campo_2_6_6.py — C08/C10 e percurso acumulado C13–C40 | OP validado e AUT decidido sintéticos na preparação do encerramento; os testes originais C09/C11/C12 de autoria/decisão continuam executados sobre IDs próprios |
| campos_a10.py — test_17_e3_partes_a_b_sem_escrita_direta_no_estado | Linha de base no percurso até P5; classificação continua registrada pelo comando; nenhuma escrita direta em estado.json |
| nucleo_2_6_1.py — T03/T04/T07/T17/T20c | Produtos nos percursos locais de preparação, antes dos encerramentos |
| nucleo_2_6_1.py — T11/T12/T12b/T13/T14/T27/T27b | Produtos nos percursos até P10/P4; recorrência e condições mantêm suas asserções |
| sessao_a8.py — test_13, test_14, test_17 | Produto antes do encerramento positivo, por helper de controle; cenários negativos de sessão permanecem |
| verificacao_por_estados.py — T01/T02/T03/T04 | Linha de base antes de encerrar P3a na preparação; selo continua testado depois da sessão |
| decisao_a12.py — test_29_template_declara_lista | Mantém a lista anterior como prefixo obrigatório e exige as duas adições A15 |
| negativos.sh — fixtures de autoria nos testes 3/4, 2.5.0-T01–T07, 5/7/12/14/16/17/19/24/25 e eventos fabricados | Celso → Celso do Vale; Helena → Helena Duarte. Identificadores de agentes nos negativos não mudaram |
| autoria_responsavel.py — validar e curar | Helena → Helena Duarte nas asserções/campos do candidato; autoria fixada e verificações de argumento ignorado mantidas |

Os lugares exatos de alteração estão em diff.patch; o auxílio foi inserido
somente nas precondições e percursos, com asserções preservadas.

## Suíte completa e rastreabilidade

**673 verificações em 28 módulos, zero falhas**, incluindo todos os módulos
Python da raiz de testes/ e negativos.sh. Conferidos códigos de saída e
mensagens FALHA/FAILED/FAIL: (alguns scripts antigos retornam zero com falha).
Subtestes/asserções não são somados como testes; regressões reexecutadas por
outros módulos não são contadas novamente. suite.txt contém os totais por
módulo e a saída integral. fontes-suite.json fixa SHA-256 dos arquivos
executados; os conteúdos foram conferidos novamente após os commits.
A trilha da execução da suíte usa o HEAD de origem antes dos commits;
os fingerprints demonstram o conteúdo efetivamente verificado.

Antes de editar, negativos.sh (51) e contexto.py (11) passaram.
Sintaxe Python e git diff --check conferidos. A execução da suíte final foi
concluída sem alterações subsequentes nos arquivos executados.

## Demonstração

```bash
cd ~/Projetos/emcia-marketplace
bash .projectdocs/demos/preparar-caso.sh controle-p10 P10
```

Caso em /tmp/emcia-demos/controle-p10, etapa corrente P10, N2,
DAD 5, GOV 3, CRI 6. O auxiliar imprime caminho e rascunhos. Sessões,
selo, baseline, classificação, OP validado, AUT decidido, conjunto revisado
e métrica apurada são registrados pelo percurso. O arquivo de estado
é apenas lido, nunca editado diretamente pelo auxiliar.

Ao parar em P6/P7/P8: versão do rascunho já incrementada, decisor,
data_decisao e justificativa_decisao preenchidos, além dos campos específicos
de validação/revisão. Só estado precisa mudar. Em P10, CAL-001 registrada
e CAL-001-C01 com drift/recomendação sem decisão; rascunho do ciclo em
versão 2, com campos humanos preenchidos, falta apenas decisao.
As decisões de etapas anteriores são executadas no percurso sintético
pelo engenheiro no terminal. demos.txt comprova paradas em P6/P7/P8 com
registro bem-sucedido após alterar só estado e chegada até P10.

## Commits e publicação

- 18a4122 — fix(A14)
- 1f8339f — fix(A15)
- 8b53238 — fix(A16)
- 5f8b51d — docs
- Este pacote — docs(evidence), seguido da tag anotada v-sprint3-poc.5.

Diff da base .4 até o commit de documentação, incluindo código/testes/docs
novos. Mudanças locais anteriores em evidências 3.1, 3.2, 3.4, 3.5 e 3.9
foram preservadas fora desses commits. Tags anteriores permanecem intactas.
Publicação solicitada: git push origin master refs/tags/v-sprint3-poc.5.
