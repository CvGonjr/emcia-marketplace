"""Percurso completo exclusivamente sintético, pelos comandos reais."""
import hashlib
import json
import subprocess
import sys
import unittest
from apoio.hook_real import CasoHook, RAIZ
from apoio.habilitacao_0d import criar
from apoio.canais import dados


class Percurso(CasoHook):
    def chamar(self, script, *args):
        r = subprocess.run([sys.executable, str(RAIZ/script), *args], cwd=self.caso,
                           text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r

    def git(self, *args):
        r = subprocess.run(['git', *args], cwd=self.caso, text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_20_habilitacao_canais_triagem_documento_emissao_entrega(self):
        exp = criar(self.base/'expediente', self.estado['caso'], 'Celso do Vale')
        self.git('init', '-q'); self.git('config', 'user.name', 'Celso do Vale')
        self.git('config', 'user.email', 'sintetico@example.invalid')
        canais = self.caso/'rascunho/canais.json'; canais.write_text(json.dumps(dados(self.caso)))
        self.chamar('eiac-campo/scripts/importar_habilitacao.py', '--expediente', str(exp), '--canais', str(canais))
        reg = json.loads((self.caso/'registro/canais.json').read_text())
        h = next(c for c in reg['canais'] if c['finalidade'] == 'habilitacao')
        self.assertEqual(h['ids']['formulario_id'], 'FORM-SINTETICO')
        self.assertEqual(h['origem']['habilitacao'], 'HAB-CONTROLE')
        self.chamar('eiac-nucleo/scripts/validar.py', '--arquivo', 'caso/00-habilitacao.md')
        self.chamar('eiac-nucleo/scripts/selar.py', '--nota', 'habilitação sintética com canais')
        self.assertEqual(self.hook('Skill', {'skill': 'eiac-campo:hb-enquadrar'}).returncode, 0)
        entrada = self.caso/'rascunho/entrada'; entrada.mkdir()
        triagem = entrada/'triagem.json'
        modelo = json.loads((RAIZ/'eiac-campo/reference/formularios/triagem.json').read_text())
        triagem.write_text(json.dumps(dict(formulario_id='SINTETICO-triagem-formulario_id',
            submissao_id='SUB-TRIAGEM', campos_ocultos={'caso': self.estado['caso']},
            perguntas=modelo['perguntas'], respostas=[1,1,3,1,1,1,2,2,2])))
        manifesto = entrada/'coleta.json'
        manifesto.write_text(json.dumps(dict(ferramenta='tally', objeto_id='SUB-TRIAGEM',
            conteiner_id='SINTETICO-triagem-formulario_id', submissao_id='SUB-TRIAGEM',
            campos_ocultos={'caso': self.estado['caso']}, modificado_em='2026-10-02T10:00:00Z',
            coletado_em='2026-10-02T11:00:00Z')))
        ref = json.loads(self.chamar('eiac-campo/scripts/receber.py', '--arquivo', str(triagem), '--manifesto', str(manifesto)).stdout)
        (self.caso/'rascunho/triagem.md').write_text(f"- [D · fonte: {ref['id']} · Celso do Vale · 2026-10-02] Respostas declaradas preservadas.\n")
        self.chamar('eiac-nucleo/scripts/validar.py', '--arquivo', 'caso/triagem.md')
        self.chamar('eiac-nucleo/scripts/avancar.py', '--apurar-nivel', 'N2', '--eixos', 'DAD 5, GOV 3, CRI 6', '--autor', 'Celso do Vale')
        for etapa in ['F0', 'P1']:
            self.chamar('eiac-nucleo/scripts/avancar.py', '--encerrar', etapa, '--autor', 'Celso do Vale')
        documento = entrada/'documento.txt'; documento.write_text('Documento sintético do processo.')
        manifesto.write_text(json.dumps(dict(ferramenta='drive', objeto_id='OBJ-DOC',
            conteiner_id='SINTETICO-documentos-pasta_id', modificado_em='2026-10-02T10:00:00Z',
            coletado_em='2026-10-02T11:00:00Z')))
        self.chamar('eiac-campo/scripts/receber.py', '--arquivo', str(documento), '--manifesto', str(manifesto))
        self.chamar('eiac-campo/scripts/entregaveis.py', '--renderizar', 'E1', '--emitir', '--autor', 'Celso do Vale')
        st = json.loads((self.caso/'registro/estado.json').read_text()); emitido = st['entregaveis_emitidos']['E1']
        self.assertEqual(hashlib.sha256((self.caso/'caso/entregaveis/E1.md').read_bytes()).hexdigest(), emitido['sha256'])
        entrega = self.caso/'rascunho/entrega.json'
        entrega.write_text(json.dumps(dict(entregavel='E1', versao=emitido['versao'], sha256=emitido['sha256'],
            arquivo_id='DEST-E1', destino_id='SINTETICO-entregas-pasta_id', destinatario='Pessoa Cliente', data='2026-10-02')))
        self.chamar('eiac-campo/scripts/entregar.py', '--entrada', str(entrega))
        eventos = [e['evento'] for e in self.eventos()]
        for tipo in ['HabilitacaoImportada', 'CanaisDefinidos', 'MaterialRecebido', 'EntregavelEmitido', 'EntregavelEntregue']:
            self.assertIn(tipo, eventos)
        self.assertEqual(eventos.count('MaterialRecebido'), 2)


if __name__ == '__main__': unittest.main(verbosity=2)
