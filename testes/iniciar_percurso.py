"""MCP sintético e operações reais: cinco aprovações, três retomadas e selo Git."""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

RAIZ=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'eiac-campo/scripts'));sys.path.insert(0,str(RAIZ/'eiac-nucleo/scripts'))
import iniciar as I
import habilitacao as H
import saida_inicial as S
import aprovacao as A
import guarda_inicial as GI

class Percurso(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=pathlib.Path(self.tmp.name);self.cfg=self.base/'config.json';self.hab='HAB-SINTETICA';self.caso='CASO-SINTETICO'
        self.responsavel='Pessoa Engenheira';self.exp=self.base/'expedientes'/self.hab;self.case=self.base/'casos'/self.caso
        self.c=dict(responsavel=self.responsavel,base_casos=str(self.base/'casos'),base_expedientes=str(self.base/'expedientes'),
            workspace_tally='WORK-SINTETICO',pasta_drive='ROOT-SINTETICA',calendario_casos='CAL-SINTETICO',navegador='google-chrome')
        I.configurar(self.cfg,self.c)
        self.literal=['Aprovo o envio do formulário e o plano administrativo de rodadas descrito',
            'Conferi e aprovo a carta apresentada','Conferi os três PDFs, signatários e o plano de assinatura',
            'Decido abrir o caso com esta árvore e o plano local até F0 liberado',
            'Aprovo os compartilhamentos listados, com pasta, destinatário e papel']
        self.grupo=0
        self.inventory=json.loads((RAIZ/'testes/apoio/inventario-mcp-real.json').read_text())
        self.pdfpatch=patch.object(I.H,'pdf_bytes',side_effect=lambda md,b:b'%PDF-1.7\n'+md.encode()+b'\n%%EOF');self.pdfpatch.start();self.addCleanup(self.pdfpatch.stop)
        self.raw=self.base/'resposta.json';self.raw.write_text('{"tipo":"dados exclusivamente sintéticos", "caso":"CASO-SINTETICO"}')
    def op(self,nome,**kwargs):
        d=dict(habilitacao=self.hab,caso=self.caso,**kwargs)
        literal='conferido' if nome=='confirmar-formulario' else self.literal[self.grupo]
        r=I.aprovar(self.cfg,nome,d,literal,'Plano sintético; '+nome)
        return I.operar(self.cfg,nome,d,r)
    def habop(self,nome,**entrada):return self.op(nome,entrada=entrada)
    def mcp(self,nome,args,ids,resposta=None,**declaracao):
        d=dict(habilitacao=self.hab,caso=self.caso,ferramenta=nome,argumentos=args,**declaracao)
        r=I.aprovar(self.cfg,'mcp',d,self.literal[self.grupo],'Efeito MCP sintético explícito')
        I.operar(self.cfg,'mcp',d,r)
        ev=dict(tool_name=nome,tool_input=args,cwd=str(self.base))
        self.assertIsNone(GI.conferir(ev,self.cfg))
        # Esta é a única substituição da origem externa: chamada simulada.
        retorno=dict(ids=ids,origem='MCP simulado, nenhum cliente real')
        if resposta is not None:retorno['resposta']=resposta
        I.registrar_retorno(self.cfg,d,retorno)
    def primeira_parte(self):
        d=dict(habilitacao=self.hab,caso=self.caso,ferramentas=self.inventory,perfil=I.calibrar(self.inventory))
        I.operar(self.cfg,'perfil',d,I.aprovar(self.cfg,'perfil',d,'Aprovo este perfil restrito','Perfil inicial'))
        d=dict(habilitacao=self.hab,caso=self.caso,texto='uso as minutas sem ratificação jurídica')
        I.operar(self.cfg,'aceitar-minutas',d,I.aprovar(self.cfg,'aceitar-minutas',d,d['texto'],'Aceitação inicial sintética'))
        self.op('iniciar',id=self.hab)
        self.habop('tratamento',escopo='administrativo',condicoes='Plano administrativo sintético',provedor='Provedor sintético',decisor=self.responsavel,evidencia=str(self.raw))
        I.retomar(self.cfg,self.hab,self.caso)
        self.mcp('mcp__tally__create_new_form',{'workspaceId':'WORK-SINTETICO','title':'Habilitação sintética'}, {'formulario_id':'FORM-SINTETICO'})
        resposta=json.loads((RAIZ/'testes/apoio/tally-load-form.json').read_text())
        resposta['data'].update(formId='FORM-SINTETICO',workspaceId='WORK-SINTETICO')
        self.mcp('mcp__tally__load_form',{'formId':'FORM-SINTETICO'}, {},resposta=resposta)
        relatorio=self.op('conferir-formulario',formulario_id='FORM-SINTETICO',modelo='habilitacao')
        self.op('confirmar-formulario',formulario_id='FORM-SINTETICO',relatorio_sha256=relatorio['sha256'])
        self.mcp('mcp__tally__publish_form',{'formId':'FORM-SINTETICO'}, {})
        self.op('caminho-manual',passo='coletar-submissoes',decisao='executar manualmente',evidencia=str(self.raw))
        self.habop('receber',id='S1',arquivo=str(self.raw),formulario='FORM-SINTETICO',workspace_id='WORK-SINTETICO',
                   submissao='SUB-S1',respondente='Pessoa Cliente',versao_perguntas='sintetica-1',rodada=0,canal='manual')
        self.habop('pendencia',id='PEND',origem='S1',pergunta='Qual o limite?',efeito='carta',rodada=1)
        self.assertEqual(I.retomar(self.cfg,self.hab,self.caso)['proximo'],'rodadas')
        self.habop('receber',id='S2',arquivo=str(self.raw),formulario='FORM-SINTETICO',workspace_id='WORK-SINTETICO',submissao='SUB-S2',
                   respondente='Pessoa Cliente',versao_perguntas='sintetica-rodada',rodada=1,canal='manual')
        self.habop('resolver',id='PEND',resposta='S2',decisor=self.responsavel,motivo='Limite confirmado pela pessoa')
        campos={k:{'valor':'Controle sintético '+k,'fonte':'S2'} for f in H.TEMPLATES.values() for k in H.TOKEN.findall((RAIZ/'eiac-campo/reference/metodo'/f).read_text())}
        campos['signatario']['valor']='Pessoa Cliente'
        self.habop('consolidar',campos=campos)
        self.grupo=1
        self.habop('revisar',decisor=self.responsavel,motivo='Carta conferida',qualificacao_0a=True,conteudo_conferido=True,evidencia=str(self.raw))
        self.habop('gerar')
        antes=json.loads((self.exp/'expediente.json').read_text())
        self.assertEqual(I.retomar(self.cfg,self.hab,self.caso)['proximo'],'conferir PDFs/assinaturas')
        self.assertEqual(json.loads((self.exp/'expediente.json').read_text()),antes)
    def terminar(self,ratificar=False):
        if ratificar:
            self.habop('revisao-juridica',revisor='Pessoa Jurista',decisor=self.responsavel,data='2026-10-05',resultado='aprovado',
                documentos={d:H.digest((RAIZ/'eiac-campo/reference/metodo'/H.TEMPLATES[d]).read_bytes()) for d in ('HAB-02','HAB-03')},evidencia=str(self.raw))
            self.habop('gerar')
        self.grupo=2
        s=json.loads((self.exp/'expediente.json').read_text())
        for doc in H.CODIGOS_HAB:
            versao=s['documentos'][doc][-1]['versao']
            self.habop('liberar',documento=doc,versao=versao,decisor=self.responsavel,pdf_conferido=True,ferramenta='Painel sintético',operador='Pessoa Cliente',
                signatarios=[dict(nome='Pessoa Cliente',papel='organizacao',competencia='controle'),dict(nome=self.responsavel,papel='emcia',competencia='controle')])
            pdf=self.base/(doc+'-assinado.pdf');pdf.write_bytes(b'%PDF-1.7\nassinatura sintetica\n%%EOF')
            self.habop('assinatura',documento=doc,versao=versao,decisor=self.responsavel,arquivo=str(pdf),evidencia=str(self.raw),referencia='Devolução sintética informada pelo engenheiro',
                conteudo_conferido=True,evidencias_conferidas=True,signatarios=[dict(nome='Pessoa Cliente',papel='organizacao',data='2026-10-05'),dict(nome=self.responsavel,papel='emcia',data='2026-10-05')])
        self.habop('concluir-0b')
        self.mcp('mcp__claude_ai_Google_Calendar__list_events',{'calendarId':'CAL-SINTETICO'}, {})
        self.habop('acessos',patrocinador='Pessoa Cliente',executor='Pessoa Executora',decisor=self.responsavel,autoridade_patrocinador='controle',executor_liberado=True,agenda_reservada=True,
            data_sessao='2026-10-15',itens=[dict(item='Fonte sintética',status='concedido',evidencia='conferência sintética')])
        self.habop('preparar-0d')
        self.grupo=3
        with patch.dict('os.environ',{'GIT_AUTHOR_NAME':self.responsavel,'GIT_AUTHOR_EMAIL':'controle@example.invalid','GIT_COMMITTER_NAME':self.responsavel,'GIT_COMMITTER_EMAIL':'controle@example.invalid'}):
            self.op('abrir',desfecho='prosseguir')
        for args in [('user.name',self.responsavel),('user.email','controle@example.invalid'),('commit.gpgsign','false')]:
            subprocess.run(['git','config',*args],cwd=self.case,check=True)
        self.mcp('mcp__claude_ai_Google_Drive__create_file',{'parentId':'ROOT-SINTETICA','title':self.caso,'contentMimeType':'application/vnd.google-apps.folder'},{'pasta_id':'PASTA-CASO'},finalidade='raiz-caso')
        self.folders={}
        for n in ('00-habilitacao','entrada-documentos','entrada-amostras','entregas','trabalho-interno'):
            ident='PASTA-'+n
            self.mcp('mcp__claude_ai_Google_Drive__create_file',{'parentId':'PASTA-CASO','title':n,'contentMimeType':'application/vnd.google-apps.folder'},{'pasta_id':ident},finalidade=n)
            self.folders[n]=ident
        self.mcp('mcp__tally__create_new_form',{'workspaceId':'WORK-SINTETICO','title':'Triagem sintética'}, {'formulario_id':'FORM-triagem'})
        self.grupo=4
        self.mcp('mcp__claude_ai_Google_Drive__share_file',{'fileId':'PASTA-CASO','emailAddress':'cliente@example.invalid','role':'reader'}, {})
        self.grupo=3
        pb=json.loads((self.case/'registro/playbook.json').read_text());canais=[]
        for f in pb['canais_previstos']:
            if f['finalidade']=='ciclo':continue # Finalidade posterior ao bloco inicial.
            ids={'tally':{'workspace_id':'WORK-SINTETICO','formulario_id':'FORM-SINTETICO' if f['finalidade']=='habilitacao' else 'FORM-'+f['finalidade']},
                'drive':{'drive_id':'DRIVE-SINTETICO','pasta_id':self.folders[{'documentos':'entrada-documentos','amostras':'entrada-amostras','entregas':'entregas','trabalho-interno':'trabalho-interno'}.get(f['finalidade'],'00-habilitacao')]},'calendar':{'calendario_id':'CAL-SINTETICO'}}[f['ferramenta']]
            canais.append(dict(f,ids=ids,proprietario='emcia',acesso_cliente='nenhum',sensivel=False,
                filtro={'campo':'caso','valor':self.caso} if f['ferramenta']=='tally' else None,marcador='[{caso}/{etapa}]' if f['ferramenta']=='calendar' else None))
        self.op('definir-canais',entrada=dict(versao=1,caso=self.caso,decidido_por=self.responsavel,data='2026-10-05',canais=canais))
        self.op('importar');self.op('validar')
        self.assertEqual(I.retomar(self.cfg,self.hab,self.caso)['proximo'],'selar')
        r=S.conferir(self.exp,self.case);self.assertFalse(r['liberado']);self.assertFalse(next(x for x in r['itens'] if x['item']=='selo confirmado no Git')['presente'])
        self.op('selar',nota='habilitação sintética importada e conferida')
        return S.conferir(self.exp,self.case)
    def test_01_percurso_e_tres_retomadas(self):
        self.primeira_parte();r=self.terminar();self.assertTrue(r['liberado'],r)
        self.assertEqual(len(r['pendencias']),2)
        self.assertEqual(I.retomar(self.cfg,self.hab,self.caso)['proximo'],'saída conferida')
        s=json.loads((self.exp/'expediente.json').read_text())
        for doc in H.CODIGOS_HAB:
            pdf=H.ler_arquivo(self.exp,s['documentos'][doc][-1]['pdf'])
            for marca in ('Controle do modelo','Revisão jurídica','ratificação','aceitacao_minutas'):
                self.assertNotIn(marca.encode(),pdf)
        evs=[json.loads(l) for l in self.cfg.with_name('eventos.jsonl').read_text().splitlines()]
        content={e['testemunho']['literal'] for e in evs if e['evento']=='AprovacaoChatRegistrada' and e['testemunho']['literal'] in self.literal}
        self.assertEqual(len(content),5)
    def test_02_ratificacao_sem_pendencia(self):
        self.primeira_parte();r=self.terminar(ratificar=True)
        self.assertTrue(r['liberado'],r);self.assertFalse(r['pendencias'])
    def test_03_efeito_mcp_sem_aprovacao(self):
        self.primeira_parte()
        with self.assertRaisesRegex(ValueError,'aprovação'):
            I.autorizar_mcp(self.cfg,dict(habilitacao=self.hab,caso=self.caso,ferramenta='mcp__claude_ai_Google_Drive__share_file',argumentos={'fileId':'PASTA-SINTETICA','emailAddress':'cliente@example.invalid','role':'reader'}))
    def test_04_id_alheio_recusado_no_caso(self):
        self.primeira_parte()
        # A recusa por perfil começa na abertura; não restringe a habilitação.
        I.B.abrir(self.caso,self.base/'casos',self.responsavel)
        self.op('perfil',ferramentas=self.inventory,perfil=I.calibrar(self.inventory))
        with self.assertRaisesRegex(ValueError,'campo oculto'):
            I.autorizar_mcp(self.cfg,dict(habilitacao=self.hab,caso=self.caso,ferramenta='mcp__tally__fetch_submissions',argumentos={'formId':'OUTRO-CASO'}))

if __name__=='__main__':unittest.main(verbosity=2)
