"""Planejamento de P2: um testemunho cobre criação e compartilhamento declarados.

Devolve uma chamada autorizada por vez; o conector continua executado pela sessão.
"""
import copy
import json
import pathlib
import re
import habilitacao as H
import aprovacao as A

NOMES = ('00-habilitacao','entrada-documentos','entrada-amostras','entregas','trabalho-interno')


def arquivo(config, caso):
    return pathlib.Path(config).with_name('provisionamento-'+H.identificador(caso)+'.json')


def fase(c, caso):
    import iniciar as I
    import estado as E
    case=pathlib.Path(c['base_casos'])/H.identificador(caso)
    H.exigir(case.is_dir(), 'provisionamento aguarda P2 aberta')
    with I.cwd(case):
        st=E.ler()
        H.exigir(st and st['etapa_atual']=='P2' and not st['cumprimentos'].get('P2',{}).get('cumprido'), 'provisionamento exige P2 aberta')
        H.exigir(st['responsavel']==c['responsavel'], 'responsável diverge do caso')
    return case


def comando(plano):
    return ['provisionar-p2', json.dumps(plano,sort_keys=True,ensure_ascii=False)]


def registro(config,c,caso):
    import iniciar as I
    p=arquivo(config,caso)
    if not p.exists(): return None
    A.hash_arquivo(p); reg=json.loads(p.read_text())
    evs=[json.loads(l) for l in pathlib.Path(config).with_name('eventos.jsonl').read_text().splitlines()]
    sha=H.digest(json.dumps(reg,sort_keys=True,ensure_ascii=False).encode())
    H.exigir(any(e.get('evento')=='ProvisionamentoP2Aprovado' and e.get('registro_sha256')==sha and e.get('caso')==caso for e in evs), 'plano de P2 sem evento íntegro')
    A.conferir(reg['testemunho'],'provisionar-p2',c['responsavel'],caso,comando(reg['plano']))
    return reg


def conteiner_aprovado(config,c,caso):
    # Não consulta P2 para casos anteriores sem plano, preservando sua interface.
    if not arquivo(config,caso).exists(): return None
    fase(c,caso); r=registro(config,c,caso)
    return r['plano']['conteiner_id']


def proximo(config,d):
    import iniciar as I
    import canais as K
    c=I.ler_config(config); caso=H.identificador(d['caso']); hab=H.identificador(d['habilitacao']); case=fase(c,caso)
    p=arquivo(config,caso)
    if p.exists(): reg=registro(config,c,caso)
    else:
        plano=dict(caso=caso,habilitacao=hab,conteiner_id=d.get('conteiner_id',c.get('pasta_drive')),
            drive_id=d.get('drive_id'),destinatario=d.get('destinatario'),papel=d.get('papel','reader'),
            pastas=list(NOMES),compartilhar=list(NOMES[:-1]))
        for k in ('conteiner_id','drive_id'):K.id_externo(plano[k])
        H.exigir(isinstance(plano['destinatario'],str) and re.fullmatch(r'[^\s@]+@[^\s@]+',plano['destinatario']), 'informe destinatário nominal do compartilhamento')
        H.exigir(plano['papel'] in ('reader','writer'), 'papel do compartilhamento inválido')
        if d.get('confirmado') is not True:
            return dict(proximo='aprovar-pastas-p2',resumo='P2: criar raiz e cinco pastas; compartilhar quatro pastas; raiz e trabalho-interno permanecem privados.',plano=plano)
        r=A.criar('provisionar-p2',c['responsavel'],caso,H.texto(d.get('trecho')),
            'Criação da árvore em P2 e compartilhamento: '+plano['destinatario']+' / '+plano['papel'], comando(plano),[config,case/'registro/playbook.json'])
        reg=dict(plano=plano,testemunho=r);I.escrever(p,reg)
        I.log(config,c,'ProvisionamentoP2Aprovado',caso=caso,registro_sha256=H.digest(json.dumps(reg,sort_keys=True,ensure_ascii=False).encode()),testemunho=A.evento(r))
    plano=reg['plano']; sha=H.digest(json.dumps(plano,sort_keys=True,ensure_ascii=False).encode())
    H.exigir(plano['habilitacao']==hab,'plano pertence a outro expediente')
    retornos=[r for r in I.registros_externos(config,hab) if r['chamada'].get('plano_p2_sha256')==sha and r['chamada'].get('caso')==caso]
    ids={r['chamada']['finalidade']:r['ids']['pasta_id'] for r in retornos if r['ids'].get('pasta_id')}
    fila=[]
    if 'raiz-caso' not in ids: fila.append(('raiz-caso',caso,plano['conteiner_id']))
    else:
        fila.extend((n,n,ids['raiz-caso']) for n in NOMES if n not in ids)
    if fila:
        finalidade,title,parent=fila[0]
        nome='mcp__claude_ai_Google_Drive__create_file';args=dict(title=title,parentId=parent,contentMimeType='application/vnd.google-apps.folder')
    elif any(n not in {r['chamada']['finalidade'] for r in retornos if r['chamada']['ferramenta']=='mcp__claude_ai_Google_Drive__share_file'} for n in plano['compartilhar']):
        compartilhadas={r['chamada']['finalidade'] for r in retornos if r['chamada']['ferramenta']=='mcp__claude_ai_Google_Drive__share_file'}
        finalidade=next(n for n in plano['compartilhar'] if n not in compartilhadas);nome='mcp__claude_ai_Google_Drive__share_file'
        args=dict(fileId=ids[finalidade],emailAddress=plano['destinatario'],role=plano['papel'])
    else:
        with I.cwd(case):
            pb=json.loads((case/'registro/playbook.json').read_text()); anterior=K.G.carregar(pb)
            canais=copy.deepcopy(anterior['canais'])
            for f in pb['canais_previstos']:
                if f['ferramenta']!='drive':continue
                finalidade={'documentos':'entrada-documentos','amostras':'entrada-amostras'}.get(f['finalidade'],f['finalidade'])
                existente=[x for x in canais if x['finalidade']==f['finalidade']]
                H.exigir(not existente or all(x['ids']['pasta_id']==ids[finalidade] for x in existente),'canal Drive existente diverge do plano; revisão humana necessária')
                if not existente:canais.append(dict(f,ids={'drive_id':plano['drive_id'],'pasta_id':ids[finalidade]},proprietario='emcia',acesso_cliente=('nenhum' if finalidade=='trabalho-interno' else 'leitura' if plano['papel']=='reader' else 'escrita'),sensivel=False,filtro=None,marcador=None))
            if canais!=anterior['canais']:
                K.definir(dict(anterior,canais=canais,versao=anterior['versao']+1),I.E.ler(),pb)
        return dict(proximo='P2',resumo='Pastas criadas, compartilhamento registrado e canal de documentos definido.')
    chamada=dict(caso=caso,habilitacao=hab,ferramenta=nome,argumentos=args,finalidade=finalidade,plano_p2_sha256=sha)
    # Subtestemunho mecânico: mesmos literal/autor; o plano pai foi conferido acima.
    r=I.aprovar(config,'mcp',chamada,reg['testemunho']['literal'],reg['testemunho']['resumo'])
    I.operar(config,'mcp',chamada,r)
    return dict(proximo='conector',resumo='Executar chamada autorizada e preservar retorno; não repetir efeito sem conferir id remoto.',chamada=chamada)
