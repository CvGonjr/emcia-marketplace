"""Uma chamada até a próxima informação ou confirmação humana, decisão 047."""
import contextlib
import copy
import fcntl
import io
import json
import pathlib
import subprocess
import sys
import habilitacao as H
import habilitacao_lotes as L
import formularios_permanentes as F
import aprovacao as A


def ler(exp):
    s = json.loads((exp/'expediente.json').read_text()); H.integridade(exp,s)
    return s


def salvar_plano(exp, chave, plano):
    s = ler(exp)
    if s.setdefault('fluxo',{}).get(chave) != plano:
        s['fluxo'][chave] = copy.deepcopy(plano)
        H.evento(s,'PlanoAdministrativoPreparado',plano=chave,sha256=H.digest(json.dumps(plano,sort_keys=True,ensure_ascii=False).encode()))
        H.salvar(exp,s)


def confirmar(d,ponto):
    r = d.get('aprovacao')
    if r is None: return None
    H.exigir(isinstance(r,dict) and r.get('ponto')==ponto and r.get('confirmado') is True,
             'aprovação explícita ausente para o ponto atual: '+ponto)
    return H.texto(r.get('trecho'))


def resumo_documentos(exp, refs):
    return [dict(documento=doc,pdf=str(exp/refs[doc]['pdf']['caminho']),
                 markdown=str(exp/refs[doc]['markdown']['caminho']),sha256=refs[doc]['pdf']['sha256']) for doc in H.CODIGOS_HAB]


def material(s):
    return {k:s.get(k) for k in ('responsavel','habilitacao','caso_reservado','fontes','campos','documentos','revisao','acessos','tratamento','pendencias','recusa')}


def plano_abertura(config,c,exp,d):
    import iniciar as I
    import canais as K
    s=ler(exp); import importar_habilitacao as M
    M.conferir(exp,d['caso'],c['responsavel'])
    pbpath=I.RAIZ/'eiac-campo/template-caso/registro/playbook.json'
    pb=json.loads(pbpath.read_text()); canais=K.declaracao_inicial(config,c,d['caso'],pb)
    inventario=pathlib.Path(d.get('inventario',pathlib.Path.home()/'emcia-op/ensaio/inventario-mcp.json')).expanduser().absolute()
    sha=A.hash_arquivo(inventario);inv=json.loads(inventario.read_text());perfil=I.calibrar(inv)
    proposta=H.guardar(exp,json.dumps(dict(perfil=perfil,inventario=inv),sort_keys=True,ensure_ascii=False).encode(),'.json')
    return dict(perfil=proposta,inventario_arquivo=str(inventario),inventario_sha256=sha,
                habilitacao=d['habilitacao'],caso=d['caso'],destino=str(pathlib.Path(c['base_casos'])/d['caso']),
                canais=canais,material_sha256=H.digest(json.dumps(material(s),sort_keys=True,ensure_ascii=False).encode()),
                playbook_sha256=A.hash_arquivo(pbpath),desfecho=H.aplicar(exp,copy.deepcopy(s),'preparar-0d',{})['desfecho_proposto'])


