"""Conferência determinística de retornos MCP sintéticos, sem conta remota."""
import copy
import hashlib
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'eiac-campo/scripts'))
import iniciar as I


class Conferencia(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name); self.cfg = self.base/'config.json'
        I.configurar(self.cfg, dict(responsavel='Pessoa Engenheira', base_casos=str(self.base/'casos'),
            base_expedientes=str(self.base/'expedientes'), workspace_tally='WORK', pasta_drive='ROOT',
            calendario_casos='CAL', navegador='google-chrome'))
        inv = json.loads((ROOT/'testes/apoio/inventario-mcp-real.json').read_text())
        self.op('perfil', ferramentas=inv, perfil=I.calibrar(inv)); self.op('iniciar', id='HAB')
        d = self.chamada('create_new_form', title='Sintético', workspaceId='WORK')
        self.op('mcp', **{k:v for k,v in d.items() if k not in ('habilitacao','caso')})
        I.registrar_retorno(self.cfg, d, {'ids':{'formulario_id':'FORM'}})
        self.raw = json.loads((ROOT/'testes/apoio/tally-load-form.json').read_text())

    def op(self, nome, literal='Aprovo estes bytes', **extra):
        d = dict(habilitacao='HAB', caso='CASO', **extra)
        r = I.aprovar(self.cfg, nome, d, literal, 'Conferência sintética')
        return I.operar(self.cfg, nome, d, r)

    def chamada(self, tool, **args):
        return dict(habilitacao='HAB', caso='CASO', ferramenta='mcp__tally__'+tool, argumentos=args)

    def ler(self, raw=None):
        d = self.chamada('load_form', formId='FORM')
        self.op('mcp', ferramenta=d['ferramenta'], argumentos=d['argumentos'])
        I.registrar_retorno(self.cfg, d, {'resposta':self.raw if raw is None else raw})

    def comparar(self, modelo='habilitacao'):
        self.ler()
        return self.op('conferir-formulario', formulario_id='FORM', modelo=modelo)

    def publicar(self):
        return self.op('mcp', ferramenta='mcp__tally__publish_form', argumentos={'formId':'FORM'})

    def negada(self, acao, trecho):
        with self.assertRaisesRegex(ValueError, trecho): acao()
        ev = json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])
        self.assertEqual(ev['evento'], 'TentativaNegada')

    def test_01_texto_diferente_impede_publicacao_e_lista(self):
        self.raw['data']['blocks'][0]['payload']['html'] += ' diferente'
        r = self.comparar(); self.assertTrue(any('texto' in d for d in r['diferencas']))
        self.negada(self.publicar, 'texto')

    def test_02_ordem_trocada(self):
        b = self.raw['data']['blocks']; b[:4] = b[2:4]+b[:2]
        r = self.comparar(); self.assertTrue(any('ordem' in d for d in r['diferencas']))
        self.negada(self.publicar, 'ordem')

    def test_03_campo_oculto_ausente(self):
        self.raw['data']['blocks'].pop(); self.raw['data']['blocksCount'] -= 1
        r = self.comparar(); self.assertTrue(any('campo oculto caso' in d for d in r['diferencas']))
        self.negada(self.publicar, 'campo oculto caso')

    def test_04_tipo_diferente(self):
        self.raw['data']['blocks'][1]['type'] = 'INPUT_EMAIL'
        r = self.comparar(); self.assertTrue(any('tipo' in d for d in r['diferencas']))
        self.negada(self.publicar, 'tipo')

    def test_05_formulario_alheio(self):
        self.negada(lambda:self.op('mcp', ferramenta='mcp__tally__load_form', argumentos={'formId':'ALHEIO'}), 'escopo')

    def test_06_ferramenta_fora_do_perfil(self):
        self.negada(lambda:self.op('mcp', ferramenta='mcp__tally__list_blocks', argumentos={'formId':'FORM'}), 'não declarada')

    def test_07_sem_leitura_nao_compara(self):
        self.negada(lambda:self.op('conferir-formulario', formulario_id='FORM', modelo='habilitacao'), 'load_form')

    def test_08_formato_desconhecido_nao_aproxima(self):
        self.raw = {'data':{'formId':'FORM','workspaceId':'WORK','blocks':[{'texto':'Sem esquema'}]}}
        r = self.comparar(); self.assertTrue(r['diferencas'])
        self.negada(self.publicar, 'formato')

    def test_09_retorno_com_id_alheio(self):
        self.raw['data']['formId'] = 'ALHEIO'
        r = self.comparar(); self.assertTrue(any('formId' in d for d in r['diferencas']))
        self.negada(self.publicar, 'formId')

    def test_10_relatorio_adulterado(self):
        r = self.comparar(); pathlib.Path(r['arquivo']).write_text('adulterado')
        self.negada(self.publicar, 'relatório')

    def confirmar(self, r, literal='conferido'):
        return self.op('confirmar-formulario', literal=literal, formulario_id='FORM', relatorio_sha256=r['sha256'])

    def test_11_confirmacao_exige_literal_conferido(self):
        r=self.comparar()
        self.negada(lambda:self.confirmar(r,'aprovo'), 'conferido')

    def test_12_divergencia_nao_pode_ser_confirmada(self):
        self.raw['data']['blocks'][0]['payload']['html']+=' diferente'
        r=self.comparar()
        self.negada(lambda:self.confirmar(r), 'texto')

    def test_13_leitura_nova_invalida_confirmacao(self):
        r=self.comparar();self.confirmar(r)
        self.raw['data']['blocks'][0]['payload']['html']+=' diferente'; self.ler()
        self.negada(self.publicar,'nova leitura')
        r=self.op('conferir-formulario',formulario_id='FORM',modelo='habilitacao')
        self.negada(self.publicar,'texto')

    def test_14_hash_de_outro_relatorio_nao_confirma(self):
        r=self.comparar();r['sha256']='0'*64
        self.negada(lambda:self.confirmar(r),'hash')

    def test_15_manual_exige_pdf(self):
        p=self.base/'nao-pdf.txt';p.write_text('Somente texto')
        self.negada(lambda:self.op('caminho-manual',literal='conferido',passo='preparar-formulario',
            formulario_id='FORM',evidencia=str(p),decisao='executar manualmente'),'PDF')

    def test_16_manual_nao_sobrepoe_divergencia(self):
        self.raw['data']['blocks'][0]['payload']['html']+=' diferente';self.comparar()
        p=self.base/'manual.pdf';p.write_bytes(b'%PDF-1.4\nSintetico\n%%EOF\n')
        self.negada(lambda:self.op('caminho-manual',literal='conferido',passo='preparar-formulario',
            formulario_id='FORM',evidencia=str(p),decisao='executar manualmente'),'texto')

    def test_17_confirmacao_sem_aprovacao(self):
        r=self.comparar()
        d=dict(habilitacao='HAB',caso='CASO',formulario_id='FORM',relatorio_sha256=r['sha256'])
        self.negada(lambda:I.operar(self.cfg,'confirmar-formulario',d,None),'aprovação')

    def test_18_workspace_do_retorno_alheio(self):
        self.raw['data']['workspaceId']='OUTRO'
        self.comparar();self.negada(self.publicar,'workspaceId')

    def test_19_campo_oculto_duplicado(self):
        self.raw['data']['blocks'][-1]['payload']['hiddenFields']*=2
        self.comparar();self.negada(self.publicar,'duplicado')

    def test_20_identico_relatorio_md_hash_e_aguarda_humano(self):
        r = self.comparar(); self.assertEqual(r['diferencas'], [])
        p = pathlib.Path(r['arquivo']); self.assertEqual(p.suffix, '.md')
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), r['sha256'])
        self.assertIn('HAB-0a-1', p.read_text())
        self.negada(self.publicar, 'conferido')

    def test_21_conferido_libera_sem_arquivo_externo(self):
        r=self.comparar();self.confirmar(r)
        self.assertTrue(self.publicar()['autorizada'])
        evs=[json.loads(l) for l in self.cfg.with_name('eventos.jsonl').read_text().splitlines()]
        e=[e for e in evs if e['evento']=='ConferenciaExternaRegistrada'][-1]
        self.assertEqual(e['evidencia_sha256'],r['sha256'])
        self.assertEqual(e['testemunho']['literal'],'conferido')

    def test_22_manual_pdf_continua_alternativa(self):
        p=self.base/'manual.pdf';p.write_bytes(b'%PDF-1.4\nSintetico\n%%EOF\n')
        self.op('caminho-manual',literal='conferido',passo='preparar-formulario',
                formulario_id='FORM',evidencia=str(p),decisao='executar manualmente')
        self.assertTrue(self.publicar()['autorizada'])

    def test_23_envelope_mcp_structured_content(self):
        self.raw={'structuredContent':self.raw,'content':[{'type':'text','text':'Retorno sintético'}]}
        r=self.comparar();self.assertEqual(r['diferencas'],[])
        self.confirmar(r);self.assertTrue(self.publicar()['autorizada'])

    def test_24_ciclo_sem_textos_fixos_nao_aproxima(self):
        r=self.comparar('ciclo')
        self.assertTrue(any('não fixa texto' in d for d in r['diferencas']))
        self.negada(self.publicar,'não fixa texto')

    def test_25_triagem_identica_e_alternativa_alterada(self):
        self.raw=json.loads((ROOT/'testes/apoio/tally-load-form-triagem.json').read_text())
        r=self.comparar('triagem');self.assertEqual(r['diferencas'],[])
        self.confirmar(r);self.assertTrue(self.publicar()['autorizada'])
        self.raw['data']['blocks'][1]['payload']['text']+=' reformulado'
        self.comparar('triagem');self.negada(self.publicar,'alternativas')

    def test_26_retorno_adulterado(self):
        self.comparar()
        p=self.cfg.with_name('mcp-retornos.json');d=json.loads(p.read_text())
        d[-1]['resultado']['resposta']['data']['blocks'][0]['payload']['html']='Alterado'
        p.write_text(json.dumps(d))
        self.negada(self.publicar,'retorno MCP adulterado')

    def test_27_hook_recusa_depois_de_leitura_nova(self):
        import guarda_inicial as G
        I.retomar(self.cfg,'HAB','CASO')
        r=self.comparar();self.confirmar(r);self.publicar()
        self.ler()
        ev=dict(tool_name='mcp__tally__publish_form',tool_input={'formId':'FORM'})
        self.assertIn('nova leitura',G.conferir(ev,self.cfg))
        self.assertEqual(json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])['evento'],'TentativaNegada')


