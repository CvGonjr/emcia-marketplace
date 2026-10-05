"""Contratos reais transcritos; nenhuma chamada a serviço ou dado de cliente."""
import copy
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'eiac-campo/scripts'))
sys.path.insert(0, str(ROOT/'eiac-nucleo/scripts'))
import iniciar as I
import escopo_externo as S
from apoio.hook_real import CasoHook
from apoio.canais import definir

FIXTURE = ROOT/'testes/apoio/inventario-mcp-real.json'
DRIVE = 'mcp__claude_ai_Google_Drive__'
CAL = 'mcp__claude_ai_Google_Calendar__'
TALLY = 'mcp__tally__'
FOLDER = 'application/vnd.google-apps.folder'


class Contrato(unittest.TestCase):
    def setUp(self):
        self.inv = json.loads(FIXTURE.read_text())

    def test_01_nome_ausente_reprova_contrato(self):
        perfis = copy.deepcopy(I.PERFIS)
        perfis['mcp__nao_existe__criar'] = copy.deepcopy(next(iter(perfis.values())))
        with self.assertRaises(ValueError):
            I.validar_contrato_perfis(self.inv, perfis)

    def test_02_parametro_ausente_reprova_contrato(self):
        perfis = copy.deepcopy(I.PERFIS)
        perfis[DRIVE+'search_files']['argumentos'][0]['campo'] = 'q'
        with self.assertRaises(ValueError):
            I.validar_contrato_perfis(self.inv, perfis)

    def test_03_cada_nome_e_parametro_consta_do_inventario(self):
        I.validar_contrato_perfis(self.inv)
        perfil = I.calibrar(self.inv)
        self.assertGreaterEqual(len(perfil['regras']), 9)
        self.assertEqual(len(perfil['regras']), len({r['ferramenta'] for r in perfil['regras']}))
        self.assertTrue(all(r['ferramenta'] in {f['nome'] for f in self.inv['ferramentas']} for r in perfil['regras']))

    def test_04_garantia_tally_ausente_e_manual_explicito(self):
        p = I.calibrar(self.inv)
        self.assertIn(TALLY+'fetch_submissions', p['recusadas'])
        manual = next(m for m in p['manuais'] if m['passo']=='coletar-submissoes')
        self.assertIn('campo oculto', manual['motivo'])
        self.assertTrue(any(m['passo']=='preparar-formulario' for m in p['manuais']))

    def test_05_criar_sem_workspace_fica_recusado(self):
        f = next(f for f in self.inv['ferramentas'] if f['nome']==TALLY+'create_new_form')
        del f['inputSchema']['properties']['workspaceId']
        p = I.calibrar(self.inv)
        self.assertIn(f['nome'], p['recusadas'])
        self.assertTrue(any('workspaceId' in m['motivo'] for m in p['manuais']))

    def test_06_publicacao_ausente_vira_acao_humana(self):
        self.inv['ferramentas'] = [f for f in self.inv['ferramentas'] if f['nome']!=TALLY+'publish_form']
        p = I.calibrar(self.inv)
        self.assertTrue(any(m['passo']=='publicar-formulario' for m in p['manuais']))
        self.assertNotIn(TALLY+'publish_form', [r['ferramenta'] for r in p['regras']])

    def test_07_schema_calendar_parcial_nao_inventa_subcampos(self):
        p = I.calibrar(self.inv)
        r = next(r for r in p['regras'] if r['ferramenta']==CAL+'create_event')
        self.assertIn('calendarId', r['parametros'])
        self.assertNotIn('attendees', r['parametros'])
        self.assertIn('attendees', p['parametros_recusados'][CAL+'create_event'])


if __name__=='__main__': unittest.main(verbosity=2)
