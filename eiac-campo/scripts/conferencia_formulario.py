"""Compara os blocos brutos do Tally com o modelo local; sem interpretação por IA.

Schema: developers.tally.so/api-reference/openapi.json. A ordem é a dos blocos.
Retorno não reconhecido produz divergência, nunca uma aprovação presumida.
"""
import html.parser
import json


class TextoHTML(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.partes=[]

    def handle_data(self, data): self.partes.append(data)

    def handle_starttag(self, tag, attrs):
        if tag=='br': self.partes.append('\n')
        if tag in ('script','style'): raise ValueError('HTML não comparável')


def texto(html):
    if not isinstance(html,str): raise ValueError('texto HTML ausente')
    p=TextoHTML();p.feed(html);p.close();return ''.join(p.partes)


def comparar(modelo, resposta, formulario, workspace):
    diferencas=[]; perguntas=[]; ocultos=[]
    try:
        if resposta.get('isError'): raise ValueError('load_form retornou erro')
        dados=resposta.get('structuredContent',resposta)['data']
        if dados['formId']!=formulario: diferencas.append('formId do retorno difere da chamada autorizada')
        if dados['workspaceId']!=workspace: diferencas.append('workspaceId do retorno difere do workspace declarado')
        blocos=dados['blocks']
        if not isinstance(blocos,list): raise ValueError('blocks precisa ser lista')
        if 'blocksCount' in dados and dados['blocksCount']!=len(blocos):
            diferencas.append('blocksCount diverge do número de blocos recebidos')
        for b in blocos:
            tipo=b['type'];payload=b['payload']
            if not isinstance(payload,dict): raise ValueError('payload precisa ser objeto')
            if tipo=='TITLE' and b['groupType']=='QUESTION':
                perguntas.append(dict(pergunta=texto(payload['html']),tipos=[],alternativas=[]))
                if payload.get('isHidden'): diferencas.append('pergunta oculta: '+perguntas[-1]['pergunta'])
            elif tipo=='HIDDEN_FIELDS':
                ocultos.extend(f['name'] for f in payload['hiddenFields'])
            elif tipo.startswith('INPUT_') or tipo in ('TEXTAREA','MULTIPLE_CHOICE_OPTION','CHECKBOX','DROPDOWN_OPTION','MULTI_SELECT_OPTION','RATING','LINEAR_SCALE'):
                if not perguntas: raise ValueError('entrada sem TITLE de pergunta')
                perguntas[-1]['tipos'].append(tipo)
                if payload.get('isHidden'): diferencas.append('entrada da pergunta oculta')
                if tipo=='MULTIPLE_CHOICE_OPTION':
                    perguntas[-1]['alternativas'].append(payload['text'])
                    if payload.get('allowMultiple') or payload.get('randomize') or payload.get('isOtherOption'):
                        diferencas.append('tipo/ordem das alternativas alterado por configuração')
            elif tipo not in ('FORM_TITLE','TITLE','TEXT','LABEL','HEADING_1','HEADING_2','HEADING_3','DIVIDER','PAGE_BREAK'):
                diferencas.append('formato de bloco não conferível: '+str(tipo))
        esperado=modelo.get('perguntas')
        if not isinstance(esperado,list) or not esperado:
            diferencas.append('modelo não fixa texto de perguntas; use conferência manual com PDF')
            esperado=[]
        if len(perguntas)!=len(esperado):
            diferencas.append(f'quantidade de perguntas: esperado {len(esperado)}, encontrado {len(perguntas)}')
        textos=[p['pergunta'] for p in esperado]
        for i,(e,a) in enumerate(zip(esperado,perguntas),1):
            a['id_modelo']=e['id']
            ref=f'pergunta {i} ({e["id"]})'
            if a['pergunta']!=e['pergunta']:
                aspecto='ordem/texto' if a['pergunta'] in textos else 'texto'
                diferencas.append(f'{ref}: {aspecto}; esperado {json.dumps(e["pergunta"],ensure_ascii=False)}, encontrado {json.dumps(a["pergunta"],ensure_ascii=False)}')
            if 'alternativas' in e:
                if not a['tipos'] or set(a['tipos'])!={'MULTIPLE_CHOICE_OPTION'}:
                    diferencas.append(ref+': tipo esperado escolha única')
                if a['alternativas']!=[x['texto'] for x in e['alternativas']]:
                    diferencas.append(ref+': texto/ordem das alternativas difere do modelo')
            elif e.get('tipo')=='texto':
                if len(a['tipos'])!=1 or a['tipos'][0] not in ('INPUT_TEXT','TEXTAREA'):
                    diferencas.append(ref+': tipo esperado texto; encontrado '+str(a['tipos']))
            else: diferencas.append(ref+': tipo do modelo sem correspondência conferível')
        if ocultos.count(modelo['campo_oculto'])!=1:
            diferencas.append('campo oculto caso ausente ou duplicado')
    except (KeyError,TypeError,ValueError,AttributeError) as exc:
        diferencas.append('formato de retorno não conferível: '+str(exc))
    return dict(diferencas=diferencas,perguntas=perguntas)


def markdown(reg, comparacao):
    linhas=['# Conferência automática de formulário','']
    for chave in ('habilitacao','caso','formulario_id','modelo','modelo_sha256','retorno_sha256'):
        linhas.append(f'- {chave}: {reg[chave]}')
    linhas+=['','## Resultado','', 'Sem divergências; aguarda confirmação humana “conferido”.' if not comparacao['diferencas'] else 'Publicação recusada:']
    linhas+=['- '+json.dumps(d,ensure_ascii=False) for d in comparacao['diferencas']]
    linhas+=['','## Perguntas observadas','']
    for i,p in enumerate(comparacao['perguntas'],1):
        linhas.append(f'{i}. '+json.dumps(p,ensure_ascii=False))
    return '\n'.join(linhas)+'\n'
