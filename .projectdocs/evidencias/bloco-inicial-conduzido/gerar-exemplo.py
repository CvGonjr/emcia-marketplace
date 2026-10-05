"""Emissão sintética com Chrome real e aceitação explícita, sem serviços externos."""
import importlib.util
import json
import pathlib
import subprocess

BASE=pathlib.Path(__file__).resolve().parent
RAIZ=BASE.parents[2]
spec=importlib.util.spec_from_file_location('teste_hab',RAIZ/'testes/habilitacao.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
t=M.Habilitacao('test_41_aceitacao_sem_ratificacao_libera_e_fica_interna');t.setUp()
try:
    t.prepare(gerar=False,juridica=False);cfg=t.aceitacao()
    t.run_action('gerar',templates=str(t.templates),navegador='google-chrome',config_emcia=str(cfg))
    pasta=BASE/'exemplo-sintetico';pasta.mkdir(exist_ok=True)
    s=t.state();reg={}
    for doc in M.H.CODIGOS_HAB:
        v=s['documentos'][doc][-1]
        for campo,sufixo in [('markdown','.md'),('pdf','.pdf')]:
            p=pasta/(doc+sufixo);p.write_bytes(M.H.ler_arquivo(t.root,v[campo]))
        subprocess.run(['pdftotext',str(pasta/(doc+'.pdf')),str(pasta/(doc+'.txt'))],check=True)
        texto=(pasta/(doc+'.txt')).read_text()
        for proibido in ('Controle do modelo','Revisão jurídica','ratificação','aceitacao_minutas'):
            assert proibido not in texto,(doc,proibido)
        assert 'Para assinatura' in texto,doc
        reg[doc]={k:v[k] for k in ('minuta','situacao_juridica')}
        reg[doc]['markdown_sha256']=v['markdown']['sha256'];reg[doc]['pdf_sha256']=v['pdf']['sha256']
    (pasta/'emissoes.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    print('Três PDFs reais Chrome conferidos por pdftotext; aceitação exclusivamente sintética; nenhuma marca interna no cliente.')
finally:t.doCleanups()