def abrir(config,c,exp,d,literal):
    import iniciar as I
    import canais as K
    import importar_habilitacao as M
    import playbook as P
    H.exigir(literal is not None or ler(exp).get('fluxo',{}).get('abertura'), 'terceira aprovação de abertura ausente')
    s=ler(exp); case=pathlib.Path(c['base_casos'])/d['caso']; reg=s.get('fluxo',{}).get('abertura')
    if reg is None:
        H.exigir(not case.exists(),'caso já existe; não adota nem migra um caso anterior')
        plano=s['fluxo']['plano_abertura']
        H.exigir(plano['material_sha256']==H.digest(json.dumps(material(s),sort_keys=True,ensure_ascii=False).encode()), 'habilitação mudou; confira novamente a abertura')
        snapshot=H.guardar(exp,json.dumps(material(s),sort_keys=True,ensure_ascii=False).encode(),'.json')
        arquivos=[config,exp/snapshot['caminho'],exp/plano['perfil']['caminho'],pathlib.Path(plano['inventario_arquivo']),I.RAIZ/'eiac-campo/template-caso/registro/playbook.json']
        arquivos.extend(I.RAIZ/'eiac-campo/reference/metodo'/nome for nome in I.B.pacote())
        r=A.criar('abrir-simplificado',c['responsavel'],d['caso'],literal,
            'Abrir caso, aprovar perfil/escopo apresentados, declarar Tally/calendário, importar, gravar 00-habilitacao e selar; Drive do caso em P2',
            ['abrir-simplificado',json.dumps(plano,sort_keys=True,ensure_ascii=False)],arquivos)
        reg=dict(plano=plano,testemunho=r,snapshot=snapshot)
        s['fluxo']['abertura']=reg;H.evento(s,'AprovacaoLoteRegistrada',operacao='abrir-simplificado',testemunho=A.evento(r));H.salvar(exp,s)
        I.log(config,c,'AprovacaoLoteRegistrada',habilitacao=d['habilitacao'],caso=d['caso'],testemunho=A.evento(r))
    plano=reg['plano'];r=reg['testemunho']
    A.conferir(r,'abrir-simplificado',c['responsavel'],d['caso'],['abrir-simplificado',json.dumps(plano,sort_keys=True,ensure_ascii=False)])
    H.exigir(plano['material_sha256']==H.digest(json.dumps(material(ler(exp)),sort_keys=True,ensure_ascii=False).encode()), 'habilitação mudou depois da aprovação de abertura')
    if not case.exists():
        with contextlib.redirect_stdout(io.StringIO()):I.B.abrir(d['caso'],c['base_casos'],c['responsavel'],exp)
    with I.cwd(case):
        st=I.E.ler();pb,erro=P.carregar()
        H.exigir(not erro and st['caso']==d['caso'] and st['responsavel']==c['responsavel'],'caso diverge da abertura aprovada')
        H.exigir(st['etapa_atual']=='F0' and not any(v.get('cumprido') for v in st['cumprimentos'].values()),'abertura simplificada não muda o percurso iniciado')
        if not any(e.get('evento')=='AprovacaoLoteRegistrada' and e.get('operacao')=='abrir-simplificado' for e in I.E.eventos()):
            I.E.evento('AprovacaoLoteRegistrada',operacao='abrir-simplificado',autor=c['responsavel'],testemunho=A.evento(r))
        cfg=json.loads(H.ler_arquivo(exp,plano['perfil']));I.conferir_perfil(cfg['perfil'],cfg['inventario'])
        cfg['aprovacao']=r
        perfilpath=pathlib.Path(config).with_name('perfil-mcp.json')
        atual=case/'registro/ferramentas-externas.json'
        definidos=[e for e in I.E.eventos() if e.get('evento')=='PerfilExternoDefinido']
        if not definidos:
            I.escrever(perfilpath,cfg);I.escrever(atual,cfg['perfil'])
            I.E.evento('PerfilExternoDefinido',autor=c['responsavel'],sha256=A.hash_arquivo(atual),testemunho=A.evento(r))
            I.log(config,c,'PerfilExternoDefinido',caso=d['caso'],fase='caso',testemunho=A.evento(r))
        else:H.exigir(json.loads(atual.read_text())==cfg['perfil'],'perfil do caso diverge da abertura aprovada')
        if not (case/'registro/canais.json').exists():K.definir(plano['canais'],st,pb)
        if not (case/'registro/habilitacao.json').exists():M.importar(exp)
        else:
            vigente=json.loads((case/'registro/habilitacao.json').read_text())['vigente']
            evs=[e for e in I.E.eventos() if e.get('evento')=='HabilitacaoImportada']
            H.exigir(evs and evs[-1]['registro_sha256']==A.hash_arquivo(case/'registro/habilitacao.json')
                     and vigente['habilitacao']==d['habilitacao'],'importação divergente; não reimporta silenciosamente')
        draft=case/'rascunho/00-habilitacao.md';destino=case/'caso/00-habilitacao.md'
        eventos=I.E.eventos()
        if not destino.exists() or not any(e.get('evento')=='AssercaoRegistrada' and e.get('arquivo')=='caso/00-habilitacao.md' for e in eventos):
            cmd=[sys.executable,str(I.RAIZ/'eiac-nucleo/scripts/validar.py'),'--arquivo','caso/00-habilitacao.md']
            resultado=subprocess.run(cmd,capture_output=True,text=True)
            H.exigir(resultado.returncode==0,resultado.stderr or resultado.stdout)
        H.exigir(destino.read_bytes()==draft.read_bytes(),'00-habilitacao diverge da importação')
        ok,motivo=P.selo_confirmado_apos_evento(pb,'F0',I.E.eventos())
        if not ok:
            resultado=subprocess.run([sys.executable,str(I.RAIZ/'eiac-nucleo/scripts/selar.py'),'--nota','habilitação simplificada importada e conferida'],capture_output=True,text=True)
            H.exigir(resultado.returncode==0,resultado.stderr or resultado.stdout)
    import saida_inicial as S
    saida=S.conferir(exp,case);H.exigir(saida['liberado'],'checklist de saída incompleto: '+str([x['item'] for x in saida['itens'] if not x['presente']]))
    return dict(proximo='F0',resumo='F0 liberado; apuração, sessões e decidir-prosseguimento permanecem no terminal.',caso=str(case),aprovacoes=3,pendencias=saida['pendencias'])


