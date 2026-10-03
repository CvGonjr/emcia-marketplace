"""Decisão 042: confirmação no Git, negativas antes do controle positivo."""
import json, pathlib, subprocess, sys, unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.preparar import produto

class SeloP3b(CasoHook):
    def setUp(self):
        super().setUp()
        from apoio.habilitacao_0d import preparar
        self.git('init','-q'); self.git('config','user.name','Celso do Vale')
        self.git('config','user.email','sintetico@example.invalid')
        self.git('config','commit.gpgsign','false')
        self.git('config','core.hooksPath',str(self.caso/'.git/hooks'))
        preparar(self.caso)
        for et in ['F0','P1']:
            self.assertEqual(self.rodar('avancar.py','--encerrar',et,'--autor','Celso do Vale').returncode,0)

    def git(self,*args):
        r=subprocess.run(['git',*args],cwd=self.caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr)

    def selar(self):
        (self.caso/'rascunho/marcador').write_text(str(len(self.eventos())))
        return self.rodar('selar.py','--nota','Selo de controle P3b')

    def p3b(self):
        r=self.rodar('avancar.py','--encerrar','P2','--autor','Celso do Vale')
        self.assertEqual(r.returncode,0,r.stderr)
        self.rodar('avancar.py','--registrar-sessao','P3a','--autor','Celso do Vale','--participantes','Marina Prado')
        produto(self.caso,'P3a')
        r=self.rodar('avancar.py','--encerrar','P3a','--autor','Celso do Vale')
        self.assertEqual(r.returncode,0,r.stderr)
        r=self.rodar('avancar.py','--registrar-sessao','P3b','--autor','Celso do Vale','--participantes','Marina Prado')
        self.assertEqual(r.returncode,0,r.stderr)

    def recusar_ambos(self,trecho):
        r=self.negado('Skill',{'skill':'eiac-campo:hb-levantar-regras'})
        self.assertIn(trecho,r.stderr)
        antes=len(self.eventos())
        r=self.rodar('avancar.py','--encerrar','P3b','--autor','Celso do Vale')
        self.assertEqual(r.returncode,1,r.stdout); self.assertIn(trecho,r.stderr)
        self.assertEqual(len(self.eventos()),antes+1)
        self.assertEqual(self.eventos()[-1]['evento'],'TentativaNegada')

    def test_01_commit_falho_posterior(self):
        self.p3b()
        hook=self.caso/'.git/hooks/pre-commit';hook.write_text('#!/bin/sh\nexit 1\n');hook.chmod(0o755)
        self.assertNotEqual(self.selar().returncode,0)
        self.recusar_ambos('confirmado')

    def test_02_confirmado_apenas_anterior(self):
        self.assertEqual(self.selar().returncode,0)
        self.p3b(); self.recusar_ambos('confirmado')

    def test_03_git_inacessivel(self):
        self.p3b();self.assertEqual(self.selar().returncode,0)
        (self.caso/'.git').rename(self.caso/'.git-inacessivel')
        self.recusar_ambos('Git')

    def test_04_commit_comum_nao_confirma(self):
        self.p3b()
        hook=self.caso/'.git/hooks/pre-commit';hook.write_text('#!/bin/sh\nexit 1\n');hook.chmod(0o755)
        self.assertNotEqual(self.selar().returncode,0);hook.unlink()
        self.git('add','-A'); self.git('commit','-qm','Commit comum')
        self.recusar_ambos('confirmado')

    def test_20_posterior_confirmado(self):
        self.p3b();self.assertEqual(self.selar().returncode,0)
        # O selo libera G7; a habilidade humana continua não delegável.
        r=self.negado('Skill',{'skill':'eiac-campo:hb-levantar-regras'})
        self.assertIn('nao e delegavel',r.stderr)
        r=self.rodar('avancar.py','--encerrar','P3b','--autor','Celso do Vale')
        self.assertEqual(r.returncode,0,r.stderr)

if __name__=='__main__': unittest.main(verbosity=2)
