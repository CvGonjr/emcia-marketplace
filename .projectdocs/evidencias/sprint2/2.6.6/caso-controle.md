# Caso de controle integral F0–P10

ID: caso-controle-2.6.6 (repositório temporário, criado a partir de
`eiac-campo/template-caso/` via `testes/campo_2_6_6.py::preparar_caso`,
sem reaproveitar estado residual de 2.5.6, 2.6.2, 2.6.3 ou 2.6.5)

HEAD: `bcc85a62fc2b8c72b4704ecd43e5e901cce39d63` (HEAD_INICIAL_2.6.6)

Data: 2026-09-19

Nível: N2 (justificativa: N1 dispensa verificação obrigatória a partir de
P5, o que esconderia parte do que este pacote precisa demonstrar — I1
exige `apuracao: medido` fora de N1, ver `checar_apuracao_por_nivel` em
`baseline.py`; N3 não é exigido pela documentação/testes consultados
para cobrir o percurso. N2 é o nível que exercita a verificação completa
sem introduzir requisitos adicionais não documentados.)

Cliente simulado/controlado: fluxo de reembolsos de uma operadora
fictícia. Responsáveis simulados: Celso do Vale (engenheiro/condução),
Fernanda Lima (analista de reembolsos), Rafael Nogueira (validação
operacional), Marina Prado (decisões humanas — autonomia, calibragem,
satisfação de inegociáveis). Nenhum dado pessoal real foi usado.

## F0

Nível apurado N2 (eixos "DAD 4, GOV 5, CRI 7"), etapa encerrada por
Celso do Vale. E1 (Ficha de Enquadramento) autorizado e materializado em
`caso/entregaveis/E1.md`, versão 1.

## P1

Levantamento inicial do processo (fonte de dados: sistema de gestão de
reembolsos, ponto de inserção declarado). Etapa encerrada.

## P2

