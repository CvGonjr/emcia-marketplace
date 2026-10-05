# emcia — marketplace de plugins

O bloco inicial é conduzido pelo Claude Code com `/eiac-campo:iniciar`: ambiente,
habilitação administrativa de 0a a 0d, abertura, canais, importação, validação e
selo até **F0 liberado para execução**. O engenheiro confere os conteúdos e aprova
os efeitos externos no chat; decisões de método continuam no terminal humano.

Este repositório é a ferramenta. Não contém caso nem dado de cliente.

| Componente | Versão | Responsabilidade |
|---|---|---|
| eiac-nucleo | 0.2.47 | Guarda, procedência, etapas e trilha; aplica contratos genéricos do caso |
| eiac-campo | 0.8.27 | Método, comandos, habilidades e operações administrativas |
| Playbook dos casos novos | 0.4.21 | Atos administrativos aprovados; decisões de método humanas |
| Pacote do método | manifesto v6 · metodo-v1.0 | 22 documentos, bytes canônicos preservados |

Caso real utiliza somente a linha de base documental aprovada **metodo-v1.0**,
publicada em [emcia-artefatos](https://github.com/CvGonjr/emcia-artefatos/) na tag
que resolve para `08bfb162d762935ed35f55e0a75bc700b81d5276`.
O [APR-01](eiac-campo/reference/metodo/EMCIA-APR-01-registro-de-aprovacoes.md)
fixa os hashes de 21 documentos, modelos e templates; seu próprio arquivo compõe
o pacote. Documento em revisão ou fora dessa aprovação não entra em caso real.
Alteração documental posterior requer aprovação e nova linha de base antes do uso.
Nenhum documento do pacote foi editado para esta entrega.

A [decisão 045](decisoes/045-bloco-inicial-conduzido.md) autoriza as diferenças
operacionais do playbook 0.4.21. O MAN-01 v1.0 ainda descreve o contrato anterior:
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
Inventário com nome e assinatura divergentes é recusado, sem afrouxar a trava.
Detalhes: [INSTALACAO.md](INSTALACAO.md).

## Percurso conduzido e retomada

Na primeira execução, o agente obtém ids pelos MCPs quando possível, pergunta
somente o que faltar e grava `~/.emcia/config.json`: responsável, bases de casos
e expedientes, workspace Tally, pasta raiz Drive, calendário e navegador.
Ele apresenta o perfil determinístico dos conectores para uma confirmação inicial.
Ferramentas sem perfil permanecem recusadas e são listadas no diagnóstico.
A calibração usa o inventário fornecido, com nomes e parâmetros literais. Neste
conector Tally, preparação do formulário e coleta filtrada de submissões exigem
ação manual registrada: não existe filtro por campo oculto em `fetch_submissions`.

O percurso sem alterações de conteúdo reúne cinco aprovações:

1. Envio do formulário e plano administrativo de coleta e esclarecimentos.
2. Conferência da carta, qualificação e campos consolidados com fonte.
3. Conferência dos três PDFs, signatários e plano de retorno das assinaturas.
4. Decisão de abrir, incluindo uma aprovação da árvore inteira e do plano local
   de canais → importação → validação → selo.
5. Conjunto dos compartilhamentos, listando destinatário, pasta/id e papel.

Cada operação recebe um testemunho com operação, resumo, trecho literal, pessoa,
data, contexto, entrada e hashes dos arquivos conferidos. O mesmo trecho pode
cobrir atos mecânicos do plano aprovado; não autoriza conteúdo, destinatário ou
papel diferente. Mudanças exigem nova aprovação. Os PDFs devolvidos e comprovantes
são indicados pelo engenheiro; o agente não inventa assinatura ou conferência.
Não há mensagem, compartilhamento ou publicação sem aprovação explícita.

A sessão registra condições administrativas antes de ler respostas; conserva
perguntas, respostas e rodadas, prepara os campos e as conferências. Depois de 0d,
abre o caso, provisiona os ids, define canais (ou usa `--canais`), importa, valida
`00-habilitacao`, sela e roda [saida_inicial.py](eiac-campo/scripts/saida_inicial.py).
O relatório confere o método, os canais, os arquivos e o selo confirmado no Git.
Evento `SeloAplicado` deixado por commit recusado não libera F0.

`/eiac-campo:iniciar` lê expediente e caso e retoma a saída ausente. Não repete
emissão, assinatura, importação ou selo já confirmados. Chamada MCP interrompida
antes de preservar seu retorno exige conferência remota por id antes de repetição.
Não há promessa de execução única de APIs sem essa conferência.

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
reais nem todas as versões de conectores. Ferramentas com interface sem perfil
exigem um perfil novo conferido; não se admite busca global como alternativa.

Regressão completa em Python 3.12 e exceção A25 documentadas em
[bloco-inicial-conduzido](.projectdocs/evidencias/bloco-inicial-conduzido/README.md).
Comandos, negativas, retomadas e conferência dos hashes são descritos em
[testes/README.md](testes/README.md). Não há dado real de cliente nos testes.

O instrumento canônico de contexto está em
[EMCIA-CTX-01](eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md).
Remissões usam esse arquivo controlado; os resumos anteriores foram retirados
pela emenda à decisão 021.
