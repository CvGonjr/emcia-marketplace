"""Recebimento humano: negativas conferem a trilha e preservam fontes."""
import hashlib
import json
import subprocess
import sys
import unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.canais import definir

SCRIPT = RAIZ/'eiac-campo/scripts/receber.py'


class Receber(CasoHook):
    def setUp(self):
        super().setUp(); definir(self.caso)
        self.estado['etapa_atual'] = 'P2'; self.salvar()
        self.arquivo = self.caso/'rascunho/entrada/amostra.txt'
        self.arquivo.parent.mkdir(parents=True); self.arquivo.write_text('documento sintético')
        self.manifesto = self.caso/'rascunho/entrada/coleta.json'
        self.dados = dict(ferramenta='drive', objeto_id='OBJ-SINTETICO',
                          conteiner_id='SINTETICO-documentos-pasta_id',
                          modificado_em='2026-10-02T10:00:00Z', coletado_em='2026-10-02T11:00:00Z')

    def executar(self, *args):
        self.manifesto.write_text(json.dumps(self.dados))
        return subprocess.run([sys.executable, str(SCRIPT), '--arquivo', str(self.arquivo),
                               '--manifesto', str(self.manifesto), *args], cwd=self.caso,
                              text=True, capture_output=True)

    def recusa(self, *args):
        antes = len(self.eventos()); originais = list((self.caso/'fontes').rglob('*'))
        r = self.executar(*args); self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertEqual(len(self.eventos()), antes+1)
        self.assertEqual(self.eventos()[-1]['evento'], 'TentativaNegada')
        self.assertEqual(list((self.caso/'fontes').rglob('*')), originais)

    def test_01_origem_nao_declarada(self):
        self.dados['conteiner_id'] = 'ALHEIO'; self.recusa()

    def test_02_etapa_errada(self):
        self.estado['etapa_atual'] = 'P9'; self.salvar(); self.recusa()

    def test_03_filtro_alheio(self):
        self.estado['etapa_atual'] = 'F0'; self.salvar()
        self.dados.update(ferramenta='tally', conteiner_id='SINTETICO-triagem-formulario_id',
                          submissao_id='SUB-01', campos_ocultos={'caso': 'outro'})
        self.recusa()

    def test_04_ausente(self):
        self.arquivo.unlink(); self.recusa()

    def test_05_hash_duplicado(self):
        self.assertEqual(self.executar().returncode, 0); self.recusa()

    def test_06_autor_agente(self):
        self.recusa('--autor', 'AG-01')

    def test_07_symlink_externo(self):
        self.arquivo.unlink(); self.arquivo.symlink_to('/etc/hosts'); self.recusa()

    def test_08_fora_preparacao(self):
        self.arquivo = self.caso/'arquivo.txt'; self.arquivo.write_text('controle'); self.recusa()

    def test_09_sem_submissao(self):
        self.estado['etapa_atual'] = 'F0'; self.salvar()
        self.dados.update(ferramenta='tally', conteiner_id='SINTETICO-triagem-formulario_id',
                          campos_ocultos={'caso': self.estado['caso']}); self.recusa()

    def test_10_sessao_agente(self):
        self.negado('Bash', {'command': f'python3 {SCRIPT} --arquivo {self.arquivo} --manifesto {self.manifesto}'})

    def test_11_data_invalida(self):
        self.dados['coletado_em'] = 'ontem'; self.recusa()

    def test_12_decisao_versao_alheia(self):
        self.assertEqual(self.executar().returncode, 0)
        p = self.caso/'rascunho/decisao.json'
        p.write_text(json.dumps(dict(decisor='Celso do Vale', motivo='Revisão', data='2026-10-02',
                                    recebimento_anterior='alheio')))
        self.recusa('--nova-versao', str(p))

    def test_13_assercao_fonte_inexistente(self):
        (self.caso/'rascunho/a.md').write_text('- [D · fonte: REC-999999 · Celso do Vale] Controle.\n')
        r = self.rodar('validar.py', '--arquivo', 'caso/a.md')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.eventos()[-1]['evento'], 'TentativaNegada')

    def test_14_fonte_adulterada(self):
        r = self.executar(); self.assertEqual(r.returncode, 0, r.stderr)
        ref = json.loads(r.stdout); (self.caso/ref['arquivo']).write_text('adulterado')
        (self.caso/'rascunho/a.md').write_text(f"- [V · fonte: {ref['id']} · Celso do Vale] Controle.\n")
        r = self.rodar('validar.py', '--arquivo', 'caso/a.md')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.eventos()[-1]['evento'], 'TentativaNegada')

    def test_22_assercao_com_fonte_registrada(self):
        r = self.executar(); self.assertEqual(r.returncode, 0, r.stderr)
        ref = json.loads(r.stdout)
        (self.caso/'rascunho/a.md').write_text(f"- [V · fonte: {ref['id']} · Celso do Vale] Documento recebido.\n")
        r = self.rodar('validar.py', '--arquivo', 'caso/a.md')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.eventos()[-1]['fontes'], {ref['id']: ref['sha256']})

    def test_20_recebe_hash_origem(self):
        r = self.executar(); self.assertEqual(r.returncode, 0, r.stderr)
        ref = json.loads(r.stdout)
        self.assertEqual(ref['sha256'], hashlib.sha256(self.arquivo.read_bytes()).hexdigest())
        self.assertEqual((self.caso/ref['arquivo']).read_bytes(), self.arquivo.read_bytes())
        self.assertEqual(ref['origem'], self.dados)
        self.assertEqual(self.eventos()[-1]['evento'], 'MaterialRecebido')

    def test_21_nova_versao_decidida(self):
        r = self.executar(); self.assertEqual(r.returncode, 0, r.stderr)
        antigo = json.loads(r.stdout)
        p = self.caso/'rascunho/decisao.json'
        p.write_text(json.dumps(dict(decisor='Celso do Vale', motivo='Revisão', data='2026-10-02',
                                    recebimento_anterior=antigo['id'])))
        r = self.executar('--nova-versao', str(p)); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotEqual(json.loads(r.stdout)['arquivo'], antigo['arquivo'])
        self.assertTrue((self.caso/antigo['arquivo']).exists())


if __name__ == '__main__': unittest.main(verbosity=2)
