"""Hook do campo antes do caso; não atribui autoridade de método ao chat."""
import json
import pathlib
import sys
import iniciar as I
import aprovacao as A
import decisao_humana as D
import caminhos as C


def conferir(ev,config=I.CONFIG):
    entrada=ev.get('tool_input',{});tool=ev.get('tool_name','');comando=entrada.get('command','')
    try:
        if tool=='Bash':
            segmentos=D._segmentos(comando)
            for seg in segmentos:
                for script,args,composto in D._invocacoes(seg):
                    if script=='__codigo_inline__' and any(n in str(args) for n in ('habilitacao','abrir_caso','iniciar')):
                        raise ValueError('ato operacional em código inline não inspecionável')
                    if script not in ('habilitacao.py','abrir_caso.py','iniciar.py'):continue
                    if script=='iniciar.py':
                        if args and args[0]=='proximo':
                            if len(segmentos)!=1 or composto or len(D._argumento(args,'--entrada'))!=1:
                                raise ValueError('proximo exige chamada simples com entrada local')
                            I.ler_config(config)
                            continue
                        if not args or args[0]!='executar':continue
                        ps=D._argumento(args,'--entrada');rs=D._argumento(args,'--aprovacao')
                        if len(segmentos)!=1 or composto or len(ps)!=1:raise ValueError('execução exige entrada simples')
                        d=json.loads(pathlib.Path(ps[0]).read_text());c=I.ler_config(config)
                        if d['operacao'] in ('mcp','conferir-formulario') and not (pathlib.Path(c['base_casos'])/d['entrada']['caso']).exists():
                            if d['operacao']=='mcp':I.autorizar_mcp(config,d['entrada'],A.ler(rs[0]) if len(rs)==1 else None)
                            continue
                        if len(rs)!=1:raise ValueError('execução exige aprovação registrada')
                        d=json.loads(pathlib.Path(ps[0]).read_text());c=I.ler_config(config)
                        A.conferir(A.ler(rs[0]),d['operacao'],c['responsavel'],d['entrada'].get('caso') or d['entrada'].get('id') or d['entrada'].get('habilitacao'),I.cmd_operacao(d['operacao'],d['entrada']))
                        continue
                    c=I.ler_config(config);rs=D._argumento(args,'--aprovacao')
                    if len(rs)!=1 or len(segmentos)!=1 or composto:raise ValueError('ato operacional sem aprovação registrada; use /eiac-campo:iniciar')
                    if script=='habilitacao.py':
                        xs=D._argumento(args,'--expediente')
                        if len(xs)!=1:raise ValueError('expediente ausente')
                        exp=pathlib.Path(xs[0]);estado=json.loads((exp/'expediente.json').read_text()) if (exp/'expediente.json').exists() else None
                        contexto=estado['caso_reservado'] if estado else D._argumento(args,'--caso')[0]
                        op='habilitacao:'+args[0]
                    else:
                        contexto=args[0];op='abrir-caso'
                    r=A.conferir(A.ler(rs[0]),op,c['responsavel'],contexto,seg)
                    for flag in ('--entrada',):
                        for p in D._argumento(args,flag):
                            if str(pathlib.Path(p).absolute()) not in r['arquivos']:raise ValueError('entrada sem hash na aprovação')
                    I.log(config,c,'AprovacaoChatRegistrada',testemunho=A.evento(r))
        elif tool.startswith('mcp__'):
            sessao=pathlib.Path(config).with_name('sessao.json')
            if not sessao.exists():raise ValueError('sessão inicial ausente; configure e use retomar antes de chamar MCP')
            s=json.loads(sessao.read_text());d=dict(habilitacao=s['habilitacao'],caso=s['caso'],ferramenta=tool,argumentos=entrada)
            r=None
            evs=[json.loads(l) for l in pathlib.Path(config).with_name('eventos.jsonl').read_text().splitlines()]
            for e in reversed(evs):
                if (e.get('evento')=='ChamadaMCPAutorizada' and e.get('ferramenta')==tool
                    and e.get('argumentos')==entrada and e.get('habilitacao')==s['habilitacao']
                    and e.get('chamada',{}).get('caso')==s['caso']):
                    # A finalidade é declaração local aprovada, nunca parâmetro inventado da API.
                    d=e['chamada'];t=e.get('testemunho')
                    r=dict(t,schema=1,aprovado=True) if t else None
                    break
                if e.get('evento')=='AprovacaoChatRegistrada':
                    t=e.get('testemunho',{})
                    if t.get('comando')==I.cmd_operacao('mcp',d):
                        r=dict(t,schema=1,aprovado=True);break
            I.autorizar_mcp(config,d,r)
        elif tool in ('Write','Edit','NotebookEdit'):
            alvo=pathlib.Path(entrada.get('file_path') or entrada.get('path') or '').absolute()
            c=I.ler_config(config) if pathlib.Path(config).exists() else None
            if c and (alvo.is_relative_to(pathlib.Path(config).parent.absolute()) or alvo.is_relative_to(pathlib.Path(c['base_expedientes']))):
                raise ValueError('estado interno não admite escrita direta; use as operações')
    except (OSError,ValueError,KeyError,TypeError,IndexError) as exc:
        try:
            if not pathlib.Path(config).exists():raise ValueError('configuração ausente')
            I.log(config,I.ler_config(config),'TentativaNegada',operacao='guarda-inicial',motivo=str(exc))
        except (OSError,ValueError,KeyError,TypeError):
            print(json.dumps(dict(evento='TentativaNegada',motivo=str(exc)),ensure_ascii=False),file=sys.stderr)
        return str(exc)
    return None


def main():
    try:
        ev=json.load(sys.stdin);erro=conferir(ev)
    except (OSError,ValueError,TypeError) as exc:
        erro=str(exc);print(json.dumps(dict(evento='TentativaNegada',motivo=erro)),file=sys.stderr)
    if erro:print(erro,file=sys.stderr);sys.exit(2)

if __name__=='__main__':main()
