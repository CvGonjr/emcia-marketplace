"""Escopo MCP sobre ids declarados; negativas verificam TentativaNegada."""
import json
import subprocess
import sys
import unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.canais import definir


class Escopo(CasoHook):
    def setUp(self):
        super().setUp(); definir(self.caso)
        self.entrada = self.caso/'rascunho/entrada/listagem.json'; self.entrada.parent.mkdir()
        self.pasta = 'SINTETICO-documentos-pasta_id'

    def listar(self):
        self.entrada.write_text(json.dumps(dict(ferramenta_externa='mcp__drive__list_files',
            argumentos={'q': f"'{self.pasta}' in parents"}, conteiner_id=self.pasta,
            objetos=['ARQUIVO-SINTETICO'], coletado_em='2026-10-02T10:00:00Z')))
        return subprocess.run([sys.executable, str(RAIZ/'eiac-campo/scripts/registrar_listagem.py'),
                               '--entrada', str(self.entrada)], cwd=self.caso, text=True, capture_output=True)

    def test_01_busca_global(self):
        self.negado('mcp__drive__list_files', {'q': "name contains 'cliente'"})

    def test_02_busca_com_or(self):
        self.negado('mcp__drive__list_files', {'q': f"'{self.pasta}' in parents or true"})

    def test_03_formulario_alheio(self):
        self.negado('mcp__tally__get_submissions', {'form_id': 'ALHEIO'})

    def test_04_destino_entrada(self):
        self.negado('mcp__drive__upload_file', {'parent_id': self.pasta})

    def test_05_leitura_sem_listagem(self):
        self.negado('mcp__drive__get_file', {'file_id': 'ARQUIVO-SINTETICO'})

    def test_06_ferramenta_desconhecida(self):
        self.negado('mcp__drive__global_search', {})

    def test_07_manifesto_adulterado(self):
        r = self.listar(); self.assertEqual(r.returncode, 0, r.stderr)
        p = self.caso/'registro/listagens.json'; d = json.loads(p.read_text())
        d['listagens'][0]['objetos'].append('ALHEIO'); p.write_text(json.dumps(d))
        self.negado('mcp__drive__get_file', {'file_id': 'ALHEIO'})

    def test_08_controle_listagem_alheia(self):
        self.entrada.write_text(json.dumps(dict(ferramenta_externa='mcp__drive__list_files',
            argumentos={'q': f"'{self.pasta}' in parents"}, conteiner_id='ALHEIO',
            objetos=['ARQUIVO-SINTETICO'], coletado_em='2026-10-02T10:00:00Z')))
        antes = len(self.eventos())
        r = subprocess.run([sys.executable, str(RAIZ/'eiac-campo/scripts/registrar_listagem.py'), '--entrada', str(self.entrada)], cwd=self.caso, text=True, capture_output=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.eventos()[antes]['evento'], 'TentativaNegada')

    def test_20_lista_e_le_por_id(self):
        r = self.hook('mcp__drive__list_files', {'q': f"'{self.pasta}' in parents"})
        self.assertEqual(r.returncode, 0, r.stderr)
        r = self.listar(); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.hook('mcp__drive__get_file', {'file_id': 'ARQUIVO-SINTETICO'}).returncode, 0)

    def test_21_envio_destino_correto(self):
        self.assertEqual(self.hook('mcp__drive__upload_file', {'parent_id': 'SINTETICO-entregas-pasta_id'}).returncode, 0)

    def test_22_formulario_correto(self):
        self.assertEqual(self.hook('mcp__tally__get_submissions', {'form_id': 'SINTETICO-triagem-formulario_id'}).returncode, 0)


if __name__ == '__main__': unittest.main(verbosity=2)
