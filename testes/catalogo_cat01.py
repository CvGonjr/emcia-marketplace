"""CAT-01: catálogo literal, correspondência e fronteira determinística."""
import copy
import json
import pathlib
import re
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
CAMPO = RAIZ / 'eiac-campo'
CAT = CAMPO / 'reference/metodo/EMCIA-CAT-01-fronteira-de-delegacao.md'
CAMPOS = ('id', 'nome', 'camada', 'natureza', 'insumo', 'saida',
          'criterio_de_verificacao', 'ag_autorizado')


def ler_cat(texto):
    anexo = texto.split('## Anexo A —', 1)[1].split('## Anexo B —', 1)[0]
    agentes = {}
    for linha in anexo.splitlines():
        if not linha.startswith('| **AG-'):
            continue
        cols = [c.strip().replace('**', '') for c in linha.strip('|').split('|')]
        for inicio, fim, isolado in re.findall(r'HB-(\d+) a HB-(\d+)|HB-(\d+)', cols[3]):
            numeros = range(int(inicio), int(fim)+1) if inicio else [int(isolado)]
            for n in numeros:
                agentes[f'HB-{n:02d}'] = cols[0]
    habilidades = []
    for linha in anexo.splitlines():
        if not linha.startswith('| **HB-'):
            continue
        cols = [c.strip().replace('**', '') for c in linha.strip('|').split('|')]
        camada, natureza = cols[2].split(' · ')
        habilidades.append(dict(zip(CAMPOS, (
            cols[0], cols[1], camada, {'Aut.': 'Automatizado', 'Híb.': 'Híbrido'}[natureza],
            cols[3], cols[4], cols[5], agentes[cols[0]],
        ))))
    correspondencia = {}
    trecho = texto.split('## Anexo C —', 1)[1].split('## Anexo D —', 1)[0]
    for linha in trecho.splitlines():
        if not re.match(r'^\| (?:F0|P\d+[a-z]?) \|', linha):
            continue
        cols = [c.strip() for c in linha.strip('|').split('|')]
        correspondencia[cols[0]] = re.findall(r'HB-\d+', cols[3])
    return habilidades, correspondencia


def ler_skills():
    resultado = {}
    for p in (CAMPO / 'skills').glob('hb-*/SKILL.md'):
        front = p.read_text().split('---', 2)[1]
        hb = re.search(r'^hb:\s*(\[.*\])$', front, re.M)
        resultado[p.parent.name] = json.loads(hb[1]) if hb else []
    return resultado


def conferir(canonicas, correspondencia, catalogo, pb, skills):
    erros = []
    literal = [{k: h.get(k) for k in CAMPOS} for h in catalogo]
    if literal != canonicas:
        erros.append('catalogo-literal')
    etapas = {e['id']: e for e in pb['etapas']}
    if {i: e.get('hb', []) for i, e in etapas.items()} != correspondencia:
        erros.append('correspondencia')
    for e in etapas.values():
        if skills.get(e['habilidade']) != e.get('hb', []):
            erros.append('frontmatter:' + e['id'])
    referencias = {hb for e in etapas.values() for hb in e.get('hb', [])}
    if not {h['id'] for h in canonicas} <= referencias:
        erros.append('hb-sem-etapa')
    por_id = {h['id']: h for h in catalogo}
    for nome, hbs in skills.items():
        if any(h not in por_id for h in hbs) or len({por_id[h]['ag_autorizado'] for h in hbs if h in por_id}) > 1:
            erros.append('skill-mistura-ag:' + nome)
    ordem = ('EX1', 'EX2', 'EX3', 'EX4')
    for e in etapas.values():
        camadas = e.get('camada_monitoramento', e['camada']) if e['id'] == 'P10' else e['camada']
        for hb in e.get('hb', []):
            camada = por_id.get(hb, {}).get('camada')
            if camada not in ('EX1', 'EX2') or any(
                    camadas.get(n) not in ordem or ordem.index(camada) > ordem.index(camadas[n])
                    for n in pb['niveis']):
                erros.append('camada-preparacao:' + e['id'])
    if 'HB-09' not in etapas['P3d'].get('hb', []) or 'HB-09' in etapas['P1'].get('hb', []):
        erros.append('hb09-p3d')
    if not any(a['id'] == 'decidir-prosseguimento' for a in pb['decisoes_humanas']):
        erros.append('ato-prosseguimento')
    if not any(p.get('descricao') == 'Decisão de prosseguimento registrada'
               and p.get('padrao') == 'registro/prosseguimento/vigente.yaml'
               and {'decisor', 'data', 'desfecho', 'motivo'} <= set(p.get('preenchidos', []))
               for p in etapas['F0'].get('produtos_encerramento', [])):
        erros.append('produto-prosseguimento')
    return erros


