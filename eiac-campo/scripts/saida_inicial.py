"""Checklist verificável do bloco inicial; F0 liberado não significa encerrado."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import iniciar as I
import habilitacao as H
import importar_habilitacao as M
import playbook as P
import estado as E
import integridade as G
import canais_registro as K


def conferir(expediente,caso):
    exp=pathlib.Path(expediente).absolute();case=pathlib.Path(caso).absolute()
    itens=[];pendencias=[]
    def item(nome,fn):
        try:
            ok=bool(fn());motivo='' if ok else 'saída ausente ou incompleta'
        except (OSError,ValueError,KeyError,TypeError,AttributeError,IndexError) as exc:ok=False;motivo=str(exc)
        itens.append(dict(item=nome,presente=ok,motivo=motivo))
    try:
        s=json.loads((exp/'expediente.json').read_text());H.integridade(exp,s)
    except (OSError,ValueError,KeyError,TypeError):s={}
    item('respostas preservadas',lambda:bool(s['fontes']) and all(H.ler_arquivo(exp,f['arquivo']) for f in s['fontes'].values()))
    item('campos com fonte',lambda:bool(s['campos']) and all(c['fonte'] in s['fontes'] for c in s['campos'].values()) and not any(p['estado']=='aberta' for p in s['pendencias'].values()))
    item('carta conferida',lambda:bool(s['revisao']) and any(e.get('tipo')=='OperacaoRegistrada' and e.get('operacao')=='revisar' and e['entrada'].get('conteudo_conferido') is True for e in s['eventos']))
    item('três PDFs assinados com evidência',lambda:H.completa(s) and all(H.ler_arquivo(exp,s['documentos'][d][-1]['assinatura']['arquivo']) and H.ler_arquivo(exp,s['documentos'][d][-1]['assinatura']['evidencia']) for d in H.CODIGOS_HAB))
    item('matriz de acessos',lambda:bool(s['acessos']) and bool(M.conferir(exp)))
    item('desfecho',lambda:any(e.get('operacao')=='preparar-0d' for e in s['eventos']) or bool(s.get('recusa')))
    for doc in ('HAB-02','HAB-03'):
        v=(s.get('documentos',{}).get(doc) or [{}])[-1]
        estado=v.get('situacao_juridica',{}).get('estado')
        ratificada=estado=='ratificada' or (estado is None and v.get('revisao_juridica',{}).get('resultado')=='aprovado' if isinstance(v.get('revisao_juridica'),dict) else False)
        if not ratificada and estado=='sem ratificação':pendencias.append('Minutas sem ratificação jurídica: '+doc+' (não bloqueante)')
    if case.is_dir():
        with I.cwd(case):
            st=E.ler();pb,erro=P.carregar()
            item('caso aberto',lambda:bool(st) and st['caso']==s['caso_reservado'] and st['responsavel']==s['responsavel'])
            def metodo():
                if erro or not G.conferir(pb)['confere']:return False
                for nome,raw in I.B.pacote().items():
                    if (case/'metodo'/nome).read_bytes()!=raw:return False
                return True
            item('método conferido',metodo)
            item('canais declarados',lambda:not erro and K.conferir(pb,pb['etapas'][0]['id']) is None)
            def importacao():
                p=case/'registro/habilitacao.json';reg=json.loads(p.read_text())
                evs=[e for e in E.eventos() if e.get('evento')=='HabilitacaoImportada']
                if not evs or evs[-1]['registro_sha256']!=H.digest(p.read_bytes()):return False
                if reg['vigente']['caso_reservado']!=s['caso_reservado']:return False
                for ref in reg['vigente']['arquivos'].values():
                    p=case/ref['caminho']
                    if p.is_symlink() or not p.resolve().is_relative_to(case.resolve()) or H.digest(p.read_bytes())!=ref['sha256']:return False
                return True
            item('importação registrada',importacao)
            def validado():
                p=case/'caso/00-habilitacao.md';draft=case/'rascunho/00-habilitacao.md'
                return p.read_bytes()==draft.read_bytes() and any(e.get('evento')=='AssercaoRegistrada' and e.get('arquivo')=='caso/00-habilitacao.md' for e in E.eventos())
            item('00-habilitacao validado',validado)
            def selo():
                if not validado():return False
                selos,err=E.selos_confirmados()
                if err or not selos:return False
                # A confirmação declarativa exige o prefixo íntegro da importação.
                ok,motivo=P.selo_confirmado_apos_evento(pb,pb['etapas'][0]['id'],E.eventos())
                if not ok:return False
                sha=selos[-1]['hash']
                r=subprocess.run(['git','show',sha+':caso/00-habilitacao.md'],capture_output=True)
                return r.returncode==0 and r.stdout==(case/'caso/00-habilitacao.md').read_bytes()
            item('selo confirmado no Git',selo)
            item('F0 liberado',lambda:not erro and bool(st) and st['etapa_atual']==pb['etapas'][0]['id'] and all(x['presente'] for x in itens))
    else:
        for nome in ('caso aberto','método conferido','canais declarados','importação registrada','00-habilitacao validado','selo confirmado no Git','F0 liberado'):
            itens.append(dict(item=nome,presente=False,motivo='caso ausente'))
    return dict(itens=itens,pendencias=pendencias,liberado=all(i['presente'] for i in itens))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--expediente',type=pathlib.Path,required=True);ap.add_argument('--caso',type=pathlib.Path,required=True);ap.add_argument('--json',action='store_true')
    a=ap.parse_args();r=conferir(a.expediente,a.caso)
    if a.json:print(json.dumps(r,ensure_ascii=False,indent=2))
    else:
        for i in r['itens']:print(('presente' if i['presente'] else 'ausente')+' — '+i['item']+(': '+i['motivo'] if i['motivo'] else ''))
        for p in r['pendencias']:print('pendência — '+p)
    raise SystemExit(0 if r['liberado'] else 1)

if __name__=='__main__':main()
