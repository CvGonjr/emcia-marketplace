"""Compara os blocos brutos do Tally com o modelo local; sem interpretação por IA.

Schema: developers.tally.so/api-reference/openapi.json. A ordem é a dos blocos.
Formato real do conector (decisão 046): o texto da pergunta vem em payload.html ou em
payload.safeHTMLSchema (trechos [texto, marcas]); a comparação usa o texto concatenado,
normalizado do mesmo modo do lado do modelo. Retorno não reconhecido produz divergência,
nunca uma aprovação presumida.
"""
import html.parser
import json
import re
import unicodedata


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


def normalizar(t):
    # Decisão 046, aplicada igualmente ao contrato e ao retorno: NFC, espaço não separável
    # como espaço comum, marcação ** de formatação removida e sem bordas. Nada além disso.
    return unicodedata.normalize('NFC',re.sub(r'\*\*(.+?)\*\*',r'\1',t)).replace(' ',' ').strip()


def texto_contrato(pergunta):
    return normalizar(pergunta), '**' in pergunta


def texto_schema(trechos):
    if not isinstance(trechos,list) or not trechos: raise ValueError('safeHTMLSchema não reconhecido')
    partes=[]; formatado=False
    for trecho in trechos:
        if not isinstance(trecho,list) or len(trecho) not in (1,2) or not isinstance(trecho[0],str):
            raise ValueError('safeHTMLSchema não reconhecido')
        if len(trecho)==2:
            marcas=trecho[1]
            if not isinstance(marcas,list) or any(m!=['font-weight','bold'] for m in marcas):
                raise ValueError('safeHTMLSchema com marcas não reconhecidas')
            if marcas:formatado=True
        partes.append(trecho[0])
    return ''.join(partes), formatado


def texto_pergunta(payload):
    if 'html' not in payload and 'safeHTMLSchema' not in payload: raise ValueError('texto da pergunta ausente')
    formatado=False; t_html=t_schema=None
    if 'safeHTMLSchema' in payload:
        t_schema,formatado=texto_schema(payload['safeHTMLSchema'])
    if 'html' in payload:
        t_html=texto(payload['html'])
        formatado=formatado or bool(re.search(r'<(b|strong|i|em|u)[\s>]',payload['html']))
    if t_html is not None and t_schema is not None and normalizar(t_html)!=normalizar(t_schema):
        raise ValueError('html e safeHTMLSchema divergentes')
    return normalizar(t_html if t_html is not None else t_schema), formatado


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
        for i,b in enumerate(blocos):
            try:
                tipo=b['type'];payload=b['payload']
                if not isinstance(tipo,str):raise ValueError('tipo precisa ser texto')
                if not isinstance(payload,dict): raise ValueError('payload precisa ser objeto')
                if tipo=='TITLE' and b['groupType']=='QUESTION':
                    pergunta,formatado=texto_pergunta(payload)
                    perguntas.append(dict(pergunta=pergunta,tipos=[],alternativas=[],formatacao=formatado))
                    if payload.get('isHidden'): diferencas.append('pergunta oculta: '+pergunta)
                elif tipo=='HIDDEN_FIELDS':
                    ocultos.extend(f['name'] for f in payload['hiddenFields'])
                elif tipo in ('INPUT_TEXT','INPUT_NUMBER','INPUT_EMAIL','INPUT_LINK','INPUT_PHONE_NUMBER','INPUT_DATE','INPUT_TIME',
                              'TEXTAREA','MULTIPLE_CHOICE_OPTION','CHECKBOX','DROPDOWN_OPTION','MULTI_SELECT_OPTION','RATING','LINEAR_SCALE'):
                    if not perguntas: raise ValueError('entrada sem TITLE de pergunta')
                    perguntas[-1]['tipos'].append(tipo)
                    if payload.get('isHidden'): diferencas.append('entrada da pergunta oculta')
                    if tipo=='MULTIPLE_CHOICE_OPTION':
                        perguntas[-1]['alternativas'].append(payload['text'])
                        if payload.get('allowMultiple') or payload.get('randomize') or payload.get('isOtherOption'):
                            diferencas.append('tipo/ordem das alternativas alterado por configuração')
                elif tipo not in ('FORM_TITLE','TITLE','TEXT','LABEL','HEADING_1','HEADING_2','HEADING_3','DIVIDER','PAGE_BREAK'):
                    raise ValueError('tipo desconhecido '+str(tipo))
            except (KeyError,TypeError,ValueError,AttributeError) as exc:
                raise ValueError(f'blocks[{i}]: {exc}') from exc
        esperado=modelo.get('perguntas')
        if not isinstance(esperado,list) or not esperado:
            diferencas.append('modelo não fixa texto de perguntas; use conferência manual com PDF')
            esperado=[]
        if len(perguntas)!=len(esperado):
            diferencas.append(f'quantidade de perguntas: esperado {len(esperado)}, encontrado {len(perguntas)}')
        textos=[texto_contrato(p['pergunta'])[0] for p in esperado]
        for i,(e,a) in enumerate(zip(esperado,perguntas),1):
            a['id_modelo']=e['id']
            esperado_texto,formato_modelo=texto_contrato(e['pergunta'])
            if formato_modelo: a['formatacao_modelo']=True
            ref=f'pergunta {i} ({e["id"]})'
            if a['pergunta']!=esperado_texto:
                aspecto='ordem/texto' if a['pergunta'] in textos else 'texto'
                diferencas.append(f'{ref}: {aspecto}; esperado {json.dumps(esperado_texto,ensure_ascii=False)}, encontrado {json.dumps(a["pergunta"],ensure_ascii=False)}')
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
