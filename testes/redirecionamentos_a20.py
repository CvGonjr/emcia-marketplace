#!/usr/bin/env python3
"""A20: alvos de redirecionamento e descritores, não o caractere >."""
import unittest
from apoio.hook_real import CasoHook

class Redirecionamentos(CasoHook):
    def test_01_stderr_protegido(self):
        self.negado('Bash', {'command':'cat rascunho/x 2>registro/erro.txt'})
    def test_02_append_protegido(self):
        self.negado('Bash', {'command':'cat rascunho/x >> caso/x.md'})
    def test_03_caminho_com_espaco(self):
        self.negado('Bash', {'command':'printf x > "'+str(self.caso/'registro/meu estado.json')+'"'})
    def test_04_stderr_dev_null(self):
        self.assertEqual(self.hook('Bash', {'command':'cat registro/estado.json 2>/dev/null'}).returncode,0)
    def test_05_stdout_dev_null(self):
        self.assertEqual(self.hook('Bash', {'command':'cat caso/x.md >/dev/null'}).returncode,0)
    def test_06_fontes_stderr_dev_null(self):
        self.assertEqual(self.hook('Bash', {'command':'ls fontes/ 2>/dev/null'}).returncode,0)
    def test_07_duplicacao_descritor(self):
        self.assertEqual(self.hook('Bash', {'command':'cat contexto/regras/x.yaml 2>&1'}).returncode,0)
    def test_08_rascunho_redirecionado(self):
        self.assertEqual(self.hook('Bash', {'command':'cat fontes/x > rascunho/copia.txt 2>/dev/null'}).returncode,0)
    def test_09_stdout_e_stderr_protegidos(self):
        self.negado('Bash', {'command':'cat rascunho/x &>registro/erro.txt'})
    def test_10_fora_do_caso(self):
        self.assertEqual(self.hook('Bash', {'command':'cat registro/estado.json > '+str(self.base/'copia.txt')}).returncode,0)
    def test_11_maior_entre_aspas_e_texto(self):
        self.assertEqual(self.hook('Bash', {'command':"printf '%s' '>' caso/x.md"}).returncode,0)
    def test_12_caractere_escapado_e_texto(self):
        self.assertEqual(self.hook('Bash', {'command':'echo \\> registro/x'}).returncode,0)

if __name__ == '__main__': unittest.main(verbosity=2)
