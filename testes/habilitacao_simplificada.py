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
        c = I.ler_config(self.cfg); c['entrada_dir'] = str(self.entrada); I.escrever(self.cfg, c)

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

    def exportacao(self, casos=('OUTRO-A', 'CASO', 'OUTRO-B')):
        with self.csv.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['Submission ID', 'caso', 'Respondente', 'HAB-0a-1'])
            w.writeheader()
            for i,caso in enumerate(casos):
                w.writerow({'Submission ID':'SUB-'+str(i), 'caso':caso, 'Respondente':'Pessoa Cliente',
                            'HAB-0a-1': 'SEGREDO-'+caso})
        s = json.loads((self.exp/'expediente.json').read_text())
        s['tratamento'] = {'escopo':'administrativo', 'condicoes':'Condições sintéticas'}; H.salvar(self.exp, s)

    def coletar(self, **extra):
        return H.executar(self.exp, 'receber-exportacao', dict(config_emcia=str(self.cfg), arquivo=str(self.csv),
            id='S1', **extra))

    def test_10_exportacao_sem_linha_do_caso(self):
        self.permanente(); self.exportacao(('OUTRO-A',))
        with self.assertRaisesRegex(ValueError, 'nenhuma submissão'): self.coletar()
        self.assertFalse((self.exp/'arquivos').exists())
        self.assertNotIn('SEGREDO-OUTRO-A', (self.exp/'expediente.json').read_text())

    def test_11_duas_submissoes_nao_escolhe(self):
        self.permanente(); self.exportacao(('CASO', 'CASO'))
        with self.assertRaisesRegex(ValueError, 'qual submissão'): self.coletar()
        self.assertFalse((self.exp/'arquivos').exists())

    def test_12_permanente_ausente_bloqueia_coleta(self):
        H.iniciar(self.exp, 'HAB', 'Pessoa Engenheira', 'CASO')
        self.exportacao()
        with self.assertRaisesRegex(ValueError, 'conferido'): self.coletar()

    def test_13_filtra_antes_de_persistir(self):
        self.permanente(); self.exportacao(); original = self.csv.read_bytes(); self.coletar()
        s = json.loads((self.exp/'expediente.json').read_text()); fonte = s['fontes']['S1']
        self.assertEqual(fonte['canal'], 'tally-exportacao')
        self.assertEqual(fonte['original_sha256'], H.digest(original))
        self.assertNotEqual(fonte['arquivo']['sha256'], H.digest(original))
        for arq in self.exp.rglob('*'):
            if arq.is_file():
                self.assertNotIn(b'SEGREDO-OUTRO', arq.read_bytes(), str(arq))
        self.assertIn(b'SEGREDO-CASO', H.ler_arquivo(self.exp, fonte['arquivo']))

    def test_14_selecao_explicita_dentre_duas(self):
        self.permanente(); self.exportacao(('CASO', 'CASO', 'OUTRO-A')); self.coletar(submissao='SUB-1')
        fonte = json.loads((self.exp/'expediente.json').read_text())['fontes']['S1']
        self.assertEqual(fonte['submissao'], 'SUB-1')
        linhas = list(csv.DictReader(io.StringIO(H.ler_arquivo(self.exp, fonte['arquivo']).decode())))
        self.assertEqual(len(linhas), 1); self.assertEqual(linhas[0]['Submission ID'], 'SUB-1')

    def test_15_arquivo_fora_da_entrada_recusa(self):
        self.permanente(); self.exportacao()
        outro = self.base/'fora.csv'; outro.write_bytes(self.csv.read_bytes()); self.csv = outro
        with self.assertRaisesRegex(ValueError, 'entrada'): self.coletar()

if __name__ == '__main__': unittest.main(verbosity=2)