def lacunas(s):
    controles={'caso_id','responsavel_emcia','status_assinatura','versao_assinada','evidencia_assinatura','data_assinatura_cliente','data_assinatura_emcia'}
    requeridos=set()
    import iniciar as I
    for doc,nome in H.TEMPLATES.items():
        md=H.documento_cliente((I.RAIZ/'eiac-campo/reference/metodo'/nome).read_text(),doc)
        requeridos.update(H.TOKEN.findall(md))
    return sorted(requeridos-controles-set(s['campos']))


def executar(config,d):
    import iniciar as I
    import acessos_administrativos as C
    c=I.ler_config(config);hab=H.identificador(d['habilitacao']);caso=H.identificador(d['caso'])
    if d.get('passo')=='P2':
        import provisionamento_p2 as Q
        return Q.proximo(config,d)
    I.retomar(config,hab,caso)
    form=F.validar(config,c,'habilitacao')
    # Nome operacional; o id conferido na configuração determina a seleção.
    formulario=dict(nome='EMCIA — Habilitação — formulário permanente',
                    id=form['formId'],link=F.link(form,caso))
    exp=pathlib.Path(c['base_expedientes'])/hab
    if not (exp/'expediente.json').exists():
        H.iniciar(exp,hab,c['responsavel'],caso)
        H.executar(exp,'tratamento-padrao',{'config_emcia':str(config)})
    s=ler(exp)
    H.exigir(s['responsavel']==c['responsavel'] and s['caso_reservado']==caso,'expediente pertence a outro responsável ou caso')
    H.exigir(not s.get('recusa'),'não prosseguir; retomada depende de decisão humana')
    if s.get('fluxo',{}).get('abertura'):
        return abrir(config,c,exp,d,None)
    if c.get('fluxo_habilitacao')!='simplificado':
        c['fluxo_habilitacao']='simplificado';I.escrever(config,c)
    if not s.get('tratamento'):H.executar(exp,'tratamento-padrao',{'config_emcia':str(config)})
    if not s['fontes'] and not (d.get('exportacao') or d.get('coleta')=='csv'):
        args={'formId':form['formId']}
        return dict(proximo='coletar-submissoes',resumo='Envie o link e leia as respostas pelo Tally. Passe todas as páginas ao script: ele gera automaticamente o CSV somente deste caso no expediente, sem download ou depósito pelo engenheiro.',
                    formulario=formulario,link=formulario['link'],ferramenta='mcp__tally__fetch_submissions',argumentos=args,
                    chamada=dict(habilitacao=hab,caso=caso,ferramenta='mcp__tally__fetch_submissions',argumentos=args))
    if not s['fontes']:
        base=pathlib.Path(c.get('entrada_dir',pathlib.Path.home()/'emcia-op/entrada'))
        arquivos=[pathlib.Path(d['exportacao'])] if d.get('exportacao') else sorted(base.glob('*.csv'))
        if len(arquivos)!=1:
            return dict(proximo='depositar-exportacao',resumo='Use o formulário permanente configurado para este caso e indique o caminho original do CSV. Coleta direta por fetch_submissions é o padrão; pasta de entrada é alternativa.',
                        formulario=formulario,link=formulario['link'])
        H.executar(exp,'receber-exportacao',dict(config_emcia=str(config),arquivo=str(arquivos[0]),id='S1',
            **{k:d[k] for k in ('submissao','coluna_submissao','coluna_respondente','respondente') if k in d}))
        s=ler(exp)
    if d.get('mensagem'):
        m=d['mensagem']
        if m['id'] not in s['fontes']:H.executar(exp,'receber-mensagem',m)
        else:
            fonte=s['fontes'][m['id']];anterior=json.loads(H.ler_arquivo(exp,fonte['arquivo']))
            H.exigir(all(anterior.get(k)==m.get(k) for k in ('texto','pergunta','respondente')),'mensagem mudou; registre nova rodada com outro id')
        s=ler(exp)
    if d.get('campos') and d['campos']!=s['campos']:
        H.executar(exp,'consolidar',{'campos':d['campos']});s=ler(exp)
    if d.get('plano_documentos'):
        plano=dict(d['plano_documentos'],geracao=dict(templates=str(I.RAIZ/'eiac-campo/reference/metodo'),navegador=c['navegador'],config_emcia=str(config)))
        salvar_plano(exp,'plano_documentos',plano);s=ler(exp)
    if not s['documentos'] or not all(s['documentos'].get(doc) and s['documentos'][doc][-1]['vigente'] and s['documentos'][doc][-1]['liberacao'] for doc in H.CODIGOS_HAB):
        faltas=lacunas(s)
        if faltas or not s.get('fluxo',{}).get('plano_documentos'):
            H.exigir(not d.get('aprovacao'),'aprovação prematura; complete campos e plano da revisão')
            return dict(proximo='esclarecer',resumo='Complete os campos com fonte; cole a resposta como mensagem. Informe qualificação, signatários, competência e painel.',
                        lacunas=faltas,fonte=str(exp/s['fontes']['S1']['arquivo']['caminho']))
        plano=s['fluxo']['plano_documentos']
        if not s.get('rascunhos_documentos'):
            H.executar(exp,'preparar-documentos',plano['geracao']);s=ler(exp)
        literal=confirmar(d,'documentos')
        if literal is None:
            return dict(proximo='aprovar-documentos',resumo='Confira os três PDFs e a qualificação; uma confirmação cobre revisar, gerar e liberar.',documentos=resumo_documentos(exp,s['rascunhos_documentos']))
        r=L.criar_aprovacao(exp,'aprovar-documentos',plano,literal)
        H.executar(exp,'aprovar-documentos',dict(plano=plano,testemunho=r));s=ler(exp)
        d=dict(d);d.pop('aprovacao',None)
    if not H.completa(s):
        if d.get('plano_assinaturas'):salvar_plano(exp,'plano_assinaturas',d['plano_assinaturas']);s=ler(exp)
        if not s.get('rascunhos_assinaturas'):
            base=pathlib.Path(c.get('entrada_dir',pathlib.Path.home()/'emcia-op/entrada'))
            if 'assinados' not in d and not any(p for p in base.glob('*.pdf') if not p.name.endswith('-relatorio.pdf')):
                H.exigir(not d.get('aprovacao'),'assinaturas ausentes; aprovação não substitui recebimento')
                return dict(proximo='depositar-assinaturas',resumo='Receba os três PDFs pelo Drive ou indique os caminhos originais; não é preciso mover para a entrada. Informe signatários, datas e referência.',
                            recebimento={'assinados':'lista dos três caminhos locais, originais ou baixados pela sessão', 'evidencias':'mapa opcional HAB-01/02/03 para caminhos dos relatórios'})
            H.executar(exp,'preparar-assinaturas',dict(config_emcia=str(config), **{k:d[k] for k in ('assinados','evidencias') if k in d}));s=ler(exp)
        plano=s.get('fluxo',{}).get('plano_assinaturas')
        if not plano:return dict(proximo='esclarecer-assinaturas',resumo='Informe nomes, papéis, datas reais de assinatura e referência do retorno.')
        literal=confirmar(d,'assinaturas')
        if literal is None:
            return dict(proximo='aprovar-assinaturas',resumo='Confira assinaturas e evidências; uma confirmação cobre os três retornos.',
                        documentos=[dict(documento=doc,assinado_sha256=s['rascunhos_assinaturas'][doc]['arquivo']['sha256'],
                            enviado_sha256=s['rascunhos_assinaturas'][doc]['enviado_sha256']) for doc in H.CODIGOS_HAB])
        r=L.criar_aprovacao(exp,'aprovar-assinaturas',plano,literal)
        H.executar(exp,'aprovar-assinaturas',dict(plano=plano,testemunho=r));s=ler(exp)
        d=dict(d);d.pop('aprovacao',None)
    if not s['acessos']:
        if not s.get('proposta_acessos'):H.executar(exp,'planejar-acessos',{});s=ler(exp)
        if not d.get('acessos'):
            return dict(proximo='confirmar-acessos',resumo='Confirme ou corrija a matriz numa mensagem, com patrocinador, executor e sessão.',matriz=str(exp/s['proposta_acessos']['relatorio']['caminho']),sha256=s['proposta_acessos']['relatorio']['sha256'])
        H.executar(exp,'confirmar-acessos',d['acessos']);s=ler(exp)
    if not any(e.get('operacao')=='preparar-0d' for e in s['eventos']):H.executar(exp,'preparar-0d',{})
    s=ler(exp)
    if not s.get('fluxo',{}).get('plano_abertura'):
        salvar_plano(exp,'plano_abertura',plano_abertura(config,c,exp,d));s=ler(exp)
    literal=confirmar(d,'abertura')
    if literal is None:
        return dict(proximo='aprovar-abertura',resumo='Aprovar perfil/escopo, abrir, declarar Tally/calendário, importar, validar e selar. Drive do caso em P2.',
                    perfil=str(exp/s['fluxo']['plano_abertura']['perfil']['caminho']),
                    perfil_sha256=s['fluxo']['plano_abertura']['perfil']['sha256'],
                    escopo=s['fluxo']['plano_abertura']['canais'],
                    destino=s['fluxo']['plano_abertura']['destino'],desfecho=s['fluxo']['plano_abertura']['desfecho'])
    return abrir(config,c,exp,d,literal)


def proximo(config,d):
    import iniciar as I
    c=I.ler_config(config);caso=H.identificador(d['caso'])
    lock=pathlib.Path(config).with_name('fluxo-'+caso+'.lock')
    if any(p.is_symlink() for p in (lock,*lock.parents)):raise H.Recusa('trava do fluxo contém symlink')
    with lock.open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        try:return executar(config,d)
        except (OSError,ValueError,KeyError,TypeError,AttributeError,subprocess.SubprocessError) as exc:
            I.log(config,c,'TentativaNegada',operacao='proximo',caso=caso,motivo=str(exc));raise H.Recusa(str(exc)) from exc
