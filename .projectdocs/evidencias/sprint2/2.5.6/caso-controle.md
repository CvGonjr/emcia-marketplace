# Caso de controle — Ação 2.5

**ID:** `CTX-TEST-2.5.6-001`
**DATA:** 18/09/2026
**HEAD:** `96d1886580b6a638ed3deff24d5328ca5ad964d1` (HEAD_INICIAL_2.5.6)

Caso construído do zero em diretório temporário isolado (cópia de
`eiac-campo/template-caso`), executado por `testes/consolidado.py`. Não
reutiliza estado residual de nenhum teste anterior. Fixtures controladas;
não representa execução real de cliente.

## Entrada

Organização fictícia de controle: convênio de saúde, processo de emissão
e envio de guia de autorização. Elementos suficientes para produzir 1
Termo, 1 Entidade, 1 Fonte e 1 Regra, e demonstrar `D`, `I` e `V` em
registros apropriados (não forçados sobre o mesmo objeto).

## P2

Candidato de Termo (`T-200`, `procedencia: I`, premissa citando "manual,
página 7") escrito em `rascunho/T-200.yaml` — confirma que P2 produz
candidato endereçável sem ele virar contexto por si só (C10).

## P3a

Não exercitado neste caso de controle — decisão de método já registrada
no 2.5.5 (medição não é objeto CTX; ver `matriz-consolidada.md`). Fora do
escopo de reverificação funcional deste pacote.

## P3b

`RN-100` nasce com `procedencia: D` (declarada, direto pelo levantamento
inicial) e depois, num ramo do caso, uma segunda Regra (`RN-115`) nasce
`procedencia: I` a partir de uma sessão simulada de P3b, referenciando
`T-100` (C11).

## P3d

`DIV-100` (registro de confronto: documento dizia 72h, observado 24h,
justificativa de leitura de volta) curado e referenciado por `RN-100`
via `classificacao_confronto.referencia_p3d`, sem duplicar o detalhe do
confronto na Regra (C07). Mesmo padrão aplicado a `RN-115`→`DIV-115`
(C11).

## Objetos CTX

### Termos

- `T-100` — `guia`, `procedencia: D`.
- `T-101`–`T-104` — variações de procedência para C01 (D válida, I sem/com
  premissa, V sem/com evidência, X fora do contrato).
- `T-105` — Termo estruturalmente inválido (sem `significado`), para C02.
- `T-106` — controle positivo de C05 (curadoria autorizada após bloqueio
  de escrita direta).
- `T-200` — candidato de P2, curado em C10.
- `T-777`, `T-778` — usados em C15 para gerar eventos de recusa.
- `T-999` — usado em C04 (rascunho→contexto).

### Entidades

- `E-100` — `Guia`, `onde_vive: [F-100]`, `procedencia: D`.

### Fontes

- `F-100` — planilha de controle de envios, `procedencia: D`, contrato
  mínimo completo.

### Regras

- `RN-100` — objeto central do percurso. Nasce `D`, versão 1 (C02).
  Tentativa de sobrescrever para `V` na mesma versão recusada (C06).
  Avança para `V`, versão 2, com histórico da versão 1 (C06). Avança
  para `V`, versão 3, `classificacao_confronto.classe: divergente`,
  `referencia_p3d: DIV-100`, com histórico da versão 2 (C07). Estado
  final capturado em `estado-final-caso.json`.
- `RN-101`, `RN-102` — autoria (C03): papéis distintos aceitos; agente
  como `autoria_conteudo` recusado.
- `RN-103`–`RN-110` — reexecução de CTX-V01/V02/V03/V05/V06/V07/V09/V11
  (C08), todas as oito violações recusadas.
- `RN-111`–`RN-114` — referências a Termo/Entidade/Fonte (C09).
- `RN-115` — P3b→CTX→P3d→CTX (C11), `I` inicial referenciando `T-100`,
  depois `V` versão 2 com `referencia_p3d: DIV-115`.
- `RN-777`, `RN-778` — geração de eventos (C15).

### Divergências (P3d)

- `DIV-100` — confronto de `RN-100`.
- `DIV-115` — confronto de `RN-115`.

## Procedência

`D`, `I` e `V` demonstrados sem forçar os três sobre o mesmo objeto:
`T-100`/`E-100`/`F-100` nascem `D` (informação declarada diretamente);
`T-102`/`RN-115` nascem `I` (premissa obrigatória, verificado sem/com);
`T-103`/`RN-100`(v2/v3) chegam a `V` (evidência obrigatória, verificado
sem/com). Valor fora do contrato (`X`) recusado.

## Curadoria

`rascunho/` → `curar.py` → `contexto/`, sempre. Nenhum objeto entrou em
`contexto/` sem passar pelo curador (C04, C10). Escrita direta em
`contexto/` recusada com `exit 2` pela guarda (C05).

## Histórico

`RN-100`: sobrescrita de `D`/versão 1 para `V`/versão 1 recusada; `V`
versão 2 com histórico da versão 1 aceita; `V` versão 3 (mudança de
`classificacao_confronto`) com histórico da versão 2 aceita. Versão 1
permanece legível dentro do registro atual, na entrada de `historico`.

## CTX-V

Oito das onze validações reexecutadas neste caso novo (CTX-V01, V02,
V03, V05, V06, V07, V09, V11) — todas as oito recusaram o cenário
inválido correspondente (C08). As três restantes (V04, V08, V10) foram
demonstradas nos testes C05/C06/C07 deste mesmo caso. Nenhuma CTX-V
contabilizada só por constar no documento.

## Consumo P4

`quadro.py` executado sobre `contexto/regras/` do caso de controle
(contendo `RN-100` e as demais Regras curadas), `exit 0` (C12, C16).

## Consumo P5

`consultar.py --id RN-100` retorna os sete campos centrais e
`procedencia: V` como dado estruturado, sem reinterpretação (C13, C14,
C16).

## Eventos

`eventos.jsonl` desta evidência demonstra: `ObjetoContextoCurado` (Termo
`T-100`, Fonte `F-100`, Entidade `E-100`, Regra `RN-100`),
`CuradoriaRecusada` (Termo `I` sem premissa; Regra com agente como autor
E referências quebradas na mesma recusa — confirma política acumulativa
do 2.5.4), `TentativaNegada` (escrita direta em `contexto/`).

## Resultado final

**16/16 verificações consolidadas (C01–C16) aprovadas.** Nenhum defeito
de código encontrado — os dois problemas identificados durante a
construção deste caso estavam nas fixtures do próprio teste novo
(`testes/consolidado.py`), corrigidos antes da execução registrada como
evidência (ver `resultado.md` §19).
