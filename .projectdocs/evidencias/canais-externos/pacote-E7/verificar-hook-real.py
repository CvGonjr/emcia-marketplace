"""Teste real opcional: MCP local sintético, sem acesso a ferramentas de clientes.

Uso: python3 verificar-hook-real.py <diretório-de-evidência>
Requer Claude Code autenticado. Não integra a suíte sem rede.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RAIZ = next(p for p in pathlib.Path(__file__).resolve().parents if (p/'testes/negativos.sh').exists())
SERVIDOR = '''import json,sys,pathlib
for line in sys.stdin:
 req=json.loads(line);method=req.get('method');ident=req.get('id')
 if ident is None:continue
 if method=='initialize':result={'protocolVersion':'2024-11-05','capabilities':{'tools':{}},'serverInfo':{'name':'controle-local','version':'1'}}
 elif method=='tools/list':result={'tools':[{'name':'ping','description':'Controle local sem efeitos externos','inputSchema':{'type':'object','properties':{},'additionalProperties':False}}]}
 elif method=='tools/call':
  pathlib.Path(sys.argv[1]).write_text('chamada real local\\n');result={'content':[{'type':'text','text':'CONTROLE-MCP-LOCAL'}]}
 else:result={}
 print(json.dumps({'jsonrpc':'2.0','id':ident,'result':result}),flush=True)
'''
RECORDER = '''import json,sys,pathlib
ev=json.load(sys.stdin)
with pathlib.Path(sys.argv[1]).open('a') as f:f.write(json.dumps({'hook_event_name':ev.get('hook_event_name'),'tool_name':ev.get('tool_name'),'tool_input':ev.get('tool_input')})+'\\n')
'''


def executar(destino, plugin=False):
    with tempfile.TemporaryDirectory(prefix='emcia-hook-mcp-') as tmp:
        root = pathlib.Path(tmp)
        caso = root/'caso'; shutil.copytree(RAIZ/'eiac-campo/template-caso', caso)
        p = caso/'registro/estado.json'; st = json.loads(p.read_text()); st['responsavel'] = 'Celso do Vale'; p.write_text(json.dumps(st))
        server = root/'server.py'; server.write_text(SERVIDOR)
        recorder = root/'recorder.py'; recorder.write_text(RECORDER)
        called = root/'called.txt'; log = root/'hooks.jsonl'
        config = root/'mcp.json'; settings = root/'settings.json'
        config.write_text(json.dumps({'mcpServers': {'controle': {'command': sys.executable, 'args': [str(server), str(called)]}}}))
        settings.write_text(json.dumps({'hooks': {'PreToolUse': [{'matcher': 'mcp__controle__.*', 'hooks': [{'type': 'command', 'command': f'{sys.executable} {recorder} {log}'}]}]}}))
        cmd = ['claude', '-p', 'Chame uma vez mcp__controle__ping. Se o hook negar, não repita. Não use outra ferramenta.', '--tools', '', '--allowedTools', 'mcp__controle__ping', '--strict-mcp-config', '--mcp-config', str(config), '--setting-sources', '', '--no-session-persistence']
        cmd += ['--plugin-dir', str(RAIZ/'eiac-nucleo')] if plugin else ['--settings', str(settings)]
        r = subprocess.run(cmd, cwd=caso, capture_output=True, text=True, timeout=55)
        result = dict(codigo=r.returncode, chamada_mcp_efetuada=called.exists())
        if plugin:
            p = caso/'registro/eventos.jsonl'
            result['eventos'] = [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
            assert not called.exists() and any(e['evento'] == 'TentativaNegada' for e in result['eventos']), result
        else:
            result['hooks'] = [json.loads(x) for x in log.read_text().splitlines()] if log.exists() else []
            assert called.exists() and result['hooks'], result
        (destino/('plugin-reproduzido.json' if plugin else 'hook-reproduzido.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    destino = pathlib.Path(sys.argv[1]); destino.mkdir(parents=True, exist_ok=True)
    executar(destino); executar(destino, plugin=True)
