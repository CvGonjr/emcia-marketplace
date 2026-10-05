"""Operações locais do bloco conduzido; MCPs são chamados pela sessão.

As aprovações são testemunhos nominais. Nenhuma decisão de método é delegada.
"""
import argparse
import copy
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

RAIZ=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RAIZ/'eiac-nucleo/scripts'))
import aprovacao as A
import estado as E
import habilitacao as H
import abrir_caso as B

CONFIG=pathlib.Path.home()/'.emcia/config.json'
CAMPOS={'responsavel','base_casos','base_expedientes','workspace_tally','pasta_drive','calendario_casos','navegador'}
HAB={'tratamento','receber','pendencia','resolver','reabrir','consolidar','revisar','revisao-juridica',
     'gerar','liberar','assinatura','ocorrencia','concluir-0b','acessos','preparar-0d','nao-prosseguir','estado'}


def escrever(p,d):
    p=pathlib.Path(p).expanduser().absolute()
    if any(x.is_symlink() for x in (p,*p.parents)): raise ValueError('configuração/registro não admite symlink')
    p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    fd,n=tempfile.mkstemp(dir=p.parent)
    try:
        with os.fdopen(fd,'w') as f:
            json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(n,p)
    finally:
        if os.path.exists(n):os.unlink(n)


def ler_config(p=CONFIG):
    A.hash_arquivo(p)
    c=json.loads(pathlib.Path(p).read_text())
    if not CAMPOS<=set(c):raise ValueError('configuração incompleta')
    H.pessoa(c['responsavel'])
    for k in CAMPOS:
        H.texto(c[k])
    return c


def log(p,c,tipo,**dados):
    ev=dict(evento=tipo,autor=c['responsavel'],data=H.agora(),**dados)
    arq=pathlib.Path(p).with_name('eventos.jsonl')
    if any(x.is_symlink() for x in (arq,*arq.parents)):raise ValueError('diário contém symlink')
    with arq.open('a') as f:f.write(json.dumps(ev,ensure_ascii=False)+'\n')
    return ev


def configurar(p,d):
    p=pathlib.Path(p)
    if p.exists():
        c=ler_config(p)
        if any(c[k]!=d.get(k) for k in CAMPOS):raise ValueError('configuração já fixada; não substitua responsável ou bases silenciosamente')
        return c
    if set(d)!=CAMPOS:raise ValueError('informe os sete campos da configuração')
    H.pessoa(d['responsavel'])
    for k in CAMPOS:H.texto(d[k])
    for k in ('base_casos','base_expedientes'):
        q=pathlib.Path(d[k]).expanduser()
        if not q.is_absolute():raise ValueError('bases exigem caminhos absolutos')
        H.local_externo(q)
    for k in ('workspace_tally','pasta_drive','calendario_casos'):
        if not re.fullmatch(r'[A-Za-z0-9_.@:+-]+',d[k]):raise ValueError('configuração exige id, não nome: '+k)
    escrever(p,d);log(p,d,'ConfiguracaoEMCIARegistrada')
    return d


# Contratos embutidos auditados contra o inventário fornecido pelo engenheiro.
PERFIS = json.loads((RAIZ/'eiac-campo/reference/perfis-conectores.json').read_text())['perfis']


def inventario(ferramentas):
    fs = ferramentas.get('ferramentas') if isinstance(ferramentas,dict) else ferramentas
    if not isinstance(fs,list): raise ValueError('inventário MCP precisa conter ferramentas')
    resultado = {}
    for f in fs:
        nome = f.get('nome',f.get('name'))
        if not isinstance(nome,str) or nome in resultado: raise ValueError('nome ausente ou ferramenta duplicada')
        schema = f.get('inputSchema')
        if isinstance(schema,dict):
            props = schema.get('properties',{})
            obrigatorios = schema.get('required',[])
        else:
            ps = f.get('parametros')
            props = {p['nome']:p for p in ps} if isinstance(ps,list) else {}
            obrigatorios = [p['nome'] for p in ps if p.get('obrigatorio')] if isinstance(ps,list) else []
        resultado[nome] = dict(properties=props,required=obrigatorios)
    return resultado


def validar_contrato_perfis(ferramentas,perfis=None):
    inv = inventario(ferramentas)
    for nome,r in (PERFIS if perfis is None else perfis).items():
        if nome not in inv: raise ValueError('ferramenta do perfil ausente do inventário: '+nome)
        props = inv[nome]['properties']
        if r['ferramenta']!=nome or r['padrao']!=re.escape(nome): raise ValueError('nome/padrão do perfil divergente')
        campos = set(r['parametros']) | set(r['obrigatorios'])
        for parte in [r,*r.get('alternativas',[])]:
            campos.update(a['campo'] for a in parte['argumentos'])
            campos.update(parte.get('ausentes',[]));campos.update(parte.get('exige_um_de',[]))
            if parte.get('quando'): campos.add(parte['quando']['campo'])
        if r.get('precondicao_registrada'): campos.add(r['precondicao_registrada']['argumento'])
        if not campos<=set(props): raise ValueError('parâmetro do perfil ausente do inventário: '+', '.join(sorted(campos-set(props))))
        if not set(inv[nome]['required'])<=set(r['obrigatorios']): raise ValueError('perfil omite parâmetro obrigatório do inventário')
        for campo,contrato in r['parametros'].items():
            atual = props[campo]
            tipo = atual.get('type') if 'type' in atual else atual.get('tipo','').split()[0]
            if tipo!=contrato['type']: raise ValueError('tipo divergente do inventário: '+campo)
    return True


