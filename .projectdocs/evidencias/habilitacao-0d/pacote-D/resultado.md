# Pacote D — recusa de restrição sem destino; implementação parcial

Campo 0.8.12. Sem vínculo declarado entre o item da matriz e um ponto do
entregável, o componente recusa E1–E5 antes da escrita, nomeando RH-xx e
produzindo TentativaNegada com o responsável fixado no caso. Não resolve a
correspondência por texto, nem coloca ressalva genérica ao fim. A inserção
localizada fica pendente do contrato de destinos, conforme escopo parcial
expressamente permitido na solicitação e registrado em 039.

Negativas foram executadas antes da implementação: todos os entregáveis
recusam por falta de destino e deixam evento; versão anterior não é sobrescrita.
Controle positivo preserva materialização sem restrição. A regressão completa
exercita os renderizadores e os percursos antigos, sem remover verificações.

O CI passou a executar habilitacao_0d.py. A documentação registra a limitação
operacional: a habilitação com restrição pode seguir, mas a emissão está
bloqueada enquanto falta vínculo determinístico. Não existe flag de dispensa.
Dados de demonstrações exclusivamente sintéticos. selar.py, a regra de P3b
e o pacote reference/metodo/ permanecem conforme a decisão aprovada.

Resultado final: 822 verificações em 37 módulos, todas aprovadas; o módulo
novo reúne 31 testes. A demonstração completa percorreu 13 etapas, produziu
cinco entregáveis e sete selos sem TentativaNegada, usando o HEAD congelado
do pacote C (`c8edc16`). A mudança D foi verificada pelos testes da árvore
atual; o percurso congelado não é apresentado como teste dessa alteração.
