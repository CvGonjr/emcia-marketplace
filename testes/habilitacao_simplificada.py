"""Contrato administrativo simplificado; negativas antes do percurso sintético."""
import copy
import csv
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'eiac-campo/scripts'))
import iniciar as I
import habilitacao as H

class Simplificada(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name); self.cfg = self.base/'config.json'
        I.configurar(self.cfg, dict(responsavel='Pessoa Engenheira', base_casos=str(self.base/'casos'),
            base_expedientes=str(self.base/'expedientes'), workspace_tally='WORK', pasta_drive='ROOT',
            calendario_casos='CAL', navegador='google-chrome'))
        self.exp = self.base/'expedientes/HAB'; self.entrada = self.base/'entrada'; self.entrada.mkdir()
        self.csv = self.entrada/'exportacao.csv'
        c = I.ler_config(self.cfg); c['entrada_dir'] = str(self.entrada); I.escrever(self.cfg, c)

    def op(self, nome, literal='conferido', **extra):
        d = dict(habilitacao='HAB', caso='CASO', **extra)
        return I.operar(self.cfg, nome, d, I.aprovar(self.cfg, nome, d, literal, 'Controle sintético'))

    def permanente(self):
        inv = json.loads((ROOT/'testes/apoio/inventario-mcp-real.json').read_text())
        self.op('perfil', ferramentas=inv, perfil=I.calibrar(inv)); self.op('iniciar', id='HAB')
        d = dict(habilitacao='HAB', caso='CASO', ferramenta='mcp__tally__create_new_form',
                 argumentos={'title':'Sintético', 'workspaceId':'WORK'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        I.registrar_retorno(self.cfg, d, {'ids':{'formulario_id':'FORM'}})
        d.update(ferramenta='mcp__tally__load_form', argumentos={'formId':'FORM'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        raw = json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())
        I.registrar_retorno(self.cfg, d, {'resposta':raw})
        rel = self.op('conferir-formulario', formulario_id='FORM', modelo='habilitacao')
        self.op('confirmar-formulario', formulario_id='FORM', relatorio_sha256=rel['sha256'])
        self.op('formulario-permanente', formulario_id='FORM', modelo='habilitacao')
        return rel

    def test_01_permanente_sem_conferencia_recusa(self):
        import formularios_permanentes as F
        with self.assertRaisesRegex(ValueError, 'conferido'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_02_contrato_anterior_recusa(self):
        import formularios_permanentes as F
        self.permanente()
        original = F.modelo
        arquivo = self.base/'novo-contrato.json'
        modelo = json.loads(original('habilitacao').read_text()); modelo['perguntas'][0]['pergunta'] += ' alterado'
        arquivo.write_text(json.dumps(modelo))
        with patch.object(F, 'modelo', return_value=arquivo), self.assertRaisesRegex(ValueError, 'contrato mudou'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_03_relatorio_adulterado_recusa(self):
        import formularios_permanentes as F
        rel = self.permanente(); pathlib.Path(rel['arquivo']).write_text('alteração')
        with self.assertRaisesRegex(ValueError, 'adulterado'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def test_04_reutiliza_sem_nova_aprovacao(self):
        import formularios_permanentes as F
        self.permanente(); antes = self.cfg.with_name('eventos.jsonl').read_bytes()
        reg = F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')
        self.assertEqual(reg['formId'], 'FORM')
        self.assertEqual(F.link(reg, 'CASO-2'), 'https://tally.so/r/FORM?caso=CASO-2')
        self.assertEqual(antes, self.cfg.with_name('eventos.jsonl').read_bytes())

    def test_05_nova_leitura_invalida_permanente(self):
        import formularios_permanentes as F
        self.permanente()
        d = dict(habilitacao='HAB', caso='CASO', ferramenta='mcp__tally__load_form', argumentos={'formId':'FORM'})
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        I.registrar_retorno(self.cfg, d, {'resposta':json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())})
        with self.assertRaisesRegex(ValueError, 'conferência'):
            F.validar(self.cfg, I.ler_config(self.cfg), 'habilitacao')

    def exportacao(self, casos=('OUTRO-A', 'CASO', 'OUTRO-B')):
        with self.csv.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['Submission ID', 'caso', 'Respondente', 'HAB-0a-1'])
            w.writeheader()
            for i,caso in enumerate(casos):
                w.writerow({'Submission ID':'SUB-'+str(i), 'caso':caso, 'Respondente':'Pessoa Cliente',
                            'HAB-0a-1': 'SEGREDO-'+caso})
        s = json.loads((self.exp/'expediente.json').read_text())
        s['tratamento'] = {'escopo':'administrativo', 'condicoes':'Condições sintéticas'}; H.salvar(self.exp, s)

    def coletar(self, **extra):
        return H.executar(self.exp, 'receber-exportacao', dict(config_emcia=str(self.cfg), arquivo=str(self.csv),
            id='S1', **extra))

    def test_10_exportacao_sem_linha_do_caso(self):
        self.permanente(); self.exportacao(('OUTRO-A',))
        with self.assertRaisesRegex(ValueError, 'nenhuma submissão'): self.coletar()
        self.assertFalse((self.exp/'arquivos').exists())
        self.assertNotIn('SEGREDO-OUTRO-A', (self.exp/'expediente.json').read_text())

    def test_11_duas_submissoes_nao_escolhe(self):
        self.permanente(); self.exportacao(('CASO', 'CASO'))
        with self.assertRaisesRegex(ValueError, 'qual submissão'): self.coletar()
        self.assertFalse((self.exp/'arquivos').exists())

    def test_12_permanente_ausente_bloqueia_coleta(self):
        H.iniciar(self.exp, 'HAB', 'Pessoa Engenheira', 'CASO')
        self.exportacao()
        with self.assertRaisesRegex(ValueError, 'conferido'): self.coletar()

    def test_13_filtra_antes_de_persistir(self):
        self.permanente(); self.exportacao(); original = self.csv.read_bytes(); self.coletar()
        s = json.loads((self.exp/'expediente.json').read_text()); fonte = s['fontes']['S1']
        self.assertEqual(fonte['canal'], 'tally-exportacao')
        self.assertEqual(fonte['original_sha256'], H.digest(original))
        self.assertNotEqual(fonte['arquivo']['sha256'], H.digest(original))
        for arq in self.exp.rglob('*'):
            if arq.is_file():
                self.assertNotIn(b'SEGREDO-OUTRO', arq.read_bytes(), str(arq))
        self.assertIn(b'SEGREDO-CASO', H.ler_arquivo(self.exp, fonte['arquivo']))

    def test_14_selecao_explicita_dentre_duas(self):
        self.permanente(); self.exportacao(('CASO', 'CASO', 'OUTRO-A')); self.coletar(submissao='SUB-1')
        fonte = json.loads((self.exp/'expediente.json').read_text())['fontes']['S1']
        self.assertEqual(fonte['submissao'], 'SUB-1')
        linhas = list(csv.DictReader(io.StringIO(H.ler_arquivo(self.exp, fonte['arquivo']).decode())))
        self.assertEqual(len(linhas), 1); self.assertEqual(linhas[0]['Submission ID'], 'SUB-1')

    def test_15_arquivo_fora_da_entrada_recusa(self):
        self.permanente(); self.exportacao()
        outro = self.base/'fora.csv'; outro.write_bytes(self.csv.read_bytes()); self.csv = outro
        with self.assertRaisesRegex(ValueError, 'entrada'): self.coletar()

    def test_20_mensagem_vazia_recusa(self):
        self.permanente(); self.exportacao(); self.coletar()
        with self.assertRaisesRegex(ValueError, 'texto'):
            H.executar(self.exp, 'receber-mensagem', dict(id='M1', respondente='Pessoa Cliente', texto='', pergunta='Limite?'))

    def test_21_mensagem_sem_novo_formulario_ou_pendencia(self):
        self.permanente(); self.exportacao(); self.coletar()
        H.executar(self.exp, 'receber-mensagem', dict(id='M1', respondente='Pessoa Cliente',
                   texto='O limite termina na entrega.', pergunta='Onde termina o processo?'))
        s = json.loads((self.exp/'expediente.json').read_text()); f = s['fontes']['M1']
        self.assertEqual(f['canal'], 'manual'); self.assertEqual(f['rodada'], 1)
        self.assertEqual(f['formulario'], 'FORM'); self.assertFalse(s['pendencias'])
        self.assertEqual(json.loads(H.ler_arquivo(self.exp, f['arquivo']))['texto'], 'O limite termina na entrega.')

    def test_30_tratamento_ausente_recusa(self):
        H.iniciar(self.exp, 'HAB', 'Pessoa Engenheira', 'CASO')
        with self.assertRaisesRegex(ValueError, 'condições administrativas'):
            H.executar(self.exp, 'tratamento-padrao', {'config_emcia':str(self.cfg)})

    def test_31_tratamento_padrao_com_hash_sem_aprovacao(self):
        H.iniciar(self.exp, 'HAB', 'Pessoa Engenheira', 'CASO')
        c = I.ler_config(self.cfg); c['tratamento_administrativo'] = dict(condicoes='Condições sintéticas', provedor='Provedor sintético')
        I.escrever(self.cfg, c)
        H.executar(self.exp, 'tratamento-padrao', {'config_emcia':str(self.cfg)})
        s = json.loads((self.exp/'expediente.json').read_text())
        self.assertEqual(s['tratamento']['texto_sha256'], H.digest('Condições sintéticas'.encode()))
        self.assertEqual(s['tratamento']['referencia'], str(self.cfg)+'#tratamento_administrativo')
        self.assertFalse(any(e['tipo']=='AprovacaoChatRegistrada' for e in s['eventos']))

    def documentos(self):
        self.permanente(); self.exportacao(); self.coletar()
        c = I.ler_config(self.cfg)
        c['aceitacao_minutas'] = dict(texto='uso as minutas sem ratificação jurídica', responsavel=c['responsavel'], data=H.agora(), revogada_em=None)
        I.escrever(self.cfg, c)
        campos = {k:{'valor':'Conteúdo sintético '+k, 'fonte':'S1'} for f in H.TEMPLATES.values()
                  for k in H.TOKEN.findall((ROOT/'eiac-campo/reference/metodo'/f).read_text())}
        campos['signatario']['valor'] = 'Pessoa Cliente'
        H.executar(self.exp, 'consolidar', {'campos':campos})
        self.geracao = dict(templates=str(ROOT/'eiac-campo/reference/metodo'), navegador='google-chrome', config_emcia=str(self.cfg))
        self.pdf_patch = patch.object(H, 'pdf_bytes', side_effect=lambda md,b:b'%PDF-1.7\n'+md.encode()+b'\n%%EOF')
        self.pdf_patch.start(); self.addCleanup(self.pdf_patch.stop)
        H.executar(self.exp, 'preparar-documentos', self.geracao)
        self.plano_docs = dict(geracao=self.geracao, qualificacao_0a=True, conteudo_conferido=True,
            liberacao=dict(ferramenta='Painel escolhido', operador='Pessoa Cliente',
            signatarios=[dict(nome='Pessoa Cliente', papel='organizacao', competencia='Representante'),
                        dict(nome='Pessoa Engenheira', papel='emcia', competencia='Responsável')]))

    def aprovar_docs(self):
        import habilitacao_lotes as L
        r = L.criar_aprovacao(self.exp, 'aprovar-documentos', self.plano_docs, 'ok')
        return H.executar(self.exp, 'aprovar-documentos', {'plano':self.plano_docs, 'testemunho':r})

    def test_40_revisao_conjunta_sem_aprovacao_recusa(self):
        self.documentos()
        with self.assertRaisesRegex(ValueError, 'aprovação'):
            H.executar(self.exp, 'aprovar-documentos', {'plano':self.plano_docs})
        self.assertFalse(json.loads((self.exp/'expediente.json').read_text())['documentos'])

    def test_41_ok_cobre_tres_documentos_com_mesmos_pdfs(self):
        self.documentos(); antes = json.loads((self.exp/'expediente.json').read_text())['rascunhos_documentos']
        self.aprovar_docs(); s = json.loads((self.exp/'expediente.json').read_text())
        for doc in H.CODIGOS_HAB:
            v = s['documentos'][doc][-1]
            self.assertEqual(v['pdf']['sha256'], antes[doc]['pdf']['sha256']); self.assertTrue(v['liberacao'])
        self.assertEqual(len([e for e in s['eventos'] if e['tipo']=='AprovacaoLoteRegistrada']), 1)
        self.assertTrue(any(e.get('operacao')=='revisar' for e in s['eventos']))

    def test_42_assinatura_sem_aprovacao_recusa(self):
        self.documentos(); self.aprovar_docs()
        with self.assertRaisesRegex(ValueError, 'aprovação'):
            H.executar(self.exp, 'aprovar-assinaturas', {'plano':{}})
        self.assertFalse(H.completa(json.loads((self.exp/'expediente.json').read_text())))

    def test_43_pdf_assinado_de_outro_documento_recusa(self):
        import habilitacao_lotes as L
        self.documentos(); self.aprovar_docs()
        for doc in H.CODIGOS_HAB: (self.entrada/(doc+'-assinado.pdf')).write_bytes(b'%PDF-1.7\nDocumento de outro cliente\n%%EOF')
        with patch.object(L, 'texto_pdf', side_effect=lambda p:pathlib.Path(p).read_bytes().decode()), self.assertRaisesRegex(ValueError, 'corresponde'):
            H.executar(self.exp, 'preparar-assinaturas', {'config_emcia':str(self.cfg)})

    def test_44_aprovacao_de_documento_adulterado_recusa(self):
        import habilitacao_lotes as L
        self.documentos(); r = L.criar_aprovacao(self.exp, 'aprovar-documentos', self.plano_docs, 'ok')
        s = json.loads((self.exp/'expediente.json').read_text())
        (self.exp/s['rascunhos_documentos']['HAB-01']['pdf']['caminho']).write_bytes(b'alterado')
        with self.assertRaises(ValueError): H.executar(self.exp, 'aprovar-documentos', {'plano':self.plano_docs, 'testemunho':r})

if __name__ == '__main__': unittest.main(verbosity=2)