def calibrar(ferramentas):
    inv = inventario(ferramentas); regras=[];recusadas=[];motivos={};parametros_recusados={}
    for nome,d in inv.items():
        r = PERFIS.get(nome)
        if r is None: motivo='ferramenta sem perfil auditado ou schema indisponível'
        else:
            try: validar_contrato_perfis(ferramentas,{nome:r});motivo=r.get('recusa')
            except (ValueError,KeyError,TypeError) as exc: motivo=str(exc)
            if not motivo or r.get('recusa')==motivo: regras.append(copy.deepcopy(r))
            extras = sorted(set(d['properties'])-set(r['parametros']))
            if extras: parametros_recusados[nome]=extras
        if motivo: recusadas.append(nome);motivos[nome]=motivo
    ativos={r['ferramenta'] for r in regras if not r.get('recusa')}
    manuais=[dict(passo='preparar-formulario',ferramenta=None,motivo='Preparar perguntas/campo oculto no painel; conferência automática por load_form quando disponível ou manual com PDF e conferido')]
    for nome,passo in [('mcp__tally__create_new_form','criar-formulario'),('mcp__tally__publish_form','publicar-formulario'),('mcp__tally__fetch_submissions','coletar-submissoes')]:
        if nome not in ativos:
            manuais.append(dict(passo=passo,ferramenta=nome if nome in inv else None,motivo=motivos.get(nome,'ferramenta ausente do inventário; ação manual do engenheiro')))
    return dict(versao=4,regras=regras,recusadas=recusadas,motivos=motivos,manuais=manuais,
                parametros_recusados=parametros_recusados,evento_aprovacao='AprovacaoExternaRegistrada',
                conferencia_formulario=dict(leitura='mcp__tally__load_form' if 'mcp__tally__load_form' in ativos else None,
                    argumento='formId',escopo='formulários criados/declarados no expediente ou caso corrente',
                    comparar=['texto exato','ordem','tipo','campo oculto caso'],relatorio='MD com SHA-256',
                    confirmacao='conferido',alternativa='PDF conferido pelo engenheiro',
                    bloqueio='divergência ou formato não conferível impede publicação'))


def conferir_perfil(p,ferramentas):
    if p!=calibrar(ferramentas):raise ValueError('perfil não coincide com os perfis embutidos; escopo não pode ser afrouxado')


def ambiente(c,inventory):
    import platform
    checks=[('Python',sys.version_info>=(3,12),'Instale Python 3.12 ou superior; '+platform.python_version()),
            ('Git',bool(shutil.which('git')),'Instale Git'),
            ('Navegador',bool(shutil.which(c['navegador'])),'Instale Chrome/Chromium e ajuste navegador')]
    for k in ('user.name','user.email'):
        r=subprocess.run(['git','config','--get',k],capture_output=True,text=True) if shutil.which('git') else None
        checks.append((k,bool(r and r.returncode==0 and r.stdout.strip()),'Configure git config --global '+k))
    p=calibrar(inventory)
    inv=inventario(inventory)
    for nome,ns in [('Tally','tally'),('Drive','Google_Drive'),('Calendar','Google_Calendar')]:
        checks.append((nome,any(ns in n for n in inv),'Conecte '+nome+' e confira /mcp'))
    necessarias={'Drive/criar e entregar':'mcp__claude_ai_Google_Drive__create_file',
                 'Drive/compartilhar':'mcp__claude_ai_Google_Drive__share_file',
                 'Drive/buscar':'mcp__claude_ai_Google_Drive__search_files',
                 'Calendar/listar':'mcp__claude_ai_Google_Calendar__list_events',
                 'Calendar/criar':'mcp__claude_ai_Google_Calendar__create_event'}
    ativos={r['ferramenta'] for r in p['regras'] if not r.get('recusa')}
    for acao,nome in necessarias.items():
        checks.append((acao,nome in ativos,'Conecte a assinatura do inventário; ferramenta sem perfil continua recusada'))
    versions={plugin:json.loads((RAIZ/plugin/'.claude-plugin/plugin.json').read_text())['version'] for plugin in ('eiac-campo','eiac-nucleo')}
    return dict(itens=[dict(item=n,presente=bool(ok),correcao='' if ok else fix) for n,ok,fix in checks],
                versoes=versions,sem_perfil=p['recusadas'],motivos=p['motivos'],caminhos_manuais=p['manuais'])


