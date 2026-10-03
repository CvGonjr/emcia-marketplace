"""Decisão 041: negativas de vínculo, encerramento e emissão antes dos controles."""
import hashlib, json, pathlib, subprocess, sys, unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.habilitacao_0d import criar
SCRIPT=RAIZ/'eiac-campo/scripts/restricoes.py'

class Restricoes(CasoHook):
    def setUp(self):
        super().setUp()
        from apoio.canais import definir
        definir(self.caso)
        exp=criar(self.base/'exp',self.estado['caso'],'Celso do Vale',restricao=True)
        r=self.campo('importar_habilitacao.py','--expediente',str(exp));self.assertEqual(r.returncode,0,r.stderr)
        self.estado.update(etapa_atual='P2',camada_atual='EX2',cumprimentos={
            'F0':{'cumprido':True,'eixos':'DAD 5, GOV 3, CRI 6','autor':'Celso do Vale'},'P1':{'cumprido':True}})
        self.salvar()
        self.fonte('F-001')
        self.baseline(['F-001'])

    def campo(self,script,*args):
        return subprocess.run([sys.executable,str(RAIZ/'eiac-campo/scripts'/script),*args],cwd=self.caso,text=True,capture_output=True)

    def fonte(self,ident,**extras):
        d=dict(id=ident,fonte='Planilha sintética',tipo='planilha',responsavel='Marina Prado',
               contrato=dict(estrutura='Uma linha por envio',significado='Registro de envios',qualidade='Conferida'),
               acesso='Leitura autorizada',procedencia='D',registrado_por='Celso do Vale',data='2026-10-03',**extras)
        p=self.caso/'rascunho'/str(ident+'.yaml');p.write_text('\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in d.items())+'\n')
        r=self.rodar('curar.py','--tipo','fonte','--arquivo',f'contexto/fontes/{ident}.yaml')
        self.assertEqual(r.returncode,0,r.stderr)

    def baseline(self,refs):
        d=dict(id='BL-001',indicador='Tempo sintético',valor_atual='10 minutos',apuracao='medido',nivel='N2',
               data='2026-10-03',procedencia='D',declarado_por='Celso do Vale',registrado_por='Celso do Vale',versao=1,fontes=refs)
        (self.caso/'rascunho/BL-001.yaml').write_text('\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in d.items())+'\n')
        r=self.campo('baseline.py','--arquivo','registro/baseline/BL-001.yaml','--ator','Celso do Vale')
        self.assertEqual(r.returncode,0,r.stderr)

    def vincular(self,*args):
        return self.campo('restricoes.py','vincular','--restricao','RH-01','--fontes','F-001',*args)

    def recusa(self,r,trecho):
        self.assertNotEqual(r.returncode,0,r.stdout);self.assertIn(trecho,r.stderr)
        self.assertEqual(self.eventos()[-1]['evento'],'TentativaNegada')
        self.assertEqual(self.eventos()[-1]['autor'],'Celso do Vale')

    def render(self):
        return self.campo('entregaveis.py','--renderizar','E2','--autor','Celso do Vale')

    def test_01_sessao(self):
        comando=f'python3 {SCRIPT} vincular --restricao RH-01 --fontes F-001'
        r=self.negado('Bash',{'command':comando});self.assertIn('Comando exato: '+comando,r.stderr)
        self.assertEqual(self.eventos()[-1]['operacao'],'vincular-restricao')

    def test_02_rh_inexistente(self):
        self.recusa(self.campo('restricoes.py','vincular','--restricao','RH-99','--fontes','F-001'),'RH-99')

    def test_03_fonte_nao_curada(self):
        self.recusa(self.campo('restricoes.py','vincular','--restricao','RH-01','--fontes','F-999'),'curada')

    def test_04_dispensa_sem_motivo(self):
        self.recusa(self.campo('restricoes.py','dispensar','--restricao','RH-01','--motivo',''),'motivo')

    def test_05_autor_agente(self):
        self.recusa(self.vincular('--autor','AG-01'),'pessoa nomeada')

    def test_06_etapa_errada(self):
        self.estado['etapa_atual']='P1';self.salvar();self.recusa(self.vincular(),'P2')

    def test_07_p2_pendente(self):
        r=self.rodar('avancar.py','--encerrar','P2','--autor','Celso do Vale')
        self.recusa(r,'RH-01');self.assertEqual(json.loads((self.caso/'registro/estado.json').read_text())['etapa_atual'],'P2')

    def test_08_emissao_pendente(self):
        self.recusa(self.render(),'RH-01');self.assertFalse((self.caso/'caso/entregaveis/E2.md').exists())

    def test_09_relacao_ausente(self):
        self.assertEqual(self.vincular().returncode,0)
        self.baseline(['REC-000001']);self.recusa(self.render(),'BL-001')

    def test_10_nova_versao_sem_decisao(self):
        self.assertEqual(self.vincular().returncode,0)
        self.estado['etapa_atual']='P3a';self.estado['cumprimentos']['P2']={'cumprido':True};self.salvar()
        antes=(self.caso/'registro/restricoes.json').read_bytes()
        self.recusa(self.vincular(),'decisão')
        self.assertEqual((self.caso/'registro/restricoes.json').read_bytes(),antes)

    def test_11_registro_adulterado(self):
        self.assertEqual(self.vincular().returncode,0)
        p=self.caso/'registro/restricoes.json';d=json.loads(p.read_text());d['vigentes'][0]['fontes']=[];p.write_text(json.dumps(d))
        self.recusa(self.render(),'integridade')

    def test_12_fonte_apenas_copiada(self):
        p=self.caso/'contexto/fontes/F-001.yaml';sys.path.insert(0,str(RAIZ/'eiac-nucleo/scripts'));import estrutura as X;d=X.carregar_yaml((self.caso/'rascunho/F-001.yaml').read_text());d['id']='F-002'
        (p.parent/'F-002.yaml').write_text('\n'.join(k+': '+json.dumps(v) for k,v in d.items()))
        self.recusa(self.campo('restricoes.py','vincular','--restricao','RH-01','--fontes','F-002'),'curada')

    def test_20_vinculo_e_marca_local(self):
        r=self.vincular();self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(self.eventos()[-1]['evento'],'RestricaoVinculada')
        r=self.render();self.assertEqual(r.returncode,0,r.stderr)
        md=(self.caso/'caso/entregaveis/E2.md').read_text()
        reg=json.loads((self.caso/'registro/habilitacao.json').read_text())['vigente']['restricoes'][0]
        linha=next(l for l in md.splitlines() if 'Tempo sintético' in l)
        for valor in ['RH-01',reg['item'],reg['motivo']]: self.assertIn(valor,linha)
        self.assertNotIn('Ressalvas',md)
        r=self.rodar('avancar.py','--encerrar','P2','--autor','Celso do Vale');self.assertEqual(r.returncode,0,r.stderr)

    def test_21_dispensa_motivada(self):
        r=self.campo('restricoes.py','dispensar','--restricao','RH-01','--motivo','Nenhuma fonte do recorte usa esse item')
        self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(self.eventos()[-1]['evento'],'RestricaoDispensada')
        r=self.rodar('avancar.py','--encerrar','P2','--autor','Celso do Vale');self.assertEqual(r.returncode,0,r.stderr)
        r=self.render();self.assertEqual(r.returncode,0,r.stderr)
        self.assertNotIn('RH-01',(self.caso/'caso/entregaveis/E2.md').read_text())

    def test_22_nova_versao_decidida_preserva_anterior(self):
        self.assertEqual(self.vincular().returncode,0)
        antigo=json.loads((self.caso/'registro/restricoes.json').read_text())['vigentes'][0]
        self.estado['etapa_atual']='P3a';self.estado['cumprimentos']['P2']={'cumprido':True};self.salvar()
        p=self.caso/'rascunho/decisao.json';p.write_text(json.dumps(dict(restricao='RH-01',versao_anterior=1,
            decisor='Celso do Vale',motivo='Revisão do recorte',data='2026-10-03')))
        r=self.vincular('--nova-versao','rascunho/decisao.json');self.assertEqual(r.returncode,0,r.stderr)
        d=json.loads((self.caso/'registro/restricoes.json').read_text())
        self.assertEqual(d['historico'],[antigo]);self.assertEqual(d['vigentes'][0]['versao'],2)

    def test_23_sem_restricao_produto_vazio(self):
        CasoHook.setUp(self)
        from apoio.canais import definir
        definir(self.caso)
        exp=criar(self.base/'sem-restricao',self.estado['caso'],'Celso do Vale')
        r=self.campo('importar_habilitacao.py','--expediente',str(exp));self.assertEqual(r.returncode,0,r.stderr)
        self.estado.update(etapa_atual='P2',cumprimentos={'F0':{'cumprido':True},'P1':{'cumprido':True}});self.salvar()
        r=self.rodar('avancar.py','--encerrar','P2','--autor','Celso do Vale');self.assertEqual(r.returncode,0,r.stderr)

    def receber(self):
        p=self.caso/'rascunho/entrada/amostra.txt';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('Amostra sintética')
        m=p.parent/'origem.json';m.write_text(json.dumps(dict(ferramenta='drive',objeto_id='OBJ-CONTROLE',
            conteiner_id='SINTETICO-documentos-pasta_id',modificado_em='2026-10-03T10:00:00Z',coletado_em='2026-10-03T11:00:00Z')))
        r=self.campo('receber.py','--arquivo',str(p),'--manifesto',str(m));self.assertEqual(r.returncode,0,r.stderr)
        return json.loads(r.stdout)['id']

    def test_13_recebimento_sem_relacao(self):
        ident=self.receber()
        self.assertEqual(self.vincular().returncode,0)
        self.baseline([ident]);self.recusa(self.render(),'relação de fonte ausente')

    def test_14_origem_adulterada_nao_libera_produto(self):
        p=self.caso/'registro/habilitacao.json';d=json.loads(p.read_text());d['vigente']['restricoes']=[];p.write_text(json.dumps(d))
        self.recusa(self.rodar('avancar.py','--encerrar','P2','--autor','Celso do Vale'),'integridade')

    def test_24_relacao_rec_curada_e_ponto_especifico(self):
        ident=self.receber()
        self.fonte('F-002',recebimentos=[ident])
        r=self.campo('restricoes.py','vincular','--restricao','RH-01','--fontes','F-002');self.assertEqual(r.returncode,0,r.stderr)
        self.baseline([ident]);r=self.render();self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn('fonte: F-002',(self.caso/'caso/entregaveis/E2.md').read_text())
        p=self.caso/'rascunho/BL-001.yaml';p.write_text(p.read_text().replace('fontes: ["'+ident+'"]', 'fontes_por_campo: '+json.dumps({'valor_atual':[ident]})))
        r=self.campo('baseline.py','--arquivo','registro/baseline/BL-001.yaml','--ator','Celso do Vale');self.assertEqual(r.returncode,0,r.stderr)
        r=self.render();self.assertEqual(r.returncode,0,r.stderr)
        linha=next(l for l in (self.caso/'caso/entregaveis/E2.md').read_text().splitlines() if 'Tempo sintético' in l)
        self.assertEqual(linha.count('RH-01'),1)
        self.assertIn('10 minutos **[RH-01',linha)

    def test_25_percurso_restrito_emite_e2(self):
        import os
        env=dict(os.environ,EMCIA_DEMO_BASE=str(self.base/'demos'))
        r=subprocess.run(['bash',str(RAIZ/'.projectdocs/demos/preparar-caso.sh'),'restrito','P4','com-restricao'],env=env,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr)
        caso=self.base/'demos/restrito'
        for script,args in [('inegociaveis.py',['--verificar','1','--arquivo','registro/baseline/BL-001.yaml','--satisfazer','--autor','Celso do Vale']),
                            ('entregaveis.py',['--renderizar','E2','--emitir','--autor','Celso do Vale'])]:
            r=subprocess.run([sys.executable,str(RAIZ/'eiac-campo/scripts'/script),*args],cwd=caso,env=env,text=True,capture_output=True)
            self.assertEqual(r.returncode,0,r.stderr)
        texto=(caso/'caso/entregaveis/E2.md').read_text()
        self.assertIn('RH-01',next(l for l in texto.splitlines() if 'Tempo de controle' in l))
        evs=[json.loads(l) for l in (caso/'registro/eventos.jsonl').read_text().splitlines()]
        self.assertTrue(any(e['evento']=='EntregavelEmitido' and e['entregavel']=='E2' for e in evs))

if __name__=='__main__': unittest.main(verbosity=2)