class ContratoGenerico(unittest.TestCase):
    def test_01_estado_mais_recente_invalida_anterior(self):
        import escopo_externo as S
        regra=dict(precondicao_registrada=dict(evento='EstadoConfirmado',argumento='id',campo_evento='objeto',
            ultimo=True,valores={'situacao':'confirmada'},campo_motivo='motivos'))
        bom=dict(evento='EstadoConfirmado',objeto='ID',autor='Pessoa Engenheira',contexto='CASO',situacao='confirmada')
        ruim=dict(bom,situacao='divergente',motivos=['diferença sintética'])
        with self.assertRaisesRegex(ValueError,'diferença sintética'):
            S.conferir_eventos({},regra,'mcp__sintetico__efeito',{'id':'ID'},[bom,ruim],'Pessoa Engenheira','CASO')
        S.conferir_eventos({},regra,'mcp__sintetico__efeito',{'id':'ID'},[ruim,bom],'Pessoa Engenheira','CASO')

    def test_02_outro_contexto_nao_altera_precondicao(self):
        import escopo_externo as S
        regra=dict(precondicao_registrada=dict(evento='EstadoConfirmado',argumento='id',campo_evento='objeto',
            ultimo=True,valores={'situacao':'confirmada'}))
        bom=dict(evento='EstadoConfirmado',objeto='ID',autor='Pessoa Engenheira',contexto='CASO',situacao='confirmada')
        S.conferir_eventos({},regra,'mcp__sintetico__efeito',{'id':'ID'},[bom,dict(bom,contexto='OUTRO',situacao='divergente')],'Pessoa Engenheira','CASO')


if __name__ == '__main__': unittest.main(verbosity=2)
