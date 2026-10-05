"""Contratos reais transcritos; nenhuma chamada a serviço ou dado de cliente."""
import copy
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'eiac-campo/scripts'))
sys.path.insert(0, str(ROOT/'eiac-nucleo/scripts'))
import iniciar as I
import escopo_externo as S
from apoio.hook_real import CasoHook
from apoio.canais import definir

FIXTURE = ROOT/'testes/apoio/inventario-mcp-real.json'
DRIVE = 'mcp__claude_ai_Google_Drive__'
CAL = 'mcp__claude_ai_Google_Calendar__'
TALLY = 'mcp__tally__'
FOLDER = 'application/vnd.google-apps.folder'


class Contrato(unittest.TestCase):
    def setUp(self):
        self.inv = json.loads(FIXTURE.read_text())

    def test_01_nome_ausente_reprova_contrato(self):
        perfis = copy.deepcopy(I.PERFIS)
        perfis['mcp__nao_existe__criar'] = copy.deepcopy(next(iter(perfis.values())))
        with self.assertRaises(ValueError):
            I.validar_contrato_perfis(self.inv, perfis)

    def test_02_parametro_ausente_reprova_contrato(self):
        perfis = copy.deepcopy(I.PERFIS)
        perfis[DRIVE+'search_files']['argumentos'][0]['campo'] = 'q'
        with self.assertRaises(ValueError):
            I.validar_contrato_perfis(self.inv, perfis)

    def test_03_cada_nome_e_parametro_consta_do_inventario(self):
        I.validar_contrato_perfis(self.inv)
        perfil = I.calibrar(self.inv)
        self.assertGreaterEqual(len(perfil['regras']), 9)
        self.assertEqual(len(perfil['regras']), len({r['ferramenta'] for r in perfil['regras']}))
        self.assertTrue(all(r['ferramenta'] in {f['nome'] for f in self.inv['ferramentas']} for r in perfil['regras']))

    def test_04_garantia_tally_ausente_e_manual_explicito(self):
        p = I.calibrar(self.inv)
        self.assertIn(TALLY+'fetch_submissions', p['recusadas'])
        manual = next(m for m in p['manuais'] if m['passo']=='coletar-submissoes')
        self.assertIn('campo oculto', manual['motivo'])
        self.assertTrue(any(m['passo']=='preparar-formulario' for m in p['manuais']))

    def test_05_criar_sem_workspace_fica_recusado(self):
        f = next(f for f in self.inv['ferramentas'] if f['nome']==TALLY+'create_new_form')
        del f['inputSchema']['properties']['workspaceId']
        p = I.calibrar(self.inv)
        self.assertIn(f['nome'], p['recusadas'])
        self.assertTrue(any('workspaceId' in m['motivo'] for m in p['manuais']))

    def test_06_publicacao_ausente_vira_acao_humana(self):
        self.inv['ferramentas'] = [f for f in self.inv['ferramentas'] if f['nome']!=TALLY+'publish_form']
        p = I.calibrar(self.inv)
        self.assertTrue(any(m['passo']=='publicar-formulario' for m in p['manuais']))
        self.assertNotIn(TALLY+'publish_form', [r['ferramenta'] for r in p['regras']])

    def test_07_schema_calendar_parcial_nao_inventa_subcampos(self):
        p = I.calibrar(self.inv)
        r = next(r for r in p['regras'] if r['ferramenta']==CAL+'create_event')
        self.assertIn('calendarId', r['parametros'])
        self.assertNotIn('attendees', r['parametros'])
        self.assertIn('attendees', p['parametros_recusados'][CAL+'create_event'])