@contextlib.contextmanager
def cwd(p):
    old=pathlib.Path.cwd();os.chdir(p)
    try:yield
    finally:os.chdir(old)


def cmd_operacao(op,entrada):
    # A entrada inteira e os bytes locais são parte da aprovação.
    return ['iniciar',op,json.dumps(entrada,sort_keys=True,ensure_ascii=False)]


def arquivos_entrada(d):
    encontrados=[]
    def visitar(v):
        if isinstance(v,dict):
            for x in v.values():visitar(x)
        elif isinstance(v,list):
            for x in v:visitar(x)
        elif isinstance(v,str) and pathlib.Path(v).is_absolute() and pathlib.Path(v).is_file():encontrados.append(pathlib.Path(v))
    visitar(d);return encontrados


def aprovar(p,op,entrada,literal,resumo):
    c=ler_config(p);contexto=entrada.get('caso') or entrada.get('id') or entrada.get('habilitacao')
    if not contexto:raise ValueError('entrada precisa identificar habilitacao/caso')
    arquivos=[pathlib.Path(p),*arquivos_entrada(entrada)]
    if op=='confirmar-formulario':
        evs=[json.loads(l) for l in pathlib.Path(p).with_name('eventos.jsonl').read_text().splitlines()]
        evs=[e for e in evs if e.get('evento')=='ConferenciaExternaRegistrada' and e.get('contexto')==contexto
             and e.get('habilitacao')==entrada.get('habilitacao') and e.get('objeto_id')==entrada.get('formulario_id')]
        if evs and evs[-1].get('relatorio'):
            reg=evs[-1]['relatorio'];arquivos.append(pathlib.Path(reg['arquivo']))
    hab=entrada.get('habilitacao') or entrada.get('id')
    if hab:
        estado=pathlib.Path(c['base_expedientes'])/H.identificador(hab)/'expediente.json'
        if estado.is_file():arquivos.append(estado)
    r=A.criar(op,c['responsavel'],contexto,literal,resumo,cmd_operacao(op,entrada),arquivos)
    log(p,c,'AprovacaoChatRegistrada',testemunho=A.evento(r))
    return r


