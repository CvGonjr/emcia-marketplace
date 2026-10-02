"""Importação humana do expediente administrativo no caso, antes do percurso.

Executar no terminal do engenheiro. A guarda bloqueia sua chamada pela sessão.
Não grava em caso/: prepara o rascunho para o validador de procedência.
"""
import argparse
import copy
import datetime
import fcntl
import hashlib
import json
import os
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/'eiac-nucleo/scripts'))
import estado as E
import playbook as P
import habilitacao as H


def serializar(dados):
    return json.dumps(dados, sort_keys=True, ensure_ascii=False).encode()


def conferir(expediente, caso=None, responsavel=None):
    """Leitura sob lock; não executa operações nem altera o expediente."""
    root=H.local_externo(expediente)
    p=root/'expediente.json'
    H.exigir(p.is_file() and not p.is_symlink(), 'expediente ausente ou inválido')
    H.exigir(not (root/'.lock').is_symlink(), 'lock inválido')
    with (root/'.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_SH)
        s=json.loads(p.read_text(encoding='utf-8'))
        H.exigir(isinstance(s,dict) and s.get('schema')==1, 'schema do expediente inválido')
        H.REGRA_PESSOA.set(s.get('pessoa_nomeada'))
        H.pessoa(s['responsavel'])
        H.identificador(s['habilitacao']); H.identificador(s['caso_reservado'])
        H.exigir(s.get('caso_aberto') is False, 'expediente inválido: caso já aberto')
        H.exigir(not s.get('recusa'), 'desfecho não prosseguir; retomada exige decisão própria')
        H.integridade(root,s)
        H.exigir(H.completa(s), 'formalização incompleta: 0b não concluída')
        H.exigir(isinstance(s.get('acessos'),dict), 'acessos ausentes: 0c não concluída')
        H.exigir(not any(p.get('estado')=='aberta' for p in s['pendencias'].values()), 'pendência aberta')
        revisoes=[e for e in s['eventos'] if e.get('tipo')=='OperacaoRegistrada' and e.get('operacao')=='revisar']
        H.exigir(bool(s.get('revisao')) and bool(revisoes)
                 and revisoes[-1]['entrada'].get('qualificacao_0a') is True, 'qualificação ausente')
        if caso is not None: H.exigir(s['caso_reservado']==caso,'identificador reservado diverge do caso')
        if responsavel is not None: H.exigir(s['responsavel']==responsavel,'responsável diverge do caso')
        # A matriz deriva da entrada com hash já preservada na operação acessos.
        entradas=[e for e in s['eventos'] if e.get('tipo')=='OperacaoRegistrada' and e.get('operacao')=='acessos']
        H.exigir(bool(entradas),'matriz sem origem registrada')
        ev=entradas[-1]; matriz=ev['entrada']
        H.exigir(H.digest(serializar(matriz))==ev['entrada_sha256'],'integridade da matriz divergente')
        atual={k:v for k,v in s['acessos'].items() if k!='data_registro'}
        H.exigir(matriz==atual,'matriz diverge da entrada preservada')
        # Reaplica as condições administrativas puras sobre uma cópia.
        H.aplicar(root,copy.deepcopy(s),'acessos',copy.deepcopy(matriz))
        pronto=H.aplicar(root,copy.deepcopy(s),'preparar-0d',{})
        arquivos={}
        for doc in H.TEMPLATES:
            v=s['documentos'][doc][-1]; assinatura=v['assinatura']
            H.exigir(v['revisao']==s['revisao'],'revisão do documento diverge da vigente')
            esperado={(x['nome'],x['papel']) for x in v['liberacao']['signatarios']}
            assinado={(x['nome'],x['papel']) for x in assinatura['signatarios']}
            H.exigir(esperado==assinado and {x[1] for x in esperado}=={'organizacao','emcia'},
                     'assinaturas incompletas ou divergentes')
            for nome,_ in esperado: H.pessoa(nome)
            for x in assinatura['signatarios']: datetime.date.fromisoformat(x['data'])
            pdf=H.ler_arquivo(root,assinatura['arquivo'])
            H.exigir(pdf.startswith(b'%PDF-') and b'%%EOF' in pdf[-2048:],'PDF assinado inválido')
            arquivos[doc+'-assinado.pdf']=(pdf,assinatura['arquivo']['sha256'])
            arquivos[doc+'-evidencia.bin']=(H.ler_arquivo(root,assinatura['evidencia']),assinatura['evidencia']['sha256'])
        arquivos['matriz-de-acessos.json']=(serializar(matriz),ev['entrada_sha256'])
        return s,pronto,arquivos,H.digest(p.read_bytes())


def caminho_seguro(relativo):
    raiz=pathlib.Path.cwd().resolve(); p=raiz/relativo
    H.exigir(p.resolve().is_relative_to(raiz),'destino fora do caso')
    H.exigir(not any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(raiz)), 'destino contém symlink')
    return p


