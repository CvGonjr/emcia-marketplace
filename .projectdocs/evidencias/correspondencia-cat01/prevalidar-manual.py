"""Reproduz a divergência documental sem alterar o contrato do caso."""

import copy
import importlib.util
import json
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True
RAIZ = pathlib.Path(__file__).resolve().parents[3]
CANONICO = RAIZ.parent / 'emcia-artefatos'
COMMIT = '2cf4ebd913b7a4de2ca7f5a2322a991bc69c1cbe'
manual = subprocess.check_output(
    ['git', 'show', COMMIT + ':EMCIA-MAN-01-manual-de-aplicacao.md'],
    cwd=CANONICO, text=True,
)
spec = importlib.util.spec_from_file_location('manual_a25', RAIZ / 'testes/manual_a25.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
pb = json.loads(subprocess.check_output([
    'git', 'show', 'ebb6bbda55ea7403bc0e09a0bc316f0a1071cf4f:eiac-campo/template-caso/registro/playbook.json',
], cwd=RAIZ, text=True))
linhas = m.ler_tabela(manual)


def conferir(contrato):
    return m.conferir(linhas, contrato, m.comandos_de_etapa(), m.atos_transversais(manual))


resultado = {
    'commit_canonico': COMMIT,
    'linha_F0_canonica': linhas[0],
    'playbook_atual': conferir(pb),
}
contrato = copy.deepcopy(pb)
contrato['decisoes_humanas'].append({
    'id': 'decidir-prosseguimento',
    'script': 'prosseguimento.py',
    'condicao': {'tipo': 'sempre'},
})
resultado['somente_ato_declarado'] = conferir(contrato)
f0 = next(etapa for etapa in contrato['etapas'] if etapa['id'] == 'F0')
f0['produtos_encerramento'] = [{
    'tipo': 'arquivo',
    'padrao': 'registro/prosseguimento/*.yaml',
    'iguais': {'desfecho': 'prosseguir'},
    'preenchidos': ['decisor', 'data', 'motivo'],
    'pessoas': ['decisor'],
    'descricao': 'Decisão de prosseguir registrada',
}]
resultado['ato_e_produto_exigidos_pelo_pedido'] = conferir(contrato)
resultado['nota'] = (
    'Contrato candidato somente em memória, para verificar a compatibilidade '
    'documental antes da implementação. Nenhum playbook foi alterado.'
)
assert resultado['playbook_atual'] == ['F0: ato decidir-prosseguimento não declarado']
assert resultado['somente_ato_declarado'] == []
assert resultado['ato_e_produto_exigidos_pelo_pedido'] == [
    'F0: produto diferente da descrição do playbook',
]
print(json.dumps(resultado, ensure_ascii=False, indent=2))
