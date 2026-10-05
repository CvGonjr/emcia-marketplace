"""Expedientes exclusivamente sintéticos, construídos pelas operações reais.

O renderizador é substituído somente nesta fixture por um PDF de controle;
nenhuma guarda, assinatura ou condição de passagem é desativada.
"""
import importlib.util
import json
import pathlib
import hashlib
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

RAIZ = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('expediente_sintetico', RAIZ/'eiac-campo/scripts/habilitacao.py')
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)


def criar(root, caso, responsavel, acessos=True, assinaturas=True, restricao=False):
    root = pathlib.Path(root)
    H.iniciar(root, 'HAB-CONTROLE', responsavel, caso)
    with tempfile.TemporaryDirectory(prefix='emcia-insumos-sinteticos-') as tmp:
        insumos = pathlib.Path(tmp)
        origem = insumos/'declaracao.json'
        origem.write_text('{"tipo":"controle exclusivamente sintético"}')
        def op(nome, **dados):
            return H.executar(root, nome, dados)
        op('receber', id='S1', arquivo=str(origem), formulario='FORM-SINTETICO',
           submissao='SUB-SINTETICA', respondente='Pessoa Patrocinadora',
           versao_perguntas='controle-1', rodada=0, escopo='administrativo')
        templates = insumos/'templates'
        shutil.copytree(RAIZ/'testes/apoio/templates-hab-v1', templates)
        campos = {k: {'valor': 'Controle sintético '+k, 'fonte': 'S1'}
                  for filename in H.TEMPLATES.values() for k in H.TOKEN.findall((templates/filename).read_text())}
        campos['organizacao']['valor'] = 'Organização Sintética'
        campos['signatario']['valor'] = 'Pessoa Patrocinadora'
        op('consolidar', campos=campos)
        op('revisar', decisor=responsavel, motivo='Revisão exclusivamente sintética',
           qualificacao_0a=True, conteudo_conferido=True, evidencia=str(origem))
        op('revisao-juridica', revisor='Pessoa Jurista', decisor=responsavel, data='2026-10-04',
           resultado='aprovado',
           documentos={doc: hashlib.sha256((templates/H.TEMPLATES[doc]).read_bytes()).hexdigest()
                       for doc in ('HAB-02', 'HAB-03')}, evidencia=str(origem))
        with patch.object(H, 'pdf_bytes', return_value=b'%PDF-1.7\ncontrole sintetico\n%%EOF'):
            op('gerar', templates=str(templates))
        if assinaturas:
            pdf = insumos/'assinado.pdf'
            pdf.write_bytes(b'%PDF-1.7\nassinatura exclusivamente sintetica\n%%EOF')
            for doc in H.TEMPLATES:
                signers = [{'nome':'Pessoa Patrocinadora','papel':'organizacao','competencia':'Controle sintético'},
                           {'nome':responsavel,'papel':'emcia','competencia':'Controle sintético'}]
                op('liberar', documento=doc, versao=1, decisor=responsavel, pdf_conferido=True,
                   ferramenta='Painel sintético', operador=responsavel, signatarios=signers)
                op('assinatura', documento=doc, versao=1, decisor=responsavel,
                   conteudo_conferido=True, evidencias_conferidas=True, arquivo=str(pdf),
                   evidencia=str(origem), referencia='Controle sintético',
                   signatarios=[dict(nome=s['nome'],papel=s['papel'],data='2026-10-02') for s in signers])
            op('concluir-0b')
        if acessos and assinaturas:
            itens=[{'item':'Fonte sintética A','status':'concedido','evidencia':'Conferência sintética'}]
            if restricao:
                itens.append({'item':'Fonte sintética B','status':'negado','evidencia':'Declaração sintética',
                              'motivo':'Amostra indisponível','restricao':'Sem verificação dessa fonte'})
            op('acessos', patrocinador='Pessoa Patrocinadora', executor='Pessoa Executora',
               decisor=responsavel, autoridade_patrocinador='Controle sintético',
               executor_liberado=True, agenda_reservada=True, data_sessao='2026-10-15', itens=itens)
            op('preparar-0d')
    return root


def preparar(caso):
    """Importa, valida e sela uma fixture de caso antes do percurso."""
    caso=pathlib.Path(caso).resolve()
    st=json.loads((caso/'registro/estado.json').read_text())
    from apoio.canais import definir
    definir(caso)
    if (caso/'registro/habilitacao.json').exists():
        return
    with tempfile.TemporaryDirectory(prefix='emcia-expediente-fixture-') as tmp:
        root=criar(pathlib.Path(tmp)/'expediente', st['caso'], st['responsavel'])
        def rodar(*args):
            r=subprocess.run(args, cwd=caso, text=True, capture_output=True)
            if r.returncode: raise RuntimeError(r.stderr or r.stdout)
        if not (caso/'.git').exists(): rodar('git','init','-q')
        rodar('git','config','user.name',st['responsavel'])
        rodar('git','config','user.email','sintetico@example.invalid')
        rodar(sys.executable,str(RAIZ/'eiac-campo/scripts/importar_habilitacao.py'),'--expediente',str(root))
        rodar(sys.executable,str(RAIZ/'eiac-nucleo/scripts/validar.py'),'--arquivo','caso/00-habilitacao.md')
        rodar(sys.executable,str(RAIZ/'eiac-nucleo/scripts/selar.py'),'--nota','habilitação sintética importada e conferida')