def operar(p,op,d,aprovacao):
    c=ler_config(p)
    try:
        if op not in HAB|{'iniciar','abrir','definir-canais','importar','validar','selar','perfil','mcp','registrar-listagem','receber-material','aceitar-minutas','revogar-minutas','caminho-manual','conferir-formulario','confirmar-formulario'}:
            raise ValueError('decisão de método não executável pela sessão: '+op)
        contexto=d.get('caso') or d.get('id') or d.get('habilitacao')
        r=A.conferir(aprovacao,op,c['responsavel'],contexto,cmd_operacao(op,d))
        for arq in [pathlib.Path(p),*arquivos_entrada(d)]:
            if str(arq.absolute()) not in r['arquivos']:raise ValueError('arquivo de entrada não conferido: '+str(arq))
        hab=H.identificador(d.get('habilitacao') or d.get('id') or contexto)
        exp=pathlib.Path(c['base_expedientes'])/hab
        case=pathlib.Path(c['base_casos'])/H.identificador(d.get('caso') or contexto)
        log(p,c,'AprovacaoChatRegistrada',testemunho=A.evento(r))
        if op=='aceitar-minutas':
            if d.get('texto')!='uso as minutas sem ratificação jurídica':raise ValueError('aceitação exige texto literal: uso as minutas sem ratificação jurídica')
            c['aceitacao_minutas']=dict(texto=d['texto'],data=H.agora(),responsavel=c['responsavel'],revogada_em=None,testemunho=A.evento(r))
            escrever(p,c);log(p,c,'MinutasAceitasSemRatificacao',aceitacao=c['aceitacao_minutas'])
            return c['aceitacao_minutas']
        if op=='revogar-minutas':
            if not c.get('aceitacao_minutas'):raise ValueError('aceitação ausente')
            c['aceitacao_minutas']['revogada_em']=H.agora()
            escrever(p,c);log(p,c,'AceitacaoMinutasRevogada',testemunho=A.evento(r))
            return {'revogada':True}
        if op=='perfil':
            inv=d['ferramentas'];profile=d['perfil'];conferir_perfil(profile,inv)
            escrever(pathlib.Path(p).with_name('perfil-mcp.json'),dict(perfil=profile,inventario=inv,aprovacao=r))
            if case.is_dir():
                with cwd(case):
                    pb=json.loads(pathlib.Path('registro/playbook.json').read_text())
                    if not pb.get('operacoes_sessao'):raise ValueError('caso antigo não migra perfil automaticamente')
                    if E.ler()['etapa_atual']!=pb['etapas'][0]['id'] or any(v.get('cumprido') for v in E.ler().get('cumprimentos',{}).values()):raise ValueError('perfil fora do bloco inicial')
                    escrever(case/'registro/ferramentas-externas.json',profile)
                    E.evento('PerfilExternoDefinido',autor=c['responsavel'],sha256=H.digest(json.dumps(profile,sort_keys=True).encode()),testemunho=A.evento(r))
            return profile
        if op=='iniciar':
            H.iniciar(exp,hab,c['responsavel'],d['caso'])
            s=json.loads((exp/'expediente.json').read_text());H.evento(s,'AprovacaoChatRegistrada',testemunho=A.evento(r));H.salvar(exp,s)
            return {'expediente':str(exp)}
        if op in HAB:
            payload=dict(d.get('entrada',{}))
            if op=='gerar':payload.update(templates=str(RAIZ/'eiac-campo/reference/metodo'),navegador=c['navegador'],config_emcia=str(p))
            if 'decisor' in payload and payload['decisor']!=c['responsavel']:raise ValueError('decisor diverge do responsável aprovado')
            # A execução grava o testemunho na mesma transação que o ato.
            return H.executar(exp,op,payload,aprovacao=r)
        if op=='abrir':
            if d.get('desfecho') not in ('prosseguir','prosseguir com restrição'):raise ValueError('decisão de abrir ausente; não prosseguir não abre caso')
            return {'caso':str(B.abrir(d['caso'],c['base_casos'],c['responsavel'],exp))}
        if op=='mcp':return autorizar_mcp(p,d,r)
        if op=='caminho-manual':return caminho_manual(p,c,d,r)
        if op=='conferir-formulario':return conferir_formulario(p,c,d)
        if op=='confirmar-formulario':return confirmar_formulario(p,c,d,r)
        with cwd(case):
            st=E.ler();pb=json.loads(pathlib.Path('registro/playbook.json').read_text())
            if not pb.get('operacoes_sessao'):raise ValueError('caso conserva playbook anterior; não delega estes atos')
            if st.get('etapa_atual')!=pb['etapas'][0]['id'] or any(v.get('cumprido') for v in st.get('cumprimentos',{}).values()):
                raise ValueError('bloco inicial já encerrado; ato reservado ao terminal')
            E.evento('AprovacaoChatRegistrada',**A.evento(r))
            if op=='registrar-listagem':
                import registrar_listagem as L
                return L.registrar(d['entrada'])
            if op=='receber-material':
                import receber as R
                return R.receber(d['arquivo'],d['manifesto'],nova_versao=d.get('nova_versao'))
            if op=='definir-canais':
                import canais as K
                return K.definir(d['entrada'],st,pb)
            if op=='importar':
                import importar_habilitacao as M
                return M.importar(exp,canais_entrada=d.get('canais'))
            if op in ('validar','selar'):
                script=RAIZ/'eiac-nucleo/scripts'/('validar.py' if op=='validar' else 'selar.py')
                args=['--arquivo','caso/00-habilitacao.md'] if op=='validar' else ['--nota',d.get('nota','habilitação importada e conferida')]
                result=subprocess.run([sys.executable,str(script),*args],text=True,capture_output=True)
                if result.returncode:raise ValueError(result.stderr or result.stdout)
                return {'saida':result.stdout}
    except (OSError,ValueError,KeyError,TypeError) as exc:
        log(p,c,'TentativaNegada',operacao=op,motivo=str(exc));raise


def registros_externos(p,hab):
    diario=pathlib.Path(p).with_name('mcp-retornos.json')
    registros=json.loads(diario.read_text()) if diario.exists() else []
    evs=[json.loads(l) for l in pathlib.Path(p).with_name('eventos.jsonl').read_text().splitlines()]
    selecionados=[]
    for reg in registros:
        if reg['habilitacao']!=hab: continue
        sha=H.digest(json.dumps(reg['resultado'],sort_keys=True,ensure_ascii=False).encode())
        chamada_sha=H.digest(json.dumps(reg['chamada'],sort_keys=True,ensure_ascii=False).encode())
        if reg['sha256']!=sha or reg.get('chamada_sha256')!=chamada_sha or not any(
            e.get('evento')=='RetornoMCPRegistrado' and e.get('sha256')==sha and e.get('chamada_sha256')==chamada_sha for e in evs):
            raise ValueError('retorno MCP adulterado ou sem registro íntegro')
        selecionados.append(reg)
    return selecionados


def declaracoes_manuais(p,hab):
    path=pathlib.Path(p).with_name('caminhos-manuais.json')
    regs=json.loads(path.read_text()) if path.exists() else []
    evs=[json.loads(l) for l in pathlib.Path(p).with_name('eventos.jsonl').read_text().splitlines()]
    for r in regs:
        if r['habilitacao']!=hab:continue
        sha=H.digest(json.dumps(r,sort_keys=True,ensure_ascii=False).encode())
        if A.hash_arquivo(r['evidencia'])!=r['evidencia_sha256'] or not any(e.get('evento')=='CaminhoManualDecidido' and e.get('registro_sha256')==sha for e in evs):
            raise ValueError('decisão manual adulterada ou sem evidência íntegra')
        yield r


