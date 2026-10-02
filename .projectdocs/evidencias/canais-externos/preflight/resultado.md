# Canais externos — linha de base e referência pendente

Data: 02/10/2026. Somente dados sintéticos nas suítes.
Marketplace: `82d9c9e7f0a8bf148a49d2c627680646830e7328`.
Artefatos: `ab09abeaa3f6aeb21ff94242a70c2ad91c3fd911`; checkout limpo.

## Pré-requisito

Decisão 039, importador humano e `exige_evento_selado` em F0 presentes.
`testes/habilitacao_0d.py`: 31 testes aprovados, incluindo importação,
recusa pela sessão e exigência de selo confirmado pelo histórico Git.
O pacote D da decisão 039 continua parcial conforme escopo registrado;
isso não impede o pré-requisito específico desta solicitação.

## Linha de base

Todos os comandos foram executados antes de qualquer alteração:

| Comando | Resultado |
|---|---|
| `bash testes/negativos.sh` | código 0; todas as travas aprovadas |
| `python3 testes/contexto.py` | código 0; 11 verificações aprovadas |
| `python3 testes/habilitacao.py` | código 0; 19 testes aprovados |
| `python3 testes/habilitacao_0d.py` | código 0; 31 testes aprovados |
| `python3 testes/consolidado.py` | código 0; 16 verificações aprovadas |

## Divergência de referência — sem decisão inferida

O pedido referencia EMCIA-TRI-01 §3.4 para as nove perguntas, na leitura
obrigatória e no requisito E3.3. No documento canônico v0.2 e no instrumento
empacotado, as nove perguntas estão em §3.3 (tabelas §3.3.1–3.3.3).
§3.4 é “Regra de pontuação e de leitura”; não contém as nove perguntas.

Os dois arquivos são idênticos, com SHA-256
`19d8f0e564c35d07989ffe589c1db2a3ee57c496fe35cff973a94f742c7bbfdb`.
Não foi constatada divergência de redação entre esses dois arquivos.
A pendência é a referência do pedido frente ao documento canônico.

AGENTS.md determina: “Não resolva divergência documental por inferência.
Registre a divergência e espere decisão humana”. Aguarda-se confirmação
para usar §3.3 como referência das perguntas e conservar §3.4 como regra
de pontuação. Nenhum formulário ou teste de correspondência foi criado.

Não foram alterados scripts, versões, playbook ou documentos controlados.
Não foram executadas ações externas nem criado commit de pacote.
O teste real dos hooks MCP (E7) ainda não foi executado; não há conclusão
sobre seu disparo. E1–E7 continuam pendentes.
O diretório preexistente `.projectdocs/figuras/` foi preservado.

## Atualização após confirmação

O usuário confirmou §3.3 para perguntas e §3.4 para pontuação e pediu corrigir
`hb-enquadrar/SKILL.md`. Pendência resolvida; implementação retomada.
A correção está registrada em `../pacote-E3/correcao-referencia.md`.
O restante deste arquivo preserva o estado do levantamento inicial.
