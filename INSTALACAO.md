# Instalação — marketplace emcia

Instale os plugins, conecte Tally e Google, e execute o bloco inicial conduzido.
O ambiente exige Python 3.12 ou superior, Git com identidade e Chrome/Chromium.
A regressão do projeto usa Python 3.12. Núcleo 0.2.46, campo 0.8.26, playbook 0.4.20.

## 1. Instalar os plugins

No Claude Code:

```text
/plugin marketplace add CvGonjr/emcia-marketplace
/plugin install eiac-nucleo@emcia
/plugin install eiac-campo@emcia
```

Se o marketplace já estiver instalado, atualize os dois plugins e reinicie a sessão.
Confira as versões instaladas. A alteração de playbook vale somente para casos novos;
caso existente conserva seu contrato e exige migração humana deliberada.

Caso real usa somente a linha de base aprovada **metodo-v1.0**, registrada no
[APR-01](eiac-campo/reference/metodo/EMCIA-APR-01-registro-de-aprovacoes.md).
Documento em revisão ou fora da aprovação não entra em caso real. O pacote é
byte a byte o da tag `metodo-v1.0`; a autorização operacional da decisão 045 não
reescreve documentos canônicos. O MAN-01 ainda requer revisão: A25 é falha conhecida.

Para testar o checkout da ferramenta, mantenha um checkout irmão de
`emcia-artefatos` na tag `metodo-v1.0`; os testes conferem também os templates
canônicos usados pela habilitação contra os hashes do APR-01.

## 2. Conectar o Tally

No terminal:

```bash
claude mcp add tally --transport http --scope user https://api.tally.so/mcp
```

Conclua a autenticação do conector. A orientação e o endpoint estão na
[documentação oficial do Tally](https://tally.so/help/mcp).
Não grave credenciais, tokens ou respostas de clientes neste repositório.

## 3. Confirmar os conectores Google

Abra `/mcp` e confirme Google Drive e Google Calendar, com as contas EMCIA.
Consulte a [documentação dos conectores Google no Claude](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors).
O comando lê nomes completos e parâmetros disponíveis; uma ferramenta desconhecida
ou sem parâmetro restritivo fica recusada. Conector presente sem operações necessárias
não basta: o diagnóstico informa as ferramentas sem perfil e a correção necessária.
Não substitua leitura por id por busca global nem afrouxe expressões de escopo.

## 4. Rodar o bloco inicial

```text
/eiac-campo:iniciar
```

A primeira execução verifica ambiente e prepara `~/.emcia/config.json` com:
responsável nominal, base local de casos, base local de expedientes, id do workspace
Tally, id da pasta raiz Drive, id do calendário e navegador. O agente obtém ids pelos
MCPs quando possível e pergunta somente o que faltar. As bases ficam fora de
repositórios da ferramenta e do método. A configuração é privada e reutilizada.

Confira uma vez o perfil de escopo mostrado. O perfil gerado é determinístico;
o inventário e sua aprovação ficam preservados. Nome e assinatura incompatíveis
permanecem recusados. Não edite estado, expediente ou perfil com Write/Edit direto.

Sem revisão jurídica aprovada para os hashes das minutas, a primeira execução pede
**“uso as minutas sem ratificação jurídica”**. Essa aceitação nominal e datada é
revogável. Sem revisão aprovada ou aceitação ativa, a geração recusa. Revisão aprovada
prevalece para o hash coberto. Parecer condicionado não é registrado como aprovado.
A situação jurídica fica no expediente e no checklist, nunca no documento do cliente.

O percurso sem retrabalho reúne cinco aprovações: envio do formulário/plano de
rodadas; carta; três PDFs/plano de assinatura; abertura com a árvore inteira; conjunto
de compartilhamentos com destinatário, pasta e papel. Não existe efeito externo sem
aprovação. Alterações de conteúdo ou destino exigem nova conferência. Indique os PDFs
assinados e evidências quando devolvidos; a sessão aguarda esse retorno sem inventá-lo.

A sequência local é abertura → planejar/provisionar → definir (ou `--canais`) →
importar → validar `00-habilitacao` → selar → conferir F0 liberado.
A aprovação de abertura inclui uma aprovação da árvore inteira; a aprovação de
compartilhamentos é separada. Trabalho-interno não é compartilhado com o cliente.

## 5. Retomar e conferir

Execute `/eiac-campo:iniciar HAB-0001 caso-0001` após interrupção. A sessão consulta
expediente e caso e continua pela saída ausente. Retorno MCP perdido exige conferir
objeto remoto por id antes de repetir criação, publicação ou compartilhamento.

O relatório também pode ser executado no terminal:

```bash
python3 /caminho/eiac-campo/scripts/saida_inicial.py \
  --expediente /base/expedientes/HAB-0001 --caso /base/casos/caso-0001
```

Cada item sai como presente ou ausente. Saída 0 exige todos os itens bloqueantes;
“Minutas sem ratificação jurídica” é pendência não bloqueante. O selo precisa estar
confirmado no Git e conter `00-habilitacao`; um evento sem commit não basta.

F0 liberado para execução não é encerrado. Apuração de nível, sessão e decisão de
prosseguimento continuam no terminal humano, assim como restrições, autonomia,
recalibragem, encerramentos EX3/EX4 e selo após P2. A aprovação no chat não libera
essas decisões pela sessão.

## Alternativa manual

As interfaces completas e JSON de entrada estão em
[reference/habilitacao.md](eiac-campo/reference/habilitacao.md) e
[reference/canais.md](eiac-campo/reference/canais.md). O engenheiro pode executar
os scripts administrativos diretamente no terminal; as conferências de conteúdo,
assinatura, integridade, origem e situação jurídica permanecem. Casos anteriores
continuam seguindo seu próprio playbook.

Aprovação e assinatura registradas são testemunhos, sem autenticação. O ambiente
local e os hooks do runtime são a fronteira de confiança; a suíte sintética não
comprova permissões remotas reais nem suporte universal dos conectores.

Instrumento de contexto:
[EMCIA-CTX-01](eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md).
Use essa referência controlada ao conferir termos, regras e fontes.
