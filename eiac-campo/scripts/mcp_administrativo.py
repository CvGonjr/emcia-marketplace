"""Conectores antes do caso: sem escopo por id, efeitos externos testemunhados."""
import json
import pathlib
import re
import habilitacao as H

PREFIXOS=('mcp__tally__','mcp__claude_ai_Google_Drive__','mcp__claude_ai_Google_Calendar__')

def contexto(config,c,d):
    hab=H.identificador(d['habilitacao']);caso=H.identificador(d.get('caso') or hab)
    case=pathlib.Path(c['base_casos'])/caso
    H.exigir(not case.is_symlink(),'caso contém symlink')
    exp=pathlib.Path(c['base_expedientes'])/hab
    if (exp/'expediente.json').exists():
        s=json.loads((exp/'expediente.json').read_text());H.integridade(exp,s)
        H.exigir(s['caso_reservado']==caso and s['responsavel']==c['responsavel'],'expediente pertence a outro caso/responsável')
    return hab,caso,case


def efeito(nome,args):
    prefixo=next((p for p in PREFIXOS if nome.startswith(p)),None)
    H.exigir(prefixo is not None,'conector fora da habilitação administrativa')
    acao=nome[len(prefixo):]
    H.exigir(bool(re.fullmatch('[A-Za-z0-9_]+',acao)) and isinstance(args,dict),'chamada MCP inválida')
    if acao.startswith(('load_','list_','get_','read_','download_','search_','fetch_','inspect_')):return False
    if nome.startswith(PREFIXOS[0]) and acao in ('create_new_form','create_blocks','configure_blocks','apply_logic','set_column_layout','set_form_title','update_custom_css','extract_brand'):return False
    if nome==PREFIXOS[1]+'create_file':return False
    if nome==PREFIXOS[2]+'create_event':
        return bool(args.get('attendees') or args.get('attendeeEmails') or args.get('visibility')=='public'
                    or args.get('notificationLevel') not in (None,'NONE','NOTIFICATION_LEVEL_UNSPECIFIED'))
    # Publicação, mensagens, compartilhamento e operações não reconhecidas como
    # leitura/rascunho precisam de confirmação, sem atribuir escopo ou inventar API.
    return True


def autorizar(config,c,d,r=None):
    import iniciar as I
    import aprovacao as A
    hab,caso,case=contexto(config,c,d)
    H.exigir(not case.exists(),'caso aberto exige perfil e escopo')
    nome=d['ferramenta'];args=d['argumentos'];externo=efeito(nome,args)
    H.exigir(not externo or r is not None,'efeito externo sem aprovação: peça ok ao engenheiro')
    if r is not None:A.conferir(r,'mcp',c['responsavel'],caso,I.cmd_operacao('mcp',d))
    if nome=='mcp__tally__publish_form':
        ev=I.conferir_relatorio_vigente(config,c,d,[json.loads(l) for l in pathlib.Path(config).with_name('eventos.jsonl').read_text().splitlines()])
        H.exigir(ev and ev['resultado']=='conferido' and not ev.get('diferencas'),
            'publicação exige conferência sem divergência e conferido'+(': '+str(ev.get('diferencas')) if ev else ''))
    I.log(config,c,'ChamadaMCPAutorizada',ferramenta=nome,argumentos=args,habilitacao=hab,chamada=d,
          fase='habilitacao',efeito_externo=externo,testemunho=A.evento(r) if r else None)
    return dict(autorizada=True,ferramenta=nome,argumentos=args)


def registrar_retorno(config,c,chamada,resultado):
    import iniciar as I
    import aprovacao as A
    import tempfile
    hab,caso,case=contexto(config,c,chamada)
    H.exigir(not case.exists(),'retorno administrativo depois da abertura recusado')
    nome=chamada['ferramenta']
    if nome=='mcp__tally__fetch_submissions':
        # O lote nunca vai para mcp-retornos, evento ou fonte. Somente o script
        # vê seus bytes, em temporário administrativo removido inclusive na recusa.
        exp=pathlib.Path(c['base_expedientes'])/hab
        with tempfile.TemporaryDirectory(dir=pathlib.Path(config).parent,prefix='.coleta-') as temp:
            arq=pathlib.Path(temp)/'retorno.json';arq.write_text(json.dumps(resultado,ensure_ascii=False))
            payload=dict(config_emcia=str(config),retorno=str(arq),formulario=chamada['argumentos']['formId'],id=chamada.get('fonte','S1'))
            for k in ('submissao','respondente'):
                if k in chamada:payload[k]=chamada[k]
            H.executar(exp,'receber-submissoes',payload)
        s=json.loads((exp/'expediente.json').read_text());f=s['fontes'][payload['id']]
        I.log(config,c,'SubmissaoDoCasoRegistrada',habilitacao=hab,caso=caso,submissao=f['submissao'],sha256=f['arquivo']['sha256'])
        return dict(registrado=True,fonte=payload['id'],submissao=f['submissao'],sha256=f['arquivo']['sha256'])
    H.exigir(isinstance(resultado,dict),'retorno MCP deve ser objeto')
    tipos=({'formulario_id'} if nome=='mcp__tally__create_new_form' else {'pasta_id'}
           if nome==PREFIXOS[1]+'create_file' and chamada['argumentos'].get('contentMimeType')=='application/vnd.google-apps.folder' else set())
    ids=resultado.get('ids',{})
    H.exigir(isinstance(ids,dict) and set(ids)<=tipos,'retorno não pode declarar ids de outra operação/ferramenta')
    H.exigir(all(isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9_.@:+-]+',v) for v in ids.values()),'id de retorno inválido')
    raw=json.dumps(resultado,sort_keys=True,ensure_ascii=False).encode();sha=H.digest(raw)
    chamada_sha=H.digest(json.dumps(chamada,sort_keys=True,ensure_ascii=False).encode())
    arq=pathlib.Path(config).with_name('mcp-retornos.json');regs=json.loads(arq.read_text()) if arq.exists() else []
    regs.append(dict(habilitacao=hab,chamada=chamada,ids=ids,resultado=resultado,sha256=sha,chamada_sha256=chamada_sha,fase='habilitacao'))
    I.escrever(arq,regs);I.log(config,c,'RetornoMCPRegistrado',sha256=sha,chamada_sha256=chamada_sha,ferramenta=nome,fase='habilitacao')
    if nome=='mcp__tally__load_form':I.evento_conferencia(config,c,chamada,chamada['argumentos']['formId'],resultado='aguardando-comparacao',diferencas=['nova leitura load_form aguarda comparação e conferido'])
    return dict(registrado=True,sha256=sha)
