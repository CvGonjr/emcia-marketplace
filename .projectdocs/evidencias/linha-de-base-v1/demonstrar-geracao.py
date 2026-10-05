"""Demonstração antes/depois com Chrome; nenhuma pessoa ou revisão real."""
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import types

RAIZ = pathlib.Path(__file__).resolve().parents[3]
SAIDA = pathlib.Path(__file__).resolve().parent / 'exemplo-sintetico'
BASE = 'd9551a90b5ee3cec5006bbbfcbdebca4cbfe0f35'
spec = importlib.util.spec_from_file_location('teste_demo_hab', RAIZ / 'testes/habilitacao.py')
testes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(testes)
atual = testes.H
antigo = types.ModuleType('habilitacao_antes')
antigo.__file__ = str(RAIZ / 'eiac-campo/scripts/habilitacao.py')
fonte = subprocess.check_output(['git', 'show', BASE + ':eiac-campo/scripts/habilitacao.py'], cwd=RAIZ)
exec(compile(fonte, antigo.__file__, 'exec'), antigo.__dict__)
SAIDA.mkdir(exist_ok=True)
resumo = {}
for rotulo, implementacao in (('antes', antigo), ('depois', atual)):
    testes.H = implementacao
    t = testes.Habilitacao()
    t.setUp()
    try:
        t.prepare(gerar=False, juridica=rotulo == 'depois')
        t.run_action('gerar', templates=str(t.templates), navegador='google-chrome')
        for doc in implementacao.TEMPLATES:
            if rotulo == 'antes' and doc != 'HAB-02':
                continue
            v = t.state()['documentos'][doc][-1]
            for campo, sufixo in (('markdown', 'md'), ('pdf', 'pdf')):
                (SAIDA / f'{doc}-{rotulo}.{sufixo}').write_bytes(implementacao.ler_arquivo(t.root, v[campo]))
            subprocess.run(['pdftotext', '-layout', str(SAIDA / f'{doc}-{rotulo}.pdf'),
                            str(SAIDA / f'{doc}-{rotulo}.txt')], check=True)
            extraido = (SAIDA / f'{doc}-{rotulo}.txt').read_text()
            if rotulo == 'depois':
                assert 'Para assinatura' in extraido
                assert all(x not in extraido for x in ('Controle do modelo', 'Revisão jurídica',
                                                       'Histórico de revisões do modelo', 'Celso do Vale'))
                resumo[doc] = {k: v[k]['sha256'] for k in ('template', 'markdown', 'pdf')}
                resumo[doc]['revisao_juridica'] = v['revisao_juridica']
            else:
                assert 'Controle do modelo' in extraido and 'Revisão jurídica' in extraido
                assert 'Para assinatura' not in extraido
        if rotulo == 'depois':
            (SAIDA / 'revisao-juridica-sintetica.json').write_bytes((t.base / 'S1.json').read_bytes())
    finally:
        t.doCleanups()
(SAIDA / 'hashes-e-revisao-sintetica.json').write_text(json.dumps(resumo, ensure_ascii=False, indent=2) + '\n')
print('MD/PDF antes e depois conferidos; documentos, pessoas e revisão jurídica exclusivamente sintéticos.')
