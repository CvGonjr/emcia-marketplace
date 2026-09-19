# Caso de controle — pacote 2.6.5

Percurso F0→E5 completo, cenário agêntico (P5 classifica como agente,
exercitando `E3-E` como AUTORIZADO em vez de NÃO APLICÁVEL), P6/P7
válidos, P8/P9/P10 válidos, os cinco inegociáveis verificados a partir
de artefato real e os seis portões avaliados. Reproduzido por
`testes/campo_2_6_5.py` (funções auxiliares) via o driver descartável
usado para gerar esta evidência — não é ainda o caso de controle
integral F0–P10 do pacote 2.6.6, que exercitará também o cenário não
agêntico e a integração completa das quatro camadas em um único caso
contínuo sem intervenção de teste.

## Percurso

```
F0 (N2, DAD4·GOV5·CRI7)
  ↓ EntregavelEmitido E1 (caso/entregaveis/E1.md, v1)

P1, P2
  ↓
P3a → registro/baseline/BL-001.yaml (medido, N2)
  ↓ InegociavelSatisfeito I1 (ref: BL-001.yaml)
P3b (sessão registrada) → P3d
  ↓ EntregavelEmitido E2 (caso/entregaveis/E2.md, v1)

P4
  ↓
P5 → classificacao_tecnologica: "agente"
  ↓ EntregavelEmitido E3-D (sempre) + EntregavelEmitido E3-E (aplicável, caso agêntico)
  ↓ E3 material consolida as duas autorizações (caso/entregaveis/E3.md, v1)

P6 → registro/operacional/OP-001.yaml (proposta → validado)
P7 → registro/governanca/autonomia/AUT-001.yaml (rascunho → proposto → decidido, Marina Prado)
  ↓ InegociavelSatisfeito I2 (ref: AUT-001.yaml)
  ↓ EntregavelEmitido E4 (caso/entregaveis/E4.md, v1)

P8 → registro/piloto/CT-001.yaml (rascunho → revisado, 2 casos, 1 célula crítica)
  ↓ InegociavelSatisfeito I3 (ref: CT-001.yaml)
P9 → registro/metricas/MET-001.yaml (planejada → apurada, tipo=resultado, 45min→32min)
  ↓ InegociavelSatisfeito I4 (ref: MET-001.yaml)
P10 → registro/calibragem/CAL-001.yaml (responsável Marina Prado, cadência mensal, ciclo 1)
  ↓ InegociavelSatisfeito I5 (ref: CAL-001.yaml)
  ↓ EntregavelEmitido E5 (caso/entregaveis/E5.md, v1; reemitido para v2 em T42)

Tentativa negativa: AG-03 tenta regravar AUT-001 já decidido → TermoAutonomiaRecusado
(fronteira agente/humano preservada mesmo após a decisão)
```

## IDs e referências

| Artefato | ID | Estado final | Caminho na evidência |
|---|---|---|---|
| Linha de base | BL-001 | registrado | `caso-controle-BL-001.yaml` |
| Termo de autonomia | AUT-001 | decidido, v3 | `caso-controle-AUT-001.yaml` |
| Especificação operacional | OP-001 | validado, v2 | `caso-controle-OP-001.yaml` |
| Conjunto de piloto | CT-001 | revisado, v2 | `caso-controle-CT-001.yaml` |
| Métrica | MET-001 | apurada, v2, tipo=resultado | `caso-controle-MET-001.yaml` |
| Rotina de calibragem | CAL-001 | — (sem campo estado; ciclo 1 registrado) | `caso-controle-CAL-001.yaml` |
| E1 | — | v1 | `caso-controle-E1.md` |
| E2 | — | v1 | `caso-controle-E2.md` |
| E3 | — | v1 (E3-D + E3-E consolidados) | `caso-controle-E3.md` |
| E4 | — | v1 | `caso-controle-E4.md` |
| E5 | — | v1→v2 (reemissão testada) | `caso-controle-E5.md` |

## Decisões dos seis portões neste caso

| Portão | Decisão | Motivo |
|---|---|---|
| E1 | AUTORIZADO | F0 encerrada com eixos/nível |
| E2 | AUTORIZADO | P1/P2/P3a/P3b/P3d encerradas + I1 satisfeito |
| E3-D | AUTORIZADO | P4/P5 encerradas |
| E3-E | AUTORIZADO | P5 classificou como agente (condição declarativa satisfeita) |
| E4 | AUTORIZADO | P6/P7 encerradas + I2 satisfeito |
| E5 | AUTORIZADO | P8/P9/P10 encerradas + I3/I4/I5 satisfeitos |

O par negativo de cada portão (etapa faltando, condição não satisfeita,
inegociável não verificado) está coberto pelos testes T13/T16/T17/T20/
T22/T28/T29/T32-T35 em `testes/campo_2_6_5.py`, não neste caso de
controle — este caso demonstra exclusivamente o caminho positivo
integral, incluindo o cenário agêntico.

## Rastreabilidade evidência → portão → autorização → artefato emitido

A cadeia completa é observável em `eventos.jsonl` desta pasta: cada
`InegociavelSatisfeito` carrega `evidencia` no formato
`<verificador> :: <motivo> (ref: <artefato>)`, e cada `EntregavelEmitido`
carrega `arquivo` e `versao` apontando para o documento material real —
nunca um evento solto sem essas referências.

## Nota sobre o driver

Este caso foi construído por um script Python que reutiliza as mesmas
funções auxiliares de `testes/campo_2_6_5.py` (`preparar_caso`,
`avancar`, `entregavel`, `inegociavel`, `preparar_*`), executado uma vez
para gerar esta evidência e depois descartado (caso temporário sob
`/tmp`). Nenhuma lógica de produção vive nesse driver — ele só
sequencia chamadas aos scripts reais de `eiac-nucleo/` e `eiac-campo/`,
exatamente como um operador humano faria via `/eiac-nucleo:*` e
`/emitir`.
