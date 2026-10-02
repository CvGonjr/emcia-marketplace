# Canais externos — resultado da implementação

E1–E7 implementados em sete commits, com arquitetura aprovada pela solicitação
e referência TRI-01 confirmada pelo usuário. §3.3 identifica as perguntas;
§3.4 identifica a pontuação. A habilidade hb-enquadrar foi corrigida e a
comparação literal de perguntas/alternativas está na suíte de formulários.

## Verificação

894 verificações distintas em 44 módulos aprovadas: regressão integral e
complemento dos novos controles, descritos em `regressao-final/complemento.md`.
Cada árvore de pacote também passou por negativos.sh, contexto.py e testes
específicos antes do commit. O percurso sintético cobre habilitação, canais
em 0d, submissão Tally de F0, documento em P2, emissão de E1 e entrega registrada.

Teste real no Claude Code 2.1.283: MCP stdio local executado com hook acionado;
com o plugin real, ferramenta não declarada foi bloqueada antes da execução
e registrada como TentativaNegada. Evidência e programa de reprodução em E7.
O grep de vocabulário no núcleo teve saída vazia, código 1.
Nenhum documento em `eiac-campo/reference/metodo/` foi alterado.

## Limites

Não houve criação, compartilhamento, publicação, convite ou envio em ferramentas
de clientes. O provisionamento exige ids reais declarados e confirmação de
cada efeito externo. Regras MCP são dados do caso e precisam corresponder aos
nomes/argumentos do conector instalado; ferramenta não configurada recusa.
O suporte a hooks foi demonstrado no Claude Code, não em outros clientes.
Scripts verificam coerência local, sem autenticar origem, resposta ou identidade
remota. Recebimento e registro de entrega permanecem atos do terminal humano.
Não foi implementado aceite nem leitura de gravações ou transcrições.
Casos já abertos conservam seu playbook; não há atualização automática.

## Versões

- `eiac-nucleo/.claude-plugin/plugin.json`: `0.2.41`
- `eiac-campo/.claude-plugin/plugin.json`: `0.8.19`
- `eiac-campo/template-caso/registro/playbook.json`: `0.4.17`

## Demonstrações

`preparar-caso.sh canais-preparo P2` e `percurso-completo.sh canais-completo`
passaram em bases temporárias, pelo commit `266a6d1`, que já contém o código
final. A revisão posterior acrescentou apenas documentação e evidências. Saídas em `demos/`.
O contêiner inicial de provisionamento precisa ser exclusivo do caso;
um espaço compartilhado de outros casos não é canal de leitura.
