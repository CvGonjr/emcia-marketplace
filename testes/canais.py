"""Canais: negativas com evento antes dos controles positivos."""
import copy
import json
import subprocess
import sys
import unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.canais import dados, definir

SCRIPT = RAIZ/'eiac-campo/scripts/canais.py'


class Canais(CasoHook):
    def setUp(self):
        super().setUp()
        self.entrada = self.caso/'rascunho/canais.json'
        self.dados = dados(self.caso)

    def executar(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.caso,
                              text=True, capture_output=True)

    def gravar(self):
        self.entrada.write_text(json.dumps(self.dados))
        return self.executar('definir', '--entrada', str(self.entrada))

    def recusa(self):
        antes = len(self.eventos())
        r = self.gravar()
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertEqual(len(self.eventos()), antes+1)
        self.assertEqual(self.eventos()[-1]['evento'], 'TentativaNegada')
        self.assertEqual(self.eventos()[-1]['autor'], 'Celso do Vale')

    def test_01_id_vazio(self):
        self.dados['canais'][0]['ids']['workspace_id'] = ''; self.recusa()

    def test_02_finalidade_desconhecida(self):
        self.dados['canais'][0]['finalidade'] = 'inventada'; self.recusa()

    def test_03_ferramenta_desconhecida(self):
        self.dados['canais'][0]['ferramenta'] = 'inventada'; self.recusa()

    def test_04_autor_agente(self):
        self.dados['decidido_por'] = 'AG-01'; self.recusa()

    def test_05_sessao_agente(self):
        self.entrada.write_text(json.dumps(self.dados))
        self.negado('Bash', {'command': f'python3 {SCRIPT} definir --entrada {self.entrada}'})

    def test_06_resolver_ausente(self):
        antes = len(self.eventos()); r = self.executar('resolver', 'F0', 'entrada')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('definir', r.stderr)
        self.assertEqual(self.eventos()[antes]['evento'], 'TentativaNegada')

    def test_07_caso_alheio(self):
        self.dados['caso'] = 'outro'; self.recusa()

    def test_08_etapa_fora_contrato(self):
        self.dados['canais'][0]['etapas'] = ['P9']; self.recusa()

    def test_09_filtro_alheio(self):
        self.dados['canais'][0]['filtro']['valor'] = 'outro'; self.recusa()

    def test_10_ids_com_caminho(self):
        self.dados['canais'][0]['ids']['workspace_id'] = '/espaco/nome'; self.recusa()

    def test_11_versao_repetida(self):
        self.assertEqual(self.gravar().returncode, 0); self.recusa()

    def test_12_entrada_malformada(self):
        self.dados['canais'] = None; self.recusa()

    def test_13_adulteracao(self):
        self.assertEqual(self.gravar().returncode, 0)
        p = self.caso/'registro/canais.json'; d = json.loads(p.read_text())
        d['canais'][1]['ids']['formulario_id'] = 'ALHEIO'; p.write_text(json.dumps(d))
        r = self.executar('resolver', 'F0', 'entrada')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.eventos()[-1]['evento'], 'TentativaNegada')

    def test_14_etapa_sem_canal_recusa_com_evento(self):
        self.estado['etapa_atual'] = 'P2'; self.salvar()
        self.negado('Skill', {'skill': 'eiac-campo:hb-extrair-regras'})
        antes = len(self.eventos())
        r = self.rodar('avancar.py', '--encerrar', 'P2', '--autor', 'Celso do Vale')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('definir', r.stderr)
        self.assertEqual(self.eventos()[antes]['evento'], 'TentativaNegada')

    def test_15_finalidade_exigida_ausente(self):
        self.dados['canais'] = [c for c in self.dados['canais'] if c['finalidade'] != 'documentos']
        self.assertEqual(self.gravar().returncode, 0)
        self.estado['etapa_atual'] = 'P2'; self.salvar()
        self.negado('Skill', {'skill': 'eiac-campo:hb-extrair-regras'})

    def test_20_planejar_somente_leitura(self):
        antes = list(self.eventos()); r = self.executar('planejar')
        self.assertEqual(r.returncode, 0, r.stderr)
        plano = json.loads(r.stdout)
        self.assertEqual(len(plano['arvore_proposta']['filhos']), 5)
        self.assertEqual(self.eventos(), antes)
        self.assertFalse((self.caso/'registro/canais.json').exists())

    def test_21_definir_resolver_historico(self):
        self.assertEqual(self.gravar().returncode, 0)
        antigo = (self.caso/'registro/canais.json').read_bytes()
        self.dados['versao'] = 2
        self.assertEqual(self.gravar().returncode, 0)
        self.assertEqual((self.caso/'registro/canais/versao-0001.json').read_bytes(), antigo)
        r = self.executar('resolver', 'E1', 'saida')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)['finalidade'], 'entregas')
        self.assertEqual([e['evento'] for e in self.eventos()], ['CanaisDefinidos']*2)

    def test_22_decisor_distinto_autoria_fixa(self):
        self.dados['decidido_por'] = 'Pessoa Engenheira'
        self.assertEqual(self.gravar().returncode, 0)
        evento = self.eventos()[-1]
        self.assertEqual(evento['autor'], 'Celso do Vale')
        self.assertEqual(evento['decidido_por'], 'Pessoa Engenheira')



if __name__ == '__main__': unittest.main(verbosity=2)
