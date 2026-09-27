# 027 — Decisão humana fora da sessão do agente (A12)

**Data:** 26/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

A verificação de F3 mostrou que o agente podia informar um nome humano em
--ator/--autor e executar uma decisão pela sessão. O argumento lexical
não distingue origem humana de origem agente. Base: v-sprint3-poc.3.

Foram lidos CLAUDE.md, índice e decisões 003, 019 e 022–025. O número 026
já registra A10 e permanece preservado. A12 recebe 027, próximo livre.

## Decisão

- Toda chamada à guarda tem origem na sessão do agente, qualquer que seja
  o nome informado. Operações humanas declaradas no playbook são negadas
  por ela e executadas pelo engenheiro no próprio terminal, fora da sessão
  do Claude Code, no diretório do caso.
- O campo declara `decisoes_humanas`: script, argumento e condição. Condições
  são incondicional, campo do rascunho ou camada da etapa alvo no nível
  apurado. O núcleo não cita script de método, etapa ou categoria de decisão
  no novo avaliador; lê o contrato do caso.
- A lista cobre governança decidida, operacional validado, recalibragem com
  decisão, apuração, sessão, campos, recorrência, satisfação de inegociáveis
  e encerramento em EX3/EX4. Inclui o wrapper de satisfação do campo e o
  auxiliar automático de controle, pois chamam operações humanas.
- A recusa gera TentativaNegada com operação, comando e responsável nominal;
  informa que a decisão é executada pelo engenheiro no próprio terminal e
  entrega o comando exato. O estado não muda por essa tentativa.
- Preparação continua permitida: rascunho/proposto, proposta, recomendação
  sem decisão, leitura, validação de asserções, curadoria e emissão.
- Ausência/ilegitimidade do contrato não desativa a guarda. Candidato ausente,
  ilegível ou fora do caso recusa. Comandos compostos condicionados por
  arquivo recusam porque podem mudar o rascunho após sua inspeção. Preparação
  usa chamadas simples. Reconhecimento não executa o shell.

## Revisão da decisão 019

A regra de autoria fixa dos componentes validar/curar/selar permanece.
A exceção que permitia ao agente informar --ator para executar decisões de
método é substituída: o engenheiro executa essas operações no próprio
terminal. O ator pode continuar como dado do comando humano; seu nome não
é credencial que autorize o agente. A 019 recebeu marca de revisão,
preservando seu texto histórico. A 003 continua vigente.

## Consequência

Núcleo 0.2.26, campo 0.8.4, playbook 0.4.7. Casos existentes atualizam
explicitamente sua lista; nunca leem o playbook do plugin como substituto.
Nenhum sinalizador desativa a guarda e não foi adicionada dependência.

Comandos e habilidades entregam ao engenheiro o comando pronto. Os scripts
no terminal mantêm validações de conteúdo, nome, sessão, selo e portões;
esta decisão não cria autenticação de identidade no sistema operacional.

Os auxiliares `.projectdocs/demos/como-agente.sh` e `preparar-caso.sh` servem
à demonstração por caso sintético. O primeiro apenas consulta a guarda; o
segundo é executado pelo engenheiro no terminal e prepara o percurso.

Testes negativos precederam a correção. Nenhum teste anterior foi removido.
Evidências: `.projectdocs/evidencias/sprint3/3.5/correcao-A12/`.
Tag da entrega: v-sprint3-poc.4.

## Ampliação posterior

A decisão 029 (A15) acrescenta revisão do piloto e definição da rotina à
lista humana. A permissão de preparação da rotina descrita nesta decisão
passa a se limitar ao rascunho: a gravação da rotina é feita no terminal.
Ciclos sem decisão continuam permitidos à sessão. A decisão 030 (A16)
substitui as comparações lexicais locais pela regra do playbook.
