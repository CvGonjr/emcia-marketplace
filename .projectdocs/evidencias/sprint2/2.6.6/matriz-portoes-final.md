# Matriz de portões — pacote 2.6.6

| Portão | Etapas | Inegociáveis | Condição | Resultado |
|--------|--------|--------------|----------|-----------|
| E1 | F0 | — | — | AUTORIZADO |
| E2 | P1, P2, P3a, P3b, P3d | I1 | — | AUTORIZADO |
| E3-D | P4, P5 | — | — | AUTORIZADO |
| E3-E | P5 | — | `classificacao_tecnologica` (P5) `contem` `"agente"` | AUTORIZADO (caso agentico; ver 2.6.5 para o par NÃO APLICÁVEL no caso não agêntico) |
| E4 | P6, P7 | I2 | — | AUTORIZADO |
| E5 | P8, P9, P10 | I3, I4, I5 | — | AUTORIZADO |

**6/6 autorizações aplicáveis conformes.**

Este caso de controle é agêntico por decisão registrada em P5
(`classificacao_tecnologica: agente`), portanto `E3-E` é aplicável e
avaliado como AUTORIZADO. O par NÃO APLICÁVEL (E3-E sobre caso não
agêntico) já foi demonstrado e testado exaustivamente no pacote 2.6.5
(`2.6.5-T22`, reconfirmado na regressão `2.6.6-C43`) e não foi
reconstruído aqui — construir um segundo caso completo apenas para repetir
essa distinção seria redundante com a evidência já persistida em
`.projectdocs/evidencias/sprint2/2.6.5/`, que este pacote preserva e não
reescreve (seção 61 do pacote 2.6.6).

Nenhuma condição foi avaliada por hard-code de método no núcleo: a
mesma função genérica `avancar.py::_avaliar_condicao()` (2.6.1/2.6.5)
foi reutilizada sem alteração.