class Administracao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name); self.cfg = self.base/'config.json'
        I.configurar(self.cfg, dict(responsavel='Pessoa Engenheira', base_casos=str(self.base/'casos'),
            base_expedientes=str(self.base/'expedientes'), workspace_tally='WORK', pasta_drive='ROOT',
            calendario_casos='CAL', navegador='google-chrome'))
        self.inv = json.loads(FIXTURE.read_text())
        self.op('perfil', ferramentas=self.inv, perfil=I.calibrar(self.inv))
        self.op('iniciar', id='HAB')
        I.retomar(self.cfg, 'HAB', 'CASO')
        self.evidencia = self.base/'decisao.txt'; self.evidencia.write_text('Evidência exclusivamente sintética.')
        self.folder('ENT', finalidade='entregas')

    def op(self, nome, **extra):
        d = dict(habilitacao='HAB', caso='CASO'); d.update(extra)
        r = I.aprovar(self.cfg, nome, d, 'Aprovo esta operação e estes bytes', 'Conferência sintética')
        return I.operar(self.cfg, nome, d, r)

    def call(self, nome, argumentos, **extra):
        return self.op('mcp', ferramenta=nome, argumentos=argumentos, **extra)

    def folder(self, ident, finalidade='documentos'):
        d = dict(habilitacao='HAB', caso='CASO', ferramenta=DRIVE+'create_file',
            argumentos=dict(title='Pasta sintética', parentId='ROOT', contentMimeType=FOLDER), finalidade=finalidade)
        r = I.aprovar(self.cfg, 'mcp', d, 'Aprovo a pasta sintética', 'Pasta e finalidade conferidas')
        I.operar(self.cfg, 'mcp', d, r)
        I.registrar_retorno(self.cfg, d, dict(ids={'pasta_id':ident}))

    def denied(self, nome, args):
        with self.assertRaises(ValueError): self.call(nome, args)
        ev = json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])
        self.assertEqual(ev['evento'], 'TentativaNegada')
        self.assertEqual(ev['autor'], 'Pessoa Engenheira')

    def test_01_busca_sem_pasta(self):
        self.denied(DRIVE+'search_files', {'query':"name contains 'cliente'"})

    def test_02_criacao_pasta_fora_conteiner(self):
        self.denied(DRIVE+'create_file', dict(title='Pasta', parentId='ALHEIO', contentMimeType=FOLDER))

    def test_03_arquivo_comum_fora_entregas(self):
        self.folder('DOC')
        self.denied(DRIVE+'create_file', dict(title='Arquivo', parentId='DOC', contentMimeType='text/plain', textContent='Sintético'))

    def test_04_compartilhar_id_nao_declarado(self):
        self.denied(DRIVE+'share_file', dict(fileId='ALHEIO', emailAddress='cliente@example.invalid', role='reader'))

    def test_05_formulario_nao_declarado(self):
        self.denied(TALLY+'fetch_submissions', dict(formId='ALHEIO'))

    def test_06_ferramenta_sem_perfil(self):
        self.denied(DRIVE+'list_recent_files', {})

    def test_07_parametro_extra(self):
        self.denied(DRIVE+'search_files', dict(query="'ENT' in parents", parentId='ALHEIO'))

    def test_08_leitura_sem_listagem(self):
        self.denied(DRIVE+'read_file_content', dict(fileId='FILE'))

    def test_09_pasta_com_conteudo_nao_e_variante_pasta(self):
        self.denied(DRIVE+'create_file', dict(title='Pasta', parentId='ROOT', contentMimeType=FOLDER, textContent='Sintético'))

    def test_10_destinatario_alterado_recusa(self):
        d = dict(habilitacao='HAB', caso='CASO', ferramenta=DRIVE+'share_file',
            argumentos=dict(fileId='ENT', emailAddress='cliente@example.invalid', role='reader'))
        r = I.aprovar(self.cfg, 'mcp', d, 'Aprovo leitor e destinatário', 'Compartilhamento conferido')
        d['argumentos']['emailAddress']='outro@example.invalid'
        with self.assertRaises(ValueError): I.operar(self.cfg, 'mcp', d, r)

    def test_11_tally_sem_filtro_recusa_mesmo_formulario_declarado(self):
        d = dict(habilitacao='HAB', caso='CASO', ferramenta=TALLY+'create_new_form', argumentos=dict(title='Sintético', workspaceId='WORK'))
        self.call(d['ferramenta'], d['argumentos']); I.registrar_retorno(self.cfg, d, dict(ids={'formulario_id':'FORM'}))
        self.denied(TALLY+'fetch_submissions', dict(formId='FORM'))

    def test_12_workspace_alheio(self):
        self.denied(TALLY+'create_new_form', dict(title='Formulário', workspaceId='ALHEIO'))

    def test_13_publicacao_sem_conferencia_do_campo_oculto(self):
        d = dict(habilitacao='HAB', caso='CASO', ferramenta=TALLY+'create_new_form', argumentos=dict(title='Sintético', workspaceId='WORK'))
        self.call(d['ferramenta'], d['argumentos']); I.registrar_retorno(self.cfg, d, dict(ids={'formulario_id':'FORM'}))
        self.denied(TALLY+'publish_form', dict(formId='FORM'))

    def test_14_listagem_com_conteiner_alheio(self):
        d = dict(habilitacao='HAB', caso='CASO', ferramenta=DRIVE+'search_files', argumentos={'query':"'ENT' in parents"})
        self.call(d['ferramenta'], d['argumentos'])
        with self.assertRaises(ValueError): I.registrar_retorno(self.cfg,d,dict(conteiner_id='ALHEIO',objetos=['FILE']))
        self.denied(DRIVE+'read_file_content', dict(fileId='FILE'))

    def test_15_retorno_nao_muda_finalidade_aprovada(self):
        p=self.cfg.with_name('mcp-retornos.json');r=json.loads(p.read_text())
        r[0]['chamada']['finalidade']='documentos';p.write_text(json.dumps(r))
        self.denied(DRIVE+'create_file', dict(title='Arquivo',parentId='ENT',contentMimeType='text/plain',textContent='Sintético'))

    def test_16_manual_sem_aprovacao(self):
        with self.assertRaises(ValueError):
            I.operar(self.cfg,'caminho-manual',dict(habilitacao='HAB',caso='CASO',passo='coletar-submissoes',evidencia=str(self.evidencia),decisao='executar manualmente'),None)
        self.assertEqual(json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])['evento'],'TentativaNegada')

    def test_17_parametro_obrigatorio_e_tipo(self):
        self.denied(DRIVE+'create_file',dict(title='Pasta',contentMimeType=FOLDER))
        self.denied(DRIVE+'search_files',dict(query="'ENT' in parents",pageSize='dez'))

    def test_18_mcp_sem_sessao_nao_passa(self):
        import guarda_inicial as G
        self.cfg.with_name('sessao.json').unlink()
        self.assertIsNotNone(G.conferir(dict(tool_name=DRIVE+'list_recent_files',tool_input={}),self.cfg))
        self.assertEqual(json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])['evento'],'TentativaNegada')

    def test_19_id_do_expediente_nao_passa_para_outro_caso(self):
        with self.assertRaises(ValueError):
            self.op('mcp',caso='OUTRO-CASO',ferramenta=DRIVE+'share_file',argumentos=dict(fileId='ENT',emailAddress='cliente@example.invalid',role='reader'))
        self.assertEqual(json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])['evento'],'TentativaNegada')

    def test_20_pasta_arquivo_entregas_compartilhamento_calendario(self):
        self.call(DRIVE+'create_file', dict(title='Arquivo', parentId='ENT', contentMimeType='text/plain', textContent='Sintético'))
        self.call(DRIVE+'share_file', dict(fileId='ENT', emailAddress='cliente@example.invalid', role='reader'))
        self.call(CAL+'list_events', dict(calendarId='CAL'))
        self.call(CAL+'create_event', dict(calendarId='CAL', summary='Sintético', startTime='2026-10-05T10:00:00Z', endTime='2026-10-05T11:00:00Z'))

    def test_21_listagem_registrada_antes_da_leitura(self):
        d = dict(habilitacao='HAB', caso='CASO', ferramenta=DRIVE+'search_files', argumentos={'query':"'ENT' in parents"})
        self.call(d['ferramenta'], d['argumentos'])
        I.registrar_retorno(self.cfg, d, dict(conteiner_id='ENT', objetos=['FILE']))
        self.call(DRIVE+'read_file_content', dict(fileId='FILE'))
        self.call(DRIVE+'download_file_content', dict(fileId='FILE'))

    def test_22_manual_decisao_e_evidencia_preservadas(self):
        self.op('caminho-manual', passo='coletar-submissoes', evidencia=str(self.evidencia), decisao='executar manualmente')
        evs = [json.loads(l) for l in self.cfg.with_name('eventos.jsonl').read_text().splitlines()]
        ev = next(e for e in evs if e['evento']=='CaminhoManualDecidido')
        self.assertEqual(ev['passo'], 'coletar-submissoes')
        self.assertEqual(ev['autor'], 'Pessoa Engenheira')
        self.assertEqual(len(ev['evidencia_sha256']), 64)

    def test_23_publicacao_apos_conferencia_manual(self):
        d = dict(habilitacao='HAB',caso='CASO',ferramenta=TALLY+'create_new_form',argumentos=dict(title='Sintético',workspaceId='WORK'))
        self.call(d['ferramenta'],d['argumentos']);I.registrar_retorno(self.cfg,d,dict(ids={'formulario_id':'FORM'}))
        self.op('caminho-manual',passo='preparar-formulario',formulario_id='FORM',evidencia=str(self.evidencia),decisao='executar manualmente')
        self.call(TALLY+'publish_form',dict(formId='FORM'))

    def test_24_formulario_sem_ferramenta_de_publicacao_caminho_manual(self):
        inv=copy.deepcopy(self.inv);inv['ferramentas']=[f for f in inv['ferramentas'] if f['nome']!=TALLY+'publish_form']
        self.op('perfil',ferramentas=inv,perfil=I.calibrar(inv))
        self.op('caminho-manual',passo='publicar-formulario',formulario_id='FORM',evidencia=str(self.evidencia),decisao='executar manualmente')
        self.denied(TALLY+'publish_form',dict(formId='FORM'))


