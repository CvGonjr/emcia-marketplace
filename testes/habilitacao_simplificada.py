"""Contrato administrativo simplificado; negativas antes do percurso sintético."""
import copy
import csv
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'eiac-campo/scripts'))
import iniciar as I
import habilitacao as H

class Simplificada(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name); self.cfg = self.base/'config.json'
        I.configurar(self.cfg, dict(responsavel='Pessoa Engenheira', base_casos=str(self.base/'casos'),
            base_expedientes=str(self.base/'expedientes'), workspace_tally='WORK', pasta_drive='ROOT',
            calendario_casos='CAL', navegador='google-chrome'))
        self.exp = self.base/'expedientes/HAB'; self.entrada = self.base/'entrada'; self.entrada.mkdir()
        self.csv = self.entrada/'exportacao.csv'

    def op(self, nome, literal='conferido', **extra):
        d = dict(habilitacao='HAB', caso='CASO', **extra)
        return I.operar(self.cfg, nome, d, I.aprovar(self.cfg, nome, d, literal, 'Controle sintético'))

    def permanente(self):
        inv = json.loads((ROOT/'testes/apoio/inventario-mcp-real.json').read_text())
        self.op('perfil', ferramentas=inv, perfil=I.calibrar(inv)); self.op('iniciar', id='HAB')
        d = dict(habilitacao='HAB', caso='CASO', ferramenta='mcp__tally__create_new_form',
                 argumentos={'title':'Sintético', 'workspaceId':'WORK'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        I.registrar_retorno(self.cfg, d, {'ids':{'formulario_id':'FORM'}})
        d.update(ferramenta='mcp__tally__load_form', argumentos={'formId':'FORM'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        raw = json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())
        I.registrar_retorno(self.cfg, d, {'resposta':raw})
        rel = self.op('conferir-formulario', formulario_id='FORM', modelo='habilitacao')
        self.op('confirmar-formulario', formulario_id='FORM', relatorio_sha256=rel['sha256'])
        self.op('formulario-permanente', formulario_id='FORM', modelo='habilitacao')
        return rel

    def test_01_permanente_sem_conferencia_recusa(self):
        import formularios_permanentes as F
        with self.assertRaisesRegex(ValueError, 'conferido'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_02_contrato_anterior_recusa(self):
        import formularios_permanentes as F
        self.permanente()
        original = F.modelo
        arquivo = self.base/'novo-contrato.json'
        modelo = json.loads(original('habilitacao').read_text()); modelo['perguntas'][0]['pergunta'] += ' alterado'
        arquivo.write_text(json.dumps(modelo))
        with patch.object(F, 'modelo', return_value=arquivo), self.assertRaisesRegex(ValueError, 'contrato mudou'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_03_relatorio_adulterado_recusa(self):
        import formularios_permanentes as F
        rel = self.permanente(); pathlib.Path(rel['arquivo']).write_text('alteração')
        with self.assertRaisesRegex(ValueError, 'adulterado'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_04_reutiliza_sem_nova_aprovacao(self):
        import formularios_permanentes as F
        self.permanente(); antes = self.cfg.with_name('eventos.jsonl').read_bytes()
        reg = F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')
        self.assertEqual(reg['formId'], 'FORM')
        self.assertEqual(F.link(reg, 'CASO-2'), 'https://tally.so/r/FORM?caso=CASO-2')
        self.assertEqual(antes, self.cfg.with_name('eventos.jsonl').read_bytes())

    def test_05_nova_leitura_invalida_permanente(self):
        import formularios_permanentes as F
        self.permanente()
        d = dict(habilitacao='HAB', caso='CASO', ferramenta='mcp__tally__load_form', argumentos={'formId':'FORM'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        I.registrar_retorno(self.cfg, d, {'resposta':json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())})
        with self.assertRaisesRegex(ValueError, 'conferência'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

if __name__ == '__main__': unittest.main(verbosity=2)
