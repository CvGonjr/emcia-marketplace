import json, pathlib, shutil, subprocess, tempfile, unittest
RAIZ = pathlib.Path(__file__).resolve().parents[1]
class Caso(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.caso=pathlib.Path(self.tmp.name)
        shutil.copytree(RAIZ/'eiac-campo/template-caso/registro', self.caso/'registro')
        (self.caso/'rascunho').mkdir()
        self.posicionar('P1')
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

class PessoaA16(Caso):
    def conferir(self,nome,permitido):
        r=subprocess.run(['python3',str(RAIZ/'eiac-nucleo/scripts/avancar.py'),'--apurar-nivel','N2','--eixos','DAD 5, GOV 3, CRI 6','--autor',nome],cwd=self.caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0 if permitido else 1,r.stdout+r.stderr)
        if not permitido: self.assertEqual(self.evento()['evento'],'TentativaNegada')
    def test_00_equipe(self): self.conferir('equipe de TI',False)
    def test_01_time(self): self.conferir('Time Comercial',False)
    def test_02_area(self): self.conferir('Área de Vendas',False)
    def test_03_nome_unico(self): self.conferir('Marina',False)
    def test_04_comite(self): self.conferir('Comitê Executivo',False)
    def test_05_pessoa(self): self.conferir('Marina Prado',True)
    def test_06_regra_do_caso(self):
        p=self.caso/'registro/playbook.json'; pb=json.loads(p.read_text()); pb['pessoa_nomeada']={'minimo_partes':2,'termos_coletivos':['Prado']}; p.write_text(json.dumps(pb)); self.conferir('Marina Prado',False)
    def campo_pessoa(self,etapa,script,rel,campo):
        from apoio.preparar import produto
        for et in ['P3a','P6','P7','P8','P9','P10']: produto(self.caso,et)
        import sys
        sys.path.insert(0,str(RAIZ/'eiac-nucleo/scripts'))
        import estrutura as X
        destino=self.caso/rel; original=destino.read_bytes(); d=X.carregar_yaml(destino.read_text())
        def gravar():
            (self.caso/'rascunho'/destino.name).write_text('\n'.join(k+': '+json.dumps(v) for k,v in d.items())+'\n')
            return subprocess.run(['python3',str(RAIZ/'eiac-campo/scripts'/script),'--arquivo',rel,'--ator','Marina Prado'],cwd=self.caso,text=True,capture_output=True)
        if campo=='revisor': d['casos'][0][campo]='equipe de TI'
        else: d[campo]='equipe de TI'
        r=gravar(); self.assertEqual(r.returncode,1,r.stderr); self.assertEqual(destino.read_bytes(),original)
        self.assertIn('pessoa',r.stderr+' '+self.evento().get('evento',''))
        if campo=='revisor': d['casos'][0][campo]='Marina Prado'
        else: d[campo]='Marina Prado'
        r=gravar(); self.assertEqual(r.returncode,0,r.stderr)
    def test_10_baseline(self): self.campo_pessoa('P3a','baseline.py','registro/baseline/BL-999.yaml','declarado_por')
    def test_11_operacional(self): self.campo_pessoa('P6','operacional.py','registro/operacional/OP-999.yaml','responsavel_operacional')
    def test_12_governanca(self): self.campo_pessoa('P7','governanca.py','registro/governanca/autonomia/AUT-999.yaml','decisor')
    def test_13_revisor(self): self.campo_pessoa('P8','piloto.py','registro/piloto/CT-999.yaml','revisor')
    def test_14_metrica(self): self.campo_pessoa('P9','metrica.py','registro/metricas/MET-999.yaml','responsavel_apuracao')
    def test_15_calibragem(self): self.campo_pessoa('P10','calibragem.py','registro/calibragem/CAL-999.yaml','responsavel')
    def test_16_novo_caso_coletivo(self):
        r=subprocess.run(['bash',str(RAIZ/'novo-caso.sh'),'coletivo','--responsavel','Time Comercial',str(self.caso/'casos')],text=True,capture_output=True)
        self.assertEqual(r.returncode,1,r.stderr); self.assertFalse((self.caso/'casos/coletivo').exists())
    def test_17_validador_autoria(self):
        (self.caso/'rascunho/a.md').write_text('- [D · Área de Vendas · 2026-09-27] fato\n')
        r=subprocess.run(['python3',str(RAIZ/'eiac-nucleo/scripts/validar.py'),'--arquivo','caso/a.md'],cwd=self.caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,1); self.assertFalse((self.caso/'caso/a.md').exists()); self.assertEqual(self.evento()['evento'],'AssercaoRecusada')
    def test_18_nome_sobrenome_sem_acentos(self): self.conferir('Marina Núcleo',False)
    def test_19_produto_responsavel_coletivo(self):
        self.posicionar('P10'); p=self.caso/'registro/calibragem/CAL-001.yaml'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('responsavel: equipe de TI\ncadencia: mensal')
        r=self.avancar('--encerrar','P10'); self.assertEqual(r.returncode,1,r.stderr); self.assertIn('produto',r.stderr); self.assertEqual(self.evento()['evento'],'TentativaNegada')
if __name__=='__main__': unittest.main(verbosity=2)
