import json, pathlib, shutil, subprocess, tempfile, unittest
RAIZ = pathlib.Path(__file__).resolve().parents[1]
class Caso(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.caso=pathlib.Path(self.tmp.name)
        shutil.copytree(RAIZ/'eiac-campo/template-caso/registro', self.caso/'registro')
        (self.caso/'rascunho').mkdir()
        self.posicionar('P1')
        from apoio.canais import definir
        definir(self.caso)
    def posicionar(self, etapa):
        p=self.caso/'registro/estado.json'; st=json.loads(p.read_text())
        st.update(responsavel='Celso do Vale', nivel='N2', etapa_atual=etapa, cumprimentos={})
        pb=json.loads((self.caso/'registro/playbook.json').read_text())
        for e in pb['etapas']:
            if e['id']==etapa:
                st['cumprimentos'][etapa]={'sessao':{'autor':'Celso do Vale','participantes':'Marina Prado'}}
                st.update(camada_atual=e['camada']['N2'],modalidade_atual=e['modalidade']); break
            st['cumprimentos'][e['id']]={'cumprido':True}
        p.write_text(json.dumps(st))
    def avancar(self,*args):
        return subprocess.run(['python3',str(RAIZ/'eiac-nucleo/scripts/avancar.py'),*args,'--autor','Celso do Vale'],cwd=self.caso,text=True,capture_output=True)
    def evento(self):
        return json.loads((self.caso/'registro/eventos.jsonl').read_text().splitlines()[-1])

PRODUTOS={
'P3a':('registro/baseline/BL-001.yaml',{'id':'BL-001','indicador':'tempo','valor_atual':'10','data':'2026-09-27'}),
'P6':('registro/operacional/OP-001.yaml',{'estado':'validado'}),
'P7':('registro/governanca/autonomia/AUT-001.yaml',{'estado':'decidido'}),
'P8':('registro/piloto/CT-001.yaml',{'estado':'revisado'}),
'P9':('registro/metricas/MET-001.yaml',{'tipo':'resultado','estado':'apurada'}),
'P10':('registro/calibragem/CAL-001.yaml',{'responsavel':'Marina Prado','cadencia':'mensal'})}
class ProdutosA14(Caso):
    def produto(self,et):
        if et=='P5':
            r=self.avancar('--registrar-campo',et,'--campo','classificacao_tecnologica','--valor','agente'); self.assertEqual(r.returncode,0,r.stderr)
        else:
            rel,dados=PRODUTOS[et]; p=self.caso/rel; p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text('\n'.join(k+': '+json.dumps(v) for k,v in dados.items()))
    def recusa_produto(self,et):
        antes=(self.caso/'registro/estado.json').read_bytes(); r=self.avancar('--encerrar',et)
        self.assertEqual(r.returncode,1,r.stdout+r.stderr); self.assertIn('produto',r.stderr); self.assertIn(et,r.stderr)
        self.assertEqual(antes,(self.caso/'registro/estado.json').read_bytes()); self.assertEqual(self.evento()['evento'],'TentativaNegada')
    def test_00_sem_P3a(self):
        self.posicionar('P3a'); self.recusa_produto('P3a')
    def test_01_sem_P5(self):
        self.posicionar('P5'); self.recusa_produto('P5')
    def test_02_sem_P6(self):
        self.posicionar('P6'); self.recusa_produto('P6')
    def test_03_sem_P7(self):
        self.posicionar('P7'); self.recusa_produto('P7')
    def test_04_sem_P8(self):
        self.posicionar('P8'); self.recusa_produto('P8')
    def test_05_sem_P9(self):
        self.posicionar('P9'); self.recusa_produto('P9')
    def test_06_sem_P10(self):
        self.posicionar('P10'); self.recusa_produto('P10')
    def test_10_com_P3a(self):
        self.posicionar('P3a'); self.produto('P3a'); r=self.avancar('--encerrar','P3a'); self.assertEqual(r.returncode,0,r.stderr)
    def test_11_com_P5(self):
        self.posicionar('P5'); self.produto('P5'); r=self.avancar('--encerrar','P5'); self.assertEqual(r.returncode,0,r.stderr)
    def test_12_com_P6(self):
        self.posicionar('P6'); self.produto('P6'); r=self.avancar('--encerrar','P6'); self.assertEqual(r.returncode,0,r.stderr)
    def test_13_com_P7(self):
        self.posicionar('P7'); self.produto('P7'); r=self.avancar('--encerrar','P7'); self.assertEqual(r.returncode,0,r.stderr)
    def test_14_com_P8(self):
        self.posicionar('P8'); self.produto('P8'); r=self.avancar('--encerrar','P8'); self.assertEqual(r.returncode,0,r.stderr)
    def test_15_com_P9(self):
        self.posicionar('P9'); self.produto('P9'); r=self.avancar('--encerrar','P9'); self.assertEqual(r.returncode,0,r.stderr)
    def test_16_com_P10(self):
        self.posicionar('P10'); self.produto('P10'); r=self.avancar('--encerrar','P10'); self.assertEqual(r.returncode,0,r.stderr)
    def test_20_estado_errado(self):
        self.posicionar('P7'); self.produto('P7'); (self.caso/PRODUTOS['P7'][0]).write_text('estado: proposto'); self.recusa_produto('P7')
    def test_21_campos_em_arquivos_diferentes(self):
        self.posicionar('P10'); self.produto('P10')
        (self.caso/PRODUTOS['P10'][0]).write_text('responsavel: Marina Prado')
        (self.caso/'registro/calibragem/CAL-002.yaml').write_text('cadencia: mensal'); self.recusa_produto('P10')
    def test_22_symlink_externo(self):
        self.posicionar('P7'); externo=self.caso.parent/(self.caso.name+'-externo.yaml'); externo.write_text('estado: decidido')
        self.addCleanup(externo.unlink); p=self.caso/PRODUTOS['P7'][0]; p.parent.mkdir(parents=True,exist_ok=True); p.symlink_to(externo); self.recusa_produto('P7')
    def test_23_regra_alternativa(self):
        self.posicionar('P1')
        from apoio.canais import definir
        definir(self.caso); p=self.caso/'registro/playbook.json'; pb=json.loads(p.read_text())
        next(e for e in pb['etapas'] if e['id']=='P1')['produtos_encerramento']=[{'tipo':'arquivo','padrao':'registro/outro/*.yaml','iguais':{'status':'feito'},'preenchidos':[],'descricao':'produto alternativo'}]
        p.write_text(json.dumps(pb)); self.recusa_produto('P1')
        alvo=self.caso/'registro/outro/a.yaml'; alvo.parent.mkdir(); alvo.write_text('status: feito')
        self.assertEqual(self.avancar('--encerrar','P1').returncode,0)
    def test_24_yaml_ilegivel(self):
        self.posicionar('P7'); self.produto('P7'); (self.caso/PRODUTOS['P7'][0]).write_text('estado: ['); self.recusa_produto('P7')
    def test_25_metrica_uso(self):
        self.posicionar('P9'); self.produto('P9'); (self.caso/PRODUTOS['P9'][0]).write_text('estado: apurada\ntipo: uso'); self.recusa_produto('P9')
    def test_26_regra_invalida(self):
        self.posicionar('P1')
        from apoio.canais import definir
        definir(self.caso); p=self.caso/'registro/playbook.json'; pb=json.loads(p.read_text())
        next(e for e in pb['etapas'] if e['id']=='P1')['produtos_encerramento']=[{'tipo':'desconhecido','descricao':'produto'}]; p.write_text(json.dumps(pb))
        r=self.avancar('--encerrar','P1'); self.assertEqual(r.returncode,1); self.assertIn('tipo de produto desconhecido',r.stderr); self.assertEqual(self.evento()['evento'],'TentativaNegada')
if __name__=='__main__': unittest.main(verbosity=2)
