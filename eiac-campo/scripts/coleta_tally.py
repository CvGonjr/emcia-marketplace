"""Filtra respostas do conector pelo campo oculto antes de persistir."""
import csv
import io
import json
import pathlib
import habilitacao as H


def paginas(retorno):
    data=retorno.get('resposta',retorno)
    if 'structuredContent' in data:data=data['structuredContent']
    if 'data' in data:data=data['data']
    ps=data.get('paginas',[data]);H.exigir(isinstance(ps,list) and ps,'retorno sem páginas conferíveis')
    for i,p in enumerate(ps):
        H.exigir(isinstance(p,dict) and isinstance(p.get('submissions'),list),'formato de submissões não conferível')
        pag=p.get('pagination',{})
        completo=p.get('hasMore')
        if completo is None and isinstance(pag,dict) and isinstance(pag.get('totalPages'),int) and isinstance(pag.get('page'),int):
            completo=pag['page']<pag['totalPages']
        H.exigir(isinstance(completo,bool),'confira todas as páginas: retorno exige hasMore ou pagination.page/totalPages')
        H.exigir(completo==(i<len(ps)-1),'reúna todas as páginas antes de registrar a submissão')
        if 'page' in p:H.exigir(p['page']==i+1,'páginas fora de ordem ou incompletas')
        if isinstance(pag,dict) and 'page' in pag:H.exigir(pag['page']==i+1,'páginas fora de ordem ou incompletas')
    return ps


def perguntas(p):
    resultado={}
    for q in p.get('questions',[]):
        H.exigir(isinstance(q,dict) and isinstance(q.get('id'),str),'metadados de pergunta não conferíveis')
        itens=[dict(id=q['id'],label=q.get('title'),type=q.get('type'))]
        itens.extend(dict(id=f.get('uuid'),label=f.get('title'),type=f.get('type')) for f in q.get('fields',[]) if isinstance(f,dict))
        for item in itens:
            if not item['id']:continue
            H.exigir(item['id'] not in resultado or resultado[item['id']]==item,'identificador de pergunta ambíguo')
            resultado[item['id']]=item
    return resultado


def respostas(s,qs):
    for f in s.get('responses',s.get('fields',[])):
        if not isinstance(f,dict):yield f;continue
        meta=qs.get(f.get('questionId'),{})
        yield dict(f,label=f.get('label',meta.get('label')),type=f.get('type',meta.get('type')))


def caso_oculto(s,qs):
    h=s.get('hiddenFields')
    candidatos=[h['caso']] if isinstance(h,dict) and 'caso' in h else []
    for f in respostas(s,qs):
        if isinstance(f,dict) and f.get('type') in ('HIDDEN_FIELDS','HIDDEN_FIELD') and f.get('label')=='caso':
            candidatos.append(f.get('answer',f.get('value')))
    return candidatos[0] if len(candidatos)==1 and isinstance(candidatos[0],str) else None


def filtrar(retorno,caso,selecao=None):
    proprias=[]
    for p in paginas(retorno):
        qs=perguntas(p)
        for s in p['submissions']:
            if not isinstance(s,dict) or caso_oculto(s,qs)!=caso:continue
            ident=H.texto(s.get('id'));proprias.append((ident,s,qs))
    H.exigir(proprias,'nenhuma submissão do caso; peça ao engenheiro a submissão correta')
    ids=[ident for ident,s,qs in proprias]
    H.exigir(len(set(ids))==len(ids),'submissão do caso duplicada nas páginas; confira a coleta')
    escolhidas=[(s,qs) for ident,s,qs in proprias if selecao is None or ident==selecao]
    H.exigir(len(escolhidas)==1,'indique qual submissão do caso vale; ids do caso: '+', '.join(ids[:10]))
    return escolhidas[0]


def receber(root,s,p):
    import iniciar as I
    import formularios_permanentes as F
    import aprovacao as A
    H.exigir(set(p)<={'config_emcia','retorno','formulario','id','submissao','respondente'},'campos extras na coleta recusados')
    config=pathlib.Path(p.get('config_emcia',I.CONFIG));c=I.ler_config(config)
    H.exigir(c['responsavel']==s['responsavel'],'responsável diverge do expediente')
    H.exigir(not (pathlib.Path(c['base_casos'])/s['caso_reservado']).exists(),'coleta administrativa encerrada; caso usa perfil e escopo')
    reg=F.validar(config,c,'habilitacao')
    H.exigir(p['formulario']==reg['formId'],'formulário da coleta diverge do permanente')
    H.exigir(s.get('tratamento'),'tratamento administrativo deve preceder a coleta')
    arq=pathlib.Path(p['retorno']);sha=A.hash_arquivo(arq)
    sub,qs=filtrar(json.loads(arq.read_text()),s['caso_reservado'],p.get('submissao'))
    H.exigir(sub.get('formId',reg['formId'])==reg['formId'],'formulário da submissão do caso diverge do permanente')
    ident=H.identificador(p['id']);H.exigir(ident not in s['fontes'],'fonte já registrada')
    H.exigir(not any(f['formulario']==reg['formId'] and f['submissao']==sub['id'] for f in s['fontes'].values()),'submissão duplicada')
    linha={'Submission ID':sub['id'],'caso':s['caso_reservado']}
    for f in respostas(sub,qs):
        H.exigir(isinstance(f,dict),'resposta do caso inválida')
        if f.get('type') in ('HIDDEN_FIELDS','HIDDEN_FIELD'):continue
        label=H.texto(f.get('label'));H.exigir(label not in linha,'pergunta duplicada ou campo de controle na resposta')
        valor=f.get('answer',f.get('value'));linha[label]=valor if isinstance(valor,str) else json.dumps(valor,ensure_ascii=False)
    nome=sub.get('respondente') or linha.get('Respondente') or p.get('respondente')
    linha['Respondente']=H.pessoa(nome)
    out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=list(linha),lineterminator='\n');w.writeheader();w.writerow(linha)
    s['fontes'][ident]=dict(formulario=reg['formId'],submissao=sub['id'],rodada=0,canal='tally',respondente=linha['Respondente'],
        versao_perguntas=reg['versao_contrato'],workspace_id=c['workspace_tally'],recebido_em=H.agora(),original_sha256=sha,
        arquivo=H.guardar(root,out.getvalue().encode(),'.csv'),conferencia_sha256=reg['relatorio_sha256'])
    H.invalidar(s)
