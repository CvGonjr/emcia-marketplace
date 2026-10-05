# emcia — marketplace de plugins

O bloco inicial é conduzido pelo Claude Code com `/eiac-campo:iniciar`: ambiente,
habilitação administrativa de 0a a 0d, abertura, canais, importação, validação e
selo até **F0 liberado para execução**. O engenheiro confere os conteúdos e aprova
os efeitos externos no chat; decisões de método continuam no terminal humano.

Este repositório é a ferramenta. Não contém caso nem dado de cliente.

| Componente | Versão | Responsabilidade |
|---|---|---|
| eiac-nucleo | 0.2.48 | Guarda, procedência, etapas e trilha; aplica contratos genéricos do caso |
| eiac-campo | 0.8.31 | Método, comandos, habilidades e operações administrativas |
| Playbook dos casos novos | 0.4.22 | Atos administrativos aprovados; decisões de método humanas |
| Pacote do método | manifesto v6 · metodo-v1.0 | 22 documentos, bytes canônicos preservados |

Caso real utiliza somente a linha de base documental aprovada **metodo-v1.0**,
publicada em [emcia-artefatos](https://github.com/CvGonjr/emcia-artefatos/) na tag
que resolve para `08bfb162d762935ed35f55e0a75bc700b81d5276`.
O [APR-01](eiac-campo/reference/metodo/EMCIA-APR-01-registro-de-aprovacoes.md)
fixa os hashes de 21 documentos, modelos e templates; seu próprio arquivo compõe
o pacote. Documento em revisão ou fora dessa aprovação não entra em caso real.
Alteração documental posterior requer aprovação e nova linha de base antes do uso.
Nenhum documento do pacote foi editado para esta entrega.

As [decisões 045](decisoes/045-bloco-inicial-conduzido.md) e
[047](decisoes/047-habilitacao-simplificada.md) autorizam as diferenças
operacionais do playbook 0.4.22. O MAN-01 v1.0 ainda descreve o contrato anterior:
`manual_a25.py` é **falha conhecida**, mantida visível até revisão canônica.
Propostas: [propostas-artefatos.md](propostas-artefatos.md).

## Instalação e início

```text
/plugin marketplace add CvGonjr/emcia-marketplace
/plugin install eiac-nucleo@emcia
/plugin install eiac-campo@emcia
```

```bash
claude mcp add tally --transport http --scope user https://api.tally.so/mcp
```

No Claude Code, confirme os conectores Google Drive e Google Calendar em `/mcp`
e execute `/eiac-campo:iniciar`. O comando verifica Python ≥3.12, Git e identidade,
Chrome/Chromium, versões, configuração e os três MCPs; faltas vêm com correção.
A presença do conector não implica que todas as suas ferramentas sejam compatíveis.
O perfil é calibrado e aprovado na abertura; dentro do caso, nome ou assinatura
divergente é recusado, sem afrouxar a trava.
Detalhes: [INSTALACAO.md](INSTALACAO.md).

## Percurso conduzido e retomada

A preparação reutilizável configura responsável, bases externas, workspace Tally,
calendário, navegador e condições administrativas. Não exige perfil antes da
abertura; o inventário real será usado nessa transição. Pasta Drive pode ser informada em P2. Ratificação ou aceitação revogável e
formulários permanentes são conferidos uma vez. `load_form(formId)` e o comparador
fixam texto, ordem, tipo e campo oculto caso; relatório sem divergências recebe
“conferido”. `formularios_permanentes` guarda tipo, id, versão/hash do contrato,
data/hash da conferência. Alteração exige nova conferência, sem recriar por cliente.

O engenheiro envia o link `?caso=<caso>` e deposita os três PDFs assinados em
`~/emcia-op/entrada/`. A sessão lê fetch_submissions; o script registra apenas
a submissão cujo campo oculto caso corresponde ao expediente, com hashes.
Zero ou várias aguardam indicação humana. CSV filtrado é alternativa manual.
Antes da abertura, Tally/Drive/Calendar leem, listam, criam rascunhos e comparam
sem perfil/escopo por id. Publicar, enviar mensagem/convite ou compartilhar
exige “ok” com resumo/data. load_form admite qualquer formId.
Esclarecimentos vêm por mensagem, preservados como fonte manual com rodada.
Matriz de 0c é pré-preenchida e confirmada/corrigida numa mensagem.

O percurso nominal tem três confirmações, que podem ser “ok”:

1. Revisão conjunta dos três documentos apresentados: revisar, gerar e liberar.
2. Conferência dos PDFs assinados, associação aos enviados e evidências.
3. Perfil/escopo apresentados, abertura, declaração Tally/calendário, importação, validação e selo.

O testemunho conserva resumo, trecho real, data, pessoa e hashes. Silêncio não vale.
Os PDFs emitidos preservam os bytes conferidos. Associação automática do retorno
exige texto integral dos enviados, extraído por Poppler/pdftotext; arquivos sem
texto ou com conteúdo divergente usam a alternativa manual com conferência humana.
Não há integração com assinatura. Mudanças exigem nova revisão.

`/eiac-campo:iniciar` carrega somente o [cartão](eiac-campo/reference/cartao-habilitacao.md)
e chama `iniciar.py proximo` uma vez por avanço, com saída curta. Criação de
expediente, tratamento padrão e coleta não têm aprovação própria. Retomada não
repete emissão, assinatura, importação ou selo. O checklist confere F0 liberado,
sem encerrá-lo; evento de selo sem commit confirmado não basta.

Drive é planejado/provisionado em P2, com uma aprovação de criação e compartilhamento.
A raiz e trabalho-interno ficam privados; cada efeito mantém ids, destinatário e
papel aprovados. P2 permanece bloqueada sem o canal de documentos.
Chamada MCP interrompida antes de preservar retorno exige conferir objeto remoto
por id antes de repetir; não se promete execução única de APIs.

## Minutas e situação jurídica

Templates são localizados pelos códigos HAB-01/02/03 na tabela do APR-01, com
exatamente um arquivo por código e SHA-256 correspondente. Nomes antigos e futuros
são aceitos quando declarados em linha de base aprovada, sem inferência por nome.

`revisao-juridica` continua disponível: exige `resultado: "aprovado"`, revisor,
decisor, data, cobertura por hash e evidência importada; `ciclo` é texto opcional.
Parecer condicionado ou reprovado não vira revisão autorizadora no expediente.
O componente não interpreta parecer nem autentica qualificação profissional.

Sem revisão aprovada para o hash, o engenheiro pode aceitar uma única vez
**“uso as minutas sem ratificação jurídica”**. A aceitação tem texto, data e
responsável em `~/.emcia/config.json`, é reutilizada e pode ser revogada.
Sem revisão nem aceitação ativa, `gerar` recusa com as duas saídas possíveis.
A revogação impede novas emissões, preservando as já emitidas e sua situação.

Revisão aprovada prevalece sobre a aceitação para os hashes cobertos. Cada emissão
registra versão/hash da minuta, data e situação “ratificada” ou “sem ratificação”,
com referência ao ato correspondente. O checklist mostra **Minutas sem ratificação
jurídica** como pendência não bloqueante. Controle interno do modelo, aviso jurídico,
histórico interno e aceitação não entram no MD/PDF do cliente; a emissão indica
“Para assinatura”. Conferências humanas da carta e dos PDFs permanecem obrigatórias.

## Terminal e decisões de método

Os comandos manuais continuam disponíveis nas referências de
[habilitação](eiac-campo/reference/habilitacao.md) e
[canais](eiac-campo/reference/canais.md). Atos administrativos do bloco inicial
podem ser executados pela sessão depois de aprovação registrada. Em casos antigos,
o playbook copiado continua mandando; atualizar plugin não migra contratos.

Apuração de nível, `decidir-prosseguimento`, sessões, restrições, autonomia,
recalibragem, encerramentos EX3/EX4 e selo após P2 permanecem no terminal humano.
A guarda recusa esses atos pela sessão mesmo com aprovação nominal anexada.
F0 liberado significa que a preparação acabou, não que F0 foi encerrado.
O engenheiro registra o prosseguimento com base na E1; “não prosseguir” encerra
F0 e bloqueia etapas seguintes conforme a decisão 043.

Depois do bloco inicial, recebimento, entrega e listagem seguem o contrato humano
correspondente. O agente prepara rascunhos; escrita em caso/, registro/ e fontes/
continua passando pelos mecanismos determinísticos, nunca por Write/Edit direto.
Asserções mantêm procedência, autoria nominal e origem verificável; recebimento
não converte declaração em verificação. EX1–EX4 permanecem resolvidas por nível.

## Limites e verificação

A aprovação no chat é testemunho local, **não autenticação**. O engenheiro e a
sessão com escrita no disco formam a fronteira de confiança das decisões 022 e 045.
Hashes fixam bytes, sem provar conteúdo remoto, identidade, acesso efetivo, assinatura
criptográfica ou recebimento pelo cliente. Assinatura permanece no painel escolhido
pelo cliente, sem integração. Dados operacionais aguardam abertura e procedência.

O núcleo continua sem nomes de instrumentos, conectores ou atos do método:
recebe regras pelo playbook do caso. Nenhuma flag desativa a guarda. O runtime precisa
executar os hooks; os testes desta entrega usam MCPs simulados, não validam contas
reais nem todas as versões de conectores. Depois da abertura, ferramentas com
interface sem perfil exigem um perfil novo conferido; busca global não contorna
a trava do caso. Não há escopo por id na habilitação anterior à abertura.

Regressão completa em Python 3.12 e exceção A25 documentadas em
[bloco-inicial-conduzido](.projectdocs/evidencias/bloco-inicial-conduzido/README.md).
Comandos, negativas, retomadas e conferência dos hashes são descritos em
[testes/README.md](testes/README.md). Não há dado real de cliente nos testes.

O instrumento canônico de contexto está em
[EMCIA-CTX-01](eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md).
Remissões usam esse arquivo controlado; os resumos anteriores foram retirados
pela emenda à decisão 021.