class CasoReal(CasoHook):
    def setUp(self):
        super().setUp(); definir(self.caso)
        self.pasta = 'SINTETICO-documentos-pasta_id'

    def test_01_parametro_extra_recusa_no_nucleo(self):
        self.negado(DRIVE+'search_files', dict(query=f"'{self.pasta}' in parents", parentId='ALHEIO'))

    def test_02_criar_arquivo_fora_entregas(self):
        self.negado(DRIVE+'create_file', dict(title='Arquivo', parentId=self.pasta, contentMimeType='text/plain', textContent='Sintético'))

    def test_03_compartilhamento_sem_aprovacao_recusa(self):
        self.negado(DRIVE+'share_file', dict(fileId=self.pasta, emailAddress='cliente@example.invalid', role='reader'))

    def test_04_calendar_alheio(self):
        self.negado(CAL+'list_events', dict(calendarId='ALHEIO'))

    def test_05_tally_sem_filtro_recusa_no_nucleo(self):
        self.negado(TALLY+'fetch_submissions', dict(formId='SINTETICO-triagem-formulario_id'))

    def test_20_busca_limitada_aceita(self):
        self.assertEqual(self.hook(DRIVE+'search_files', dict(query=f"'{self.pasta}' in parents")).returncode, 0)

    def test_21_pasta_e_arquivo_entregas_com_aprovacao(self):
        for parent,tipo,conteudo in [(self.pasta,FOLDER,{}),('SINTETICO-entregas-pasta_id','text/plain',dict(textContent='Sintético'))]:
            args=dict(title='Sintético',parentId=parent,contentMimeType=tipo,**conteudo)
            self.aprovar(DRIVE+'create_file',args)
            self.assertEqual(self.hook(DRIVE+'create_file',args).returncode,0)

    def test_22_leitura_com_listagem_integra(self):
        import subprocess
        entrada=self.caso/'rascunho/entrada/lista.json';entrada.parent.mkdir()
        args={'query':f"'{self.pasta}' in parents"}
        entrada.write_text(json.dumps(dict(ferramenta_externa=DRIVE+'search_files',argumentos=args,conteiner_id=self.pasta,objetos=['FILE'],coletado_em='2026-10-05T10:00:00Z')))
        r=subprocess.run([sys.executable,str(ROOT/'eiac-campo/scripts/registrar_listagem.py'),'--entrada',str(entrada)],cwd=self.caso,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(self.hook(DRIVE+'read_file_content',dict(fileId='FILE')).returncode,0)
        self.assertEqual(self.hook(DRIVE+'download_file_content',dict(fileId='FILE')).returncode,0)

    def test_23_compartilhamento_parametros_exatos(self):
        args=dict(fileId=self.pasta,emailAddress='cliente@example.invalid',role='reader')
        self.aprovar(DRIVE+'share_file',args)
        self.assertEqual(self.hook(DRIVE+'share_file',args).returncode,0)
        self.negado(DRIVE+'share_file',dict(args,role='writer'))
        self.negado(DRIVE+'share_file',dict(args,emailAddress='outro@example.invalid'))

    def aprovar(self,nome,args):
        from apoio.hook_real import NUCLEO
        import subprocess
        code="import estado as E,json,sys;E.evento('AprovacaoExternaRegistrada',autor='Celso do Vale',contexto=E.ler()['caso'],ferramenta=sys.argv[1],argumentos=json.loads(sys.argv[2]),testemunho={'literal':'Aprovo estes bytes','resumo':'Controle sintético','data':'2026-10-05T10:00:00Z'})"
        r=subprocess.run([sys.executable,'-c',code,nome,json.dumps(args)],cwd=self.caso,env=dict(self.env,PYTHONPATH=str(NUCLEO)),capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)


if __name__=='__main__': unittest.main(verbosity=2)
