#!/usr/bin/env python3
"""A17: estado exibe o último selo confirmado pelo histórico do caso."""
import json, subprocess, unittest
from apoio.hook_real import CasoHook

class Selo(CasoHook):
    def git(self,*args):
        r=subprocess.run(['git',*args],cwd=self.caso,text=True,capture_output=True)
        self.assertEqual(r.returncode,0,r.stderr)
        return r.stdout.strip()
    def setUp(self):
        super().setUp()
        self.git('init','-q')
        self.git('config','user.name','Celso do Vale')
        self.git('config','user.email','controle@exemplo.com')
        self.git('add','-A'); self.git('commit','-qm','abertura')
    def estado_exibido(self):
        r=self.rodar('estado.py'); self.assertEqual(r.returncode,0,r.stderr)
        return json.loads(r.stdout)
    def aplicar(self,nota):
        (self.caso/'rascunho/marcador.txt').write_text(nota)
        r=self.rodar('selar.py','--nota',nota)
        self.assertEqual(r.returncode,0,r.stderr)
        return self.git('rev-parse','HEAD')
    def test_01_sem_selo_nao_inventa_hash(self):
        self.assertIsNone(self.estado_exibido().get('selo'))
    def test_02_commit_recusado_nao_exibe_selo_aplicado(self):
        hook=self.caso/'.git/hooks/pre-commit'; hook.write_text('#!/bin/sh\nexit 1\n'); hook.chmod(0o755)
        (self.caso/'rascunho/x').write_text('controle')
        self.assertNotEqual(self.rodar('selar.py','--nota','recusado').returncode,0)
        self.assertIsNone(self.estado_exibido().get('selo'))
    def test_03_hash_data_nota(self):
        sha=self.aplicar('primeiro selo')
        selo=self.estado_exibido()['selo']
        self.assertEqual(selo['hash'],sha); self.assertEqual(selo['nota'],'primeiro selo')
        self.assertEqual(selo['data'],self.eventos()[-1]['data'])
        self.assertEqual(self.git('status','--porcelain'),'')
    def test_04_ultimo_selo(self):
        self.aplicar('primeiro'); sha=self.aplicar('segundo')
        self.assertEqual(self.estado_exibido()['selo']['hash'],sha)
        self.assertEqual(self.estado_exibido()['selo']['nota'],'segundo')
    def test_05_commit_posterior_nao_troca_hash(self):
        sha=self.aplicar('selo')
        (self.caso/'rascunho/extra').write_text('extra')
        self.git('add','-A'); self.git('commit','-qm','posterior')
        self.assertEqual(self.estado_exibido()['selo']['hash'],sha)
    def test_06_resumo_mostra_selo(self):
        sha=self.aplicar('selo de controle')
        r=self.rodar('estado.py','--resumo')
        self.assertIn(sha,r.stdout); self.assertIn('selo de controle',r.stdout)
    def test_07_tentativa_posterior_nao_apaga_selo(self):
        sha=self.aplicar('confirmado')
        hook=self.caso/'.git/hooks/pre-commit'; hook.write_text('#!/bin/sh\nexit 1\n'); hook.chmod(0o755)
        (self.caso/'rascunho/marcador.txt').write_text('alterado')
        self.assertNotEqual(self.rodar('selar.py','--nota','falhou').returncode,0)
        self.assertEqual(self.estado_exibido()['selo']['hash'],sha)

if __name__ == '__main__': unittest.main(verbosity=2)
