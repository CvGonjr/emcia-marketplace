# 041 — Restrição vinculada à fonte do contexto

**Data:** 03/10/2026 · **Estado:** aprovada pelo pedido da parte A · **Completa:** 039, pacote D

## Contexto

EMCIA-HAB-01 §3.4 exige que a restrição acompanhe o item afetado, no ponto
em que aparece no entregável, sem ressalva genérica. O pedido identifica
esse item como o objeto Fonte F-xxx do EMCIA-CTX-01 §3.7. A 039 preservou
esse trabalho até existir contrato explícito de destino.

## Decisão

O engenheiro vincula cada RH importado a uma ou mais fontes curadas em P2,
ou registra dispensa motivada quando nenhuma fonte é afetada. Os atos são
reservados ao terminal humano pela regra `vincular-restricao` da guarda.
O autor vem do responsável fixado no caso; nenhuma identidade de agente
é admitida. Recusas produzem TentativaNegada e a guarda devolve o comando.

`registro/restricoes.json` contém vigentes e histórico, com importação,
versão, autoria e data. Revisão exige decisão que identifique RH e versão
anterior, com pessoa nomeada, motivo e data. Fora de P2 só cabe revisão de
vínculo existente após P2 encerrada; nunca nova vinculação inicial tardia.

P2 declara produto genérico de cobertura entre duas coleções de registros.
Todo id da origem tem registro no destino com um dos estados declarados.
Origem e destino devem conferir com hashes dos eventos declarados. Origem
vazia satisfaz sem exigir registro de destino. O núcleo desconhece o domínio
administrativo, seus ids e estados; lê apenas o contrato do playbook.

Os artefatos materializados declaram fontes do registro ou fontes por campo.
Cada valor que depende de fonte restrita recebe marca com RH, F, item negado,
restrição e motivo. REC pode resolver por `recebimentos` explicitamente
registrado no objeto F curado; o recebimento e os bytes precisam conferir.
Relação ausente recusa nomeando a asserção. Nenhum vínculo é inferido de
nomes ou texto livre. RH pendente bloqueia a materialização antes da escrita.

## Consequência

A limitação parcial de 039 é substituída por vínculo explícito. E1 de caso
restrito fica pendente até resolver RH em P2; a demonstração o emite depois
desse ato. Não existe dispensa automática nem seção final de ressalvas.
A regra não cria uma fonte verificada para item cujo acesso foi negado.

Núcleo 0.2.44, campo 0.8.21, playbook 0.4.18. O MAN-01 v0.1 empacotado
permanece intacto; a emenda local `reference/manual-emenda-041.json` declara
somente as mudanças de P2 para conferência da parte A. A conferência preserva
a detecção das duas divergências no manual base, e exige que a emenda coincida
com o playbook. A proposta do MAN-01 v0.2 está na evidência, não é uma edição
ou aprovação automática de documento canônico.

Evidência: `.projectdocs/evidencias/parte-a-operacional/A3/`.
