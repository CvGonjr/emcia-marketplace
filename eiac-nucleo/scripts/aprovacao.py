"""Testemunho local de aprovação nominal, vinculado a operação e bytes.

Não autentica o chat, a pessoa ou o conteúdo remoto. O disco é a fronteira.
"""
import datetime
import hashlib
import json
import pathlib
import shlex
import re
import estado as E


def hash_arquivo(p):
    p=pathlib.Path(p)
    if any(x.is_symlink() for x in (p,*p.parents)): raise ValueError('aprovação não admite symlink')
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tokens(comando):
    partes=shlex.split(comando) if isinstance(comando,str) else list(comando)
    if '--aprovacao' in partes:
        i=partes.index('--aprovacao'); partes=partes[:i]+partes[i+2:]
    if any(p.startswith('--aprovacao=') for p in partes):
        partes=[p for p in partes if not p.startswith('--aprovacao=')]
    return partes


def criar(operacao,autor,contexto,literal,resumo,comando,arquivos=()):
    r=dict(schema=1,aprovado=True,operacao=operacao,autor=autor,contexto=contexto,
           literal=literal,resumo=resumo,data=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           comando=tokens(comando),arquivos={str(pathlib.Path(p).absolute()):hash_arquivo(p) for p in arquivos})
    conferir(r,operacao,autor,contexto,comando)
    return r


def conferir(r,operacao,autor,contexto,comando):
    if not isinstance(r,dict) or r.get('schema')!=1 or r.get('aprovado') is not True:
        raise ValueError('aprovação explícita registrada ausente')
    if not isinstance(r.get('autor'),str) or len(re.findall(r'[^\W\d_]+',r['autor']))<2 or E.autor_e_agente(r['autor']) or re.search(r'[<>{}]',r['autor']): raise ValueError('aprovação exige pessoa nomeada')
    if (r.get('operacao'),r.get('autor'),r.get('contexto'))!=(operacao,autor,contexto):
        raise ValueError('aprovação pertence a outra operação, responsável ou contexto')
    for k in ('literal','resumo'):
        if not isinstance(r.get(k),str) or not r[k].strip(): raise ValueError('aprovação sem '+k)
    d=datetime.datetime.fromisoformat(r['data'].replace('Z','+00:00'))
    if d.tzinfo is None: raise ValueError('data da aprovação exige fuso')
    if r.get('comando')!=tokens(comando): raise ValueError('comando diverge da aprovação registrada')
    if not isinstance(r.get('arquivos'),dict): raise ValueError('aprovação sem mapa de arquivos')
    for p,h in r['arquivos'].items():
        if hash_arquivo(p)!=h: raise ValueError('arquivo alterado depois da aprovação: '+p)
    return r


def ler(caminho):
    hash_arquivo(caminho)
    return json.loads(pathlib.Path(caminho).read_text())


def evento(r):
    return {k:r[k] for k in ('operacao','autor','contexto','literal','resumo','data','comando','arquivos')}


def avaliar(pb,st,comando):
    """Contrato opcional do caso; ausência conserva o contrato anterior."""
    import decisao_humana as H
    segs=H._segmentos(comando)
    for segmento in segs:
        for script,args,composto in H._invocacoes(segmento):
            for regra in pb.get('operacoes_sessao',[]):
                if script!=regra['script']: continue
                if regra.get('subcomandos') and (not args or args[0] not in regra['subcomandos']): continue
                if regra.get('argumento'):
                    valores=H._argumento(args,regra['argumento'])
                    if not valores: continue
                    if regra.get('valor_argumento') and valores!=[regra['valor_argumento']]: continue
                if st['etapa_atual'] not in regra['etapas']:
                    return regra['id'],'operação fora das etapas autorizadas à sessão'
                if len(segs)!=1 or composto: return regra['id'],'operação aprovada exige chamada simples'
                try:
                    if not E.pessoa_nomeada(st['responsavel'],pb['pessoa_nomeada']):raise ValueError('responsável do caso não é pessoa nomeada')
                    caminhos=H._argumento(args,'--aprovacao')
                    if len(caminhos)!=1: raise ValueError('ato operacional sem aprovação registrada; use --aprovacao')
                    r=conferir(ler(caminhos[0]),regra['id'],st['responsavel'],st['caso'],segmento)
                    # Todo arquivo de entrada precisa estar fixado pelo testemunho.
                    for flag in regra.get('arquivos',[]):
                        for valor in H._argumento(args,flag):
                            if str(pathlib.Path(valor).absolute()) not in r['arquivos']:
                                raise ValueError('entrada sem hash na aprovação: '+valor)
                    for valor in regra.get('artefatos',[]):
                        if str(pathlib.Path(valor).absolute()) not in r['arquivos']:raise ValueError('artefato sem hash na aprovação: '+valor)
                    for dir_reg in regra.get('diretorios_entrada',[]):
                        for pasta in H._argumento(args,dir_reg['argumento']):
                            arq=str((pathlib.Path(pasta)/dir_reg['arquivo']).absolute())
                            if arq not in r['arquivos']:raise ValueError('estado de entrada sem hash na aprovação')
                    E.evento('AprovacaoChatRegistrada',**evento(r))
                except (OSError,ValueError,KeyError,TypeError) as exc: return regra['id'],str(exc)
    return None


def validar_contrato(pb):
    regras=pb.get('operacoes_sessao',[])
    if not isinstance(regras,list): return 'operacoes_sessao precisa ser lista'
    vistos=set();etapas={e['id'] for e in pb['etapas']}
    for r in regras:
        if (not isinstance(r,dict) or not isinstance(r.get('id'),str) or r['id'] in vistos
            or not isinstance(r.get('script'),str) or pathlib.Path(r['script']).name!=r['script']
            or not isinstance(r.get('etapas'),list) or not r['etapas'] or not set(r['etapas'])<=etapas
            or not isinstance(r.get('arquivos',[]),list)):
            return 'operacoes_sessao: contrato inválido'
        vistos.add(r['id'])
    return None
