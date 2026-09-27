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

class RevisaoA15(Caso):
    def guarda(self,script,texto,extra=''):
        self.posicionar('P1'); (self.caso/'rascunho/TESTE.yaml').write_text(texto)
        cmd=f'python3 "{RAIZ / "eiac-campo/scripts" / script}" --arquivo registro/TESTE.yaml --ator "Celso do Vale" {extra}'
        return subprocess.run(['python3',str(RAIZ/'eiac-nucleo/scripts/guarda.py')],cwd=self.caso,input=json.dumps({'tool_name':'Bash','tool_input':{'command':cmd}}),text=True,capture_output=True)
    def negado(self,script,texto,extra=''):
        r=self.guarda(script,texto,extra); self.assertEqual(r.returncode,2,r.stderr); self.assertIn('proprio terminal',r.stderr); self.assertEqual(self.evento()['evento'],'TentativaNegada')
    def test_00_revisao(self): self.negado('piloto.py','estado: revisado\nrevisado_por: Celso do Vale')
    def test_01_rotina(self): self.negado('calibragem.py','responsavel: Celso do Vale\ncadencia: mensal')
    def test_02_rascunho_permitido(self): self.assertEqual(self.guarda('piloto.py','estado: rascunho').returncode,0)
    def test_03_baseline_medicao_permitida(self): self.assertEqual(self.guarda('baseline.py','apuracao: medido').returncode,0)
    def test_04_metrica_calculo_permitido(self): self.assertEqual(self.guarda('metrica.py','estado: apurada').returncode,0)
    def test_05_ciclo_sem_decisao(self): self.assertEqual(self.guarda('calibragem.py','recomendacao_agente: recalibrar','--ciclo').returncode,0)
if __name__=='__main__': unittest.main(verbosity=2)
