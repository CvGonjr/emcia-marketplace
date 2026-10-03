"""Caso sintético e entradas no contrato dos hooks do Claude Code."""
import json, os, pathlib, shutil, subprocess, sys, tempfile, unittest
RAIZ = pathlib.Path(__file__).resolve().parents[2]
NUCLEO = RAIZ / 'eiac-nucleo/scripts'

class CasoHook(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name)
        self.caso = self.base / 'controle'
        shutil.copytree(RAIZ / 'eiac-campo/template-caso', self.caso)
        self.estado = json.loads((self.caso/'registro/estado.json').read_text())
        self.estado.update(responsavel='Celso do Vale', nivel='N2')
        self.salvar()
        (self.caso/'rascunho').mkdir(exist_ok=True)
        self.env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.caso))

    def salvar(self):
        (self.caso/'registro/estado.json').write_text(json.dumps(self.estado))

    def rodar(self, script, *args, entrada=None, cwd=None):
        return subprocess.run([sys.executable, str(NUCLEO/script), *args],
                              cwd=cwd or self.caso, env=self.env, input=entrada,
                              text=True, capture_output=True)

    def hook(self, ferramenta, entrada, cwd=None, evento='PreToolUse', **campos):
        entrada = dict(entrada)
        if ferramenta == 'Edit':
            entrada.setdefault('old_string', 'P10'); entrada.setdefault('new_string', 'F0')
        elif ferramenta == 'Write':
            entrada.setdefault('content', 'controle sintético')
        payload = dict(session_id='sessao-controle', transcript_path=str(self.base/'sessao.jsonl'),
                       cwd=str(cwd or self.caso), permission_mode='default', hook_event_name=evento,
                       tool_name=ferramenta, tool_input=entrada, tool_use_id='toolu_controle')
        payload.update(campos)
        return self.rodar('guarda.py', entrada=json.dumps(payload), cwd=cwd)

    def negado(self, ferramenta, entrada, **kwargs):
        antes = len(self.eventos())
        r = self.hook(ferramenta, entrada, **kwargs)
        self.assertEqual(r.returncode, 2, r.stderr)
        evs = self.eventos()
        self.assertEqual(len(evs), antes+1)
        self.assertEqual(evs[-1]['evento'], 'TentativaNegada')
        self.assertEqual(evs[-1]['autor'], 'Celso do Vale')
        return r

    def eventos(self):
        p = self.caso/'registro/eventos.jsonl'
        return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []

    def preparar_habilidade(self):
        self.estado.update(etapa_atual='P3b', cumprimentos={
            'P2': {'cumprido': True}, 'P3a': {'cumprido': True},
            'P3b': {'sessao': {'autor': 'Celso do Vale', 'participantes': 'Marina Prado'}}})
        self.salvar()
        log = self.caso/'registro/eventos.jsonl'
        # Selo real permite que A18 continue exercitando G1, sem mascará-la por G7.
        log.write_text('')
        self.rodar('avancar.py','--registrar-sessao','P3b','--autor','Celso do Vale','--participantes','Marina Prado')
        ev=self.eventos()[-1]
        with log.open('a') as f:
            f.write(json.dumps(dict(evento='EtapaEncerrada',etapa='P2',autor='Celso do Vale',componente=ev['componente']))+'\n')
        for args in [('init','-q'),('config','user.name','Celso do Vale'),
                     ('config','user.email','sintetico@example.invalid'),('config','commit.gpgsign','false')]:
            subprocess.run(['git',*args],cwd=self.caso,check=True,capture_output=True)
        r=self.rodar('selar.py','--nota','Estado declarado da fixture')
        self.assertEqual(r.returncode,0,r.stderr)
        self.skill = self.base/'.claude/plugins/cache/emcia/eiac-campo/0.8.5/skills/hb-levantar-regras/SKILL.md'
        self.skill.parent.mkdir(parents=True)
        shutil.copyfile(RAIZ/'eiac-campo/skills/hb-levantar-regras/SKILL.md', self.skill)
