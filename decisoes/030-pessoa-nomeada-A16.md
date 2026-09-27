# 030 — Pessoa nomeada sem termos coletivos (A16)

**Data:** 27/09/2026 · **Estado:** firme por instrução do usuário

## Contexto

A comparação do valor inteiro recusava equipe, mas aceitava equipe de TI.
O teste 2.6.5-T09b registrava a lacuna na gravação. 029 já registra A15.

## Decisão

O playbook declara `pessoa_nomeada`: mínimo de duas partes de nome e lista
lexical de termos coletivos, incluindo siglas, plurais e equivalentes em
inglês. O núcleo normaliza caixa e acentos, separa palavras e recusa qualquer
palavra presente na lista. Valores e lista pertencem ao campo, não ao código.
Identificadores de agentes continuam recusados onde se exige pessoa.

A mesma função serve à abertura, autores do avanço/sessão/campos/recorrência,
autoria de asserções, curadoria e histórico, responsável fixo do selo,
esforço e campos nominais dos seis scripts de registro do campo. O playbook
lista os campos pessoais da curadoria em `campos_pessoa`; o produto de P10
declara `pessoas: [responsavel]` para conferir a mesma regra ao encerrar.
Ciclos de preparação do agente mantêm sua autoria própria; só a decisão
exige pessoa. O mecanismo lexical não comprova identidade civil ou origem:
a barreira de origem continua sendo a guarda da decisão 027/029.

Habilitação é anterior ao caso: lê explicitamente a regra do template na
abertura e copia-a ao expediente externo; operações seguintes usam essa
cópia. Expedientes anteriores sem a regra usam o template de habilitação.
Casos abertos nunca consultam o playbook do plugin como alternativa.

## Verificação

`testes/pessoa_a16.py`: coletivos compostos, primeiro nome isolado, nome
válido, regra alternativa do caso e registros pelos scripts reais.
2.6.5-T09b passa a exigir recusa já na gravação, sem arquivo criado.
Nomes incompletos de fixtures anteriores ganham sobrenome; nenhuma trava
anterior é retirada para acomodar a nova checagem.
