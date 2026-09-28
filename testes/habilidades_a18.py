#!/usr/bin/env python3
"""A18: rotas reais de carregamento, inclusive com sessão e selo."""
import json, os, unittest
from apoio.hook_real import CasoHook, RAIZ

class Habilidades(CasoHook):
    def setUp(self):
        super().setUp()
        self.preparar_habilidade()

    def test_01_read_instalado_absoluto(self):
        self.negado('Read', {'file_path': str(self.skill)})

    def test_02_read_relativo(self):
        self.negado('Read', {'file_path': os.path.relpath(self.skill, self.caso)})

    def test_03_read_pontos(self):
        self.negado('Read', {'file_path': str(self.skill.parent/'../hb-levantar-regras/SKILL.md')})

    def test_04_read_link(self):
        link = self.caso/'rascunho/apoio.md'
        link.symlink_to(self.skill)
        self.negado('Read', {'file_path': str(link)})

    def test_05_ferramenta_skill(self):
        entrada=json.loads((RAIZ/'testes/apoio/entradas_sessao_37.json').read_text())['Skill']
        self.negado('Skill', entrada)

    def test_06_ferramenta_skill_sem_namespace(self):
        self.negado('Skill', {'skill': 'hb-levantar-regras'})

    def test_07_expansao_direta(self):
        self.negado('', {}, evento='UserPromptExpansion', expansion_type='slash_command',
                    command_name='eiac-campo:hb-levantar-regras', command_args='', command_source='plugin',
                    prompt='/eiac-campo:hb-levantar-regras')

    def test_08_bash_leitura(self):
        self.negado('Bash', {'command': 'cat '+str(self.skill)})

    def test_09_grep_conteudo(self):
        self.negado('Grep', {'path': str(self.skill), 'pattern': '.', 'output_mode': 'content'})

    def test_10_habilidade_delegavel(self):
        self.assertEqual(self.hook('Skill', {'skill':'eiac-campo:hb-enquadrar'}).returncode, 0)

    def test_11_hooks_instalados_cobrem_rotas(self):
        hooks = json.loads((RAIZ/'eiac-nucleo/hooks/hooks.json').read_text())['hooks']
        self.assertIn('Skill', hooks['PreToolUse'][0]['matcher'].split('|'))
        self.assertIn('UserPromptExpansion', hooks)
    def test_12_nao_delegavel_n1(self):
        self.estado['nivel']='N1'; self.salvar()
        self.negado('Skill', {'skill':'eiac-campo:hb-levantar-regras'})

    def test_13_nao_delegavel_n3(self):
        self.estado['nivel']='N3'; self.salvar()
        self.negado('Skill', {'skill':'eiac-campo:hb-levantar-regras'})

if __name__ == '__main__': unittest.main(verbosity=2)
