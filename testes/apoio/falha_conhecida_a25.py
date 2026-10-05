"""Executa A25 intacto e aceita somente a divergência expressa da decisão 045."""
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import manual_a25 as M
ESPERADO=['ato humano selar-apos-P2 ausente das seções 3.3 e 3.4']

def divergencias():
    return M.conferir(M.ler_tabela(M.MANUAL.read_text()),__import__('json').loads(M.PLAYBOOK.read_text()),M.comandos_de_etapa(),M.atos_transversais(M.MANUAL.read_text()))

def main():
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(M))
    conhecida=(r.testsRun==5 and not r.errors and len(r.failures)==1
        and r.failures[0][0].id().endswith('.test_01_manual_confere_com_playbook') and divergencias()==ESPERADO)
    if conhecida:print('FALHA CONHECIDA A25 — decisão 045; quatro negativas passaram; teste canônico inalterado')
    raise SystemExit(0 if conhecida else 1)

if __name__=='__main__':main()
