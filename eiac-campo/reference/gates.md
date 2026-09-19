# Portões de emissão

Todo entregável tem **exatamente um portão**. O portão declara as etapas que precisam estar encerradas e as asserções que o sustentam. Nenhum caso altera esse mapeamento depois de aberto.

## Entregáveis ao cliente

| # | Entregável | Fase | Etapas exigidas | Modelo |
|---|---|---|---|---|
| E1 | Ficha de enquadramento e nível | F0 | F0 | Modelo E1, ação 1.6 |
| E2 | Dossiê verificado | F1 | P1, P2, P3a, P3b, P3d | Modelo E2 |
| E3-D | Decisão da solução — **sempre emitido** | F2 | P4, P5 | Modelo E3, parte de decisão |
| E3-E | Especificação da solução — **condicionado ao portão de P5** | F2 | P5 concluído por agente | Modelo E3, parte de especificação |
| E4 | Guia operacional | F3 | P6, P7 | Modelo E4 |
| E5 | Relatório de piloto e calibragem | F4 | P8, P9, P10 | Modelo E5 |

### O portão do E3

`E3-E` só existe se a classificação tecnológica do P5 concluir que a solução é um agente. Quando conclui que não é, `E3-D` registra qual tecnologia atende e o caso segue sem `E3-E`.

**Emitir `E3-E` quando P5 concluiu que não é agente é erro de método, não de formato.**

## Itens inegociáveis

Cinco itens não escalam para baixo. Cada um é condição de emissão do seu entregável.

| # | Item | Passo | Bloqueia |
|---|---|---|---|
| 1 | Medição inicial registrada, `apuracao` diferente de `estimado` | P3a | E2 |
| 2 | Termo de autonomia escrito | P7 | E4 |
| 3 | Casos de teste com saída esperada | P8 | E5 |
| 4 | Ao menos uma métrica de resultado, não só de uso | P9 | E5 |
| 5 | Responsável nomeado pela recalibragem, com nome próprio | P10 | E5 |

## Artefatos internos — sem portão

Não são entregues ao cliente e não têm condição de emissão.

| Artefato | Produzido em | Alimenta |
|---|---|---|
| Regras candidatas | P2 | P3d |
| Lacunas documentais | P2 | Roteiro de campo |
| Registro de sessão de campo | P3b | Abertura de P3d |
| Log de divergência | P3d | Calibragem da triagem |
| Log de tentativas negadas | Todas | Lição aprendida |
| Quadro de Contraste | Sprint 4 | Anexo do relatório |

## Correspondência entregável × passo (resolvida)

A correspondência entre entregáveis e passos foi fixada por
EMCIA-CAM-01/EMCIA-ESP-01 v0.2 (17/09/2026), coincidindo com o relatório
do PFC: **E4 = P6, P7**; **E5 = P8, P9, P10**. Ver `decisoes/013` no
repositório. A tabela acima já reflete essa correspondência.

Fixar o portão não significa afirmar que os cinco entregáveis já são
emitíveis em produção — a validação semântica completa dos cinco
inegociáveis e a materialização dos documentos pertencem aos pacotes
2.6.2–2.6.5 (Sprint 2 do Code Plugin).

## Verificação semântica e materialização (pacote 2.6.5)

Os cinco inegociáveis passam a ser verificados a partir de artefato real,
nunca de flag solta: `scripts/inegociaveis.py --verificar <N> --arquivo
<artefato>` lê o registro correspondente (`registro/baseline/` para I1,
`registro/governanca/autonomia/` para I2, `registro/piloto/` para I3,
`registro/metricas/` para I4, `registro/calibragem/` para I5) e só chama
`avancar.py --satisfazer-inegociavel` depois de confirmar semanticamente
que o requisito está atendido.

Cada entregável passa a ter arquivo material real em
`caso/entregaveis/<ID>.md`, renderizado por `scripts/entregaveis.py` a
partir desses mesmos artefatos — nunca preenchido com texto genérico
quando falta evidência. `avancar.py --emitir --materializar <arquivo>`
recusa registrar `EntregavelEmitido` se o arquivo indicado não existir ou
estiver vazio (D-12).

`E3-E` avaliado sobre um caso não agêntico devolve `NAO_APLICAVEL`, não
falha — é resultado legítimo do método, não erro de emissão.
