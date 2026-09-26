"""A9: emissão exige o artefato declarado pelo playbook do caso."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / 'eiac-nucleo/scripts/avancar.py'


class EmissaoA9(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.caso = pathlib.Path(self.tmp.name)
        shutil.copytree(RAIZ / 'eiac-campo/template-caso/registro', self.caso / 'registro')
        self.estado = self.caso / 'registro/estado.json'
        self.pbpath = self.caso / 'registro/playbook.json'
        pb = json.loads(self.pbpath.read_text())
        for ent in pb['entregaveis']:
            ent['artefato'] = 'caso/entregaveis/' + ('E3' if ent['id'].startswith('E3-') else ent['id']) + '.md'
            ent['comando_materializacao'] = '/eiac-campo:emitir'
        self.pbpath.write_text(json.dumps(pb))
        st = json.loads(self.estado.read_text())
        st.update(responsavel='Celso do Vale', nivel='N2', etapa_atual='P6')
        st['cumprimentos'] = {et['id']: {'cumprido': True} for et in pb['etapas']}
        st['cumprimentos']['P5']['classificacao_tecnologica'] = 'agente'
        st['inegociaveis'] = {str(i['n']): {'satisfeito': True, 'autor': 'Celso do Vale',
                                          'evidencia': 'registro/evidencia.yaml'} for i in pb['inegociaveis']}
        self.estado.write_text(json.dumps(st))

    def executar(self, entregavel='E3-D', *args):
        return subprocess.run(['python3', str(SCRIPT), '--emitir', entregavel,
                               '--autor', 'Celso do Vale', *args], cwd=self.caso,
                              text=True, capture_output=True)

    def evento(self):
        return json.loads((self.caso / 'registro/eventos.jsonl').read_text().splitlines()[-1])

    def arquivo(self, caminho='caso/entregaveis/E3.md', conteudo='# Blueprint real\n'):
        p = self.caso / caminho
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(conteudo)
        return p

    def configurar(self, fn):
        pb = json.loads(self.pbpath.read_text())
        fn(pb)
        self.pbpath.write_text(json.dumps(pb))

    def recusa(self, entregavel='E3-D', *args, partes=()):
        antes = self.estado.read_bytes()
        r = self.executar(entregavel, *args)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        for parte in partes:
            self.assertIn(parte, r.stderr)
        self.assertEqual(self.estado.read_bytes(), antes)
        ev = self.evento()
        self.assertIn(ev['evento'], ('RecusaEmissao', 'TentativaNegada'))
        self.assertEqual(ev['autor'], 'Celso do Vale')
        self.assertIn(r.stderr.strip(), ev['motivo'])

    def test_00_sem_artefato(self):
        self.recusa(partes=('caso/entregaveis/E3.md', '/eiac-campo:emitir'))

    def test_01_arquivo_vazio(self):
        self.arquivo(conteudo=' \n')
        self.recusa(partes=('vazi',))

    def test_02_diretorio_nao_e_arquivo(self):
        (self.caso / 'caso/entregaveis/E3.md').mkdir(parents=True)
        self.recusa(partes=('caso/entregaveis/E3.md',))

    def test_03_materializar_nao_contorna_caminho(self):
        outro = self.arquivo('rascunho/outro.md')
        self.recusa('E3-D', '--materializar', str(outro), partes=('caso/entregaveis/E3.md',))

    def test_04_caminho_nao_declarado(self):
        self.configurar(lambda pb: pb['entregaveis'][2].pop('artefato'))
        self.recusa(partes=('artefato',))

    def test_05_caminho_fora_do_caso(self):
        self.configurar(lambda pb: pb['entregaveis'][2].update(artefato='../fora.md'))
        self.recusa(partes=('artefato',))

    def test_06_todos_os_portoes_exigem_arquivo(self):
        for ent in ('E1', 'E2', 'E3-E', 'E4', 'E5'):
            with self.subTest(ent=ent):
                self.recusa(ent, partes=('artefato', '/eiac-campo:emitir'))

    def test_07_arquivo_existente(self):
        self.arquivo()
        r = self.executar()
        self.assertEqual(r.returncode, 0, r.stderr)
        ev = self.evento()
        self.assertEqual(ev['evento'], 'EntregavelEmitido')
        self.assertTrue(pathlib.Path(ev['arquivo']).is_file())
        self.assertEqual(ev['versao'], 1)
        self.assertEqual(json.loads(self.estado.read_text())['entregaveis_emitidos']['E3-D']['versao'], 1)

    def test_08_materializacao_explicita(self):
        p = self.arquivo()
        self.assertEqual(self.executar('E3-D', '--materializar', str(p)).returncode, 0)

    def test_09_nao_aplicavel_sem_arquivo(self):
        st = json.loads(self.estado.read_text())
        st['cumprimentos']['P5']['classificacao_tecnologica'] = 'caso isolado'
        self.estado.write_text(json.dumps(st))
        antes = self.estado.read_bytes()
        r = self.executar('E3-E')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('NAO_APLICAVEL', r.stdout)
        self.assertEqual(self.evento()['evento'], 'EntregavelNaoAplicavel')
        self.assertEqual(self.estado.read_bytes(), antes)
        self.assertFalse((self.caso / 'caso/entregaveis/E3.md').exists())

    def test_10_regra_alternativa_do_caso(self):
        self.configurar(lambda pb: pb['entregaveis'][2].update(
            artefato='saida/decisao.txt', comando_materializacao='/outro:gerar'))
        self.recusa(partes=('saida/decisao.txt', '/outro:gerar'))
        self.arquivo('saida/decisao.txt')
        self.assertEqual(self.executar().returncode, 0)

    def test_11_reemissao_incrementa_versao(self):
        self.arquivo()
        self.assertEqual(self.executar().returncode, 0)
        self.assertEqual(self.executar().returncode, 0)
        self.assertEqual(self.evento()['versao'], 2)

    def test_12_template_declara_todos(self):
        pb = json.loads((RAIZ / 'eiac-campo/template-caso/registro/playbook.json').read_text())
        for ent in pb['entregaveis']:
            self.assertTrue(ent.get('artefato'))
            self.assertEqual(ent.get('comando_materializacao'), '/eiac-campo:emitir')


if __name__ == '__main__':
    unittest.main(verbosity=2)
