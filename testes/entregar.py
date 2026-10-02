"""Entrega: negativas antes do controle de emissão e registro humano."""
import hashlib
import json
import subprocess
import sys
import unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.canais import definir

SCRIPT = RAIZ/'eiac-campo/scripts/entregar.py'


class Entregar(CasoHook):
    def setUp(self):
        super().setUp(); definir(self.caso)
        self.arquivo = self.caso/'caso/entregaveis/E1.md'
        self.arquivo.parent.mkdir(parents=True); self.arquivo.write_text('entregável sintético')
        self.estado['cumprimentos']['F0'] = {'cumprido': True}
        self.salvar()
        self.entrada = self.caso/'rascunho/entrega.json'
        self.dados = dict(entregavel='E1', versao=1,
                          sha256=hashlib.sha256(self.arquivo.read_bytes()).hexdigest(),
                          arquivo_id='DEST-SINTETICO', destino_id='SINTETICO-entregas-pasta_id',
                          destinatario='Pessoa Cliente', data='2026-10-02')

    def emitir(self):
        r = self.rodar('avancar.py', '--emitir', 'E1', '--autor', 'Celso do Vale')
        self.assertEqual(r.returncode, 0, r.stderr)

    def executar(self, *args):
        self.entrada.write_text(json.dumps(self.dados))
        return subprocess.run([sys.executable, str(SCRIPT), '--entrada', str(self.entrada), *args],
                              cwd=self.caso, text=True, capture_output=True)

    def recusa(self, *args):
        antes = len(self.eventos()); r = self.executar(*args)
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertEqual(len(self.eventos()), antes+1)
        self.assertEqual(self.eventos()[-1]['evento'], 'TentativaNegada')

    def test_01_nao_emitido(self):
        self.recusa()

    def test_02_versao_divergente(self):
        self.emitir(); self.dados['versao'] = 2; self.recusa()

    def test_03_hash_divergente(self):
        self.emitir(); self.dados['sha256'] = '0'*64; self.recusa()

    def test_04_destino_alheio(self):
        self.emitir(); self.dados['destino_id'] = 'ALHEIO'; self.recusa()

    def test_05_destinatario_agente(self):
        self.emitir(); self.dados['destinatario'] = 'AG-01'; self.recusa()

    def test_06_arquivo_alterado_apos_emissao(self):
        self.emitir(); self.arquivo.write_text('outro conteúdo')
        self.dados['sha256'] = hashlib.sha256(self.arquivo.read_bytes()).hexdigest(); self.recusa()

    def test_07_autor_agente(self):
        self.emitir(); self.recusa('--autor', 'AG-01')

    def test_08_sessao_agente(self):
        self.negado('Bash', {'command': f'python3 {SCRIPT} --entrada {self.entrada}'})

    def test_09_destino_entrada(self):
        self.emitir(); self.dados['destino_id'] = 'SINTETICO-documentos-pasta_id'; self.recusa()

    def test_20_entrega_emitida(self):
        self.emitir(); r = self.executar(); self.assertEqual(r.returncode, 0, r.stderr)
        reg = json.loads(r.stdout)
        self.assertEqual(reg['sha256'], self.dados['sha256'])
        self.assertEqual(self.eventos()[-1]['evento'], 'EntregavelEntregue')
        self.assertNotIn('aceite', reg)


if __name__ == '__main__': unittest.main(verbosity=2)
