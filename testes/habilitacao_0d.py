"""Passagem 0d: negativas primeiro, sobre componentes reais e dados sintéticos."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from apoio.habilitacao_0d import criar, H, RAIZ
from apoio.hook_real import CasoHook

IMPORTADOR=RAIZ/'eiac-campo/scripts/importar_habilitacao.py'


class Importacao(CasoHook):
    def setUp(self):
        super().setUp()
        self.exp=criar(self.base/'expediente',self.estado['caso'],'Celso do Vale')

    def importar(self, *args):
        return subprocess.run([sys.executable,str(IMPORTADOR),'--expediente',str(self.exp),*args],
                              cwd=self.caso,text=True,capture_output=True)

    def alterar(self, fn):
        p=self.exp/'expediente.json'; s=json.loads(p.read_text()); fn(s); p.write_text(json.dumps(s))

    def recusa(self, trecho, *args):
        antes=len(self.eventos()); r=self.importar(*args)
        self.assertNotEqual(r.returncode,0,r.stdout)
        self.assertIn(trecho,r.stderr)
        self.assertEqual(len(self.eventos()),antes+1)
        self.assertEqual(self.eventos()[-1]['evento'],'TentativaNegada')
        self.assertEqual(self.eventos()[-1]['autor'],'Celso do Vale')
        return r

    def test_01_sem_formalizacao(self):
        self.alterar(lambda s:s['documentos']['HAB-01'][-1].update(assinatura=None))
        self.recusa('formalização')

    def test_02_sem_acessos(self):
        self.alterar(lambda s:s.update(acessos=None)); self.recusa('acessos')

    def test_03_caso_divergente(self):
        self.alterar(lambda s:s.update(caso_reservado='outro')); self.recusa('reservado')

    def test_04_responsavel_divergente(self):
        self.alterar(lambda s:s.update(responsavel='Outra Pessoa')); self.recusa('responsável')

    def test_05_nao_prosseguir(self):
        H.executar(self.exp,'nao-prosseguir',{'decisor':'Celso do Vale','motivo':'Controle negativo',
                                         'condicao_retomada':'Nova decisão necessária'})
        self.recusa('não prosseguir')

    def test_06_pdf_adulterado(self):
        s=json.loads((self.exp/'expediente.json').read_text())
        ref=s['documentos']['HAB-01'][-1]['assinatura']['arquivo']
        (self.exp/ref['caminho']).write_bytes(b'%PDF-1.7\nadulterado\n%%EOF')
        self.recusa('integridade')

    def test_07_sessao_do_agente(self):
        r=self.negado('Bash',{'command':f'python3 {IMPORTADOR} --expediente {self.exp}'})
        self.assertIn('Comando exato:',r.stderr)
        self.assertEqual(self.eventos()[-1]['operacao'],'importar-habilitacao')

    def test_08_segunda_importacao(self):
        r=self.importar(); self.assertEqual(r.returncode,0,r.stderr)
        self.recusa('importação anterior')

    def test_09_autor_agente(self):
        self.recusa('autor','--autor','AG-01')

    def test_10_etapa_encerrada(self):
        self.estado['cumprimentos']['F0']={'cumprido':True}; self.salvar()
        self.recusa('etapa encerrada')

    def test_11_matriz_adulterada(self):
        self.alterar(lambda s:s['acessos']['itens'][0].update(item='Outra fonte'))
        self.recusa('matriz')

    def test_20_importa_apenas_artefatos_autorizados(self):
        r=self.importar(); self.assertEqual(r.returncode,0,r.stderr)
        reg=json.loads((self.caso/'registro/habilitacao.json').read_text())
        v=reg['vigente']; self.assertEqual(v['desfecho'],'prosseguir')
        self.assertEqual(len(v['arquivos']),7)
        self.assertEqual(self.eventos()[-1]['evento'],'HabilitacaoImportada')
        self.assertFalse((self.caso/'caso/00-habilitacao.md').exists())
        draft=self.caso/'rascunho/00-habilitacao.md'
        self.assertTrue(all(x.startswith('- [') for x in draft.read_text().splitlines()))
        r=self.rodar('validar.py','--arquivo','caso/00-habilitacao.md')
        self.assertEqual(r.returncode,0,r.stderr)
        import hashlib
        for ref in v['arquivos'].values():
            self.assertEqual(hashlib.sha256((self.caso/ref['caminho']).read_bytes()).hexdigest(),ref['sha256'])

    def test_21_reimportacao_decidida_preserva_historico(self):
        r=self.importar(); self.assertEqual(r.returncode,0,r.stderr)
        antigo=json.loads((self.caso/'registro/habilitacao.json').read_text())['vigente']
        p=self.base/'decisao.json'; p.write_text(json.dumps(dict(decisor='Celso do Vale',
            motivo='Nova conferência sintética',data='2026-10-02',importacao_anterior=antigo['id'])))
        r=self.importar('--decisao-reimportacao',str(p)); self.assertEqual(r.returncode,0,r.stderr)
        reg=json.loads((self.caso/'registro/habilitacao.json').read_text())
        self.assertEqual(reg['historico'],[antigo])
        self.assertNotEqual(reg['vigente']['id'],antigo['id'])
        self.assertTrue(all((self.caso/r['caminho']).exists() for r in antigo['arquivos'].values()))


if __name__=='__main__': unittest.main(verbosity=2)
