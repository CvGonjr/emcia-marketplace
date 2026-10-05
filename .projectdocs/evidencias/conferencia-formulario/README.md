# Conferência automática de formulário — 05/10/2026

Ensaio sintético, sem conta remota e sem dados de cliente. Campo 0.8.28,
núcleo 0.2.48, playbook 0.4.21. O método empacotado permanece metodo-v1.0.

## Regressão integral

| Momento | Python | Verificações | Módulos | Falhas inesperadas |
|---|---|---:|---:|---:|
| Linha de base 4c3da34 | 3.12.12 | 1054 | 52 | 0 |
| Linha de base 4c3da34 | 3.14.4 | 1056 | 52 | 0 |
| Item 1 | 3.12.12 | 1061 | 52 | 0 |
| Item 1 | 3.14.4 | 1063 | 52 | 0 |
| Final | 3.12.12 | 1090 | 53 | 0 |
| Final | 3.14.4 | 1092 | 53 | 0 |

A suíte bruta não é inteiramente verde: manual_a25.py conserva a única falha
conhecida da decisão 045, em test_01, com a divergência exata
“ato humano selar-apos-P2 ausente das seções 3.3 e 3.4”. As quatro negativas
passam. O runner exige identidade dessa falha, inclui a saída bruta/código 1
e recusa qualquer outra divergência; não exclui módulos. Duas verificações
adicionais em 3.14 decorrem da disponibilidade de PyYAML, sem dependência nova.

A regressão integral foi executada em checkout temporário do marketplace, com
checkout irmão do canônico na tag aprovada 08bfb16. Isso evita confundir o
rascunho local posterior do emcia-artefatos com a linha de base do pacote.
Os arquivos de baseline, item-1 e final contêm saídas integrais, versões e HEAD.

## Negativas e contrato

perfil-antes.txt demonstra a ausência inicial de load_form (43 testes nessa
primeira rodada; a bateria final possui 47). comparacao-antes.txt e
confirmacao-antes.txt registram testes anteriores às implementações. As saídas
“depois” e contratos-3.12/3.14 registram os controles corrigidos.

conferencia_formulario.py executa 29 testes: texto, ordem, tipo, campo oculto,
formId alheio, ferramenta fora do perfil, retorno/relatório adulterado, hashes,
contexto, formato desconhecido, confirmação literal, PDF, nova leitura,
escolha única/alternativas da triagem e contrato genérico do último evento.
O percurso integrado de início usa scripts/hooks reais e MCP simulado.

inventario-origem.json conserva a assinatura literal e o SHA-256 do inventário
fornecido. calibracao-inventario-real.json contém o perfil completo atualizado,
load_form/formId, comparação/relatório/confirmado, recusas e alternativas manuais.
Schemas de ferramentas continuam vindo exclusivamente desse inventário.

schema-blocos-fonte.json registra o SHA-256 do OpenAPI e os trechos de schema
necessários para o adaptador, obtidos da fonte primária:
https://developers.tally.so/api-reference/openapi.json.
O exemplo oficial de TITLE + entrada subsequente está em
https://developers.tally.so/documentation/creating-a-contact-form.
A metadata da ferramenta consultada anuncia structuredContent.data.blocks
como payload bruto. A fixture é sintética nesse formato; não comprova retorno
em conta real. Outros formatos são recusados com diagnóstico, sem interpretar
ledger por IA. O modelo de ciclo não fixa texto de perguntas: permanece manual.

## Relatórios e integridade

reproduzir-relatorios.py gera identico.md, texto-diferente.md, ordem-trocada.md
e oculto-ausente.md com scripts reais em contexto sintético. relatorios-hashes.json
registra SHA-256, diferenças e autorização/recusa da publicação. Somente o exemplo
idêntico, confirmado com “conferido”, libera publicação; nenhuma API é executada.

integridade.json confere hashes da implementação e bytes de cada documento do
pacote contra o objeto Git da tag e o manifesto. metodo_empacotado.py também
confere APR-01 na regressão integral. vocabulario-nucleo.txt registra a busca
sem ocorrências de vocabulário do método/conectores nos scripts do núcleo.

Para reproduzir a suíte, use reexecutar-suite.py com caminho de saída e Python
3.12/3.14 no PATH (inclusive python3 dos subprocessos), TMPDIR fora dos repositórios
e PYTHONDONTWRITEBYTECODE=1. O checkout irmão do canônico deve estar na tag
metodo-v1.0. Para os exemplos, execute reproduzir-relatorios.py nas mesmas condições.