class CatalogoCAT01(unittest.TestCase):
    def setUp(self):
        self.canonicas, self.relacao = ler_cat(CAT.read_text())
        self.catalogo = json.loads((CAMPO / 'reference/habilidades.json').read_text())['habilidades']
        self.pb = json.loads((CAMPO / 'template-caso/registro/playbook.json').read_text())
        self.skills = ler_skills()

    def conferir(self):
        return conferir(self.canonicas, self.relacao, self.catalogo, self.pb, self.skills)

    def test_00_catalogo_corresponde_ao_canonico(self):
        self.assertEqual(len(self.canonicas), 21)
        self.assertEqual(len(self.relacao), 13)
        self.assertEqual(self.conferir(), [])

    def test_01_negativa_de_cada_campo_literal(self):
        for campo in CAMPOS:
            with self.subTest(campo=campo):
                salvo = copy.deepcopy(self.catalogo)
                self.catalogo[0][campo] = 'valor divergente'
                self.assertIn('catalogo-literal', self.conferir())
                self.catalogo = salvo

    def test_02_correspondencia_divergente(self):
        self.pb['etapas'][0]['hb'].pop()
        self.assertIn('correspondencia', self.conferir())

    def test_03_frontmatter_divergente(self):
        self.skills['hb-enquadrar'].pop()
        self.assertIn('frontmatter:F0', self.conferir())

    def test_04_hb_sem_etapa(self):
        for e in self.pb['etapas']:
            e['hb'] = [h for h in e.get('hb', []) if h != 'HB-05']
        self.assertIn('hb-sem-etapa', self.conferir())

    def test_05_skill_mistura_agentes(self):
        self.skills['hb-enquadrar'].append('HB-06')
        self.assertIn('skill-mistura-ag:hb-enquadrar', self.conferir())

    def test_06_hb_superior_a_etapa_em_um_nivel(self):
        self.pb['etapas'][1]['camada']['N1'] = 'EX1'
        self.assertIn('camada-preparacao:P1', self.conferir())

    def test_07_monitoramento_de_p10_respeita_camada(self):
        self.pb['etapas'][-1]['camada_monitoramento']['N3'] = 'EX1'
        self.assertIn('camada-preparacao:P10', self.conferir())

    def test_08_hb09_fora_de_p3d(self):
        etapa = next(e for e in self.pb['etapas'] if e['id'] == 'P3d')
        etapa['hb'] = [h for h in etapa.get('hb', []) if h != 'HB-09']
        self.pb['etapas'][1]['hb'].append('HB-09')
        self.assertIn('hb09-p3d', self.conferir())

    def test_09_ato_ausente(self):
        self.pb['decisoes_humanas'] = [a for a in self.pb['decisoes_humanas'] if a['id'] != 'decidir-prosseguimento']
        self.assertIn('ato-prosseguimento', self.conferir())

    def test_10_produto_ausente(self):
        self.pb['etapas'][0]['produtos_encerramento'] = []
        self.assertIn('produto-prosseguimento', self.conferir())


if __name__ == '__main__':
    unittest.main(verbosity=2)