def escopos(p,c,hab,caso,operacao):
    conhecidos={'workspace_id':[c['workspace_tally']],'calendario_id':[c['calendario_casos']],
                'pasta_id':[],'formulario_id':[],'objeto_id':[],'entregas':[]}
    if operacao=='provisionar':conhecidos['pasta_id'].append(c['pasta_drive'])
    exp=pathlib.Path(c['base_expedientes'])/hab
    if (exp/'expediente.json').exists():
        state=json.loads((exp/'expediente.json').read_text());H.integridade(exp,state)
        if state['caso_reservado']!=caso or state['responsavel']!=c['responsavel']:
            raise ValueError('escopo externo diverge do caso/responsável fixado no expediente')
        conhecidos['formulario_id'].extend(f['formulario'] for f in state['fontes'].values())
    for retorno in registros_externos(p,hab):
        if (retorno['chamada'].get('caso') or hab)!=caso: continue
        for k,v in retorno['ids'].items():conhecidos.setdefault(k,[]).append(v)
        if retorno['chamada'].get('finalidade')=='entregas' and retorno['ids'].get('pasta_id'):
            conhecidos['entregas'].append(retorno['ids']['pasta_id'])
        conhecidos['objeto_id'].extend(retorno['resultado'].get('objetos',[]))
    for manual in declaracoes_manuais(p,hab):
        if manual.get('caso')==caso and manual.get('formulario_id'): conhecidos['formulario_id'].append(manual['formulario_id'])
    case=pathlib.Path(c['base_casos'])/H.identificador(caso)
    if (case/'registro/canais.json').exists():
        import canais_registro as K
        with cwd(case):
            pb=json.loads(pathlib.Path('registro/playbook.json').read_text())
            for canal in K.carregar(pb)['canais']:
                for k,v in canal['ids'].items():conhecidos.setdefault(k,[]).append(v)
                if canal['finalidade']=='entregas' and canal['direcao']=='saida':conhecidos['entregas'].append(canal['ids']['pasta_id'])
    return conhecidos


def autorizar_mcp(p,d,r=None):
    """Conferência anterior à chamada. Não executa API, não inventa retorno."""
    import escopo_externo as S
    c=ler_config(p);arq=pathlib.Path(p).with_name('perfil-mcp.json')
    cfg=json.loads(arq.read_text());conferir_perfil(cfg['perfil'],cfg['inventario'])
    nome=d['ferramenta'];args=d['argumentos']
    regra=S.regra_aplicavel(cfg['perfil'],nome,args)
    hab=H.identificador(d['habilitacao']);caso=H.identificador(d.get('caso') or hab)
    conhecidos=escopos(p,c,hab,caso,regra['operacao'])
    for a in regra['argumentos']:
        val=S.argumento(args,a['campo'])
        vals=conhecidos['entregas'] if a.get('finalidade')=='entregas' else conhecidos.get(a.get('campo_id'),[])
        if a['tipo']=='expressao':ok=isinstance(val,str) and any(re.fullmatch(a['expressao'].replace('{id}',re.escape(v)),val) for v in vals)
        elif a['tipo']=='id_listado':ok=val in conhecidos['objeto_id']
        elif a['tipo']=='constante':ok=val==a['valor']
        else:ok=isinstance(val,str) and val in vals
        if not ok:raise ValueError('id/expressão fora do escopo declarado: '+a['campo'])
    if regra['operacao']=='compartilhar' and args.get('fileId')==c['pasta_drive']:raise ValueError('não compartilhe a raiz EMCIA')
    if regra.get('exige_aprovacao') and r is None:raise ValueError('efeito externo sem aprovação no chat registrada')
    if r is not None:A.conferir(r,'mcp',c['responsavel'],caso,cmd_operacao('mcp',d))
    evs=[json.loads(l) for l in pathlib.Path(p).with_name('eventos.jsonl').read_text().splitlines()]
    if nome=='mcp__tally__publish_form': conferir_relatorio_vigente(p,c,d,evs)
    # Os mesmos parâmetros, inclusive papel e destinatário, pertencem ao testemunho.
    aprovado=dict(evento=cfg['perfil']['evento_aprovacao'],ferramenta=nome,argumentos=args,autor=c['responsavel'],contexto=caso,testemunho=A.evento(r) if r else None)
    S.conferir_eventos(cfg['perfil'],regra,nome,args,[*evs,aprovado],c['responsavel'],caso)
    log(p,c,'ChamadaMCPAutorizada',ferramenta=nome,argumentos=args,habilitacao=hab,chamada=d,testemunho=A.evento(r) if r else None)
    case=pathlib.Path(c['base_casos'])/caso
    if case.is_dir() and regra.get('exige_aprovacao'):
        with cwd(case): E.evento(cfg['perfil']['evento_aprovacao'],**{k:v for k,v in aprovado.items() if k!='evento'})
    return dict(autorizada=True,ferramenta=nome,argumentos=args)


