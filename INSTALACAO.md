# Instalação — marketplace emcia

Use Python 3.12 ou superior no PATH, Git e Claude Code. Para PDFs da habilitação,
instale Google Chrome ou Chromium. Nenhuma biblioteca Python externa é
obrigatória; o leitor YAML funciona sem PyYAML.

## 1. Instalar os dois plugins

No Claude Code:

```text
/plugin marketplace add CvGonjr/emcia-marketplace
/plugin install eiac-nucleo@emcia
/plugin install eiac-campo@emcia
```

Reinicie a sessão e confira os plugins e comandos. A revisão operacional usa
núcleo 0.2.44, campo 0.8.22, playbook 0.4.18 e manifesto v4. Para trabalhar pelo
checkout local:

```bash
git clone https://github.com/CvGonjr/emcia-marketplace.git
cd emcia-marketplace
python3 --version
python3 testes/metodo_empacotado.py
```

O teste confere os hashes; com o checkout irmão de emcia-artefatos disponível,
compara também os bytes ao objeto Git do commit canônico fixado no manifesto.
O pacote instalado funciona offline. Documentos em revisão continuam com sua
aprovação pendente.

## 2. Configurar os conectores

Configure no Claude Code os conectores MCP de Tally, Google Drive e Google
Calendar, com credenciais e acessos do engenheiro. Confira na interface MCP
as ferramentas carregadas, seus nomes e seus argumentos efetivos antes de
preparar a declaração do caso. A instalação dos plugins não instala nem
configura esses conectores.

Tally usa workspace e formulário por id; Drive usa drive e pasta por id;
Calendar usa calendário por id e marcador `[caso/etapa]`. Não procure canais
pelo nome da organização. Ajuste `registro/ferramentas-externas.json` no terminal
às assinaturas do conector instalado, mantendo ids e escopo restritos.

A evidência E7 demonstrou chamada real e hook PreToolUse numa ferramenta MCP
stdio sintética, usando **Claude Code 2.1.283**. Essa é a versão testada;
não constitui demonstração de hooks em outros clientes ou versões. Confira
`.projectdocs/evidencias/canais-externos/pacote-E7/` e a decisão 040.
Cada efeito externo e cada compartilhamento exige confirmação explícita no chat.

## 3. Habilitar e abrir

Leia [MAN-01 §3.2](eiac-campo/reference/metodo/EMCIA-MAN-01-manual-de-aplicacao.md),
[CAN-01](eiac-campo/reference/metodo/EMCIA-CAN-01-protocolo-de-canais-externos.md) e
[ROT-02](eiac-campo/reference/metodo/EMCIA-ROT-02-roteiro-de-habilitacao.md).
Consulte [reference/habilitacao.md](eiac-campo/reference/habilitacao.md) para
as operações e os campos JSON do expediente. Os templates HAB-01/02/03 são
lidos de `auxiliares/` do checkout canônico, preservados com hash e revisados
humanamente antes da liberação dos PDFs. A assinatura ocorre pelo painel externo.

Inicialize o expediente no terminal, antes da sessão, fora de repositórios:

```bash
python3 eiac-campo/scripts/habilitacao.py iniciar --expediente /base/habilitacoes/HAB-0001 --id HAB-0001 --caso caso-0001 --responsavel "Nome Sobrenome"
```

Depois da formalização e dos acessos, abra no terminal:

```bash
./novo-caso.sh caso-0001 /base/casos --responsavel "Nome Sobrenome" --expediente /base/habilitacoes/HAB-0001
cd /base/casos/caso-0001
```

`--expediente` é opcional na abertura e não importa material. A base opcional
não pode estar dentro de Git; o destino precisa ser novo. O responsável precisa
ser pessoa nomeada. A abertura confere SHA-256, copia o pacote para `metodo/` e
prepara o commit inicial; se esse commit falhar, configure Git e registre-o.

## 4. Definir canais, importar, gravar e selar

Em caso aberto, planeje e provisione os canais com `/eiac-campo:canais`.
Provisionar pelo MCP exige declaração prévia de contêiner exclusivo do caso;
sem ela, use a interface externa e depois declare os ids. O engenheiro executa:

