# 011 — Testes negativos antes do caminho feliz

**Data:** setembro de 2026 · **Estado:** firme

## Contexto

Neste produto, o comportamento de recusa **é** a funcionalidade. Um teste que verifica que a guarda funciona é fraco; um teste que quebra quando a guarda é removida é forte.

## Decisão

As três primeiras fatias de construção são negativas: camada negada, asserção recusada, etapa bloqueada.

A suíte tem treze testes. Doze provam que algo recusa. O quarto é controle positivo — asserção bem marcada precisa gravar, senão o validador está apenas quebrado.

Rodam no CI a cada push. **Falha é regressão de trava: conserte a trava, não o teste.**

## Consequência

O CI acumula histórico de que as travas operavam em cada versão. Isso é evidência de sprint que se produz sozinha.

O CI também recusa mudança nos scripts do núcleo sem que a versão do plugin suba — com o playbook sendo o método, versão de plugin e versão de método são a mesma coisa.
