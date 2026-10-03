"""Passagem 0d: negativas primeiro, sobre componentes reais e dados sintéticos."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from apoio.habilitacao_0d import criar, H, RAIZ
from apoio.hook_real import CasoHook

IMPORTADOR=RAIZ/'eiac-campo/scripts/importar_habilitacao.py'


class Importacao(CasoHook):
    def setUp(self):
        super().setUp()
        self.exp=criar(self.base/'expediente',self.estado['caso'],'Celso do Vale')
        from apoio.canais import definir
        definir(self.caso)

    def importar(self, *args):
        return subprocess.run([sys.executable,str(IMPORTADOR),'--expediente',str(self.exp),*args],
                              cwd=self.caso,text=True,capture_output=True)

    def alterar(self, fn):
        p=self.exp/'expediente.json'; s=json.loads(p.read_text()); fn(s); p.write_text(json.dumps(s))

    def recusa(self, trecho, *args):
        antes=len(self.eventos()); r=self.importar(*args)
        self.assertNotEqual(r.returncode,0,r.stdout)
        self.assertIn(trecho,r.stderr)
        self.assertEqual(len(self.eventos()),antes+1)
        self.assertEqual(self.eventos()[-1]['evento'],'TentativaNegada')
        self.assertEqual(self.eventos()[-1]['autor'],'Celso do Vale')
        return r

    def test_01_sem_formalizacao(self):
        self.alterar(lambda s:s['documentos']['HAB-01'][-1].update(assinatura=None))
        self.recusa('formalização')

    def test_02_sem_acessos(self):
        self.alterar(lambda s:s.update(acessos=None)); self.recusa('acessos')

    def test_03_caso_divergente(self):
        self.alterar(lambda s:s.update(caso_reservado='outro')); self.recusa('reservado')

    def test_04_responsavel_divergente(self):
        self.alterar(lambda s:s.update(responsavel='Outra Pessoa')); self.recusa('responsável')

    def test_05_nao_prosseguir(self):
        H.executar(self.exp,'nao-prosseguir',{'decisor':'Celso do Vale','motivo':'Controle negativo',
                                         'condicao_retomada':'Nova decisão necessária'})
        self.recusa('não prosseguir')

    def test_06_pdf_adulterado(self):
        s=json.loads((self.exp/'expediente.json').read_text())
        ref=s['documentos']['HAB-01'][-1]['assinatura']['arquivo']
        (self.exp/ref['caminho']).write_bytes(b'%PDF-1.7\nadulterado\n%%EOF')
        self.recusa('integridade')

    def test_07_sessao_do_agente(self):
        r=self.negado('Bash',{'command':f'python3 {IMPORTADOR} --expediente {self.exp}'})
        self.assertIn('Comando exato:',r.stderr)
        self.assertEqual(self.eventos()[-1]['operacao'],'importar-habilitacao')

    def test_08_segunda_importacao(self):
        r=self.importar(); self.assertEqual(r.returncode,0,r.stderr)
        self.recusa('importação anterior')

    def test_09_autor_agente(self):
        self.recusa('autor','--autor','AG-01')

    def test_10_etapa_encerrada(self):
        self.estado['cumprimentos']['F0']={'cumprido':True}; self.salvar()
        self.recusa('etapa encerrada')

    def test_11_matriz_adulterada(self):
        self.alterar(lambda s:s['acessos']['itens'][0].update(item='Outra fonte'))
        self.recusa('matriz')

    def test_20_importa_apenas_artefatos_autorizados(self):
        r=self.importar(); self.assertEqual(r.returncode,0,r.stderr)
        reg=json.loads((self.caso/'registro/habilitacao.json').read_text())
        v=reg['vigente']; self.assertEqual(v['desfecho'],'prosseguir')
        self.assertEqual(len(v['arquivos']),7)
        self.assertEqual(self.eventos()[-1]['evento'],'HabilitacaoImportada')
        self.assertFalse((self.caso/'caso/00-habilitacao.md').exists())
        draft=self.caso/'rascunho/00-habilitacao.md'
        self.assertTrue(all(x.startswith('- [') for x in draft.read_text().splitlines()))
        r=self.rodar('validar.py','--arquivo','caso/00-habilitacao.md')
        self.assertEqual(r.returncode,0,r.stderr)
        import hashlib
        for ref in v['arquivos'].values():
            self.assertEqual(hashlib.sha256((self.caso/ref['caminho']).read_bytes()).hexdigest(),ref['sha256'])

    def test_21_reimportacao_decidida_preserva_historico(self):
        r=self.importar(); self.assertEqual(r.returncode,0,r.stderr)
        antigo=json.loads((self.caso/'registro/habilitacao.json').read_text())['vigente']
        p=self.base/'decisao.json'; p.write_text(json.dumps(dict(decisor='Celso do Vale',
            motivo='Nova conferência sintética',data='2026-10-02',importacao_anterior=antigo['id'])))
        r=self.importar('--decisao-reimportacao',str(p)); self.assertEqual(r.returncode,0,r.stderr)
        reg=json.loads((self.caso/'registro/habilitacao.json').read_text())
        self.assertEqual(reg['historico'],[antigo])
        self.assertNotEqual(reg['vigente']['id'],antigo['id'])
        self.assertTrue(all((self.caso/r['caminho']).exists() for r in antigo['arquivos'].values()))

    def test_22_migra_formulario_com_vinculo(self):
        r=self.importar(); self.assertEqual(r.returncode,0,r.stderr)
        canais=json.loads((self.caso/'registro/canais.json').read_text())
        canal=next(c for c in canais['canais'] if c['finalidade']=='habilitacao')
        self.assertEqual(canal['ids']['formulario_id'],'FORM-SINTETICO')
        self.assertEqual(canal['origem']['fontes'],['S1'])
        self.assertEqual(canal['origem']['habilitacao'],'HAB-CONTROLE')
        import hashlib
        self.assertEqual(canal['origem']['expediente_sha256'],hashlib.sha256((self.exp/'expediente.json').read_bytes()).hexdigest())

    def test_12_workspace_divergente_recusa_com_evento(self):
        self.alterar(lambda s:s['fontes']['S1'].update(workspace_id='WORKSPACE-ALHEIO'))
        self.recusa('workspace')

    def test_13_canais_ausentes_recusa_com_evento(self):
        (self.caso/'registro/canais.json').unlink()
        self.recusa('canais ausentes')


class SeloConfirmado(CasoHook):
    def setUp(self):
        super().setUp()
        self.exp=criar(self.base/'expediente',self.estado['caso'],'Celso do Vale')
        from apoio.canais import definir
        definir(self.caso)
        self.git('init','-q'); self.git('config','user.name','Celso do Vale')
        self.git('config','user.email','sintetico@example.invalid')
        self.git('config','commit.gpgsign','false')
        self.git('config','core.hooksPath',str(self.caso/'.git/hooks'))
        self.git('add','-A'); self.git('commit','-qm','abertura sintética')

    def git(self,*args):
        r=subprocess.run(['git',*args],cwd=self.caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr); return r.stdout.strip()

    def importar(self):
        from apoio.canais import definir
        definir(self.caso)
        r=subprocess.run([sys.executable,str(IMPORTADOR),'--expediente',str(self.exp)],
                         cwd=self.caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr)

    def selar(self):
        (self.caso/'rascunho/marcador').write_text(str(len(self.eventos())))
        return self.rodar('selar.py','--nota','selo sintético confirmado')

    def bloqueado(self):
        return self.negado('Skill',{'skill':'eiac-campo:hb-enquadrar'})

    def test_01_habilidade_sem_evento(self):
        r=self.bloqueado(); self.assertIn('HabilitacaoImportada',r.stderr)

    def test_02_importacao_sem_selo(self):
        self.importar(); r=self.bloqueado(); self.assertIn('SeloAplicado',r.stderr)

    def test_03_encerrar_sem_selo(self):
        self.importar(); antes=len(self.eventos())
        r=self.rodar('avancar.py','--encerrar','F0','--autor','Celso do Vale')
        self.assertNotEqual(r.returncode,0,r.stdout); self.assertIn('SeloAplicado',r.stderr)
        self.assertEqual(len(self.eventos()),antes+1)
        self.assertEqual(self.eventos()[-1]['evento'],'TentativaNegada')

    def test_04_commit_recusado_nao_libera(self):
        self.importar()
        hook=self.caso/'.git/hooks/pre-commit';hook.write_text('#!/bin/sh\nexit 1\n');hook.chmod(0o755)
        self.assertNotEqual(self.selar().returncode,0)
        r=self.bloqueado(); self.assertIn('confirmado',r.stderr)

    def test_05_selo_anterior_nao_libera(self):
        self.assertEqual(self.selar().returncode,0)
        self.importar(); self.bloqueado()

    def test_06_git_inacessivel_recusa(self):
        self.importar(); self.assertEqual(self.selar().returncode,0)
        (self.caso/'.git').rename(self.caso/'.git-indisponivel')
        r=self.bloqueado(); self.assertIn('Git',r.stderr)

    def test_07_reimportacao_exige_novo_selo(self):
        self.importar();self.assertEqual(self.selar().returncode,0)
        ident=json.loads((self.caso/'registro/habilitacao.json').read_text())['vigente']['id']
        p=self.base/'decisao.json';p.write_text(json.dumps(dict(decisor='Celso do Vale',motivo='Nova conferência',
            data='2026-10-02',importacao_anterior=ident)))
        r=subprocess.run([sys.executable,str(IMPORTADOR),'--expediente',str(self.exp),
            '--decisao-reimportacao',str(p)],cwd=self.caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr);self.bloqueado()

    def test_08_commit_comum_nao_confirma_tentativa_recusada(self):
        self.importar()
        hook=self.caso/'.git/hooks/pre-commit';hook.write_text('#!/bin/sh\nexit 1\n');hook.chmod(0o755)
        self.assertNotEqual(self.selar().returncode,0);hook.unlink()
        self.git('add','-A');self.git('commit','-qm','commit comum, sem aplicação de selo')
        self.bloqueado()

    def test_20_selo_posterior_libera_habilidade_e_encerramento(self):
        self.importar()
        r=self.rodar('validar.py','--arquivo','caso/00-habilitacao.md');self.assertEqual(r.returncode,0,r.stderr)
        r=self.selar();self.assertEqual(r.returncode,0,r.stderr)
        r=self.hook('Skill',{'skill':'eiac-campo:hb-enquadrar'});self.assertEqual(r.returncode,0,r.stderr)
        r=self.rodar('avancar.py','--encerrar','F0','--autor','Celso do Vale');self.assertEqual(r.returncode,0,r.stderr)

    def test_21_contrato_alternativo_generico(self):
        self.importar()
        p=self.caso/'registro/playbook.json';pb=json.loads(p.read_text())
        pb['etapas'][0]['exige_evento_selado']='FontePreparada';p.write_text(json.dumps(pb))
        log=self.caso/'registro/eventos.jsonl';evs=self.eventos()
        for e in evs:
            if e['evento']=='HabilitacaoImportada':e['evento']='FontePreparada'
        log.write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in evs))
        r=self.selar();self.assertEqual(r.returncode,0,r.stderr)
        r=self.hook('Skill',{'skill':'eiac-campo:hb-enquadrar'});self.assertEqual(r.returncode,0,r.stderr)


class Abertura(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=pathlib.Path(self.tmp.name)
        self.exp=criar(self.base/'expediente','controle','Celso do Vale')
        self.destino=self.base/'casos';self.destino.mkdir()

    def abrir(self,*args,raiz=RAIZ):
        return subprocess.run(['bash',str(raiz/'novo-caso.sh'),'controle','--responsavel',
            'Celso do Vale',str(self.destino),*args],text=True,capture_output=True)

    def recusa(self,r,trecho):
        self.assertNotEqual(r.returncode,0,r.stdout);self.assertIn(trecho,r.stderr)
        self.assertIn('TentativaNegada',r.stderr)
        self.assertFalse((self.destino/'controle').exists())
        log=self.destino/'.emcia-abertura-eventos.jsonl'
        evento=json.loads(log.read_text().splitlines()[-1])
        self.assertEqual(evento['evento'],'TentativaNegada')
        self.assertEqual(evento['autor'],'Celso do Vale')

    def copia_ferramenta(self):
        copia=self.base/'ferramenta';copia.mkdir()
        shutil.copyfile(RAIZ/'novo-caso.sh',copia/'novo-caso.sh')
        shutil.copytree(RAIZ/'eiac-campo',copia/'eiac-campo')
        shutil.copytree(RAIZ/'eiac-nucleo',copia/'eiac-nucleo')
        return copia

    def test_00_base_antes_e_depois_da_opcao(self):
        for depois in (False, True):
            with self.subTest(base_depois=depois):
                nome = 'ordem-' + str(depois).lower()
                args = [nome, '--responsavel', 'Celso do Vale', str(self.destino)] if depois else [nome, str(self.destino), '--responsavel', 'Celso do Vale']
                r = subprocess.run([sys.executable, str(RAIZ/'eiac-campo/scripts/abrir_caso.py'), *args], text=True, capture_output=True)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertTrue((self.destino/nome/'registro/estado.json').is_file())

    def test_01_manifesto_divergente(self):
        copia=self.copia_ferramenta()
        manifesto=json.loads((copia/'eiac-campo/reference/metodo/manifesto.json').read_text())
        nome=next(iter(manifesto['documentos']))
        p=copia/'eiac-campo/reference/metodo'/nome;p.write_text(p.read_text()+'controle adulterado')
        self.recusa(self.abrir(raiz=copia),'SHA-256')

    def test_02_identificador_divergente_antes_da_abertura(self):
        p=self.exp/'expediente.json';d=json.loads(p.read_text());d['caso_reservado']='outro';p.write_text(json.dumps(d))
        self.recusa(self.abrir('--expediente',str(self.exp)),'reservado')

    def test_03_expediente_incompleto(self):
        p=self.exp/'expediente.json';d=json.loads(p.read_text());d['acessos']=None;p.write_text(json.dumps(d))
        self.recusa(self.abrir('--expediente',str(self.exp)),'acessos')

    def test_20_percurso_desde_novo_caso(self):
        r=self.abrir('--expediente',str(self.exp));self.assertEqual(r.returncode,0,r.stderr)
        caso=self.destino/'controle'
        manifesto=json.loads((caso/'metodo/manifesto.json').read_text())
        import hashlib
        for nome,sha in manifesto['documentos'].items():
            self.assertEqual(hashlib.sha256((caso/'metodo'/nome).read_bytes()).hexdigest(),sha)
        for key,value in [('user.name','Celso do Vale'),('user.email','sintetico@example.invalid')]:
            subprocess.run(['git','config',key,value],cwd=caso,check=True)
        def rodar(path,*args,entrada=None):
            r=subprocess.run([sys.executable,str(RAIZ/path),*args],cwd=caso,input=entrada,text=True,capture_output=True)
            self.assertEqual(r.returncode,0,r.stderr);return r
        from apoio.canais import definir
        definir(caso)
        rodar('eiac-campo/scripts/importar_habilitacao.py','--expediente',str(self.exp))
        rodar('eiac-nucleo/scripts/validar.py','--arquivo','caso/00-habilitacao.md')
        from apoio.canais import definir
        definir(caso)
        rodar('eiac-nucleo/scripts/selar.py','--nota','habilitação conferida')
        rodar('eiac-nucleo/scripts/guarda.py',entrada=json.dumps(dict(tool_name='Skill',tool_input={'skill':'eiac-campo:hb-enquadrar'})))
        st=json.loads(rodar('eiac-nucleo/scripts/estado.py').stdout)
        self.assertTrue(st['integridade_referencia']['confere'])

    def test_21_diagnostico_de_integridade_nao_bloqueia(self):
        r=self.abrir();self.assertEqual(r.returncode,0,r.stderr)
        caso=self.destino/'controle';p=caso/'metodo/manifesto.json'
        manifesto=json.loads(p.read_text());nome=next(iter(manifesto['documentos']))
        (caso/'metodo'/nome).write_text('adulterado')
        estado=caso/'registro/estado.json';antes=estado.read_bytes()
        trilha=caso/'registro/eventos.jsonl';eventos=trilha.read_bytes()
        r=subprocess.run([sys.executable,str(RAIZ/'eiac-nucleo/scripts/estado.py')],cwd=caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertFalse(json.loads(r.stdout)['integridade_referencia']['confere'])
        self.assertEqual(estado.read_bytes(),antes);self.assertEqual(trilha.read_bytes(),eventos)
        r=subprocess.run([sys.executable,str(RAIZ/'eiac-nucleo/scripts/avancar.py'),
            '--apurar-nivel','N2','--eixos','DAD 5, GOV 3, CRI 6','--autor','Celso do Vale'],cwd=caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr)


class Restricoes(CasoHook):
    def setUp(self):
        super().setUp()
        self.exp=criar(self.base/'expediente',self.estado['caso'],'Celso do Vale',restricao=True)
        from apoio.canais import definir
        definir(self.caso)
        r=subprocess.run([sys.executable,str(IMPORTADOR),'--expediente',str(self.exp)],
                         cwd=self.caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr)
        # Insumo real de E1; a restrição precisa ser a causa da recusa.
        self.estado.update(nivel='N2',cumprimentos={'F0':{'cumprido':True,'eixos':'DAD 5, GOV 3, CRI 6','autor':'Celso do Vale'}})
        self.salvar()

    def renderizar(self,entregavel):
        return subprocess.run([sys.executable,str(RAIZ/'eiac-campo/scripts/entregaveis.py'),
            '--renderizar',entregavel,'--autor','Celso do Vale'],cwd=self.caso,text=True,capture_output=True)

    def test_01_restricao_sem_destino_recusa_com_evento(self):
        for ent in ['E1','E2','E3','E4','E5']:
            with self.subTest(ent=ent):
                antes=len(self.eventos());r=self.renderizar(ent)
                self.assertNotEqual(r.returncode,0,r.stdout);self.assertIn('RH-01',r.stderr)
                self.assertIn('destino',r.stderr)
                self.assertEqual(len(self.eventos()),antes+1)
                self.assertEqual(self.eventos()[-1]['evento'],'TentativaNegada')
                self.assertEqual(self.eventos()[-1]['autor'],'Celso do Vale')
                self.assertFalse((self.caso/'caso/entregaveis'/str(ent+'.md')).exists())

    def test_02_recusa_nao_sobrescreve_entregavel_anterior(self):
        p=self.caso/'caso/entregaveis/E1.md';p.parent.mkdir(parents=True);p.write_text('versão sintética anterior')
        r=self.renderizar('E1');self.assertNotEqual(r.returncode,0,r.stdout)
        self.assertEqual(p.read_text(),'versão sintética anterior')
        self.assertEqual(self.eventos()[-1]['evento'],'TentativaNegada')

    def test_20_sem_restricao_materializa_comportamento_existente(self):
        p=self.caso/'registro/habilitacao.json';reg=json.loads(p.read_text())
        reg['vigente']['restricoes']=[];reg['vigente']['desfecho']='prosseguir';p.write_text(json.dumps(reg))
        r=self.renderizar('E1');self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn('Nível de complexidade declarado',(self.caso/'caso/entregaveis/E1.md').read_text())


if __name__=='__main__': unittest.main(verbosity=2)