def importar(expediente, autor=None, decisao=None):
    st=E.ler(); pb,erro=P.carregar()
    H.exigir(st is not None and not erro,erro or 'caso ausente')
    pessoa=st.get('responsavel')
    H.exigir(E.pessoa_nomeada(pessoa),'responsável do caso inválido')
    H.exigir(autor is None,'autor vem do responsável fixado no caso; argumento recusado')
    H.exigir(not any(x.get('cumprido') for x in st['cumprimentos'].values())
             and not any(x.get('evento')=='EtapaEncerrada' for x in E.eventos()), 'caso já tem etapa encerrada')
    for area in ('registro','fontes','rascunho'): caminho_seguro(area)
    registro=caminho_seguro('registro/habilitacao.json')
    anterior=json.loads(registro.read_text()) if registro.exists() else None
    historico=copy.deepcopy(anterior.get('historico',[]))+[anterior['vigente']] if anterior else []
    evs=[e for e in E.eventos() if e.get('evento')=='HabilitacaoImportada']
    H.exigir(bool(anterior)==bool(evs), 'registro e evento de importação divergentes')
    decisao_registrada=None
    if anterior:
        H.exigir(decisao is not None,'importação anterior; reimportação exige decisão explícita')
        decisao_registrada=json.loads(pathlib.Path(decisao).read_text())
        H.exigir(decisao_registrada.get('decisor')==pessoa,'decisor da reimportação diverge do responsável')
        H.texto(decisao_registrada.get('motivo'))
        datetime.date.fromisoformat(decisao_registrada['data'])
        H.exigir(decisao_registrada.get('importacao_anterior')==anterior['vigente']['id'],
                 'decisão não identifica importação anterior')
    else: H.exigir(decisao is None,'decisão de reimportação sem importação anterior')
    s,pronto,arquivos,hash_expediente=conferir(expediente,st['caso'],pessoa)
    agora=datetime.datetime.now(datetime.timezone.utc).isoformat()
    ident=f"importacao-{len(historico)+1:03d}-{agora[:10]}"
    destino=caminho_seguro('fontes/habilitacao/'+ident)
    H.exigir(not destino.exists(),'destino de importação já existe')
    H.exigir(len({i['item'] for i in s['acessos']['itens']})==len(s['acessos']['itens']),
             'matriz contém itens duplicados; identifique cada fonte sem ambiguidade')
    ids={r['item']:r['id'] for v in historico for r in v['restricoes']}
    sequencia=max([int(r[3:]) for r in ids.values()]+[0])
    restricoes=[]
    for i in s['acessos']['itens']:
        if i['status']!='negado': continue
        if i['item'] not in ids:
            sequencia+=1; ids[i['item']]=f'RH-{sequencia:02d}'
        restricoes.append(dict(id=ids[i['item']],item=i['item'],motivo=i['motivo'],restricao=i['restricao']))
    refs={nome:dict(caminho=str((destino/nome).relative_to(pathlib.Path.cwd())),sha256=sha)
          for nome,(_,sha) in arquivos.items()}
    vigente=dict(id=ident,habilitacao=s['habilitacao'],caso_reservado=s['caso_reservado'],
                 expediente=str(pathlib.Path(expediente).resolve()),expediente_sha256=hash_expediente,
                 desfecho=pronto['desfecho_proposto'],patrocinador=s['acessos']['patrocinador'],
                 executor=s['acessos']['executor'],data_sessao=s['acessos']['data_sessao'],
                 restricoes=restricoes,arquivos=refs,autor=pessoa,data=agora,
                 decisao_reimportacao=decisao_registrada)
    md=[]
    for doc in H.TEMPLATES:
        ref=refs[doc+'-assinado.pdf']['caminho'].removeprefix('fontes/')
        md.append(f"- [V · documento: {ref} · {agora[:10]} · {pessoa}] {doc}: documento assinado; conferência humana preservada nas evidências.\n")
    md.append(f"- [D · {vigente['patrocinador']} · {agora[:10]}] Patrocinador: {vigente['patrocinador']}. Executor: {vigente['executor']}; sessão em {vigente['data_sessao']}.\n")
    ref=refs['matriz-de-acessos.json']['caminho'].removeprefix('fontes/')
    for i in s['acessos']['itens']:
        md.append(f"- [V · documento: {ref} · {agora[:10]} · {pessoa}] Matriz registrada: {i['status']} — {i['item']}.\n")
    for r in restricoes:
        md.append(f"- [D · {pessoa} · {agora[:10]}] {r['id']}: {r['item']}; motivo: {r['motivo']}; restrição: {r['restricao']}.\n")
    md.append(f"- [D · {pessoa} · {agora[:10]}] Desfecho: {vigente['desfecho']}.\n")
    # Texto administrativo não pode introduzir linhas/colchetes de marcação.
    for valor in [vigente['patrocinador'],vigente['executor'],pessoa,*[r[k] for r in restricoes for k in ('item','motivo','restricao')],*[i['item'] for i in s['acessos']['itens']]]:
        H.exigir(not any(c in valor for c in '\n\r[]·'),'texto incompatível com marcação de procedência')
    destino.parent.mkdir(parents=True,exist_ok=True)
    draft=caminho_seguro('rascunho/00-habilitacao.md'); draft.parent.mkdir(exist_ok=True)
    backup_reg=registro.read_bytes() if registro.exists() else None
    backup_draft=draft.read_bytes() if draft.exists() else None
    with tempfile.TemporaryDirectory(prefix='.importacao-',dir=pathlib.Path.cwd()) as tmp:
        stage=pathlib.Path(tmp); folder=stage/'fontes'; folder.mkdir()
        for nome,(data,sha) in arquivos.items():
            H.exigir(H.digest(data)==sha,'hash divergente na cópia: '+nome)
            (folder/nome).write_bytes(data)
            H.exigir(H.digest((folder/nome).read_bytes())==sha,'hash divergente após cópia: '+nome)
        (stage/'registro.json').write_text(json.dumps(dict(schema=1,vigente=vigente,historico=historico),indent=2,ensure_ascii=False)+'\n')
        (stage/'rascunho.md').write_text(''.join(md),encoding='utf-8')
        try:
            os.replace(folder,destino)
            os.replace(stage/'rascunho.md',draft)
            os.replace(stage/'registro.json',registro)
            E.evento('HabilitacaoImportada',autor=pessoa,importacao=ident,habilitacao=s['habilitacao'],
                     desfecho=vigente['desfecho'],arquivos=refs,registro_sha256=H.digest(registro.read_bytes()))
        except Exception:
            shutil.rmtree(destino,ignore_errors=True)
            for p,backup in ((registro,backup_reg),(draft,backup_draft)):
                if backup is None: p.unlink(missing_ok=True)
                else: p.write_bytes(backup)
            raise
    return vigente


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expediente',required=True,type=pathlib.Path)
    ap.add_argument('--decisao-reimportacao',type=pathlib.Path)
    ap.add_argument('--autor',help='recusado: autoria é fixada no caso')
    a=ap.parse_args()
    try:
        caminho_seguro('registro')
        lock=caminho_seguro('registro/.importacao.lock')
        with lock.open('a') as f:
            fcntl.flock(f,fcntl.LOCK_EX)
            resultado=importar(a.expediente,a.autor,a.decisao_reimportacao)
        print(json.dumps(resultado,ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,TypeError,AttributeError) as exc:
        E.evento('TentativaNegada',autor=(E.ler() or {}).get('responsavel'),
                 operacao='importar-habilitacao',motivo=str(exc))
        ap.exit(1,'Recusado: '+str(exc)+'\n')


if __name__=='__main__': main()
