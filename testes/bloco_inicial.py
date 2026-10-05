"""Bloco conduzido, aprovação como testemunho e limites determinísticos."""
import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'eiac-campo/scripts'))
sys.path.insert(0,str(ROOT/'eiac-nucleo/scripts'))
import iniciar as I
import aprovacao as A

class BlocoInicial(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base=pathlib.Path(self.tmp.name); self.cfg=self.base/'config.json'
        self.config=dict(responsavel='Pessoa Engenheira',base_casos=str(self.base/'casos'),
            base_expedientes=str(self.base/'expedientes'),workspace_tally='WORK',pasta_drive='ROOT',
            calendario_casos='CAL',navegador='google-chrome')
        I.configurar(self.cfg,self.config)
    def test_01_sem_aprovacao_recusa_e_registra(self):
        with self.assertRaises(ValueError):
            I.operar(self.cfg,'iniciar',{'id':'HAB','caso':'CASO'},None)
        ev=json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])
        self.assertEqual(ev['evento'],'TentativaNegada')
        self.assertEqual(ev['autor'],'Pessoa Engenheira')
        self.assertFalse((self.base/'expedientes/HAB').exists())
    def test_02_decisao_metodo_nao_tem_rota(self):
        for nome in ('apurar-nivel','decidir-prosseguimento','registrar-sessao','vincular-restricao'):
            with self.subTest(nome=nome),self.assertRaises(ValueError):
                I.operar(self.cfg,nome,{},None)
    def test_03_recibo_nao_aceita_entrada_alterada(self):
        p=self.base/'entrada.json'; p.write_text('{}')
        cmd=['python3','canais.py','definir','--entrada',str(p)]
        r=A.criar('definir-canais','Pessoa Engenheira','CASO','Aprovo os canais',
                  'canais conferidos',cmd,[p])
        p.write_text('{"alterado":true}')
        with self.assertRaises(ValueError): A.conferir(r,'definir-canais','Pessoa Engenheira','CASO',cmd)
    def test_04_perfil_nao_afrouxa_escopo(self):
        ferramentas=[{'nome':'mcp__claude_ai_Google_Drive__search_files','inputSchema':{'properties':{'query':{'type':'string'},'pageSize':{'type':'integer'},'pageToken':{'type':'string'},'excludeContentSnippets':{'type':'boolean'},'snippetVerbosity':{'type':'string'}}}},
            {'nome':'mcp__claude_ai_Google_Drive__global_search','inputSchema':{'properties':{'query':{'type':'string'}}}}]
        p=I.calibrar(ferramentas)
        self.assertEqual(len(p['regras']),1)
        self.assertEqual(p['recusadas'],['mcp__claude_ai_Google_Drive__global_search'])
        self.assertEqual(p['regras'][0]['argumentos'][0]['expressao'],"'{id}' in parents(?: and trashed = false)?")
        p['regras'][0]['argumentos'][0]['expressao']='.*'
        with self.assertRaises(ValueError): I.conferir_perfil(p,ferramentas)
    def test_05_config_reutilizada_sem_trocar_autor(self):
        self.assertEqual(I.configurar(self.cfg,self.config),self.config)
        with self.assertRaises(ValueError): I.configurar(self.cfg,dict(self.config,responsavel='Outra Pessoa'))
    def test_06_parametro_de_escopo_ausente_nao_gera_regra(self):
        p=I.calibrar([{'nome':'mcp__claude_ai_Google_Drive__search_files','inputSchema':{'properties':{'q':{'type':'string'}}}}])
        self.assertFalse(p['regras']); self.assertEqual(len(p['recusadas']),1)

    def test_10_nucleo_sem_instrumentos_ou_conectores(self):
        import re
        termos=re.compile(r'EMCIA|CTX-[0-9V]|CAT-01|MAN-01|HAB-0|HB-[0-9]|AG-[0-9]|\bF0\b|\bP[0-9][a-z]?\b|Tally|Google Drive|Google Calendar|habilitacao|triagem|prosseguimento')
        for p in (ROOT/'eiac-nucleo/scripts').glob('*.py'):
            self.assertIsNone(termos.search(p.read_text()),p.name)

    def test_11_config_ilegivel_recusa_sem_autor_inventado(self):
        import guarda_inicial as G
        self.cfg.write_text('{')
        ev={'tool_name':'Bash','tool_input':{'command':'python3 habilitacao.py iniciar --expediente /tmp/nao-criar --caso C'}}
        self.assertIsNotNone(G.conferir(ev,self.cfg))

    def test_07_saida_ausente_nao_libera(self):
        import saida_inicial as S
        r=S.conferir(self.base/'ausente',self.base/'caso-ausente')
        self.assertFalse(r['liberado'])
        self.assertTrue(all(not x['presente'] for x in r['itens']))

    def test_08_recusa_bootstrap_tambem_fica_na_trilha(self):
        import guarda_inicial as G
        ev={'tool_name':'Bash','tool_input':{'command':'python3 habilitacao.py iniciar --expediente /tmp/nao-criar --id H --caso C --responsavel "Pessoa Engenheira"'}}
        self.assertIn('aprovação',G.conferir(ev,self.cfg))
        self.assertEqual(json.loads(self.cfg.with_name('eventos.jsonl').read_text().splitlines()[-1])['evento'],'TentativaNegada')

    def test_09_aceitacao_revogavel_pela_operacao_aprovada(self):
        d={'habilitacao':'HAB','texto':'uso as minutas sem ratificação jurídica'}
        r=I.aprovar(self.cfg,'aceitar-minutas',d,d['texto'],'Aceitação inicial sintética')
        I.operar(self.cfg,'aceitar-minutas',d,r)
        self.assertIsNone(I.ler_config(self.cfg)['aceitacao_minutas']['revogada_em'])
        d={'habilitacao':'HAB'}
        r=I.aprovar(self.cfg,'revogar-minutas',d,'Revogo a aceitação','Revogação sintética')
        I.operar(self.cfg,'revogar-minutas',d,r)
        self.assertTrue(I.ler_config(self.cfg)['aceitacao_minutas']['revogada_em'])

