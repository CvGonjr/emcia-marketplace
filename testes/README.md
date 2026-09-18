# Testes

```bash
bash testes/negativos.sh
```

Trinta e três verificações: as 26 do baseline e sete verificações do contrato
canônico D/I/V. Há negativas e controles positivos — o que é bem formado
precisa passar, senão a trava está apenas quebrada.

Os 11 testes estruturais dos quatro objetos CTX rodam separadamente:

```bash
python3 testes/contexto.py
```

O total acumulado é de 44 verificações.

As recusas são verificadas **pela mensagem**, não só pelo código de saída. Num ponto em que várias travas recusam, conferir apenas o `exit` deixa o teste passar mesmo com a trava certa removida — foi o que aconteceu com o 18 até a mensagem entrar na asserção.

| # | Prova |
|---|---|
| 1 | Habilidade de camada não delegável não carrega |
| 2 | Escrita direta em `caso/` é negada |
| 2b | Redirecionamento de shell para `caso/` é negado |
| 3 | Asserção sem procedência é recusada |
| 4 | Asserção bem marcada é gravada |
| 5 | Etapa presencial não encerra sem sessão registrada |
| 6 | Autor agente é recusado |
| 7 | Entregável com portão fechado não emite |
| 8 | Playbook sem itens inegociáveis não carrega |
| 14 | Nível fora dos declarados no playbook é recusado |
| 15 | Nível apurado por agente é recusado |
| 16 | Nível válido grava e emite `NivelApurado` *(controle positivo)* |
| 17 | Com o nível apurado pelo comando, F0 encerra *(controle positivo)* |
| 18 | Selo por agente é recusado |
| 19 | Selo fora de repositório git é recusado |
| 20 | Selo grava commit com o autor nomeado e emite `SeloAplicado` *(controle positivo)* |
| 21 | Selo sem nada a selar é recusado |
| 22 | A fronteira anunciada acompanha o nível *(controle positivo)* |
| 23 | Etapa não delegável aparece como tal em qualquer nível *(controle positivo)* |
| 24 | Documento citado que não está em `fontes/` é recusado |
| 25 | Documento presente grava e registra o hash na trilha *(controle positivo)* |

## Contrato D/I/V — pacote 2.5.0

| ID | Prova |
|---|---|
| 2.5.0-T01 | `D` válido é aceito sem evidência de verificação |
| 2.5.0-T02 | `I` sem premissa é recusado |
| 2.5.0-T03 | `I` com premissa é aceito |
| 2.5.0-T04 | `V` sem evidência é recusado |
| 2.5.0-T05 | `V` com evidência é aceito |
| 2.5.0-T06 | `X`, `campo` e `externo` são recusados como procedência |
| 2.5.0-T07 | `V` coexiste com `apuracao: medido` em dimensão separada |

O teste 2.5.0-T08 é a execução acumulada desta suíte: os 26 cenários do
baseline permanecem presentes, com os marcadores por extenso atualizados para
os códigos canônicos.

## Objetos CTX — pacote 2.5.1

| ID | Prova |
|---|---|
| 2.5.1-T01 | Termo mínimo válido é aceito |
| 2.5.1-T02 | Entidade mínima válida é aceita |
| 2.5.1-T03 | Regra mínima válida é aceita |
| 2.5.1-T04 | Fonte mínima válida é aceita |
| 2.5.1-T05 | Termo sem `significado` é recusado |
| 2.5.1-T06 | Entidade sem `entidade` é recusada |
| 2.5.1-T07 | Regra sem `estabilidade` é recusada |
| 2.5.1-T08 | Fonte sem `contrato.significado` é recusada |
| 2.5.1-T09 | D/I/V é representável nos quatro objetos |
| 2.5.1-T10 | Taxonomias obsoletas são recusadas como procedência |
| 2.5.1-T11 | Os sete campos centrais da Regra são obrigatórios no schema |

Rodam contra uma cópia temporária do template, sem tocar em caso real.

**Falha aqui é regressão de trava, não de funcionalidade.** Não conserte o teste; conserte a trava.

## Deslocamento da fronteira por nível

Cinco testes cobrem o que CAT-01 seção 3.6 estabelece: **a camada de uma etapa depende do nível do caso.**

| # | Prova |
|---|---|
| 9 | P1 em N3 é `EX3` — habilidade não carrega |
| 10 | A mesma P1 em N1 é `EX2` — carrega |
| 11 | Sem nível apurado, nenhuma etapa após F0 opera |
| 12 | F0 não encerra sem o nível |
| 13 | Playbook com camada plana, sem mapa por nível, é recusado |

O par 9 e 10 é o mais importante do conjunto: mesma etapa, mesma habilidade, resultado oposto conforme o nível. Se os dois passarem juntos, a fronteira desloca.
