# Matriz de entregáveis — pacote 2.6.6

| Entregável | Autorização | Arquivo | Versão | Evento | Resultado |
|------------|-------------|---------|--------|--------|-----------|
| E1 | E1 | `caso/entregaveis/E1.md` | 1 | `EntregavelEmitido` (entregavel=E1) | PASS |
| E2 | E2 | `caso/entregaveis/E2.md` | 1 | `EntregavelEmitido` (entregavel=E2) | PASS |
| E3 | E3-D + E3-E (consolidados em um único arquivo) | `caso/entregaveis/E3.md` | 1 | `EntregavelEmitido` (entregavel=E3-D), `EntregavelEmitido` (entregavel=E3-E) | PASS |
| E4 | E4 | `caso/entregaveis/E4.md` | 1 | `EntregavelEmitido` (entregavel=E4) | PASS |
| E5 | E5 | `caso/entregaveis/E5.md` | 1 | `EntregavelEmitido` (entregavel=E5) | PASS |

**5/5 entregáveis materiais recuperáveis.**

E3-D e E3-E são duas autorizações internas distintas (linhas separadas na
matriz de portões), mas ambas apontam para o mesmo arquivo material
`caso/entregaveis/E3.md` — confirmando que o cliente recebe um único
Blueprint da Solução, com Parte A (decisão, sempre presente) e Parte B
(especificação do agente, presente porque E3-E avaliou AUTORIZADO neste
caso). Cópias dos cinco arquivos estão preservadas em
`.projectdocs/evidencias/sprint2/2.6.6/caso-controle-E{1..5}.md`.

Nenhum dos cinco arquivos contém texto `ALTERE-ME` além do placeholder de
"Engajamento" (metadado de cabeçalho, não coberto pelas fontes do caso —
mesma convenção herdada do 2.6.5, não uma lacuna nova deste pacote).
