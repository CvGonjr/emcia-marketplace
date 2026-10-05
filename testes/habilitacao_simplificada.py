"""Contrato administrativo simplificado; negativas antes do percurso sintético."""
import copy
import csv
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'eiac-campo/scripts'))
import iniciar as I
import habilitacao as H

class Simplificada(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name); self.cfg = self.base/'config.json'
        I.configurar(self.cfg, dict(responsavel='Pessoa Engenheira', base_casos=str(self.base/'casos'),
            base_expedientes=str(self.base/'expedientes'), workspace_tally='WORK', pasta_drive='ROOT',
            calendario_casos='CAL', navegador='google-chrome'))
        self.exp = self.base/'expedientes/HAB'; self.entrada = self.base/'entrada'; self.entrada.mkdir()
        self.csv = self.entrada/'exportacao.csv'
        c = I.ler_config(self.cfg); c['entrada_dir'] = str(self.entrada); I.escrever(self.cfg, c)

    def op(self, nome, literal='conferido', **extra):
        d = dict(habilitacao='HAB', caso='CASO', **extra)
        return I.operar(self.cfg, nome, d, I.aprovar(self.cfg, nome, d, literal, 'Controle sintético'))

    def permanente(self):
        inv = json.loads((ROOT/'testes/apoio/inventario-mcp-real.json').read_text())
        self.op('perfil', ferramentas=inv, perfil=I.calibrar(inv)); self.op('iniciar', id='HAB')
        d = dict(habilitacao='HAB', caso='CASO', ferramenta='mcp__tally__create_new_form',
                 argumentos={'title':'Sintético', 'workspaceId':'WORK'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        I.registrar_retorno(self.cfg, d, {'ids':{'formulario_id':'FORM'}})
        d.update(ferramenta='mcp__tally__load_form', argumentos={'formId':'FORM'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        raw = json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())
        I.registrar_retorno(self.cfg, d, {'resposta':raw})
        rel = self.op('conferir-formulario', formulario_id='FORM', modelo='habilitacao')
        self.op('confirmar-formulario', formulario_id='FORM', relatorio_sha256=rel['sha256'])
        self.op('formulario-permanente', formulario_id='FORM', modelo='habilitacao')
        return rel

    def test_01_permanente_sem_conferencia_recusa(self):
        import formularios_permanentes as F
        with self.assertRaisesRegex(ValueError, 'conferido'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_02_contrato_anterior_recusa(self):
        import formularios_permanentes as F
        self.permanente()
        original = F.modelo
        arquivo = self.base/'novo-contrato.json'
        modelo = json.loads(original('habilitacao').read_text()); modelo['perguntas'][0]['pergunta'] += ' alterado'
        arquivo.write_text(json.dumps(modelo))
        with patch.object(F, 'modelo', return_value=arquivo), self.assertRaisesRegex(ValueError, 'contrato mudou'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_03_relatorio_adulterado_recusa(self):
        import formularios_permanentes as F
        rel = self.permanente(); pathlib.Path(rel['arquivo']).write_text('alteração')
        with self.assertRaisesRegex(ValueError, 'adulterado'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_04_reutiliza_sem_nova_aprovacao(self):
        import formularios_permanentes as F
        self.permanente(); antes = self.cfg.with_name('eventos.jsonl').read_bytes()
        reg = F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')
        self.assertEqual(reg['formId'], 'FORM')
        self.assertEqual(F.link(reg, 'CASO-2'), 'https://tally.so/r/FORM?caso=CASO-2')
        self.assertEqual(antes, self.cfg.with_name('eventos.jsonl').read_bytes())

    def test_05_nova_leitura_invalida_permanente(self):
        import formularios_permanentes as F
        self.permanente()
        d = dict(habilitacao='HAB', caso='CASO', ferramenta='mcp__tally__load_form', argumentos={'formId':'FORM'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        I.registrar_retorno(self.cfg, d, {'resposta':json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())})
        with self.assertRaisesRegex(ValueError, 'conferência'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def exportacao(self, casos=('OUTRO-A', 'CASO', 'OUTRO-B')):
        with self.csv.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['Submission ID', 'caso', 'Respondente', 'HAB-0a-1'])
            w.writeheader()
            for i,caso in enumerate(casos):
                w.writerow({'Submission ID':'SUB-'+str(i), 'caso':caso, 'Respondente':'Pessoa Cliente',
                            'HAB-0a-1': 'SEGREDO-'+caso})
        s = json.loads((self.exp/'expediente.json').read_text())
        s['tratamento'] = {'escopo':'administrativo', 'condicoes':'Condições sintéticas'}; H.salvar(self.exp, s)

    def coletar(self, **extra):
        return H.executar(self.exp, 'receber-exportacao', dict(config_emcia=str(self.cfg), arquivo=str(self.csv),
            id='S1', **extra))

    def test_10_exportacao_sem_linha_do_caso(self):
        self.permanente(); self.exportacao(('OUTRO-A',))
        with self.assertRaisesRegex(ValueError, 'nenhuma submissão'): self.coletar()
        self.assertFalse((self.exp/'arquivos').exists())
        self.assertNotIn('SEGREDO-OUTRO-A', (self.exp/'expediente.json').read_text())

    def test_11_duas_submissoes_nao_escolhe(self):
        self.permanente(); self.exportacao(('CASO', 'OUTRO-A', 'CASO'))
        with self.assertRaisesRegex(ValueError, 'qual submissão') as recusada: self.coletar()
        self.assertIn('SUB-0', str(recusada.exception)); self.assertIn('SUB-2', str(recusada.exception))
        self.assertNotIn('SUB-1', str(recusada.exception)); self.assertNotIn('SEGREDO', str(recusada.exception))
        self.assertFalse((self.exp/'arquivos').exists())

    def test_12_permanente_ausente_bloqueia_coleta(self):
        H.iniciar(self.exp, 'HAB', 'Pessoa Engenheira', 'CASO')
        self.exportacao()
        with self.assertRaisesRegex(ValueError, 'conferido'): self.coletar()

    def test_13_filtra_antes_de_persistir(self):
        self.permanente(); self.exportacao(); original = self.csv.read_bytes()
        with self.assertRaisesRegex(ValueError, 'campos'):
            self.coletar(linhas=[{'caso':'OUTRO-A', 'resposta':'SEGREDO-OUTRO-A'}])
        self.coletar()
        s = json.loads((self.exp/'expediente.json').read_text()); fonte = s['fontes']['S1']
        self.assertEqual(fonte['canal'], 'tally-exportacao')
        self.assertEqual(fonte['original_sha256'], H.digest(original))
        self.assertNotEqual(fonte['arquivo']['sha256'], H.digest(original))
        for arq in self.exp.rglob('*'):
            if arq.is_file():
                self.assertNotIn(b'SEGREDO-OUTRO', arq.read_bytes(), str(arq))
        self.assertIn(b'SEGREDO-CASO', H.ler_arquivo(self.exp, fonte['arquivo']))

    def test_14_selecao_explicita_dentre_duas(self):
        self.permanente(); self.exportacao(('CASO', 'CASO', 'OUTRO-A')); self.coletar(submissao='SUB-1')
        fonte = json.loads((self.exp/'expediente.json').read_text())['fontes']['S1']
        self.assertEqual(fonte['submissao'], 'SUB-1')
        linhas = list(csv.DictReader(io.StringIO(H.ler_arquivo(self.exp, fonte['arquivo']).decode())))
        self.assertEqual(len(linhas), 1); self.assertEqual(linhas[0]['Submission ID'], 'SUB-1')

    def test_15_arquivo_fora_da_entrada_recusa(self):
        self.permanente(); self.exportacao()
        outro = self.base/'fora.csv'; outro.write_bytes(self.csv.read_bytes()); self.csv = outro
        with self.assertRaisesRegex(ValueError, 'entrada'): self.coletar()

    def test_20_mensagem_vazia_recusa(self):
        self.permanente(); self.exportacao(); self.coletar()
        with self.assertRaisesRegex(ValueError, 'texto'):
            H.executar(self.exp, 'receber-mensagem', dict(id='M1', respondente='Pessoa Cliente', texto='', pergunta='Limite?'))

    def test_21_mensagem_sem_novo_formulario_ou_pendencia(self):
        self.permanente(); self.exportacao(); self.coletar()
        H.executar(self.exp, 'receber-mensagem', dict(id='M1', respondente='Pessoa Cliente',
                   texto='O limite termina na entrega.', pergunta='Onde termina o processo?'))
        s = json.loads((self.exp/'expediente.json').read_text()); f = s['fontes']['M1']
        self.assertEqual(f['canal'], 'manual'); self.assertEqual(f['rodada'], 1)
        self.assertEqual(f['formulario'], 'FORM'); self.assertFalse(s['pendencias'])
        self.assertEqual(json.loads(H.ler_arquivo(self.exp, f['arquivo']))['texto'], 'O limite termina na entrega.')

    def test_30_tratamento_ausente_recusa(self):
        H.iniciar(self.exp, 'HAB', 'Pessoa Engenheira', 'CASO')
        with self.assertRaisesRegex(ValueError, 'condições administrativas'):
            H.executar(self.exp, 'tratamento-padrao', {'config_emcia':str(self.cfg)})

    def test_31_tratamento_padrao_com_hash_sem_aprovacao(self):
        H.iniciar(self.exp, 'HAB', 'Pessoa Engenheira', 'CASO')
        c = I.ler_config(self.cfg); c['tratamento_administrativo'] = dict(condicoes='Condições sintéticas', provedor='Provedor sintético')
        I.escrever(self.cfg, c)
        H.executar(self.exp, 'tratamento-padrao', {'config_emcia':str(self.cfg)})
        s = json.loads((self.exp/'expediente.json').read_text())
        self.assertEqual(s['tratamento']['texto_sha256'], H.digest('Condições sintéticas'.encode()))
        self.assertEqual(s['tratamento']['referencia'], str(self.cfg)+'#tratamento_administrativo')
        self.assertFalse(any(e['tipo']=='AprovacaoChatRegistrada' for e in s['eventos']))

    def documentos(self):
        self.permanente(); self.exportacao(); self.coletar()
        c = I.ler_config(self.cfg)
        c['aceitacao_minutas'] = dict(texto='uso as minutas sem ratificação jurídica', responsavel=c['responsavel'], data=H.agora(), revogada_em=None)
        I.escrever(self.cfg, c)
        campos = {k:{'valor':'Conteúdo sintético '+k, 'fonte':'S1'} for f in H.TEMPLATES.values()
                  for k in H.TOKEN.findall((ROOT/'eiac-campo/reference/metodo'/f).read_text())}
        campos['signatario']['valor'] = 'Pessoa Cliente'
        H.executar(self.exp, 'consolidar', {'campos':campos})
        self.geracao = dict(templates=str(ROOT/'eiac-campo/reference/metodo'), navegador='google-chrome', config_emcia=str(self.cfg))
        self.pdf_patch = patch.object(H, 'pdf_bytes', side_effect=lambda md,b:b'%PDF-1.7\n'+md.encode()+b'\n%%EOF')
        self.pdf_patch.start(); self.addCleanup(self.pdf_patch.stop)
        H.executar(self.exp, 'preparar-documentos', self.geracao)
        self.plano_docs = dict(geracao=self.geracao, qualificacao_0a=True, conteudo_conferido=True,
            liberacao=dict(ferramenta='Painel escolhido', operador='Pessoa Cliente',
            signatarios=[dict(nome='Pessoa Cliente', papel='organizacao', competencia='Representante'),
                        dict(nome='Pessoa Engenheira', papel='emcia', competencia='Responsável')]))

    def aprovar_docs(self):
        import habilitacao_lotes as L
        r = L.criar_aprovacao(self.exp, 'aprovar-documentos', self.plano_docs, 'ok')
        return H.executar(self.exp, 'aprovar-documentos', {'plano':self.plano_docs, 'testemunho':r})

    def test_40_revisao_conjunta_sem_aprovacao_recusa(self):
        self.documentos()
        with self.assertRaisesRegex(ValueError, 'aprovação'):
            H.executar(self.exp, 'aprovar-documentos', {'plano':self.plano_docs})
        self.assertFalse(json.loads((self.exp/'expediente.json').read_text())['documentos'])

    def test_41_ok_cobre_tres_documentos_com_mesmos_pdfs(self):
        self.documentos(); antes = json.loads((self.exp/'expediente.json').read_text())['rascunhos_documentos']
        self.aprovar_docs(); s = json.loads((self.exp/'expediente.json').read_text())
        for doc in H.CODIGOS_HAB:
            v = s['documentos'][doc][-1]
            self.assertEqual(v['pdf']['sha256'], antes[doc]['pdf']['sha256']); self.assertTrue(v['liberacao'])
        self.assertEqual(len([e for e in s['eventos'] if e['tipo']=='AprovacaoLoteRegistrada']), 1)
        self.assertTrue(any(e.get('operacao')=='revisar' for e in s['eventos']))

    def test_42_assinatura_sem_aprovacao_recusa(self):
        self.documentos(); self.aprovar_docs()
        with self.assertRaisesRegex(ValueError, 'aprovação'):
            H.executar(self.exp, 'aprovar-assinaturas', {'plano':{}})
        self.assertFalse(H.completa(json.loads((self.exp/'expediente.json').read_text())))

    def test_43_pdf_assinado_de_outro_documento_recusa(self):
        import habilitacao_lotes as L
        self.documentos(); self.aprovar_docs()
        for doc in H.CODIGOS_HAB: (self.entrada/(doc+'-assinado.pdf')).write_bytes(b'%PDF-1.7\nDocumento de outro cliente\n%%EOF')
        with patch.object(L, 'texto_pdf', side_effect=lambda p:pathlib.Path(p).read_bytes().decode()), self.assertRaisesRegex(ValueError, 'corresponde'):
            H.executar(self.exp, 'preparar-assinaturas', {'config_emcia':str(self.cfg)})

    def test_44_aprovacao_de_documento_adulterado_recusa(self):
        import habilitacao_lotes as L
        self.documentos(); r = L.criar_aprovacao(self.exp, 'aprovar-documentos', self.plano_docs, 'ok')
        s = json.loads((self.exp/'expediente.json').read_text())
        (self.exp/s['rascunhos_documentos']['HAB-01']['pdf']['caminho']).write_bytes(b'alterado')
        with self.assertRaises(ValueError): H.executar(self.exp, 'aprovar-documentos', {'plano':self.plano_docs, 'testemunho':r})

    def test_50_matriz_nao_presume_acesso_concedido(self):
        self.permanente()
        with self.csv.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['Submission ID','caso','Respondente','HAB-0c-3','HAB-0c-5'])
            w.writeheader(); w.writerow({'Submission ID':'SUB-1','caso':'CASO','Respondente':'Pessoa Cliente',
                'HAB-0c-3':'Planilha de vendas', 'HAB-0c-5':'Sistema restrito'})
        s = json.loads((self.exp/'expediente.json').read_text()); s['tratamento'] = {'escopo':'administrativo'}; H.salvar(self.exp,s)
        self.coletar(); r = H.executar(self.exp, 'planejar-acessos', {})
        self.assertEqual(r['itens'][0]['item'], 'Planilha de vendas')
        self.assertEqual(r['itens'][0]['status'], 'a-confirmar'); self.assertEqual(r['respostas_0c']['HAB-0c-5'], 'Sistema restrito')
        self.assertIsNone(json.loads((self.exp/'expediente.json').read_text())['acessos'])

    def test_51_acessos_sem_mensagem_explicita_recusa(self):
        self.permanente(); self.exportacao(); self.coletar()
        with self.assertRaisesRegex(ValueError, 'mensagem'):
            H.executar(self.exp, 'confirmar-acessos', {'matriz':{}})

    def test_60_abertura_canais_sem_drive(self):
        import canais as K
        from formularios_permanentes import validar
        self.permanente()
        c = I.ler_config(self.cfg); c['formularios_permanentes']['triagem'] = dict(c['formularios_permanentes']['habilitacao'], formId='TRIAGEM')
        pb = json.loads((ROOT/'eiac-campo/template-caso/registro/playbook.json').read_text())
        with patch('formularios_permanentes.validar', side_effect=lambda p,c,t:c['formularios_permanentes'][t]):
            reg = K.declaracao_inicial(self.cfg, c, 'CASO', pb)
        K.validar(reg, {'caso':'CASO'}, pb)
        self.assertEqual({x['ferramenta'] for x in reg['canais']}, {'tally','calendar'})
        self.assertTrue(any(x['finalidade']=='triagem' for x in reg['canais']))
        self.assertEqual(pb['canais_por_etapa']['P2'], [{'finalidade':'documentos','direcao':'entrada'}])

    def test_61_drive_antes_de_p2_mesmo_com_aprovacao_recusa(self):
        self.permanente(); c = I.ler_config(self.cfg); c['fluxo_habilitacao'] = 'simplificado'; I.escrever(self.cfg,c)
        with self.assertRaisesRegex(ValueError, 'P2'):
            self.op('mcp', ferramenta='mcp__claude_ai_Google_Drive__create_file',
                argumentos={'title':'Pasta', 'parentId':'ROOT', 'contentMimeType':'application/vnd.google-apps.folder'})
        self.assertEqual(json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])['evento'], 'TentativaNegada')

    def test_70_proximo_executa_inicial_sem_aprovacao(self):
        self.permanente(); self.configurar_fluxo()
        r = I.proximo(self.cfg, {'habilitacao':'HAB-NOVA','caso':'CASO-NOVO'})
        self.assertEqual(r['proximo'], 'depositar-exportacao')
        self.assertIn('?caso=CASO-NOVO', r['link'])
        s = json.loads((self.base/'expedientes/HAB-NOVA/expediente.json').read_text())
        self.assertTrue(s['tratamento']); self.assertFalse(s['fontes'])
        self.assertFalse(any(e['tipo']=='AprovacaoLoteRegistrada' for e in s['eventos']))

    def configurar_fluxo(self):
        c = I.ler_config(self.cfg)
        c['tratamento_administrativo'] = dict(condicoes='Condições sintéticas', provedor='Provedor sintético')
        c['aceitacao_minutas'] = dict(texto='uso as minutas sem ratificação jurídica', responsavel=c['responsavel'], data=H.agora(), revogada_em=None)
        I.escrever(self.cfg,c)

    def test_71_abertura_sem_terceira_aprovacao_recusa(self):
        import fluxo_habilitacao as F
        self.permanente(); self.configurar_fluxo()
        with self.assertRaisesRegex(ValueError, 'aprovação'):
            F.abrir(self.cfg, I.ler_config(self.cfg), self.exp, {'habilitacao':'HAB','caso':'CASO'}, None)
        self.assertFalse((self.base/'casos/CASO').exists())

    def triagem_permanente(self):
        d = dict(habilitacao='HAB', caso='CASO', ferramenta='mcp__tally__create_new_form', argumentos={'title':'Triagem sintética','workspaceId':'WORK'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos']); I.registrar_retorno(self.cfg,d,{'ids':{'formulario_id':'TRIAGEM'}})
        d.update(ferramenta='mcp__tally__load_form', argumentos={'formId':'TRIAGEM'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        raw = json.loads((ROOT/'testes/apoio/tally-load-form-triagem.json').read_text()); raw['data'].update(formId='TRIAGEM', workspaceId='WORK')
        I.registrar_retorno(self.cfg,d,{'resposta':raw})
        r = self.op('conferir-formulario', formulario_id='TRIAGEM', modelo='triagem')
        self.op('confirmar-formulario', formulario_id='TRIAGEM', relatorio_sha256=r['sha256'])
        self.op('formulario-permanente', formulario_id='TRIAGEM', modelo='triagem')

    def percurso(self):
        self.permanente(); self.triagem_permanente(); self.configurar_fluxo()
        c=I.ler_config(self.cfg); c.pop('pasta_drive'); I.escrever(self.cfg,c)
        self.chamadas = []
        def avancar(**d):
            r = I.proximo(self.cfg, dict(habilitacao='HAB', caso='CASO', **d)); self.chamadas.append(r['proximo']); return r
        self.assertEqual(avancar()['proximo'], 'depositar-exportacao')
        with self.csv.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['Submission ID','caso','Respondente','HAB-0a-1','HAB-0c-3','HAB-0c-5']); w.writeheader()
            for caso in ('OUTRO-A','CASO','OUTRO-B'):
                w.writerow({'Submission ID':'SUB-'+caso,'caso':caso,'Respondente':'Pessoa Cliente',
                    'HAB-0a-1':'SEGREDO-'+caso,'HAB-0c-3':'Planilha de vendas', 'HAB-0c-5':'Sistema restrito'})
        self.assertEqual(avancar()['proximo'],'esclarecer')
        campos = {k:{'valor':'Conteúdo sintético '+k,'fonte':'M1'} for f in H.TEMPLATES.values()
                  for k in H.TOKEN.findall((ROOT/'eiac-campo/reference/metodo'/f).read_text())}
        campos['signatario']['valor']='Pessoa Cliente'
        self.pdfpatch = patch.object(H,'pdf_bytes',side_effect=lambda md,b:b'%PDF-1.7\n'+md.encode()+b'\n%%EOF')
        self.pdfpatch.start();self.addCleanup(self.pdfpatch.stop)
        plano = dict(qualificacao_0a=True,conteudo_conferido=True,liberacao=dict(ferramenta='Painel escolhido',operador='Pessoa Cliente',
            signatarios=[dict(nome='Pessoa Cliente',papel='organizacao',competencia='Representante'),dict(nome='Pessoa Engenheira',papel='emcia',competencia='Responsável')]))
        self.assertEqual(avancar(mensagem=dict(id='M1',respondente='Pessoa Cliente',pergunta='Onde termina?',texto='Na entrega.'),campos=campos,plano_documentos=plano)['proximo'],'aprovar-documentos')
        self.assertEqual(avancar(aprovacao=dict(ponto='documentos',confirmado=True,trecho='ok'))['proximo'],'depositar-assinaturas')
        s = json.loads((self.exp/'expediente.json').read_text())
        for doc in H.CODIGOS_HAB:
            raw = H.ler_arquivo(self.exp,s['documentos'][doc][-1]['pdf'])
            (self.entrada/(doc+'-assinado.pdf')).write_bytes(raw+'\nAssinatura sintética\n%%EOF'.encode())
        import habilitacao_lotes as L
        self.textpatch = patch.object(L,'texto_pdf',side_effect=lambda p:' '.join(pathlib.Path(p).read_bytes().decode().split()))
        self.textpatch.start();self.addCleanup(self.textpatch.stop)
        signatarios=[dict(nome='Pessoa Cliente',papel='organizacao',data='2026-10-05'),dict(nome='Pessoa Engenheira',papel='emcia',data='2026-10-05')]
        self.assertEqual(avancar(plano_assinaturas=dict(referencia='Devolução sintética',signatarios=signatarios))['proximo'],'aprovar-assinaturas')
        acessos=dict(confirmado=True,trecho='Confirmo a matriz com acesso concedido à planilha e sistema negado',matriz=dict(
            patrocinador='Pessoa Cliente',executor='Pessoa Executora',decisor='Pessoa Engenheira',data_sessao='2026-10-15',
            autoridade_patrocinador='Responsável pelo processo',executor_liberado=True,agenda_reservada=True,
            itens=[dict(item='Planilha de vendas',status='concedido',evidencia='Mensagem humana sintética'),
                   dict(item='Sistema restrito',status='negado',evidencia='Mensagem humana sintética',motivo='Acesso indisponível',restricao='Sem verificar o sistema')]))
        self.assertEqual(avancar(aprovacao=dict(ponto='assinaturas',confirmado=True,trecho='ok'),acessos=acessos)['proximo'],'aprovar-abertura')
        with patch.dict('os.environ',{'GIT_AUTHOR_NAME':'Pessoa Engenheira','GIT_AUTHOR_EMAIL':'sintetico@example.invalid','GIT_COMMITTER_NAME':'Pessoa Engenheira','GIT_COMMITTER_EMAIL':'sintetico@example.invalid'}):
            r=avancar(aprovacao=dict(ponto='abertura',confirmado=True,trecho='ok'))
        self.assertEqual(r['proximo'],'F0')
        self.case=self.base/'casos/CASO'
        return r

    def test_80_percurso_completo_tres_aprovacoes_dois_depositos(self):
        r = self.percurso(); s = json.loads((self.exp/'expediente.json').read_text())
        aprovacoes = [e for e in s['eventos'] if e['tipo']=='AprovacaoLoteRegistrada']
        self.assertEqual(len(aprovacoes),3); self.assertTrue(all(e['testemunho']['literal']=='ok' for e in aprovacoes))
        self.assertEqual(len(self.chamadas),7); self.assertEqual(r['aprovacoes'],3)
        canais = json.loads((self.case/'registro/canais.json').read_text())
        self.assertFalse(any(c['ferramenta']=='drive' for c in canais['canais']))
        self.assertEqual(len(json.loads((self.case/'registro/habilitacao.json').read_text())['vigente']['restricoes']),1)
        for arq in self.exp.rglob('*'):
            if arq.is_file(): self.assertNotIn(b'SEGREDO-OUTRO',arq.read_bytes(),str(arq))
        for doc in H.CODIGOS_HAB:
            md = H.ler_arquivo(self.exp,s['documentos'][doc][-1]['markdown'])
            self.assertNotIn(b'Controle do modelo',md);self.assertNotIn('Revisão jurídica'.encode(),md)
        antes=(self.exp/'expediente.json').read_bytes()
        self.assertEqual(I.proximo(self.cfg,dict(habilitacao='HAB',caso='CASO'))['proximo'],'F0')
        self.assertEqual(antes,(self.exp/'expediente.json').read_bytes())
        import os
        if os.environ.get('EMCIA_EVIDENCIA_SINTETICA'):
            pathlib.Path(os.environ['EMCIA_EVIDENCIA_SINTETICA']).write_text(json.dumps(dict(aprovacoes=3,depositos=2,chamadas_script=7,passos=self.chamadas,
                mensagens_esclarecimento=1,drive_na_abertura=False,isolamento='nenhum SEGREDO-OUTRO em qualquer arquivo do expediente',
                documentos={d:dict(enviado=s['documentos'][d][-1]['pdf']['sha256'],assinado=s['documentos'][d][-1]['assinatura']['arquivo']['sha256']) for d in H.CODIGOS_HAB}),ensure_ascii=False,indent=2)+'\n')

    def test_81_p2_exige_aprovacao_e_cria_pastas(self):
        self.percurso()
        import provisionamento_p2 as Q
        import canais_registro as K
        with I.cwd(self.case):
            pb=json.loads((self.case/'registro/playbook.json').read_text())
            self.assertIn('ausente',K.conferir(pb,'P2'))
            st=I.E.ler();st['nivel']='N1';st['etapa_atual']='P2';st['cumprimentos']['F0']={'cumprido':True};st['cumprimentos']['P1']={'cumprido':True}
            (self.case/'registro/estado.json').write_text(json.dumps(st))
        d=dict(habilitacao='HAB',caso='CASO',passo='P2',conteiner_id='ROOT',drive_id='DRIVE',destinatario='cliente@example.invalid')
        r=I.proximo(self.cfg,d);self.assertEqual(r['proximo'],'aprovar-pastas-p2')
        r=I.proximo(self.cfg,dict(d,confirmado=True,trecho='ok'))
        efeitos=0
        while r['proximo']=='conector':
            chamada=r['chamada'];efeitos+=1
            args=chamada['argumentos']
            self.assertIsNone(__import__('guarda_inicial').conferir(dict(tool_name=chamada['ferramenta'],tool_input=args),self.cfg) if self._sessao() else None)
            ids={'pasta_id':'ID-'+chamada['finalidade']} if chamada['ferramenta'].endswith('create_file') else {}
            I.registrar_retorno(self.cfg,chamada,{'ids':ids})
            r=I.proximo(self.cfg,d)
            self.assertLessEqual(efeitos,10)
        self.assertEqual(efeitos,10);self.assertEqual(r['proximo'],'P2')
        with I.cwd(self.case):self.assertIsNone(K.conferir(pb,'P2'))
        canais=json.loads((self.case/'registro/canais.json').read_text())['canais']
        self.assertEqual(next(c for c in canais if c['finalidade']=='trabalho-interno')['acesso_cliente'],'nenhum')
        evs=[json.loads(l) for l in self.cfg.with_name('eventos.jsonl').read_text().splitlines()]
        self.assertEqual(len([e for e in evs if e['evento']=='ProvisionamentoP2Aprovado']),1)

    def _sessao(self):
        I.escrever(self.cfg.with_name('sessao.json'),dict(habilitacao='HAB',caso='CASO'));return True

    def test_90_config_existente_recebe_padrao_sem_trocar_responsavel(self):
        c=I.ler_config(self.cfg); d={k:c[k] for k in I.CAMPOS}
        d['tratamento_administrativo']=dict(condicoes='Condições padrão',provedor='Provedor declarado')
        novo=I.configurar(self.cfg,d)
        self.assertEqual(novo['tratamento_administrativo'],d['tratamento_administrativo'])
        self.assertEqual(novo['responsavel'],c['responsavel'])

    def test_91_proximo_composto_e_decisao_metodo_recusados(self):
        import guarda_inicial as G
        self.permanente(); self.configurar_fluxo()
        entrada=self.base/'ato.json';entrada.write_text(json.dumps(dict(habilitacao='HAB',caso='CASO')))
        cmd='python3 iniciar.py proximo --entrada '+str(entrada)
        self.assertIsNone(G.conferir(dict(tool_name='Bash',tool_input={'command':cmd}),self.cfg))
        self.assertIsNotNone(G.conferir(dict(tool_name='Bash',tool_input={'command':cmd+'; python3 prosseguimento.py'}),self.cfg))
        with self.assertRaisesRegex(ValueError, 'decisão de método'):
            I.operar(self.cfg,'decidir-prosseguimento',{},None)

    def test_92_coleta_na_cli_nao_expoe_outro_caso(self):
        import subprocess
        self.permanente(); self.configurar_fluxo(); self.exportacao(('OUTRO-A','OUTRO-B'))
        entrada=self.base/'ato.json';entrada.write_text(json.dumps(dict(habilitacao='HAB',caso='CASO')))
        r=subprocess.run([sys.executable,str(ROOT/'eiac-campo/scripts/iniciar.py'),'proximo','--config',str(self.cfg),'--entrada',str(entrada)],capture_output=True,text=True)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('nenhuma submissão',r.stderr)
        self.assertNotIn('OUTRO-A',r.stdout+r.stderr);self.assertNotIn('OUTRO-B',r.stdout+r.stderr)
        self.assertFalse(json.loads((self.exp/'expediente.json').read_text())['fontes'])

if __name__ == '__main__': unittest.main(verbosity=2)
