# Matriz F0–P10 — caso de controle do pacote 2.6.6

Percurso executado no caso de controle temporário (ver `caso-controle.md` e
`caso-controle-driver.py`). Todas as 13 etapas foram atingidas em ordem,
sem bypass (nenhuma escrita direta em `registro/`), via os scripts reais
(`avancar.py`, `curar.py`, `consultar.py`, `operacional.py`, `governanca.py`,
`piloto.py`, `metrica.py`, `baseline.py`, `calibragem.py`,
`inegociaveis.py`, `entregaveis.py`).

| Etapa | Entrada | HB | AG/ator | EX | Saída | Evidência | Estado |
|------|---------|----|----------|----|-------|-----------|--------|
| F0 | Triagem inicial, nível N2 | HB-01/02/03 | Celso do Vale (humano) | EX1→EX2 | Nível apurado, E1 emitido | `avancar.py --apurar-nivel N2`, evento `NivelApurado`; `caso-controle-E1.md` | Conforme |
| P1 | Setor e processo-alvo | HB-08/09 | Celso do Vale (humano) | EX2 | Etapa encerrada | evento `EtapaEncerrada` (P1) | Conforme |
| P2 | Documentos e entrevistas | HB-07 | Celso do Vale (humano, via `curar.py`) | EX2 | RN-101 curada em `contexto/regras/` | `caso-controle-RN-101.yaml`, evento `ObjetoContextoCurado` | Conforme |
| P3a | Estado atual observado | — | Marina Prado (declarante) / Celso do Vale (registrado_por) | EX3 | Linha de base BL-101 (medido, N2) | `caso-controle-BL-101.yaml`, evento `LinhaDeBaseRegistrada` | Conforme |
| P3b | Relato do patrocinador | HB-04/05 (hb-levantar-regras) | Celso do Vale (humano, sessão obrigatória) | EX4 | Sessão registrada, etapa encerrada | evento `SessaoDeCampoRegistrada`, `EtapaEncerrada` (P3b) | Conforme |
| P3d | RN-101 confrontada | HB (hb-confrontar) | Celso do Vale (humano) | EX3 | Etapa encerrada (sem divergência aberta) | evento `EtapaEncerrada` (P3d) | Conforme |
| P4 | RN-101 estruturada | HB-10 | Celso do Vale, consulta via `consultar.py` | EX2 | RN-101 consumida sem reinferência | saída de `consultar.py --id RN-101` | Conforme |
| P5 | RN-101 + contexto | HB-11/12 | Celso do Vale (humano) | EX2/EX3 | `classificacao_tecnologica: agente` | `estado-final-caso.json.cumprimentos.P5` (ver achado 2.6.6-D01) | Conforme (ver ressalva abaixo) |
| P6 | E3 (Parte A/B) | HB-14 (proposta), validação humana | AG-02 (proposta) / Rafael Nogueira (validação) | EX2 (agente) / EX3 (validação) | OP-101 validado | `caso-controle-OP-101.yaml`, evento `EspecificacaoOperacionalValidada` | Conforme |
| P7 | OP-101 validado | HB-14 | AG-03 (minuta) / Marina Prado (decisão) | EX2 (agente) / EX4 (decisão) | AUT-101 decidido | `caso-controle-AUT-101.yaml`, evento `AutonomiaDecidida` | Conforme |
| P8 | Dossiê + contexto | HB-15/16 | Celso do Vale (elaboração) / Marina Prado (revisão) | EX2/EX3 | CT-101 revisado, 1 caso aderente + 1 divergente (honesto) | `caso-controle-CT-101.yaml`, evento `ConjuntoPilotoRevisado` | Conforme |
| P9 | Medições do piloto e linha de base | HB-17 | Marina Prado (apuração) | EX2 | MET-101 (resultado, `baseline_ref: BL-101`) + MET-102 (uso) | `caso-controle-MET-101.yaml`, `caso-controle-MET-102.yaml`, evento `MetricaApurada` | Conforme |
| P10 | Saídas em operação | HB-18 | AG-04 (detecção/ciclos) / Marina Prado (decisão) | EX2 (monitoramento) / EX4 (decisão) | CAL-101 + 2 ciclos (ciclo 2 com drift decidido) | `caso-controle-CAL-101*.yaml`, evento `RecorrenciaRegistrada`, `DecisaoRecalibragemRegistrada` | Conforme |

**13/13 etapas conformes.**

## Ressalva registrada em P5

Não existe, em `eiac-campo/scripts/`, um caminho executável equivalente a
`baseline.py`/`operacional.py`/`governanca.py` para o conteúdo semântico
de P5 (`classificacao_tecnologica`). `hb-classificar/SKILL.md` produz
apenas `caso/P5-classificacao.md` em texto livre; não há
`eiac-campo/scripts/classificar.py`. O caso de controle registra o campo
estruturado necessário para exercitar `E3-E` diretamente em
`st["cumprimentos"]["P5"]`, com evidência antes/depois preservada em
`caso-controle-log-comandos.txt` e no log completo
(`teste-2.6.6-saida-completa.txt`). Esta é a mesma lacuna já observada e
documentada durante o pacote 2.6.5 (não corrigida ali por estar fora do
escopo daquele pacote). O pacote 2.6.6, por princípio (não introduzir
capacidade nova), também não implementa o script ausente — apenas
registra o achado como defeito (ver `resultado.md` §25, `D-2.6.6-01`).
