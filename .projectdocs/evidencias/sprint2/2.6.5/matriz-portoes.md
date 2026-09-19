# Matriz de portões — pacote 2.6.5

Estado final, após implementação. Fonte: `eiac-campo/template-caso/registro/playbook.json`
(`entregaveis`), `eiac-nucleo/scripts/avancar.py::emitir()`, `eiac-campo/reference/gates.md`.

| Portão | Etapas | Condição | Inegociáveis | Artefato resultante | Estado |
|--------|--------|----------|---------------|----------------------|--------|
| E1 | F0 | — | — | `caso/entregaveis/E1.md` | CONFORME |
| E2 | P1, P2, P3a, P3b, P3d | — | I1 | `caso/entregaveis/E2.md` | CONFORME |
| E3-D | P4, P5 | — | — | `caso/entregaveis/E3.md` (Parte A) | CONFORME |
| E3-E | P5 | `classificacao_tecnologica` (etapa P5) `contem` `"agente"` | — | `caso/entregaveis/E3.md` (Parte B) | CONFORME (AUTORIZADO/NÃO APLICÁVEL distintos de NEGADO) |
| E4 | P6, P7 | — | I2 | `caso/entregaveis/E4.md` | CONFORME |
| E5 | P8, P9, P10 | — | I3, I4, I5 | `caso/entregaveis/E5.md` | CONFORME |

## Leitura da matriz

- **E3-D e E3-E não são dois entregáveis ao cliente.** Ambos alimentam o
  mesmo arquivo material `caso/entregaveis/E3.md` — `entregaveis.py::render_e3`
  sempre escreve a Parte A (decisão) e só acrescenta a Parte B (blueprint do
  agente) quando `classificacao_tecnologica` do cumprimento de P5 contém
  `"agente"`. Ver T26/T27 e caso-controle.md.
- **E3-E resolve em três resultados distintos**, nunca apenas
  PASS/FAIL: `AUTORIZADO` (caso agêntico com P5 completo), `NAO_APLICAVEL`
  (caso não agêntico — resultado legítimo do método, não falha) e `NEGADO`
  (só ocorreria se a condição referenciasse campo/etapa/operador inválido
  no playbook — contrato inválido, T25).
- Nenhum portão é aberto por flag: `avancar.emitir()` sempre reavalia
  etapas do portão + condição declarativa + registro estruturado dos
  inegociáveis a cada chamada (T13/T14, T20/T21, T28/T30, T32-T36).
- Todos os seis portões têm par negativo/positivo demonstrado (seção 60
  do pacote) — ver `matriz-entregaveis.md` e os testes T13-T42.
