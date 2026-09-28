#!/usr/bin/env python3
"""A21: recusa é evento; não vira asserção com procedência inventada."""
import unittest
from apoio.hook_real import CasoHook, RAIZ

class Recusa(CasoHook):
    def test_01_instrucoes_nao_pedem_marca_invalida(self):
        texto=(RAIZ/'eiac-campo/skills/hb-levantar-regras/SKILL.md').read_text()
        self.assertNotIn('[tentativa-negada',texto)
        self.assertIn('TentativaNegada',texto)
        self.assertNotIn('registre em `caso/log-tentativas.md`',texto)
    def test_02_recusa_e_evento_sem_assercoes(self):
        self.preparar_habilidade()
        antes=set((self.caso/'caso').rglob('*'))
        self.negado('Read', {'file_path':str(self.skill)})
        self.assertEqual(set((self.caso/'caso').rglob('*')),antes)

if __name__ == '__main__': unittest.main(verbosity=2)
