"""A12: origem na guarda identifica agente, independentemente do nome."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
GUARDA = RAIZ / 'eiac-nucleo/scripts/guarda.py'
# Contrato explícito para exercitar a versão anterior antes da implementação.
REGRAS = [
    {'id': 'decidir-prosseguimento', 'script': 'prosseguimento.py', 'condicao': {'tipo': 'sempre'}},
    {'id': 'decidir-autonomia', 'script': 'governanca.py', 'condicao': {'tipo': 'arquivo', 'argumento': '--arquivo', 'diretorio': 'rascunho', 'campo': 'estado', 'operador': 'igual', 'valor': 'decidido', 'preparacao': ['rascunho', 'proposto']}},
    {'id': 'validar-operacional', 'script': 'operacional.py', 'condicao': {'tipo': 'arquivo', 'argumento': '--arquivo', 'diretorio': 'rascunho', 'campo': 'estado', 'operador': 'igual', 'valor': 'validado', 'preparacao': ['proposta']}},
    {'id': 'decidir-recalibragem', 'script': 'calibragem.py', 'condicao': {'tipo': 'arquivo', 'argumento': '--arquivo', 'diretorio': 'rascunho', 'campo': 'decisao', 'operador': 'preenchido'}},
    *[{'id': flag, 'script': 'avancar.py', 'argumento': '--'+flag, 'condicao': {'tipo': 'sempre'}} for flag in ['apurar-nivel', 'registrar-sessao', 'registrar-campo', 'registrar-recorrencia', 'satisfazer-inegociavel']],
    {'id': 'satisfazer-inegociavel-campo', 'script': 'inegociaveis.py', 'argumento': '--satisfazer', 'condicao': {'tipo': 'sempre'}},
    {'id': 'preparar-controle', 'script': 'preparar-caso.sh', 'condicao': {'tipo': 'sempre'}},
    {'id': 'encerrar-camada-humana', 'script': 'avancar.py', 'argumento': '--encerrar', 'condicao': {'tipo': 'camada', 'camadas': ['EX3', 'EX4']}},
]


class DecisaoA12(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.caso = pathlib.Path(self.tmp.name)
        shutil.copytree(RAIZ / 'eiac-campo/template-caso/registro', self.caso / 'registro')
        (self.caso / 'rascunho').mkdir()
        self.estado = self.caso / 'registro/estado.json'
        self.pbpath = self.caso / 'registro/playbook.json'
        self.configurar(lambda pb: pb.update(decisoes_humanas=REGRAS))
        self.posicionar('P6')
        self.rascunho('AUT-001.yaml', 'estado: decidido\n')
        self.rascunho('OP-001.yaml', 'estado: validado\n')
        self.rascunho('CAL-001-C01.yaml', 'decisao: recalibrar\n')

    def configurar(self, fn):
        pb = json.loads(self.pbpath.read_text())
        fn(pb)
        self.pbpath.write_text(json.dumps(pb))

    def posicionar(self, etapa, nivel='N2'):
        pb = json.loads(self.pbpath.read_text())
        st = json.loads(self.estado.read_text())
        st.update(responsavel='Celso do Vale', etapa_atual=etapa, nivel=nivel)
        st['cumprimentos'] = {}
        for et in pb['etapas']:
            if et['id'] == etapa:
                st.update(camada_atual=et['camada'][nivel], modalidade_atual=et['modalidade'])
                break
            st['cumprimentos'][et['id']] = {'cumprido': True}
        self.estado.write_text(json.dumps(st))

    def rascunho(self, nome, texto):
        (self.caso / 'rascunho' / nome).write_text(texto)

    def executar(self, comando, ferramenta='Bash'):
        return subprocess.run(['python3', str(GUARDA)], cwd=self.caso,
                              input=json.dumps({'tool_name': ferramenta,
                                                'tool_input': {'command': comando}}),
                              text=True, capture_output=True)

    def comando(self, script, argumentos):
        plugin = 'eiac-nucleo' if script == 'avancar.py' else 'eiac-campo'
        return f'python3 "{RAIZ / plugin / "scripts" / script}" {argumentos}'

    def recusa(self, comando, operacao):
        antes = self.estado.read_bytes()
        r = self.executar(comando)
        self.assertEqual(r.returncode, 2, r.stdout+r.stderr)
        self.assertIn('engenheiro', r.stderr)
        self.assertIn('proprio terminal', r.stderr)
        self.assertIn(comando, r.stderr)
        self.assertEqual(self.estado.read_bytes(), antes)
        ev = json.loads((self.caso / 'registro/eventos.jsonl').read_text().splitlines()[-1])
        self.assertEqual(ev['evento'], 'TentativaNegada')
        self.assertEqual(ev['autor'], 'Celso do Vale')
        self.assertEqual(ev['comando'], comando)
        self.assertEqual(ev['operacao'], operacao)

    def permitido(self, comando):
        r = self.executar(comando)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_00_governanca_decidido_nome_humano(self):
        self.recusa(self.comando('governanca.py', '--arquivo registro/governanca/autonomia/AUT-001.yaml --ator "Celso do Vale"'), 'decidir-autonomia')

    def test_01_operacional_validado_nome_humano(self):
        self.recusa(self.comando('operacional.py', '--arquivo registro/operacional/OP-001.yaml --ator "Celso do Vale"'), 'validar-operacional')

    def test_02_calibragem_com_decisao(self):
        self.recusa(self.comando('calibragem.py', '--arquivo registro/calibragem/CAL-001-C01.yaml --ciclo --ator "Celso do Vale"'), 'decidir-recalibragem')

    def test_03_apurar_nivel(self):
        self.recusa(self.comando('avancar.py', '--apurar-nivel N3 --autor "Celso do Vale" --eixos "DAD 4, GOV 3, CRI 8"'), 'apurar-nivel')

    def test_04_registrar_sessao(self):
        self.recusa(self.comando('avancar.py', '--registrar-sessao P6 --autor "Celso do Vale" --participantes "X"'), 'registrar-sessao')

    def test_05_registrar_campo(self):
        self.recusa(self.comando('avancar.py', '--registrar-campo P5 --campo classificacao_tecnologica --valor agente --autor "Celso do Vale"'), 'registrar-campo')

    def test_06_registrar_recorrencia(self):
        self.recusa(self.comando('avancar.py', '--registrar-recorrencia P10 --cadencia mensal --responsavel "Celso do Vale" --autor "Celso do Vale"'), 'registrar-recorrencia')

    def test_07_satisfazer_inegociavel(self):
        self.recusa(self.comando('avancar.py', '--satisfazer-inegociavel 2 --evidencia AUT-001 --autor "Celso do Vale"'), 'satisfazer-inegociavel')

    def test_08_encerrar_ex3(self):
        self.recusa(self.comando('avancar.py', '--encerrar P6 --autor "Celso do Vale"'), 'encerrar-camada-humana')

    def test_09_encerrar_ex4(self):
        self.posicionar('P7')
        self.recusa(self.comando('avancar.py', '--encerrar P7 --autor "Celso do Vale"'), 'encerrar-camada-humana')

    def test_10_camada_da_etapa_alvo_nao_cache(self):
        self.posicionar('P1')
        self.recusa(self.comando('avancar.py', '--encerrar P6 --autor "Celso do Vale"'), 'encerrar-camada-humana')

    def test_11_opcao_com_igual(self):
        self.recusa(self.comando('avancar.py', '--registrar-sessao=P6 --autor="Celso do Vale"'), 'registrar-sessao')

    def test_12_cadeia_de_comandos(self):
        c = 'pwd && '+self.comando('avancar.py', '--apurar-nivel N2 --autor "Celso do Vale"')
        self.recusa(c, 'apurar-nivel')

    def test_13_shell_interno(self):
        c = "bash -c '"+self.comando('avancar.py', '--registrar-sessao P6 --autor "Celso do Vale"')+"'"
        self.recusa(c, 'registrar-sessao')

    def test_14_rascunho_ausente(self):
        c = self.comando('governanca.py', '--arquivo registro/governanca/autonomia/AUT-999.yaml --ator "Celso do Vale"')
        self.recusa(c, 'decidir-autonomia')

    def test_15_rascunho_ilegivel(self):
        self.rascunho('AUT-001.yaml', 'estado: [\n')
        self.recusa(self.comando('governanca.py', '--arquivo registro/governanca/autonomia/AUT-001.yaml --ator "Celso do Vale"'), 'decidir-autonomia')

    def test_16_regra_ausente_nao_desativa_guarda(self):
        self.configurar(lambda pb: pb.pop('decisoes_humanas'))
        r = self.executar('pwd')
        self.assertEqual(r.returncode, 2)
        self.assertIn('decisoes_humanas', r.stderr)

    def test_17_condicao_desconhecida(self):
        self.configurar(lambda pb: pb['decisoes_humanas'][0]['condicao'].update(tipo='preferencia'))
        r = self.executar('pwd')
        self.assertEqual(r.returncode, 2)
        self.assertIn('condicao', r.stderr)

    def test_18_mudar_rascunho_na_mesma_chamada(self):
        self.rascunho('AUT-001.yaml', 'estado: proposto\n')
        c = "sed -i s/proposto/decidido/ rascunho/AUT-001.yaml && "+self.comando('governanca.py', '--arquivo registro/governanca/autonomia/AUT-001.yaml --ator "Celso do Vale"')
        self.recusa(c, 'decidir-autonomia')

    def test_19_contrato_alternativo_sem_vocabulario_do_metodo(self):
        self.configurar(lambda pb: pb['decisoes_humanas'].append({'id': 'outra-decisao', 'script': 'outro.py', 'argumento': '--confirmar', 'condicao': {'tipo': 'sempre'}}))
        self.recusa('python3 outro.py --confirmar --autor "Celso do Vale"', 'outra-decisao')

    def test_20_governanca_proposto(self):
        self.rascunho('AUT-001.yaml', 'estado: proposto\n')
        self.permitido(self.comando('governanca.py', '--arquivo registro/governanca/autonomia/AUT-001.yaml --ator AG-01'))

    def test_21_operacional_proposta(self):
        self.rascunho('OP-001.yaml', 'estado: proposta\n')
        self.permitido(self.comando('operacional.py', '--arquivo registro/operacional/OP-001.yaml --ator AG-01'))

    def test_22_calibragem_recomendacao_sem_decisao(self):
        self.rascunho('CAL-001-C01.yaml', 'recomendacao_agente: recalibrar\n')
        self.permitido(self.comando('calibragem.py', '--arquivo registro/calibragem/CAL-001-C01.yaml --ciclo --ator AG-01'))

    def test_23_leitura(self):
        self.permitido('cat registro/estado.json')
        self.permitido('python3 '+str(RAIZ/'eiac-nucleo/scripts/estado.py'))
        self.permitido('cat '+str(RAIZ/'eiac-campo/scripts/governanca.py'))

    def test_24_validador_curador_emissao(self):
        for comando in ['python3 validar.py --arquivo caso/regra.yaml', 'python3 curar.py --tipo regra --arquivo contexto/regras/RN-001.yaml', 'python3 entregaveis.py --renderizar E3 --autor "Celso do Vale" --emitir']:
            self.permitido(comando)

    def test_25_encerrar_ex2(self):
        self.posicionar('P1')
        self.permitido(self.comando('avancar.py', '--encerrar P1 --autor "Celso do Vale"'))

    def test_26_mesma_etapa_ex2_em_n1(self):
        self.posicionar('P3a', 'N1')
        self.permitido(self.comando('avancar.py', '--encerrar P3a --autor "Celso do Vale"'))

    def test_27_texto_nao_e_execucao(self):
        self.permitido('echo "python3 avancar.py --apurar-nivel N3"')

    def test_28_terminal_direto_apura_nivel(self):
        r = subprocess.run(['python3', str(RAIZ/'eiac-nucleo/scripts/avancar.py'), '--apurar-nivel', 'N3', '--autor', 'Celso do Vale', '--eixos', 'DAD 4, GOV 3, CRI 8'], cwd=self.caso, text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(self.estado.read_text())['nivel'], 'N3')

    def test_29_template_declara_lista(self):
        pb = json.loads((RAIZ/'eiac-campo/template-caso/registro/playbook.json').read_text())
        declaradas = {r['id']: r for r in pb.get('decisoes_humanas', [])}
        for regra in REGRAS:
            self.assertEqual(declaradas.get(regra['id']), regra)
        self.assertEqual(set(declaradas) - {r['id'] for r in REGRAS}, {"revisar-piloto", "definir-rotina", "importar-habilitacao", "definir-canais", "receber-material", "entregar-material", "registrar-listagem", "vincular-restricao"})

    def test_30_satisfacao_por_wrapper_campo(self):
        self.recusa('python3 inegociaveis.py --verificar 2 --arquivo registro/governanca/autonomia/AUT-001.yaml --satisfazer --autor "Celso do Vale"', 'satisfazer-inegociavel-campo')

    def test_31_auxiliar_automatico_exige_terminal(self):
        self.recusa('bash .projectdocs/demos/preparar-caso.sh controle P7', 'preparar-controle')

    def test_32_verificar_inegociavel_sem_satisfazer(self):
        self.permitido('python3 inegociaveis.py --verificar 2 --arquivo registro/governanca/autonomia/AUT-001.yaml')

    def test_33_encerramento_composto_contexto_incerto(self):
        self.posicionar('P3a', 'N1')
        self.recusa('cd /tmp/outro-caso && '+self.comando('avancar.py', '--encerrar P3a --autor "Celso do Vale"'), 'encerrar-camada-humana')

    def test_34_opcao_interpretador_com_valor(self):
        c = self.comando('avancar.py', '--registrar-sessao P6 --autor "Celso do Vale"').replace('python3 ', 'python3 -W ignore ', 1)
        self.recusa(c, 'registrar-sessao')

    def test_35_execucao_por_modulo(self):
        self.recusa('python3 -m avancar --registrar-sessao P6 --autor "Celso do Vale"', 'registrar-sessao')

    def test_36_codigo_inline_invoca_script_de_decisao(self):
        self.recusa("python3 -c 'import avancar; avancar.main()' --registrar-sessao P6 --autor \"Celso do Vale\"", 'registrar-sessao')


if __name__ == '__main__':
    unittest.main(verbosity=2)
