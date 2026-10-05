"""Pré-preenchimento literal de 0c; confirmação humana não presume concessão."""
import csv
import io
import json
import habilitacao as H


def planejar(root, s):
    fontes = [(i,f) for i,f in s['fontes'].items() if f['canal'] in ('tally-exportacao','tally')]
    H.exigir(fontes, 'matriz exige coleta do caso')
    ident, fonte = fontes[-1]
    linhas = list(csv.DictReader(io.StringIO(H.ler_arquivo(root, fonte['arquivo']).decode())))
    H.exigir(len(linhas)==1 and linhas[0]['caso']==s['caso_reservado'], 'origem da matriz pertence a outro caso')
    from formularios_permanentes import modelo
    contrato = json.loads(modelo('habilitacao').read_text())
    respostas = {p['id']:linhas[0].get(p['id'], linhas[0].get(p['pergunta'], ''))
                 for p in contrato['perguntas'] if p['id'].startswith('HAB-0c-')}
    itens = [dict(item=l, status='a-confirmar', evidencia=ident)
             for l in respostas.get('HAB-0c-3', '').splitlines() if l.strip()]
    s['proposta_acessos'] = dict(origem=ident, origem_sha256=fonte['arquivo']['sha256'], respostas_0c=respostas, itens=itens)
    md='# Matriz de acessos proposta\n\nFonte: '+ident+' · '+fonte['arquivo']['sha256']+'\n\n'
    md+='\n'.join(k+': '+v for k,v in respostas.items())+'\n\nStatus: a confirmar; não presume concessão.\n'
    s['proposta_acessos']['relatorio']=H.guardar(root,md.encode(),'.md')
    return s['proposta_acessos']


def confirmar(root, s, p):
    H.exigir(p.get('confirmado') is True and isinstance(p.get('trecho'), str) and p['trecho'].strip(),
             'confirme ou corrija a matriz numa mensagem explícita')
    matriz = p.get('matriz'); H.exigir(isinstance(matriz, dict), 'matriz ausente')
    H.exigir(matriz.get('decisor') == s['responsavel'], 'decisor diverge do responsável')
    H.aplicar(root, s, 'acessos', matriz)
    from habilitacao_lotes import registrar_operacao
    registrar_operacao(s, 'acessos', matriz)
    H.evento(s, 'MatrizConfirmadaPorMensagem', trecho=p['trecho'], matriz_sha256=H.digest(json.dumps(matriz,sort_keys=True,ensure_ascii=False).encode()))
    return {'registrado':True, 'operacao':'confirmar-acessos'}