Regra RN-101 ("quando o pedido de reembolso chega completo, a análise
inicial é feita em até 1 dia útil") curada via `curar.py --tipo regra`
(caminho autorizado — escrita direta em `contexto/regras/` foi testada e
recusada antes, G2b). Etapa encerrada.

## P3a

Linha de base BL-101 registrada antes do piloto: indicador "tempo de
análise inicial do pedido de reembolso", valor atual "3 dias úteis",
apuração `medido`, nível N2, procedência V, declarada por Fernanda Lima,
registrada por Celso do Vale. I1 verificado por `inegociaveis.py` e
satisfeito por Marina Prado.

## P3b

Etapa não delegável. Skill `hb-levantar-regras` recusada sem sessão
(guarda G1); AG-01 tentando encerrar recusado (autor precisa ser pessoa
nomeada). Sessão humana registrada por Celso do Vale, skill liberada,
etapa encerrada pelo humano.

## P3d

Confronto de RN-101 encerrado sem divergência aberta.

## E2

Emitido após I1 satisfeito e P1–P3d encerradas. Materializado em
`caso/entregaveis/E2.md`, versão 1, citando literalmente `valor_atual`/
`apuracao` de BL-101 (não inventados).

## P4

RN-101 consultada via `consultar.py --id RN-101` (consumo estruturado,
não reinferência de prosa). Etapa encerrada.

## P5

Classificação tecnológica registrada como `agente` (ver ressalva sobre a
lacuna de script executável em `matriz-f0-p10.md`). Decisão registrada
como decorrência das evidências do caso, não forçada para abrir o
portão — o cenário do caso (classificação automática de pedidos de
reembolso com regras de escalonamento) é legitimamente agêntico.

## E3-D

Emitido após P4/P5 válidas. AUTORIZADO.

## E3-E

Aplicável (condição declarativa `classificacao_tecnologica contem
"agente"` satisfeita). AUTORIZADO.

## E3

Materializado em `caso/entregaveis/E3.md`, versão 1 — um único arquivo
com Parte A (decisão) e Parte B (blueprint do agente, presente porque
E3-E autorizou).

## P6

Etapa encerrada. Especificação operacional OP-101: AG-02 propõe (papel
legítimo de agente); AG-02 tentando validar a própria proposta é
recusado; Rafael Nogueira (humano) valida.

## Validação humana de P6

Confirmada — `checar_validacao`/`E.autor_e_agente` em `operacional.py`
recusam a validação por AG-02 e aceitam Rafael Nogueira. Ver
`teste-2.6.6-C09.txt`.

## P7

Sessão humana registrada, etapa encerrada. AUT-101: AG-03 prepara
minuta e propõe (papel legítimo); AG-03 tentando decidir é recusado.

## Decisão humana de autonomia

Marina Prado decide AUT-101 (`estado: decidido`, justificativa
registrada). Ver `teste-2.6.6-C11.txt`/`C12.txt`.

## I2

Verificado por `inegociaveis.py` a partir de AUT-101 decidido e
satisfeito por Marina Prado.

## E4

Emitido após P6+P7+I2. Materializado em `caso/entregaveis/E4.md`,
versão 1.

## P8

CT-101 revisado com 2 casos, ambos com `saida_esperada` declarada
previamente: CT-101-01 aderente (`saida_obtida` igual à esperada) e
CT-101-02 **divergente** (`saida_obtida` diferente da esperada,
calculado deterministicamente por `piloto.py`, nunca declarado
manualmente) — falha funcional honesta que não impede o Estúdio de
prosseguir, pois I3 exige apenas que os casos possuam saída esperada
definida antes da execução, não 100% de acerto.

## I3

Verificado por `inegociaveis.py` a partir de CT-101 revisado e satisfeito
por Marina Prado.

## P9

MET-102 (métrica de uso, "128 pedidos/mês") e MET-101 (métrica de
resultado, `baseline_ref: BL-101`, "1 dia útil" contra a linha de base de
"3 dias úteis") registradas e apuradas. Nenhuma causalidade declarada
além do que os dados sustentam.

## I4

Verificado por `inegociaveis.py` a partir de MET-101 (tipo `resultado`,
apurada) e satisfeito por Marina Prado.

## P10 — configuração

CAL-101 registrada: responsável Marina Prado, cadência mensal,
`metricas_ref: [MET-101, MET-102]`. Sessão registrada, etapa encerrada,
recorrência registrada via `avancar.py --registrar-recorrencia`
(mecanismo genérico do núcleo).

## P10 — ciclo 1

AG-04 registra ciclo sem drift (`drift_detectado: false`) — caminho
positivo legítimo, sem exigir recomendação/decisão.

## P10 — ciclo 2

AG-04 detecta e quantifica drift ("tempo de análise voltou a subir para
2.5 dias úteis", variação de +150% sobre o resultado apurado em P9) e
recomenda recalibrar.

## Drift

Confirmado no ciclo 2 (`drift_detectado: true`, `drift_descricao`/
`drift_quantificacao` preenchidas pelo agente).

## Decisão humana

AG-04 tentando gravar `decisao: recalibrar` é recusado ("agente não pode
decidir recalibragem"). Marina Prado decide recalibrar
(`decisor`, `data_decisao`, `justificativa_decisao` preenchidos).

## I5

Verificado por `inegociaveis.py` a partir de CAL-101 (`responsavel:
Marina Prado`, pessoa nomeada) e satisfeito por Marina Prado.

## E5

Emitido após P8+P9+P10 e I3+I4+I5. Materializado em
`caso/entregaveis/E5.md`, versão 1, citando literalmente o resultado
contra a linha de base ("Tempo de análise inicial do pedido de
reembolso | 3 dias úteis | 1 dia útil").

## HB/AG utilizadas

Ver `matriz-hb-ag-final.md`. Neste caso: HB-01/02/03 (F0), HB-07 (P2),
HB-08/09 (P1), HB-10 (P4), HB-11/12 (P5), HB-14 (P7), HB-15/16 (P8),
HB-17 (P9), HB-18 (P10) — 14/18. Agentes: AG-02 (P6), AG-03 (P7), AG-04
(P10) participaram ativamente; AG-01 verificado apenas pela fronteira
formal (C21).

## Eventos

56 eventos persistidos em `eventos.jsonl`, cobrindo início do caso
(`NivelApurado`), 12 mudanças de etapa (`EtapaEncerrada`), 3 sessões
humanas (`SessaoDeCampoRegistrada`), 1 curadoria (`ObjetoContextoCurado`),
5 satisfações de inegociável (`InegociavelSatisfeito`), decisões de
autonomia e recalibragem, casos de teste, calibragem, 11 emissões de
portão/entregável (`EntregavelEmitido`) e 3 recusas com trilha
(`TentativaNegada`, `RecusaMaquina`, mais as recusas específicas de
`EspecificacaoOperacionalRecusada`, `TermoAutonomiaRecusado`,
`CicloCalibragemRecusado`).

## Entregáveis

Cinco arquivos materiais reais, todos não vazios e recuperáveis:
`caso/entregaveis/E1.md`, `E2.md`, `E3.md`, `E4.md`, `E5.md` — cópias em
`caso-controle-E{1..5}.md` neste diretório.

## Resultado final

13/13 etapas conformes, 5/5 inegociáveis satisfeitos, 6/6 autorizações
conformes (caso agêntico), 5/5 entregáveis materializados, 0 bypass
manual detectado, 1 achado de lacuna documentado (P5 sem script
executável — mesmo achado do 2.6.5), 1 defeito novo encontrado e
corrigido (`calibragem.py::checar_autoria` — ver `resultado.md` §25/§26).