from apoio.hook_real import CasoHook

class AutorizacaoCaso(CasoHook):
    def recibo(self,op,cmd,arquivos=()):
        r=A.criar(op,'Celso do Vale',self.estado['caso'],'Aprovo estes bytes e esta operação',
                  'Controle exclusivamente sintético',cmd,arquivos)
        arq=self.base/'aprovacao.json';arq.write_text(json.dumps(r));return arq
    def test_01_operacional_sem_aprovacao(self):
        self.negado('Bash',{'command':'python3 canais.py definir --entrada rascunho/canais.json'})
    def test_02_operacional_aprovado(self):
        entrada=self.caso/'rascunho/canais.json';entrada.write_text('{}')
        cmd=['python3','canais.py','definir','--entrada',str(entrada)]
        r=self.recibo('definir-canais',cmd,[entrada])
        import shlex
        out=self.hook('Bash',{'command':shlex.join(cmd+['--aprovacao',str(r)])})
        self.assertEqual(out.returncode,0,out.stderr)
        self.assertEqual(self.eventos()[-1]['evento'],'AprovacaoChatRegistrada')
    def test_03_aprovacao_nao_delega_metodo(self):
        cmd=['python3','avancar.py','--apurar-nivel','N1','--autor','Celso do Vale']
        r=self.recibo('apurar-nivel',cmd)
        import shlex
        self.negado('Bash',{'command':shlex.join(cmd+['--aprovacao',str(r)])})
    def test_04_apos_p2_selo_humano(self):
        self.estado['cumprimentos']['P2']={'cumprido':True};self.salvar()
        self.negado('Bash',{'command':'python3 selar.py --nota teste'})
        self.assertEqual(self.eventos()[-1]['operacao'],'selar-apos-P2')
    def test_05_operacional_fora_f0(self):
        self.estado['etapa_atual']='P2';self.salvar()
        self.negado('Bash',{'command':'python3 receber.py --arquivo rascunho/entrada/x --manifesto rascunho/entrada/y'})
    def test_06_caso_anterior_conserva_trava_humana(self):
        (self.caso/'registro/playbook.json').write_bytes((ROOT/'testes/apoio/playbook-0.4.19.json').read_bytes())
        self.negado('Bash',{'command':'python3 canais.py definir --entrada rascunho/canais.json'})
        self.assertIn('decisao humana',self.eventos()[-1]['motivo'])
    def test_07_aprovacao_sem_hash_da_entrada(self):
        entrada=self.caso/'rascunho/canais.json';entrada.write_text('{}')
        cmd=['python3','canais.py','definir','--entrada',str(entrada)];r=self.recibo('definir-canais',cmd)
        import shlex
        self.negado('Bash',{'command':shlex.join(cmd+['--aprovacao',str(r)])})
    def test_08_comando_composto_recusado(self):
        entrada=self.caso/'rascunho/canais.json';entrada.write_text('{}')
        cmd=['python3','canais.py','definir','--entrada',str(entrada)];r=self.recibo('definir-canais',cmd,[entrada])
        import shlex
        self.negado('Bash',{'command':shlex.join(cmd+['--aprovacao',str(r)])+'; echo alteracao'})

if __name__=='__main__': unittest.main(verbosity=2)