def registrar_retorno(p,chamada,resultado):
    import escopo_externo as S
    c=ler_config(p);logfile=pathlib.Path(p).with_name('eventos.jsonl')
    evs=[json.loads(l) for l in logfile.read_text().splitlines()]
    if not any(e.get('evento')=='ChamadaMCPAutorizada' and e.get('chamada')==chamada for e in evs):
        raise ValueError('retorno sem chamada aprovada correspondente')
    cfg=json.loads(pathlib.Path(p).with_name('perfil-mcp.json').read_text())
    conferir_perfil(cfg['perfil'],cfg['inventario'])
    regra=S.regra_aplicavel(cfg['perfil'],chamada['ferramenta'],chamada['argumentos'])
    nome=chamada['ferramenta']
    tipos=({'pasta_id'} if nome=='mcp__claude_ai_Google_Drive__create_file' and regra['operacao']=='provisionar'
           else {'formulario_id'} if nome=='mcp__tally__create_new_form' else set())
    ids=resultado.get('ids',{})
    if not isinstance(ids,dict) or not set(ids)<=tipos:raise ValueError('retorno não pode declarar ids de outra operação/ferramenta')
    for v in ids.values():
        if not isinstance(v,str) or not re.fullmatch(r'[A-Za-z0-9_.@:+-]+',v):raise ValueError('id de retorno inválido')
    objetos=resultado.get('objetos',[])
    if not isinstance(objetos,list) or len(set(objetos))!=len(objetos):raise ValueError('objetos da listagem inválidos')
    if objetos or 'conteiner_id' in resultado:
        if regra['operacao']!='listar':raise ValueError('objetos precisam vir de listagem restrita')
        conteiner=resultado['conteiner_id']
        if not isinstance(conteiner,str) or not re.fullmatch(r'[A-Za-z0-9_.@:+-]+',conteiner):raise ValueError('contêiner inválido')
        if not any(a['tipo']=='expressao' and re.fullmatch(a['expressao'].replace('{id}',re.escape(conteiner)),S.argumento(chamada['argumentos'],a['campo'])) for a in regra['argumentos']):
            raise ValueError('contêiner não corresponde à listagem autorizada')
        for v in objetos:
            if not isinstance(v,str) or not re.fullmatch(r'[A-Za-z0-9_.@:+-]+',v):raise ValueError('objeto da listagem inválido')
    reg=pathlib.Path(p).with_name('mcp-retornos.json');anteriores=json.loads(reg.read_text()) if reg.exists() else []
    raw=json.dumps(resultado,sort_keys=True,ensure_ascii=False).encode()
    chamada_sha=H.digest(json.dumps(chamada,sort_keys=True,ensure_ascii=False).encode())
    anteriores.append(dict(habilitacao=chamada['habilitacao'],chamada=chamada,ids=ids,resultado=resultado,sha256=H.digest(raw),chamada_sha256=chamada_sha))
    escrever(reg,anteriores);log(p,c,'RetornoMCPRegistrado',sha256=H.digest(raw),chamada_sha256=chamada_sha,ferramenta=nome)
    if regra['operacao']=='listar':log(p,c,'ListagemExternaRegistrada',conteiner_id=resultado.get('conteiner_id'),objetos=objetos,sha256=H.digest(raw))
    if nome=='mcp__tally__load_form':
        evento_conferencia(p,c,chamada,chamada['argumentos']['formId'],resultado='aguardando-comparacao',diferencas=['nova leitura load_form aguarda comparação e conferido'])


def evento_conferencia(p,c,d,formulario,**dados):
    evento=dict(objeto_id=formulario,contexto=d['caso'],habilitacao=d['habilitacao'],**dados)
    log(p,c,'ConferenciaExternaRegistrada',**evento)
    case=pathlib.Path(c['base_casos'])/H.identificador(d['caso'])
    if case.is_dir():
        with cwd(case):E.evento('ConferenciaExternaRegistrada',autor=c['responsavel'],**evento)


def leitura_formulario(p,d,formulario):
    regs=[r for r in registros_externos(p,d['habilitacao'])
          if r['chamada'].get('caso')==d['caso'] and r['chamada']['ferramenta']=='mcp__tally__load_form'
          and r['chamada']['argumentos']=={'formId':formulario}]
    if not regs:raise ValueError('conferência exige retorno load_form do formulário declarado')
    return regs[-1]


