# Caso de controle — P6/P7

**ID:** `PP-TEST-2.6.2-001`
**HEAD:** `3f7fb2a1926619a27ba009e0fc07637ecaf18b74` (HEAD_INICIAL_2.6.2)
**Data:** 19/09/2026

Caso construído do zero em diretório temporário isolado (cópia de
`eiac-campo/template-caso`), percorrido manualmente F0→P7 via
`avancar.py`, `operacional.py` e `governanca.py`. Não reutiliza estado
residual de nenhum teste anterior. Fixtures controladas; não representa
execução real de cliente.

## 1. Entrada P5/E3

Caso fictício: convênio de saúde, processo de emissão e envio de guia de
autorização (mesma organização de controle usada nos casos de 2.5.6/2.6.1).
Percurso F0→P5 encerrado com nível N1, incluindo sessão de campo em P3b e
sessão registrada em P5 (necessária para carregar `hb-classificar` sob a
correção de G1 deste pacote). P5 encerrada normalmente por
`avancar.py --encerrar P5`.

## 2. Contexto utilizado

Referência a `RN-100` (regra central dos casos de controle anteriores,
2.5.6/2.6.1) como fonte da exceção de P6/P7 — citada em `excecao` (P6) e
em `gatilhos_escalonamento` (P7), sem reabrir ou modificar o contrato CTX.

## 3. P6 — desenho operacional

`OP-001` nasce `estado: proposta`, versão 1, gravado por `AG-02` (agente):
ponto de inserção nominado (recebimento da autorização no sistema de
gestão de guias), entrada, saída, ator humano (Claudia Ferreira), sistema,
exceção, fallback e responsável operacional. Validado por humano nomeado
(Rafael Nogueira) na versão 2, `estado: validado`. Etapa P6 encerrada por
`avancar.py --encerrar P6`.

## 4. Fronteiras identificadas

`excecao`: guia sem correspondência na camada de contexto (RN-100) ou
valor acima de R$ 5.000. `fallback`: fila manual de Claudia Ferreira, com
motivo registrado. Ambas preservadas no registro final (`OP-001.yaml`,
versão 2).

## 5. P7 — minuta de autonomia

`AUT-001` nasce `estado: rascunho`, versão 1, gravado por `AG-03`
(agente), referenciando `operacional_ref: OP-001` (já validado —
tentativa anterior a esse ponto teria sido recusada, ver
`2.6.2-T08`). Avança para `estado: proposto`, versão 2, ainda por `AG-03`.
As três listas (`faz_sozinha`, `exige_aprovacao`, `nunca_faz`) e os
`gatilhos_escalonamento` preenchidos pelo agente como preparação.

## 6. Tentativa de decisão por agente

`AG-03` tenta gravar `estado: decidido`, versão 3, com `decisor: AG-03`.

**Resultado: RECUSADA.**

```
decisor nao pode ser agente: 'AG-03'
agente nao pode decidir autonomia: o estado 'decidido' exige ator humano
nomeado, nunca agente (CAT-01 3.5.1).
```

Evento `TermoAutonomiaRecusado` registrado, com os dois erros, o ator
(`AG-03`) e o estado tentado (`decidido`).

## 7. Decisão humana

Marina Prado (pessoa nomeada, papel de decisora de autonomia) grava
`estado: decidido`, versão 3, com `decisor: Marina Prado`,
`data_decisao: 2026-09-19` e `justificativa_decisao` preenchida
referenciando a revisão jurídica e o alinhamento com Claudia Ferreira.
Evento `AutonomiaDecidida` registrado. Sessão de campo registrada para
P7 (`Marina Prado, Celso do Vale`) e etapa P7 encerrada por
`avancar.py --encerrar P7` (P7 é `delegavel: false`, exige sessão).

## 8. Registro final da autonomia

`registro/governanca/autonomia/AUT-001.yaml`, versão 3, `estado: decidido`
— ver `caso-controle-AUT-001.yaml` nesta pasta. Histórico da preparação
(versões 1 e 2) preservado no percurso de eventos (`eventos.jsonl`), não
sobrescrito.

## 9. Evidência disponível para inegociável 2

`avancar.py --satisfazer-inegociavel 2 --autor "Marina Prado" --evidencia
"registro/governanca/autonomia/AUT-001.yaml (estado: decidido, versao: 3,
decisor: Marina Prado, data_decisao: 2026-09-19)"` — aceito, evento
`InegociavelSatisfeito` registrado. O núcleo não avaliou a semântica do
conteúdo do termo (isso é 2.6.5); apenas confirmou que a evidência é uma
string não vazia associada a autor humano e ao item real do playbook.

**Nota honesta sobre E4:** com P6/P7 encerradas e o inegociável 2
satisfeito por caminho autorizado, `avancar.py --emitir E4` retornou
`exit 0` e produziu evento `EntregavelEmitido` — o portão estrutural
(etapas encerradas + inegociável com registro rastreável) está satisfeito
pelo mecanismo genérico de 2.6.1. Isso **não** constitui a validação
semântica do inegociável 2 nem a materialização do documento E4, ambas
atribuídas ao pacote 2.6.5. Este resultado é reportado tal como ocorreu,
sem suprimir nem reinterpretar.

## 10. Eventos

Sequência completa em `eventos.jsonl` desta pasta: `NivelApurado`,
sete `EtapaEncerrada` (F0,P1,P2,P3a,P3b,P3d,P4), duas
`SessaoDeCampoRegistrada` (P3b, P5), `EtapaEncerrada` P5,
`EspecificacaoOperacionalRegistrada` (proposta v1),
`EspecificacaoOperacionalValidada` (validado v2), `EtapaEncerrada` P6,
dois `TermoAutonomiaRegistrado` (rascunho v1, proposto v2),
`TermoAutonomiaRecusado` (tentativa de agente), `AutonomiaDecidida`
(decisão humana v3), `SessaoDeCampoRegistrada` P7, `EtapaEncerrada` P7,
`InegociavelSatisfeito` (n=2), `EntregavelEmitido` (E4).

## 11. Resultado

P6 e P7 executáveis, com fronteira agente×humano preservada em ambos:
agente prepara (proposta/rascunho/proposto), humano decide
(validado/decidido). Nenhuma decisão de autonomia foi tomada por agente
— cada tentativa foi recusada com evento rastreável. Evidência completa
para o inegociável 2 produzida e registrada pelo caminho autorizado.
