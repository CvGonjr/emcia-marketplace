# Portões de emissão

Todo entregável tem **exatamente um portão**. O portão declara as etapas que precisam estar encerradas e as asserções que o sustentam. Nenhum caso altera esse mapeamento depois de aberto.

## Entregáveis ao cliente

| # | Entregável | Fase | Etapas exigidas | Modelo |
|---|---|---|---|---|
| E1 | Ficha de enquadramento e nível | F0 | F0 | Modelo E1, ação 1.6 |
| E2 | Dossiê verificado | F1 | P1, P2, P3a, P3b, P3d | Modelo E2 |
| E3-D | Decisão da solução — **sempre emitido** | F2 | P4, P5 | Modelo E3, parte de decisão |
| E3-E | Especificação da solução — **condicionado ao portão de P5** | F2 | P5 concluído por agente | Modelo E3, parte de especificação |
| E4 | Guia operacional | F3 | P6, P7 *(ver pendência)* | Modelo E4 |
| E5 | Relatório de piloto e calibragem | F4 | P9, P10 *(ver pendência)* | Modelo E5 |

### O portão do E3

`E3-E` só existe se a classificação tecnológica do P5 concluir que a solução é um agente. Quando conclui que não é, `E3-D` registra qual tecnologia atende e o caso segue sem `E3-E`.

**Emitir `E3-E` quando P5 concluiu que não é agente é erro de método, não de formato.**

## Itens inegociáveis

Cinco itens não escalam para baixo. Cada um é condição de emissão do seu entregável.

| # | Item | Passo | Bloqueia |
|---|---|---|---|
| 1 | Medição inicial registrada, `apuracao` diferente de `estimado` | P3a | E2 |
| 2 | Termo de autonomia escrito | P7 | E4 |
| 3 | Casos de teste com saída esperada | P8 | *ver pendência* |
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

## Pendência bloqueante

A correspondência entre entregáveis e passos diverge entre documentos:

- **Relatório do PFC:** P6–P7 em E4, P8–P10 em E5
- **Documentos internos:** P6–P8 em E4, P9–P10 em E5

A diferença decide onde o item inegociável 3 é cobrado. **Não resolva por conta própria** — a emissão de E4 e E5 fica suspensa até a decisão.