def conferir_formulario(p,c,d):
    import conferencia_formulario as F
    formulario=d['formulario_id'];modelo=d['modelo']
    if modelo not in ('habilitacao','triagem','ciclo'):raise ValueError('modelo não declarado em reference/formularios')
    if formulario not in escopos(p,c,d['habilitacao'],d['caso'],'ler')['formulario_id']:
        raise ValueError('formulário fora do escopo declarado')
    leitura=leitura_formulario(p,d,formulario)
    arq_modelo=RAIZ/'eiac-campo/reference/formularios'/(modelo+'.json')
    sha_modelo=A.hash_arquivo(arq_modelo)
    comp=F.comparar(json.loads(arq_modelo.read_text()),leitura['resultado'].get('resposta',{}),formulario,c['workspace_tally'])
    reg=dict(habilitacao=d['habilitacao'],caso=d['caso'],formulario_id=formulario,modelo=modelo,
             modelo_sha256=sha_modelo,retorno_sha256=leitura['sha256'])
    md=F.markdown(reg,comp).encode('utf-8');sha=H.digest(md)
    pasta=pathlib.Path(p).parent/'conferencias'
    if any(x.is_symlink() for x in (pasta,*pasta.parents)):raise ValueError('relatório não admite symlink')
    pasta.mkdir(exist_ok=True,mode=0o700);arquivo=pasta/(sha+'.md')
    if arquivo.exists():
        if A.hash_arquivo(arquivo)!=sha:raise ValueError('relatório existente adulterado')
    else:
        with arquivo.open('xb') as f:f.write(md)
    reg.update(arquivo=str(arquivo.absolute()),sha256=sha,diferencas=comp['diferencas'])
    evento_conferencia(p,c,d,formulario,resultado='divergente' if comp['diferencas'] else 'aguardando-conferido',
                       diferencas=comp['diferencas'],relatorio=reg,evidencia_sha256=sha)
    return reg


def conferir_relatorio_vigente(p,c,d,eventos):
    formulario=d.get('formulario_id') or d.get('argumentos',{}).get('formId')
    evs=[e for e in eventos if e.get('evento')=='ConferenciaExternaRegistrada'
         and e.get('objeto_id')==formulario and e.get('contexto')==d['caso']
         and e.get('habilitacao')==d['habilitacao'] and e.get('autor')==c['responsavel']]
    if not evs:return None
    ev=evs[-1];reg=ev.get('relatorio')
    if reg:
        import conferencia_formulario as F
        modelo=reg['modelo']
        if modelo not in ('habilitacao','triagem','ciclo'):raise ValueError('relatório com modelo não declarado')
        arq_modelo=RAIZ/'eiac-campo/reference/formularios'/(modelo+'.json')
        leitura=leitura_formulario(p,d,formulario)
        if leitura['sha256']!=reg['retorno_sha256'] or A.hash_arquivo(arq_modelo)!=reg['modelo_sha256']:
            raise ValueError('relatório desatualizado: retorno/modelo mudou; execute conferir-formulario')
        comp=F.comparar(json.loads(arq_modelo.read_text()),leitura['resultado'].get('resposta',{}),formulario,c['workspace_tally'])
        if (A.hash_arquivo(reg['arquivo'])!=reg['sha256'] or H.digest(F.markdown(reg,comp).encode())!=reg['sha256']
            or reg['sha256']!=ev['evidencia_sha256'] or reg['diferencas']!=comp['diferencas']):
            raise ValueError('relatório de conferência adulterado')
    return ev


def confirmar_formulario(p,c,d,r):
    if r['literal']!='conferido':raise ValueError('confirmação exige texto literal: conferido')
    evs=[json.loads(l) for l in pathlib.Path(p).with_name('eventos.jsonl').read_text().splitlines()]
    ev=conferir_relatorio_vigente(p,c,d,evs)
    if not ev or not ev.get('relatorio'):raise ValueError('execute conferir-formulario antes de confirmar-formulario')
    reg=ev['relatorio']
    if d.get('relatorio_sha256')!=reg['sha256']:raise ValueError('hash do relatório diverge da confirmação')
    if reg['diferencas']:raise ValueError('conferência divergente: '+str(reg['diferencas']))
    if reg['arquivo'] not in r['arquivos']:raise ValueError('relatório sem hash na aprovação')
    evento_conferencia(p,c,d,d['formulario_id'],resultado='conferido',diferencas=[],relatorio=reg,
                       evidencia_sha256=reg['sha256'],testemunho=A.evento(r))
    return dict(conferido=True,relatorio=reg)


