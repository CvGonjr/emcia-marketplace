"""Negativas do ato humano de F0, integridade e bloqueio após encerramento."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
CAMPO = RAIZ / 'eiac-campo/scripts'
NUCLEO = RAIZ / 'eiac-nucleo/scripts'


class Prosseguimento(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.caso = pathlib.Path(self.tmp.name)
        shutil.copytree(RAIZ / 'eiac-campo/template-caso', self.caso, dirs_exist_ok=True)
        p = self.caso / 'registro/estado.json'; st = json.loads(p.read_text())
        st.update(caso='CONTROLE-SINTETICO', responsavel='Celso do Vale')
        p.write_text(json.dumps(st))
        from apoio.habilitacao_0d import preparar
        preparar(self.caso)
        self.rodar(NUCLEO / 'avancar.py', '--apurar-nivel', 'N1', '--eixos', 'DAD 3, GOV 3, CRI 3', '--autor', 'Celso do Vale', ok=True)
        (self.caso / 'caso/E1-ficha.md').write_text('- [D · Celso do Vale] Ficha de enquadramento exclusivamente sintética.\n')
        self.dados = dict(versao=1, decisor='Celso do Vale', data='2026-10-03',
                          desfecho='prosseguir', motivo='Controle sintético aprovado', ficha='caso/E1-ficha.md')

    def rodar(self, script, *args, ok=False):
        r = subprocess.run([sys.executable, str(script), *args], cwd=self.caso, text=True, capture_output=True)
        if ok: self.assertEqual(r.returncode, 0, r.stdout+r.stderr)
        return r

    def decidir(self, ok=False):
        (self.caso / 'rascunho/prosseguimento.json').write_text(json.dumps(self.dados, ensure_ascii=False))
        return self.rodar(CAMPO / 'prosseguimento.py', '--entrada', 'rascunho/prosseguimento.json', ok=ok)

    def encerrar(self, etapa='F0', ok=False):
        return self.rodar(NUCLEO / 'avancar.py', '--encerrar', etapa, '--autor', 'Celso do Vale', ok=ok)

    def evento(self):
        return json.loads((self.caso / 'registro/eventos.jsonl').read_text().splitlines()[-1])

    def recusa(self, funcao):
        antes = (self.caso / 'registro/estado.json').read_bytes()
        r = funcao()
        self.assertNotEqual(r.returncode, 0, r.stdout+r.stderr)
        self.assertEqual(self.evento()['evento'], 'TentativaNegada')
        self.assertEqual((self.caso / 'registro/estado.json').read_bytes(), antes)
        return r

    def test_00_f0_sem_decisao_recusa(self):
        self.assertIn('produto', self.recusa(self.encerrar).stderr)

    def test_01_sessao_recusa_e_devolve_comando_exato(self):
        cmd = f'python3 {CAMPO}/prosseguimento.py --entrada rascunho/prosseguimento.json'
        antes = (self.caso / 'registro/estado.json').read_bytes()
        r = subprocess.run([sys.executable, str(NUCLEO/'guarda.py')], cwd=self.caso,
                           input=json.dumps(dict(tool_name='Bash', tool_input=dict(command=cmd))), text=True, capture_output=True)
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn(cmd, r.stderr)
        self.assertEqual(self.evento()['operacao'], 'decidir-prosseguimento')
        self.assertEqual(self.evento()['comando'], cmd)
        self.assertEqual((self.caso / 'registro/estado.json').read_bytes(), antes)

    def test_02_cada_campo_obrigatorio_recusa(self):
        original = self.dados.copy()
        for campo in original:
            with self.subTest(campo=campo):
                self.dados = {k:v for k,v in original.items() if k != campo}
                self.recusa(self.decidir)

    def test_03_nome_de_agente_recusa(self):
        self.dados['decisor'] = 'AG-01'; self.recusa(self.decidir)

    def test_04_nome_coletivo_recusa(self):
        self.dados['decisor'] = 'Equipe Técnica'; self.recusa(self.decidir)

    def test_05_desfecho_inexistente_recusa(self):
        self.dados['desfecho'] = 'talvez'; self.recusa(self.decidir)

    def test_06_data_impossivel_recusa(self):
        self.dados['data'] = '2026-02-30'; self.recusa(self.decidir)

    def test_07_ficha_ausente_recusa(self):
        (self.caso / self.dados['ficha']).unlink(); self.recusa(self.decidir)

    def test_08_ficha_fora_do_caso_recusa(self):
        self.dados['ficha'] = '../fora.md'; self.recusa(self.decidir)

    def test_09_sobrescrita_recusa(self):
        self.decidir(ok=True)
        anterior = (self.caso/'registro/prosseguimento/decisao-0001.yaml').read_bytes()
        self.dados['motivo'] = 'Sobrescrita'; self.recusa(self.decidir)
        self.assertEqual((self.caso/'registro/prosseguimento/decisao-0001.yaml').read_bytes(), anterior)

    def test_10_adulteracao_do_vigente_recusa(self):
        self.decidir(ok=True)
        p = self.caso/'registro/prosseguimento/vigente.yaml'
        p.write_text(p.read_text().replace('Controle sintético aprovado', 'Outro motivo'))
        self.recusa(self.encerrar)

    def test_11_vigente_negativo_nao_usa_positivo_anterior(self):
        self.decidir(ok=True); self.dados.update(versao=2,desfecho='não prosseguir')
        self.decidir(ok=True); self.encerrar(ok=True)
        self.assertIn('continuidade', self.recusa(lambda: self.encerrar('P1')).stderr)

    def test_12_nao_prosseguir_encerra_f0_e_bloqueia_p1(self):
        self.dados['desfecho'] = 'não prosseguir'; self.decidir(ok=True); self.encerrar(ok=True)
        st = json.loads((self.caso/'registro/estado.json').read_text())
        self.assertTrue(st['cumprimentos']['F0']['cumprido'])
        self.recusa(lambda: self.encerrar('P1'))
        r = subprocess.run([sys.executable,str(NUCLEO/'guarda.py')],cwd=self.caso,
                           input=json.dumps(dict(tool_name='Skill',tool_input=dict(skill='eiac-campo:hb-mapear-contexto'))),text=True,capture_output=True)
        self.assertEqual(r.returncode,2,r.stderr); self.assertEqual(self.evento()['evento'],'TentativaNegada')

    def test_13_nova_decisao_libera_e_preserva_anterior(self):
        self.dados['desfecho']='não prosseguir'; self.decidir(ok=True); self.encerrar(ok=True)
        p=self.caso/'registro/prosseguimento/decisao-0001.yaml'; anterior=p.read_bytes()
        self.dados.update(versao=2,desfecho='prosseguir',motivo='Retomada sintética decidida')
        self.decidir(ok=True); self.encerrar('P1',ok=True)
        self.assertEqual(p.read_bytes(),anterior)

    def test_14_e1_materializa_os_dois_desfechos(self):
        for desfecho in ('prosseguir','não prosseguir'):
            with self.subTest(desfecho=desfecho):
                self.dados.update(versao=1 if desfecho=='prosseguir' else 2,desfecho=desfecho)
                self.decidir(ok=True)
                if desfecho=='prosseguir': self.encerrar(ok=True)
                self.rodar(CAMPO/'entregaveis.py','--renderizar','E1','--autor','Celso do Vale',ok=True)
                md=(self.caso/'caso/entregaveis/E1.md').read_text()
                self.assertIn(desfecho,md); self.assertIn(self.dados['motivo'],md)
                self.assertIn(hashlib.sha256((self.caso/self.dados['ficha']).read_bytes()).hexdigest(),md)

    def test_15_caso_anterior_conserva_contrato(self):
        p=self.caso/'registro/playbook.json'
        p.write_bytes(subprocess.check_output(['git','show','ebb6bbd:eiac-campo/template-caso/registro/playbook.json'],cwd=RAIZ))
        self.encerrar(ok=True)

    def test_16_decisao_negativa_bloqueia_registro_de_sessao_seguinte(self):
        self.dados['desfecho']='não prosseguir'; self.decidir(ok=True); self.encerrar(ok=True)
        self.recusa(lambda: self.rodar(NUCLEO/'avancar.py','--registrar-sessao','P1',
                                     '--autor','Celso do Vale','--participantes','Marina Prado'))

    def test_17_produto_sintetico_sem_evento_nao_libera(self):
        self.decidir(ok=True)
        log=self.caso/'registro/eventos.jsonl'
        log.write_text(''.join(json.dumps(e)+'\n' for e in map(json.loads,log.read_text().splitlines())
                               if e['evento']!='ProsseguimentoDecidido'))
        self.recusa(self.encerrar)

    def test_18_motivo_vazio_recusa(self):
        self.dados['motivo']='   '; self.recusa(self.decidir)

    def test_19_e1_sem_decisao_recusa_com_evento(self):
        p=self.caso/'registro/estado.json'; st=json.loads(p.read_text())
        st['cumprimentos']['F0']['cumprido']=True
        p.write_text(json.dumps(st))  # Fixture isolada de materialização.
        self.recusa(lambda: self.rodar(CAMPO/'entregaveis.py','--renderizar','E1','--autor','Celso do Vale'))


if __name__ == '__main__': unittest.main(verbosity=2)
