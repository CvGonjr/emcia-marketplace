"""Emenda 047 item 9: conectores administrativos e fronteira da abertura."""
import copy
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'eiac-campo/scripts'))
import iniciar as I
import habilitacao as H
import guarda_inicial as G
import habilitacao_simplificada as HS
from apoio.hook_real import CasoHook

DRIVE='mcp__claude_ai_Google_Drive__'
CAL='mcp__claude_ai_Google_Calendar__'

class Administrativa(unittest.TestCase):
    setUp=HS.Simplificada.setUp
    op=HS.Simplificada.op
    configurar_fluxo=HS.Simplificada.configurar_fluxo
    percurso=HS.Simplificada.percurso

    def permanente(self):
        H.iniciar(self.exp,'HAB','Pessoa Engenheira','CASO')
        I.retomar(self.cfg,'HAB','CASO')
        d=dict(habilitacao='HAB',caso='CASO',ferramenta='mcp__tally__load_form',argumentos={'formId':'FORM'})
        I.autorizar_mcp(self.cfg,d)
        I.registrar_retorno(self.cfg,d,{'resposta':json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())})
        rel=I.operar(self.cfg,'conferir-formulario',dict(habilitacao='HAB',caso='CASO',formulario_id='FORM',modelo='habilitacao'),None)
        self.op('confirmar-formulario',formulario_id='FORM',relatorio_sha256=rel['sha256'])
        self.op('formulario-permanente',formulario_id='FORM',modelo='habilitacao')
        return rel

    def triagem_permanente(self):
        d=self.chamada('mcp__tally__load_form',{'formId':'TRIAGEM'})
        I.autorizar_mcp(self.cfg,d)
        raw=json.loads((ROOT/'testes/apoio/tally-load-form-triagem.json').read_text());raw['data'].update(formId='TRIAGEM',workspaceId='WORK')
        I.registrar_retorno(self.cfg,d,{'resposta':raw})
        r=I.operar(self.cfg,'conferir-formulario',dict(habilitacao='HAB',caso='CASO',formulario_id='TRIAGEM',modelo='triagem'),None)
        self.op('confirmar-formulario',formulario_id='TRIAGEM',relatorio_sha256=r['sha256'])
        self.op('formulario-permanente',formulario_id='TRIAGEM',modelo='triagem')

    def chamada(self,nome,args):
        return dict(habilitacao='HAB',caso='CASO',ferramenta=nome,argumentos=args)

    def resposta(self,casos=('OUTRO-A','CASO','OUTRO-B')):
        return {'resposta':{'submissions':[dict(id='SUB-'+str(i),hiddenFields={'caso':caso},respondente='Pessoa Cliente',
            responses=[dict(label='HAB-0a-1',answer='SEGREDO-'+caso)]) for i,caso in enumerate(casos)],'hasMore':False}}

    def coletar(self,result=None,**extra):
        self.permanente(); self.configurar_fluxo()
        H.executar(self.exp,'tratamento-padrao',{'config_emcia':str(self.cfg)})
        d=self.chamada('mcp__tally__fetch_submissions',{'formId':'FORM'}); d.update(extra)
        # Simula o hook antes da leitura; nome/seleção chegam depois como metadados locais.
        I.autorizar_mcp(self.cfg,{k:d[k] for k in ('habilitacao','caso','ferramenta','argumentos')})
        return I.registrar_retorno(self.cfg,d,self.resposta() if result is None else result)

    def test_01_efeitos_externos_sem_ok_recusam_e_registram(self):
        H.iniciar(self.exp,'HAB','Pessoa Engenheira','CASO');I.retomar(self.cfg,'HAB','CASO')
        for nome,args in [('mcp__tally__publish_form',{'formId':'FORM'}),(DRIVE+'share_file',{'fileId':'FORA','role':'reader','emailAddress':'cliente@example.invalid'}),
            (CAL+'create_event',{'calendarId':'FORA','attendees':[{'email':'cliente@example.invalid'}]}),(CAL+'send_message',{'text':'Sintético'})]:
            with self.subTest(nome=nome):
                self.assertIn('aprovação',G.conferir(dict(tool_name=nome,tool_input=args),self.cfg))
                self.assertEqual(json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])['evento'],'TentativaNegada')

    def test_02_registrar_outro_caso_recusa_sem_copiar(self):
        with self.assertRaisesRegex(ValueError,'nenhuma submissão'):
            self.coletar(self.resposta(('OUTRO-A',)))
        for p in self.exp.rglob('*'):
            if p.is_file():self.assertNotIn(b'SEGREDO-OUTRO',p.read_bytes())

    def test_03_duas_submissoes_exigem_selecao(self):
        with self.assertRaisesRegex(ValueError,'qual submissão') as exc:self.coletar(self.resposta(('CASO','OUTRO-A','CASO')))
        self.assertIn('SUB-0',str(exc.exception));self.assertIn('SUB-2',str(exc.exception));self.assertNotIn('SUB-1',str(exc.exception))
        d=self.chamada('mcp__tally__fetch_submissions',{'formId':'FORM'});d['submissao']='SUB-2'
        I.autorizar_mcp(self.cfg,d);I.registrar_retorno(self.cfg,d,self.resposta(('CASO','OUTRO-A','CASO')))
        self.assertEqual(json.loads((self.exp/'expediente.json').read_text())['fontes']['S1']['submissao'],'SUB-2')

    def test_04_selecionar_id_alheio_recusa(self):
        with self.assertRaisesRegex(ValueError,'qual submissão'):
            self.coletar(submissao='SUB-0')

    def test_05_pagina_incompleta_nao_registra_fonte(self):
        r=self.resposta();r['resposta']['hasMore']=True
        with self.assertRaisesRegex(ValueError,'páginas'):self.coletar(r)
        self.assertFalse(json.loads((self.exp/'expediente.json').read_text())['fontes'])

    def test_06_caso_nao_oculto_recusa(self):
        r=self.resposta(('CASO',));r['resposta']['submissions'][0].pop('hiddenFields')
        r['resposta']['submissions'][0]['caso']='CASO'
        with self.assertRaisesRegex(ValueError,'nenhuma submissão'):self.coletar(r)

    def test_07_leituras_rascunhos_sem_perfil_sem_ids(self):
        H.iniciar(self.exp,'HAB','Pessoa Engenheira','CASO');I.retomar(self.cfg,'HAB','CASO')
        for nome,args in [('mcp__tally__load_form',{'formId':'FORA'}),('mcp__tally__fetch_submissions',{'formId':'FORA'}),
            ('mcp__tally__create_new_form',{'title':'Sintético'}),('mcp__tally__create_blocks',{'formId':'FORA'}),(DRIVE+'search_files',{'query':'sem pasta'}),
            (DRIVE+'read_file_content',{'fileId':'FORA'}),(DRIVE+'create_file',{'title':'Rascunho','parentId':'FORA'}),(CAL+'list_events',{'calendarId':'FORA'})]:
            with self.subTest(nome=nome):self.assertIsNone(G.conferir(dict(tool_name=nome,tool_input=args),self.cfg))
        self.assertFalse(self.cfg.with_name('perfil-mcp.json').exists())
        with patch.object(I,'calibrar',side_effect=AssertionError('não calibra antes da abertura')):
            I.ambiente(I.ler_config(self.cfg),json.loads((ROOT/'testes/apoio/inventario-mcp-real.json').read_text()))

    def test_08_submissao_unica_so_registra_caso(self):
        self.coletar();s=json.loads((self.exp/'expediente.json').read_text());f=s['fontes']['S1']
        self.assertEqual(f['canal'],'tally');self.assertEqual(f['submissao'],'SUB-1')
        for p in self.exp.rglob('*'):
            if p.is_file():self.assertNotIn(b'SEGREDO-OUTRO',p.read_bytes())
        if self.cfg.with_name('mcp-retornos.json').exists():
            self.assertNotIn('SEGREDO-OUTRO',self.cfg.with_name('mcp-retornos.json').read_text())

    def test_09_ok_simples_fixa_efeito_destinatario_resumo_data(self):
        H.iniciar(self.exp,'HAB','Pessoa Engenheira','CASO');I.retomar(self.cfg,'HAB','CASO')
        d=self.chamada(DRIVE+'share_file',{'fileId':'FORA','emailAddress':'cliente@example.invalid','role':'reader'})
        r=I.aprovar(self.cfg,'mcp',d,'ok','Compartilhar arquivo com Pessoa Cliente')
        I.autorizar_mcp(self.cfg,d,r)
        self.assertIsNone(G.conferir(dict(tool_name=d['ferramenta'],tool_input=d['argumentos']),self.cfg))
        d['argumentos']['emailAddress']='outro@example.invalid'
        self.assertIsNotNone(G.conferir(dict(tool_name=d['ferramenta'],tool_input=d['argumentos']),self.cfg))
        evs=[json.loads(l) for l in self.cfg.with_name('eventos.jsonl').read_text().splitlines()]
        aprovado=next(e for e in evs if e.get('evento')=='AprovacaoChatRegistrada')
        self.assertTrue(aprovado['data']);self.assertEqual(aprovado['testemunho']['literal'],'ok')
        self.assertIn('Compartilhar',aprovado['testemunho']['resumo'])

    def test_10_conferencia_sem_declaracao_de_formid(self):
        self.permanente()
        self.assertFalse(self.cfg.with_name('perfil-mcp.json').exists())

    def test_10b_formato_api_publica_paginado(self):
        perguntas=[dict(id='Q-CASO',title='caso',type='HIDDEN_FIELDS'),dict(id='Q-RESPOSTA',title='HAB-0a-1',type='INPUT_TEXT')]
        ps=[]
        for i,caso in enumerate(('OUTRO-A','CASO')):
            ps.append(dict(page=i+1,hasMore=i==0,questions=perguntas,submissions=[dict(id='SUB-'+str(i),formId='FORM',responses=[
                dict(questionId='Q-CASO',answer=caso),dict(questionId='Q-RESPOSTA',answer='SEGREDO-'+caso)])]))
        self.coletar({'resposta':{'paginas':ps}},respondente='Pessoa Cliente')
        self.assertEqual(json.loads((self.exp/'expediente.json').read_text())['fontes']['S1']['submissao'],'SUB-1')
        for p in self.exp.rglob('*'):
            if p.is_file():self.assertNotIn(b'SEGREDO-OUTRO',p.read_bytes())

    def test_10c_coleta_nao_fica_liberada_apos_abrir(self):
        self.percurso(direta=True)
        d=self.chamada('mcp__tally__fetch_submissions',{'formId':'FORM'})
        with self.assertRaises(ValueError):I.autorizar_mcp(self.cfg,d)
        with self.assertRaises(ValueError):I.registrar_retorno(self.cfg,d,self.resposta())

    def test_11_percurso_conector_e_perfil_na_abertura(self):
        self.percurso(direta=True)
        self.assertTrue((self.case/'registro/ferramentas-externas.json').is_file())
        import os
        if os.environ.get('EMCIA_EVIDENCIA_MCP'):
            pathlib.Path(os.environ['EMCIA_EVIDENCIA_MCP']).write_text(json.dumps(dict(aprovacoes_administrativas=3,depositos=1,coleta='fetch_submissions',
                chamadas_proximo=len(self.chamadas),registro_retorno_coleta=1,perfil_antes_da_abertura=False,perfil_na_abertura=True,
                estados=self.chamadas,isolamento='nenhum SEGREDO-OUTRO no expediente'),ensure_ascii=False,indent=2)+'\n')
        evs=[json.loads(l) for l in (self.case/'registro/eventos.jsonl').read_text().splitlines()]
        self.assertTrue(any(e['evento']=='PerfilExternoDefinido' for e in evs))
        with self.assertRaisesRegex(ValueError,'não declarada'):
            I.autorizar_mcp(self.cfg,self.chamada(DRIVE+'list_recent_files',{}))
        for p in self.exp.rglob('*'):
            if p.is_file():self.assertNotIn(b'SEGREDO-OUTRO',p.read_bytes())

class DepoisDaAbertura(CasoHook):
    def test_01_ferramenta_sem_perfil_continua_negada_pelo_nucleo(self):
        self.negado('mcp__claude_ai_Google_Drive__list_recent_files',{})

if __name__=='__main__':unittest.main(verbosity=2)