def caminho_manual(p,c,d,r):
    cfg=json.loads(pathlib.Path(p).with_name('perfil-mcp.json').read_text());conferir_perfil(cfg['perfil'],cfg['inventario'])
    opcoes=[m for m in cfg['perfil']['manuais'] if m['passo']==d.get('passo')]
    if len(opcoes)!=1:raise ValueError('passo manual não corresponde ao relatório da calibração')
    if d.get('decisao')!='executar manualmente':raise ValueError('decisão manual explícita ausente')
    evidencia=pathlib.Path(d['evidencia']);sha=A.hash_arquivo(evidencia)
    formulario=d.get('formulario_id')
    if formulario is not None and (not isinstance(formulario,str) or not re.fullmatch(r'[A-Za-z0-9_.@:+-]+',formulario)):
        raise ValueError('formulário manual exige id')
    if d['passo']=='preparar-formulario' and not formulario:raise ValueError('conferência manual exige formulário declarado')
    if d['passo']=='preparar-formulario':
        if r['literal']!='conferido':raise ValueError('confirmação manual exige texto literal: conferido')
        raw=evidencia.read_bytes()
        if not raw.startswith(b'%PDF-') or b'%%EOF' not in raw[-2048:]:raise ValueError('conferência manual exige PDF completo')
        evs=[json.loads(l) for l in pathlib.Path(p).with_name('eventos.jsonl').read_text().splitlines()]
        ev=conferir_relatorio_vigente(p,c,d,evs)
        if ev and ev.get('diferencas') and ev.get('resultado')=='divergente':
            raise ValueError('corrija divergências antes da publicação: '+str(ev['diferencas']))
    if d.get('workspace_id',c['workspace_tally'])!=c['workspace_tally']:raise ValueError('workspace manual diverge da configuração')
    reg=dict(opcoes[0],habilitacao=d['habilitacao'],caso=d['caso'],decisao=d['decisao'],autor=c['responsavel'],data=H.agora(),
             evidencia=str(evidencia.absolute()),evidencia_sha256=sha,formulario_id=formulario,testemunho=A.evento(r))
    arquivo=pathlib.Path(p).with_name('caminhos-manuais.json');anteriores=json.loads(arquivo.read_text()) if arquivo.exists() else []
    anteriores.append(reg);escrever(arquivo,anteriores)
    registro_sha=H.digest(json.dumps(reg,sort_keys=True,ensure_ascii=False).encode())
    log(p,c,'CaminhoManualDecidido',**{k:v for k,v in reg.items() if k not in ('autor','data')},registro_sha256=registro_sha)
    if d['passo']=='preparar-formulario':
        evento=dict(objeto_id=formulario,contexto=d['caso'],habilitacao=d['habilitacao'],resultado='conferido',evidencia_sha256=sha,testemunho=A.evento(r))
        log(p,c,'ConferenciaExternaRegistrada',**evento)
        case=pathlib.Path(c['base_casos'])/H.identificador(d['caso'])
        if case.is_dir():
            with cwd(case):E.evento('ConferenciaExternaRegistrada',autor=c['responsavel'],**evento)
    return reg


def retomar(p,hab,caso):
    c=ler_config(p);escrever(pathlib.Path(p).with_name('sessao.json'),dict(habilitacao=H.identificador(hab),caso=H.identificador(caso)))
    exp=pathlib.Path(c['base_expedientes'])/H.identificador(hab)
    case=pathlib.Path(c['base_casos'])/H.identificador(caso)
    if not (exp/'expediente.json').exists():return {'proximo':'iniciar','expediente':str(exp)}
    s=json.loads((exp/'expediente.json').read_text());H.integridade(exp,s)
    if s.get('recusa'):proximo='não prosseguir; aguardar decisão humana'
    elif any(v['estado']=='aberta' for v in s['pendencias'].values()):proximo='rodadas'
    elif not s['revisao']:proximo='consolidar/conferir carta'
    elif not s['documentos'] or not all(v[-1]['vigente'] for v in s['documentos'].values()):proximo='gerar'
    elif not H.completa(s):proximo='conferir PDFs/assinaturas'
    elif not s['acessos']:proximo='acessos'
    elif not case.exists():proximo='decisão de abrir'
    elif not (case/'registro/habilitacao.json').exists():proximo='provisionar/definir/importar'
    elif not (case/'caso/00-habilitacao.md').exists():proximo='validar'
    else:
        import playbook as P
        with cwd(case):
            pb,erro=P.carregar();ok,motivo=P.selo_confirmado_apos_evento(pb,pb['etapas'][0]['id'],E.eventos()) if not erro else (False,erro)
        proximo='saída conferida' if ok else 'selar'
    return dict(proximo=proximo,expediente=str(exp),caso=str(case),estado=s)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('operacao',choices=['calibrar','ambiente','configurar','aprovar','executar','retomar','retorno'])
    ap.add_argument('--config',type=pathlib.Path,default=CONFIG);ap.add_argument('--entrada',type=pathlib.Path,required=True)
    ap.add_argument('--aprovacao',type=pathlib.Path)
    a=ap.parse_args()
    try:
        d=json.loads(a.entrada.read_text())
        if a.operacao=='calibrar':r=calibrar(d)
        elif a.operacao=='configurar':r=configurar(a.config,d)
        elif a.operacao=='ambiente':r=ambiente(ler_config(a.config),d['ferramentas'])
        elif a.operacao=='aprovar':r=aprovar(a.config,d['operacao'],d['entrada'],d['literal'],d['resumo'])
        elif a.operacao=='executar':r=operar(a.config,d['operacao'],d['entrada'],A.ler(a.aprovacao) if a.aprovacao else None)
        elif a.operacao=='retorno':r=registrar_retorno(a.config,d['chamada'],d['resultado'])
        else:r=retomar(a.config,d['habilitacao'],d['caso'])
        print(json.dumps(r,ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        try:log(a.config,ler_config(a.config),'TentativaNegada',operacao=a.operacao,motivo=str(exc))
        except (OSError,ValueError,KeyError,TypeError):print(json.dumps(dict(evento='TentativaNegada',motivo=str(exc))),file=sys.stderr)
        ap.exit(1,'Recusado: '+str(exc)+'\n')

if __name__=='__main__':main()
