"""A10: campos declarados, autoria nominal e E3 por comandos reais."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / 'eiac-nucleo/scripts/avancar.py'
VALORES = ['agente', 'caso isolado', 'habilitador acoplado']


class CamposA10(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.caso = pathlib.Path(self.tmp.name) / 'caso'
        shutil.copytree(RAIZ / 'eiac-campo/template-caso/registro', self.caso / 'registro')
        self.estado = self.caso / 'registro/estado.json'
        self.pbpath = self.caso / 'registro/playbook.json'
        self.configurar(lambda pb: next(e for e in pb['etapas'] if e['id'] == 'P5').update(
            campos_registraveis={'classificacao_tecnologica': {'valores': VALORES}}))
        st = json.loads(self.estado.read_text())
        st.update(responsavel='Celso do Vale', etapa_atual='P5', nivel='N2')
        st['cumprimentos'] = {}
        self.estado.write_text(json.dumps(st))

    def configurar(self, fn):
        pb = json.loads(self.pbpath.read_text())
        fn(pb)
        self.pbpath.write_text(json.dumps(pb))

    def executar(self, *args, autor='Celso do Vale'):
        return subprocess.run(['python3', str(SCRIPT), *args, '--autor', autor],
                              cwd=self.caso, text=True, capture_output=True)

    def eventos(self):
        return [json.loads(l) for l in (self.caso / 'registro/eventos.jsonl').read_text().splitlines()]

    def registrar(self, etapa='P5', campo='classificacao_tecnologica', valor='agente', **kwargs):
        return self.executar('--registrar-campo', etapa, '--campo', campo, '--valor', valor, **kwargs)

    def recusa(self, partes, **kwargs):
        antes = self.estado.read_bytes()
        r = self.registrar(**kwargs)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        for parte in partes:
            self.assertIn(parte, r.stderr)
        self.assertEqual(self.estado.read_bytes(), antes)
        ev = self.eventos()[-1]
        self.assertEqual(ev['evento'], 'TentativaNegada')
        self.assertEqual(ev['autor'], 'Celso do Vale')
        self.assertEqual(ev['acao_tentada'], 'registrar_campo')
        self.assertIn(r.stderr.strip(), ev['motivo'])

    def test_00_campo_nao_declarado(self):
        self.recusa(['nao declarado'], campo='inventado')

    def test_01_valor_fora_da_taxonomia(self):
        self.recusa(['valores aceitos', *VALORES], valor='automacao')

    def test_02_autor_agente(self):
        self.recusa(['pessoa nomeada'], autor='AG-01')

    def test_03_etapa_futura(self):
        self.recusa(['etapa corrente'], etapa='P6')

    def test_04_etapa_passada(self):
        self.recusa(['etapa corrente'], etapa='P4')

    def test_05_etapa_desconhecida(self):
        self.recusa(['nao existe'], etapa='P99')

    def test_06_etapa_corrente_encerrada(self):
        st = json.loads(self.estado.read_text())
        st['cumprimentos']['P5'] = {'cumprido': True}
        self.estado.write_text(json.dumps(st))
        self.recusa(['encerrada'])

    def test_07_valor_vazio(self):
        self.recusa(['valor'], valor='  ')

    def test_08_autor_generico(self):
        self.recusa(['pessoa nomeada'], autor='equipe')

    def test_09_sem_campo(self):
        antes = self.estado.read_bytes()
        r = self.executar('--registrar-campo', 'P5', '--valor', 'agente')
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.estado.read_bytes(), antes)
        self.assertEqual(self.eventos()[-1]['evento'], 'TentativaNegada')

    def test_10_campo_reservado_nao_pode_ser_declarado(self):
        self.configurar(lambda pb: next(e for e in pb['etapas'] if e['id'] == 'P5')[
            'campos_registraveis'].update(cumprido={}))
        self.recusa(['reservado'], campo='cumprido', valor='true')

    def test_11_taxonomia_invalida(self):
        self.configurar(lambda pb: next(e for e in pb['etapas'] if e['id'] == 'P5')[
            'campos_registraveis']['classificacao_tecnologica'].update(valores='agente'))
        self.recusa(['valores'])

    def test_12_agente_com_playbook_invalido(self):
        self.pbpath.write_text('{')
        self.recusa(['playbook invalido'], autor='agente-teste')

    def test_13_categorias_aceitas(self):
        for valor in VALORES:
            with self.subTest(valor=valor):
                r = self.registrar(valor=valor)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(json.loads(self.estado.read_text())['cumprimentos']['P5'][
                    'classificacao_tecnologica'], valor)
                ev = self.eventos()[-1]
                self.assertEqual(ev['evento'], 'CampoRegistrado')
                self.assertEqual((ev['etapa'], ev['campo'], ev['valor'], ev['autor']),
                                 ('P5', 'classificacao_tecnologica', valor, 'Celso do Vale'))

    def test_14_substituicao_tem_historico(self):
        self.assertEqual(self.registrar().returncode, 0)
        self.assertEqual(self.registrar(valor='caso isolado').returncode, 0)
        ev = self.eventos()
        self.assertEqual([e['valor'] for e in ev], ['agente', 'caso isolado'])
        self.assertEqual(ev[-1]['anterior'], 'agente')

    def test_15_campo_livre_de_outro_metodo(self):
        self.configurar(lambda pb: next(e for e in pb['etapas'] if e['id'] == 'P5')[
            'campos_registraveis'].update(observacao={}))
        r = self.registrar(campo='observacao', valor='texto humano sem taxonomia')
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_16_declaracao_do_template(self):
        pb = json.loads((RAIZ / 'eiac-campo/template-caso/registro/playbook.json').read_text())
        et = next(e for e in pb['etapas'] if e['id'] == 'P5')
        self.assertEqual(et.get('campos_registraveis', {}).get('classificacao_tecnologica'),
                         {'valores': VALORES})

    def test_17_e3_partes_a_b_sem_escrita_direta_no_estado(self):
        # Desde a abertura, este percurso apenas LÊ estado.json; toda escrita
        # passa por novo-caso, avancar e selar. Nenhuma fixture de estado.
        base = pathlib.Path(self.tmp.name) / 'ponta-a-ponta'
        r = subprocess.run(['bash', str(RAIZ / 'novo-caso.sh'), 'controle', '--responsavel',
                            'Celso do Vale', str(base)], text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.caso = base / 'controle'
        self.estado = self.caso / 'registro/estado.json'
        for key, value in [('user.name', 'Celso do Vale'), ('user.email', 'teste@exemplo.com')]:
            subprocess.run(['git', 'config', key, value], cwd=self.caso, check=True)
        r = self.executar('--apurar-nivel', 'N2', '--eixos', 'DAD 5, GOV 3, CRI 6')
        self.assertEqual(r.returncode, 0, r.stderr)
        pb = json.loads((self.caso / 'registro/playbook.json').read_text())
        for et in pb['etapas']:
            if et['id'] == 'P5':
                r = self.registrar()
                self.assertEqual(r.returncode, 0, r.stderr)
            cam = et['camada']['N2']
            if pb['encerramento_por_camada'][cam] or et.get('delegavel') is False:
                r = self.executar('--registrar-sessao', et['id'], '--participantes',
                                  'Celso do Vale, Pessoa Cliente')
                self.assertEqual(r.returncode, 0, r.stderr)
            r = self.executar('--encerrar', et['id'])
            self.assertEqual(r.returncode, 0, r.stderr)
            if any(e.get('exige_selo_apos') == et['id'] for e in pb['etapas']):
                r = subprocess.run(['python3', str(RAIZ / 'eiac-nucleo/scripts/selar.py'),
                                    '--autor', 'Celso do Vale', '--nota', 'controle E3'],
                                   cwd=self.caso, text=True, capture_output=True)
                self.assertEqual(r.returncode, 0, r.stderr)
            if et['id'] == 'P5':
                break
        r = subprocess.run(['python3', str(RAIZ / 'eiac-campo/scripts/entregaveis.py'),
                            '--renderizar', 'E3', '--autor', 'Celso do Vale', '--emitir'],
                           cwd=self.caso, text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        texto = (self.caso / 'caso/entregaveis/E3.md').read_text()
        self.assertIn('Parte A', texto)
        self.assertIn('Parte B', texto)
        emitidos = [e['entregavel'] for e in self.eventos() if e['evento'] == 'EntregavelEmitido']
        self.assertEqual(emitidos, ['E3-D', 'E3-E'])
        self.assertTrue(any(e['evento'] == 'CampoRegistrado' for e in self.eventos()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