```bash
python3 /checkout/emcia-marketplace/eiac-campo/scripts/canais.py planejar
python3 /checkout/emcia-marketplace/eiac-campo/scripts/canais.py definir --entrada rascunho/canais.json
python3 /checkout/emcia-marketplace/eiac-campo/scripts/importar_habilitacao.py --expediente /base/habilitacoes/HAB-0001
python3 /checkout/emcia-marketplace/eiac-nucleo/scripts/validar.py --arquivo caso/00-habilitacao.md
python3 /checkout/emcia-marketplace/eiac-nucleo/scripts/selar.py --nota "habilitação importada e conferida"
```

Prepare antes uma declaração completa conforme
[reference/canais.md](eiac-campo/reference/canais.md). Como alternativa a definir
antes, passe `--canais rascunho/canais.json` à importação. A ordem é abertura →
planejar/provisionar → definir (ou `--canais`) → importar → gravar → selar → F0.
Sem canais coerentes, importação recusa. Sem selo confirmado no histórico Git
contendo a importação, F0 permanece bloqueado.

Abra a sessão na raiz do caso. `CLAUDE_PROJECT_DIR` identifica essa raiz para
os hooks; execute os scripts de operação nela. `/eiac-nucleo:estado` mostra a
etapa, camada, referência do método e último selo confirmado. O estado
corrente F0, sozinho, não significa que suas condições de entrada foram satisfeitas.

## 5. Conferir as recusas

Em um caso sintético, verifique que escrita direta em `caso/`, `contexto/`,
`registro/` e `fontes/` produz negativa e evento. Conteúdo começa em `rascunho/`
e segue validação, curadoria ou recebimento. A referência do contexto é somente
[EMCIA-CTX-01](eiac-campo/reference/metodo/EMCIA-CTX-01-instrumento-de-registro-da-camada-de-contexto.md).

Tente importar ou definir canais pela sessão: a guarda deve recusar e devolver
o comando para o terminal humano. Teste uma ferramenta MCP não declarada ou
com id fora do caso: a guarda deve recusar antes da chamada. Teste asserção
sem D/I/V: o validador deve recusar. Com P3b corrente, selo ausente ou deixado
por commit recusado não pode liberar encerramento; a habilidade continua
não delegável mesmo com selo e sessão humana.

Para regressão determinística no checkout, use Python 3.12 e rode os módulos
indicados em [testes/README.md](testes/README.md). As suítes incluem controles
positivos e negativos, sem dados de cliente. O executador completo e as saídas
estão em `.projectdocs/evidencias/documentacao-operacional/`.

## 6. Operar e atualizar

Recebimento e entrega são registrados no terminal por `receber.py` e `entregar.py`.
Listagem registrada precede leitura MCP por id. Em P2, todo RH é vinculado a fonte
curada ou dispensado com motivo por `restricoes.py` (`vincular-restricao`).
Depois do último encerramento de P2, sele antes de P3b. Não copie arquivos
manualmente para `fontes/` nem escreva registros pelo chat.

Os scripts conferem coerência local e hashes; não autenticam pessoas, origem
remota ou permissões efetivas. Acesso humano de escrita ao disco é a fronteira
de confiança. Confirmação no chat não substitui os atos humanos do terminal.
Assinatura eletrônica integrada, aceite, gravação e transcrição ficam fora
do escopo aprovado.

Atualize o marketplace pela interface de plugins e reinicie a sessão. Casos
existentes conservam seus contratos; a migração é humana e explícita.
Não substitua o playbook do caso por leitura do plugin.

| Sintoma | Conferência |
|---|---|
| Comandos ausentes | Instalação dos dois plugins e reinício da sessão |
| MCP ausente | Configuração e credenciais dos conectores no Claude Code |
| Importação recusa canais ausentes | Definição prévia ou `--canais` completo |
| F0 bloqueado | Importação, gravação e selo confirmado no Git |
| P2 não encerra | RH vinculados ou dispensados; hashes e fontes curadas |
| P3b bloqueado | Sessão exigida e selo confirmado após o último encerramento de P2 |
| PDF não é gerado | Chrome/Chromium, campos dos templates e revisão humana |
| Hash do método divergente | Pacote e manifesto preservados, sem edição manual |
| Hook não dispara | Runtime e instalação; repetir as provas no ambiente efetivo |
