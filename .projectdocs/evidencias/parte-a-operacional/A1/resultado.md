# A1 — abertura e regressão descoberta

Base 88ac1f4; Python CPython 3.12.12, sem PyYAML (dependência opcional).
A falha de argparse informada não se reproduziu nessa revisão 3.12;
o teste adicional antes da mudança passou nas duas ordens. Foi adotado
`parse_intermixed_args` para declarar explicitamente o suporte ao uso.

A suíte inicial encontrou `pessoa_a16.test_13_revisor`: o leitor mínimo
perdia a estrutura de uma lista JSON de objetos. A reprodução contra o
código original está em yaml-antes.txt. A leitura agora usa json.loads
para coleções JSON inline e mantém o leitor YAML anterior como alternativa.
Nenhum teste foi enfraquecido nem dependência adicionada.

A regressão integral após a correção passou: 893 verificações em 44 módulos.
O teste dedicado adicional do leitor, executado depois, acrescenta uma
verificação (yaml-depois.txt); o total correspondente é 894. O teste novo
foi inicialmente colocado após sys.exit; sua posição foi corrigida e a
reprodução do defeito original preservada separadamente.
Versões: campo 0.8.20, núcleo 0.2.42; playbook permanece 0.4.17 até A3.
