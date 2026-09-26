# 026 — Campos da etapa declarados e registrados pelo núcleo (A10)

**Data:** 26/09/2026 · **Estado:** firme quanto à correção solicitada

## Contexto

O renderizador de E3 e sua condição de emissão liam a classificação de P5,
mas nenhum comando a registrava. Testes injetavam o campo em estado.json.
A10 fecha esse caminho ausente sobre a versão v-sprint3-poc.2, junto com A9.
A decisão 024 permanece como A8; 025 registra A9 e 026 registra A10.

## Decisão

- Etapas declaram `campos_registraveis`: mapa de nomes para regras. Uma
  regra pode declarar `valores`, lista de textos exatos aceitos; sem
  taxonomia, aceita texto não vazio. Campos internos da máquina são
  reservados e não podem ser declarados para escrita por esse mecanismo.
- `avancar.py --registrar-campo <etapa> --campo <nome> --valor <valor>
  --autor <pessoa>` e `/eiac-nucleo:registrar-campo` conferem etapa corrente
  ainda aberta, campo declarado, valor e autoria nominal.
- O registro produz `CampoRegistrado` com etapa, campo, valor, valor
  anterior e autor. Cada recusa produz `TentativaNegada`, sem alterar
  estado. Tentativa de agente é atribuída ao responsável nominal do caso.
- O campo declara em P5 `classificacao_tecnologica` com `agente`,
  `caso isolado` e `habilitador acoplado`, conforme passo 5 (§3.4.5) do
  EMCIA-MET-01. A habilidade instrui registrar a conclusão confirmada
  antes de encerrar P5. A justificativa escrita permanece no artefato.
- Nomes da classificação, valores e etapa pertencem ao playbook de campo;
  o código do núcleo aplica contrato genérico.

## Auditoria

Todos os campos lidos por entregaveis.py foram conferidos. Somente
`cumprimentos.P5.classificacao_tecnologica` não tinha caminho de registro.
`caso` vem da abertura, `nivel` e eixos de apuração, `cumprido`/autor do
encerramento. E2, E4 e E5 usam arquivos estruturados com comandos de
baseline, operacional, governança, piloto, métrica e calibragem.
A tabela completa de campos e comandos está no resultado da evidência.
Não se criam espelhos desses artefatos em estado.json.

A fonte canônica local e a cópia empacotada do MET-01 foram conferidas e
são idênticas. O documento conserva seu estado “Em revisão”, aprovação
pendente. A taxonomia é aplicada por instrução expressa desta correção;
essa implementação não declara aprovação integral do documento.

## Consequência

Núcleo 0.2.25, campo 0.8.3 e playbook 0.4.6. Casos existentes precisam
atualizar explicitamente suas declarações. As recusas, inclusive contrato
inválido, têm trilha; campo ausente não ganha valor presumido.

Os testes negativos precederam a implementação. Fixtures de classificação
passam pelo comando, sessão e encerramento reais. Um teste ponta a ponta
abre caso com novo-caso.sh e materializa E3 Partes A/B sem escrita direta
no estado pelo teste. O escopo é o caminho de registro e emissão, não a
ampliação do conteúdo do renderizador de E3.

Evidências: `.projectdocs/evidencias/sprint3/3.4/correcao-A9-A10/`.
A entrega conjunta recebe a tag anotada v-sprint3-poc.3.
