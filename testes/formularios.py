"""Redação fixa da triagem e isolamento na preparação de submissões."""
import copy
import json
import pathlib
import re
import subprocess
import sys
import unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.canais import definir


def perguntas(texto):
    trecho = texto.split('### 3.3 As nove perguntas', 1)[1].split('### 3.4 ', 1)[0]
    itens = []
    for linha in trecho.splitlines():
        m = re.fullmatch(r'\| \*\*((?:DAD|GOV|CRI)-[123])\*\* \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|', linha)
        if m:
            itens.append(dict(id=m[1], pergunta=m[2], alternativas=[dict(pontos=i, texto=m[i+2]) for i in range(1,4)]))
    return itens


class Redacao(unittest.TestCase):
    def test_01_divergencia_reprova(self):
        instrumento = (RAIZ/'eiac-campo/reference/metodo/EMCIA-TRI-01-instrumento-de-triagem.md').read_text()
        modelo = json.loads((RAIZ/'eiac-campo/reference/formularios/triagem.json').read_text())
        modelo['perguntas'][0]['pergunta'] += ' reformulada'
        self.assertNotEqual(modelo['perguntas'], perguntas(instrumento))

    def test_20_redacao_exata_perguntas_e_alternativas(self):
        instrumento = (RAIZ/'eiac-campo/reference/metodo/EMCIA-TRI-01-instrumento-de-triagem.md').read_text()
        modelo = json.loads((RAIZ/'eiac-campo/reference/formularios/triagem.json').read_text())
        self.assertEqual(len(modelo['perguntas']), 9)
        self.assertEqual(modelo['perguntas'], perguntas(instrumento))
        self.assertEqual(modelo['secao_perguntas'], '3.3')
        self.assertEqual(modelo['secao_pontuacao'], '3.4')


class Formularios(CasoHook):
    def setUp(self):
        super().setUp(); definir(self.caso)
        self.p = self.caso/'rascunho/entrada/submissoes.json'; self.p.parent.mkdir()
        self.sub = dict(formulario_id='SINTETICO-triagem-formulario_id', submissao_id='SUB-1',
                        campos_ocultos={'caso': self.estado['caso']})

    def executar(self, *args):
        return subprocess.run([sys.executable, str(RAIZ/'eiac-campo/scripts/formularios.py'), *args],
                              cwd=self.caso, text=True, capture_output=True)

    def test_01_formulario_alheio(self):
        self.p.write_text('[]'); antes = len(self.eventos())
        r = self.executar('submissoes', '--etapa', 'F0', '--entrada', str(self.p), '--formulario', 'ALHEIO')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.eventos()[antes]['evento'], 'TentativaNegada')

    def test_20_outro_caso_ignorado_sem_registro(self):
        outro = copy.deepcopy(self.sub); outro['campos_ocultos']['caso'] = 'outro-caso'
        self.p.write_text(json.dumps([outro, self.sub])); antes = self.eventos()
        r = self.executar('submissoes', '--etapa', 'F0', '--entrada', str(self.p), '--formulario', self.sub['formulario_id'])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [self.sub]); self.assertEqual(self.eventos(), antes)

    def test_21_link_com_caso_sem_envio(self):
        antes = self.eventos(); r = self.executar('link', '--etapa', 'F0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('caso='+self.estado['caso'], json.loads(r.stdout)['link_preparado'])
        self.assertEqual(self.eventos(), antes)


if __name__ == '__main__': unittest.main(verbosity=2)
