"""Relatórios sintéticos: scripts reais e retornos de fixture; nenhuma chamada MCP."""
import copy
import json
import pathlib
import shutil
import sys
import tempfile

ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'eiac-campo/scripts'))
import iniciar as I

destino=pathlib.Path(__file__).resolve().parent
resumos={}
with tempfile.TemporaryDirectory() as temp:
    base=pathlib.Path(temp);p=base/'config.json'
    I.configurar(p,dict(responsavel='Pessoa Engenheira',base_casos=str(base/'casos'),
        base_expedientes=str(base/'expedientes'),workspace_tally='WORK',pasta_drive='ROOT',
        calendario_casos='CAL',navegador='google-chrome'))
    def op(nome,literal='Aprovo o ensaio sintético',**extra):
        d=dict(habilitacao='HAB-SINTETICA',caso='CASO-SINTETICO',**extra)
        return I.operar(p,nome,d,I.aprovar(p,nome,d,literal,'Ensaio, sem conta real'))
    inv=json.loads((ROOT/'testes/apoio/inventario-mcp-real.json').read_text())
    op('perfil',ferramentas=inv,perfil=I.calibrar(inv));op('iniciar',id='HAB-SINTETICA')
    criar=dict(habilitacao='HAB-SINTETICA',caso='CASO-SINTETICO',ferramenta='mcp__tally__create_new_form',
        argumentos=dict(title='Somente sintético',workspaceId='WORK'))
    op('mcp',ferramenta=criar['ferramenta'],argumentos=criar['argumentos'])
    I.registrar_retorno(p,criar,{'ids':{'formulario_id':'FORM'}})
    original=json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())
    for nome in ('identico','texto-diferente','ordem-trocada','oculto-ausente'):
        raw=copy.deepcopy(original);b=raw['data']['blocks']
        if nome=='texto-diferente':b[0]['payload']['html']+=' reformulado'
        if nome=='ordem-trocada':b[:4]=b[2:4]+b[:2]
        if nome=='oculto-ausente':b.pop();raw['data']['blocksCount']-=1
        ler=dict(habilitacao='HAB-SINTETICA',caso='CASO-SINTETICO',ferramenta='mcp__tally__load_form',argumentos={'formId':'FORM'})
        op('mcp',ferramenta=ler['ferramenta'],argumentos=ler['argumentos'])
        I.registrar_retorno(p,ler,{'resposta':raw})
        reg=op('conferir-formulario',formulario_id='FORM',modelo='habilitacao')
        shutil.copyfile(reg['arquivo'],destino/(nome+'.md'))
        if not reg['diferencas']:
            op('confirmar-formulario',literal='conferido',formulario_id='FORM',relatorio_sha256=reg['sha256'])
        try:
            op('mcp',ferramenta='mcp__tally__publish_form',argumentos={'formId':'FORM'})
            autorizada=True;recusa=None
        except ValueError as exc:autorizada=False;recusa=str(exc)
        reg['arquivo']=nome+'.md';resumos[nome]=dict(relatorio=reg,publicacao_autorizada=autorizada,motivo=recusa)
(destino/'relatorios-hashes.json').write_text(json.dumps(resumos,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({n:dict(sha256=r['relatorio']['sha256'],publicacao_autorizada=r['publicacao_autorizada']) for n,r in resumos.items()},ensure_ascii=False,indent=2))
