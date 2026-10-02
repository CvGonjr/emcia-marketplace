"""A23: responsável da recorrência conferido contra a fonte vigente do caso."""
import json, pathlib, subprocess, sys, unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.preparar import produto

REGRA = dict(padrao='registro/calibragem/CAL-*.yaml',
             excluir_padrao='registro/calibragem/*-C*.yaml', campo='responsavel',
             campo_versao='versao', selecao='maior_versao',
             orientacao_troca='Para trocar o responsavel, grave uma nova versao da rotina pelo engenheiro no proprio terminal, antes da recorrencia.')

class RecorrenciaA23(CasoHook):
    def setUp(self):
        super().setUp()
        self.estado.update(etapa_atual='P10', cumprimentos={'P10': {'cumprido': True}})
        self.salvar()
        self.pb = json.loads((self.caso/'registro/playbook.json').read_text())
        self.et = next(e for e in self.pb['etapas'] if e['id']=='P10')
        self.et['coerencia_responsavel_recorrencia'] = dict(REGRA)
        self.salvar_pb()

    def salvar_pb(self):
        (self.caso/'registro/playbook.json').write_text(json.dumps(self.pb))

    def fonte(self, nome='CAL-001.yaml', pessoa='Celso do Vale', versao=1, **extras):
        p = self.caso/'registro/calibragem'/nome
        p.parent.mkdir(parents=True, exist_ok=True)
        d = dict(responsavel=pessoa, versao=versao, **extras)
        p.write_text('\n'.join(k+': '+json.dumps(v, ensure_ascii=False) for k,v in d.items())+'\n')
        return p

    def recorrencia(self, pessoa='Celso do Vale', etapa='P10'):
        return self.rodar('avancar.py', '--registrar-recorrencia', etapa,
                          '--autor', 'Celso do Vale', '--cadencia', 'mensal', '--responsavel', pessoa)

    def recusa(self, pessoa='Marina Prado', trecho=None):
        antes = (self.caso/'registro/estado.json').read_bytes()
        n = len(self.eventos())
        r = self.recorrencia(pessoa)
        self.assertEqual(r.returncode, 1, r.stdout+r.stderr)
        self.assertEqual((self.caso/'registro/estado.json').read_bytes(), antes)
        evs = self.eventos()
        self.assertEqual(len(evs), n+1)
        self.assertIn(evs[-1]['evento'], ['TentativaNegada','RecusaMaquina'])
        self.assertEqual(evs[-1]['acao_tentada'], 'registrar_recorrencia')
        if trecho: self.assertIn(trecho, r.stderr)
        return r

    def test_01_responsavel_divergente_recusado_com_orientacao(self):
        self.fonte()
        r = self.recusa(trecho='Marina Prado')
        self.assertIn('Celso do Vale', r.stderr)
        self.assertIn(REGRA['orientacao_troca'], r.stderr)

    def test_02_sem_rotina_recusado(self):
        self.recusa(trecho=REGRA['padrao'])

    def test_03_versao_mais_alta_nao_e_nome_lexicografico(self):
        self.fonte('CAL-999.yaml', 'Celso do Vale', 2)
        self.fonte('CAL-001.yaml', 'Marina Prado', 10)
        self.recusa('Celso do Vale', 'Marina Prado')
        self.assertEqual(self.recorrencia('Marina Prado').returncode, 0)

    def test_04_ciclo_nao_substitui_rotina(self):
        self.fonte()
        self.fonte('CAL-001-C01.yaml', 'Marina Prado', 100)
        self.recusa('Marina Prado', 'Celso do Vale')
        self.assertEqual(self.recorrencia().returncode, 0)

    def test_05_versao_invalida_nao_libera_por_rotina_antiga(self):
        self.fonte('CAL-001.yaml', 'Marina Prado', 1)
        self.fonte('CAL-002.yaml', 'Marina Prado', 'invalida')
        self.recusa(trecho='versao')

    def test_06_empate_com_responsaveis_distintos_recusado(self):
        self.fonte('CAL-001.yaml', 'Celso do Vale', 3)
        self.fonte('CAL-002.yaml', 'Marina Prado', 3)
        self.recusa(trecho='ambigu')

    def test_07_link_para_fora_do_caso_recusado(self):
        alvo = self.base/'externo.yaml'
        alvo.write_text('responsavel: Marina Prado\nversao: 1\n')
        (self.caso/'registro/calibragem').mkdir(parents=True, exist_ok=True)
        (self.caso/'registro/calibragem/CAL-001.yaml').symlink_to(alvo)
        self.recusa(trecho='fora do caso')

    def test_08_contrato_invalido_recusado_com_evento(self):
        self.et['coerencia_responsavel_recorrencia']['selecao'] = 'primeiro'
        self.salvar_pb()
        self.recusa(trecho='selecao')

    def test_09_mesmo_responsavel_aceito_com_fonte_rastreavel(self):
        self.fonte()
        r = self.recorrencia()
        self.assertEqual(r.returncode, 0, r.stderr)
        st = json.loads((self.caso/'registro/estado.json').read_text())
        registro = st['cumprimentos']['P10']['estado_recorrente']
        self.assertEqual(registro['responsavel'], 'Celso do Vale')
        self.assertEqual(registro['fonte_responsavel']['arquivo'], 'registro/calibragem/CAL-001.yaml')
        self.assertEqual(registro['fonte_responsavel']['versao'], 1)
        self.assertEqual(self.eventos()[-1]['evento'], 'RecorrenciaRegistrada')
        self.assertEqual(self.eventos()[-1]['fonte_responsavel'], registro['fonte_responsavel'])

    def test_10_troca_por_nova_versao_gravada_pelo_script(self):
        produto(self.caso, 'P9')
        produto(self.caso, 'P10')
        self.assertEqual(self.recorrencia().returncode, 0)
        fonte = self.caso/'registro/calibragem/CAL-999.yaml'
        texto = fonte.read_text().replace('responsavel: "Celso do Vale"', 'responsavel: "Marina Prado"').replace('versao: 1', 'versao: 2')
        (self.caso/'rascunho/CAL-999.yaml').write_text(texto)
        r = subprocess.run([sys.executable, str(RAIZ/'eiac-campo/scripts/calibragem.py'),
                            '--arquivo', 'registro/calibragem/CAL-999.yaml', '--ator', 'Celso do Vale'],
                           cwd=self.caso, text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.recusa('Celso do Vale', 'Marina Prado')
        r = self.recorrencia('Marina Prado')
        self.assertEqual(r.returncode, 0, r.stderr)
        st = json.loads((self.caso/'registro/estado.json').read_text())
        ciclo = st['cumprimentos']['P10']['estado_recorrente']
        self.assertEqual(ciclo['fonte_responsavel']['versao'], 2)
        self.assertEqual(ciclo['ciclo'], 2)
        self.assertEqual(ciclo['historico'][0]['responsavel'], 'Celso do Vale')

    def test_11_regra_generica_outro_caminho_campo_etapa(self):
        self.et['id'] = 'Z99'
        self.pb['canais_por_etapa']['Z99'] = self.pb['canais_por_etapa'].pop('P10')
        for canal in self.pb['canais_previstos']:
            canal['etapas'] = ['Z99' if x == 'P10' else x for x in canal['etapas']]
        for ent in self.pb['entregaveis']:
            ent['portao'] = ['Z99' if x=='P10' else x for x in ent['portao']]
        for item in self.pb['inegociaveis']:
            if item.get('passo')=='P10': item['passo']='Z99'
        self.et['coerencia_responsavel_recorrencia'].update(padrao='registro/agenda/*.yaml', excluir_padrao='registro/agenda/*-ciclo.yaml', campo='titular', campo_versao='revisao')
        self.salvar_pb()
        self.estado.update(etapa_atual='Z99', cumprimentos={'Z99': {'cumprido': True}})
        self.salvar()
        p = self.caso/'registro/agenda/rotina.yaml'
        p.parent.mkdir()
        p.write_text('titular: Marina Prado\nrevisao: 4\n')
        r = self.recorrencia('Celso do Vale', 'Z99')
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn('Marina Prado', r.stderr)
        self.assertEqual(self.recorrencia('Marina Prado', 'Z99').returncode, 0)

    def test_12_fonte_ilegivel_nao_e_ignorada(self):
        self.fonte('CAL-001.yaml', 'Marina Prado')
        (self.caso/'registro/calibragem/CAL-002.yaml').write_bytes(b'\xff')
        self.recusa(trecho='ilegivel')

if __name__ == '__main__': unittest.main(verbosity=2)
