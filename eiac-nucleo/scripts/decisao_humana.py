"""Condições declaradas de operações humanas recebidas pela guarda.

Não executa shell. Reconhece invocações e lê o candidato correspondente;
nome informado nunca transforma uma chamada da sessão em decisão humana.
"""
import pathlib
import re
import shlex

import estrutura as X
import playbook as P


def validar(regras):
    if not isinstance(regras, list) or not regras:
        return 'playbook sem decisoes_humanas validas'
    ids = set()
    for regra in regras:
        if not isinstance(regra, dict):
            return 'decisoes_humanas: operacao precisa ser objeto'
        if not isinstance(regra.get('id'), str) or not regra['id'] or regra['id'] in ids:
            return 'decisoes_humanas: id ausente ou duplicado'
        ids.add(regra['id'])
        script = regra.get('script')
        if not isinstance(script, str) or not script or pathlib.Path(script).name != script:
            return 'decisoes_humanas: script precisa ser nome de arquivo'
        arg = regra.get('argumento')
        if arg is not None and (not isinstance(arg, str) or not arg.startswith('--')):
            return 'decisoes_humanas: argumento invalido'
        c = regra.get('condicao')
        if not isinstance(c, dict) or c.get('tipo') not in ('sempre', 'arquivo', 'camada', 'apos_etapa'):
            return 'decisoes_humanas: condicao desconhecida ou ausente'
        if c['tipo'] == 'apos_etapa' and not isinstance(c.get('etapa'),str):
            return 'decisoes_humanas: etapa de referência ausente'
        if c['tipo'] == 'camada' and (not arg or not isinstance(c.get('camadas'), list) or not c['camadas']
                                     or any(not isinstance(v, str) for v in c['camadas'])):
            return 'decisoes_humanas: condicao de camada invalida'
        if c['tipo'] == 'arquivo':
            if any(not isinstance(c.get(k), str) or not c[k] for k in ('argumento', 'diretorio', 'campo')):
                return 'decisoes_humanas: condicao de arquivo incompleta'
            diretorio = pathlib.Path(c['diretorio'])
            if diretorio.is_absolute() or '..' in diretorio.parts:
                return 'decisoes_humanas: diretorio precisa ser relativo ao caso'
            if 'preparacao' in c and (not isinstance(c['preparacao'], list) or not c['preparacao']):
                return 'decisoes_humanas: preparacao precisa declarar valores'
            if c.get('operador') not in ('igual', 'preenchido') or (c['operador'] == 'igual' and 'valor' not in c):
                return 'decisoes_humanas: operador de arquivo invalido'
    return None


def _argumento(tokens, nome):
    valores = []
    for i, token in enumerate(tokens):
        if token == nome:
            valores.append(tokens[i+1] if i+1 < len(tokens) and not tokens[i+1].startswith('--') else '')
        elif token.startswith(nome+'='):
            valores.append(token[len(nome)+1:])
    return valores


def _segmentos(comando):
    lexer = shlex.shlex(comando.replace('\n', ';'), posix=True, punctuation_chars=';&|()<>')
    lexer.whitespace_split = True
    tokens = list(lexer)
    segmentos, atual = [], []
    for token in tokens:
        if token and all(c in ';&|()<>' for c in token):
            if atual:
                segmentos.append(atual)
                atual = []
        else:
            atual.append(token)
    if atual:
        segmentos.append(atual)
    return segmentos


def _invocacoes(tokens, profundidade=0):
    if profundidade > 8:
        raise ValueError('shell aninhado demais para inspecao')
    if not tokens:
        return []
    tokens = list(tokens)
    while tokens and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', tokens[0]):
        tokens.pop(0)
    if not tokens:
        return []
    exe = pathlib.Path(tokens[0]).name
    if exe in ('command', 'exec', 'env'):
        rest = tokens[1:]
        while rest and (rest[0].startswith('-') or re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', rest[0])):
            rest.pop(0)
        return _invocacoes(rest, profundidade+1)
    if exe in ('bash', 'sh', 'zsh'):
        for i, token in enumerate(tokens[1:], 1):
            if token.startswith('-') and 'c' in token and i+1 < len(tokens):
                internos = _segmentos(tokens[i+1])
                return [(script, args, composto or len(internos) != 1)
                        for segmento in internos
                        for script, args, composto in _invocacoes(segmento, profundidade+1)]
        return [(pathlib.Path(tokens[1]).name, tokens[2:], False)] if len(tokens) > 1 else []
    if re.fullmatch(r'python(?:\d+(?:\.\d+)*)?', exe):
        rest = tokens[1:]
        while rest and rest[0].startswith('-'):
            if rest[0] == '-c':
                return [('__codigo_inline__', rest[1:], False)]
            if rest[0] == '-m':
                return [(rest[1].rsplit('.', 1)[-1]+'.py', rest[2:], False)] if len(rest) > 1 else []
            if rest[0] in ('-W', '-X'):
                rest = rest[2:]
            else:
                rest.pop(0)
        return [(pathlib.Path(rest[0]).name, rest[1:], False)] if rest else []
    return [(exe, tokens[1:], False)]


def avaliar(pb, st, comando):
    """Devolve (operação, motivo) quando requer terminal humano; senão None.

    Comandos compostos que invocam operação condicionada por arquivo são
    recusados: um passo anterior pode mudar o rascunho após a inspeção.
    """
    try:
        segmentos = _segmentos(comando)
        invocacoes = [item for segmento in segmentos for item in _invocacoes(segmento)]
    except ValueError:
        return 'comando-nao-inspecionavel', 'Comando shell ilegivel; nao e possivel conferir decisoes humanas.'
    for script, args, composto in invocacoes:
        for regra in pb['decisoes_humanas']:
            if script == '__codigo_inline__':
                fonte = args[0] if args else ''
                nome = regra['script']
                if nome in fonte or re.search(r'\b'+re.escape(pathlib.Path(nome).stem)+r'\b', fonte):
                    candidatas = [r for r in pb['decisoes_humanas'] if r['script'] == nome]
                    selecionada = next((r for r in candidatas if r.get('argumento')
                                        and _argumento(args[1:], r['argumento'])), regra)
                    return selecionada['id'], 'Codigo inline invoca componente de decisao sem condicao inspecionavel.'
            if script != regra['script']:
                continue
            argumento = regra.get('argumento')
            valores = _argumento(args, argumento) if argumento else []
            if argumento and not valores:
                continue
            c = regra['condicao']
            if c['tipo'] == 'apos_etapa':
                if st.get('cumprimentos',{}).get(c['etapa'],{}).get('cumprido'):
                    return regra['id'], 'Operação após etapa encerrada reservada ao terminal humano.'
            if c['tipo'] == 'sempre':
                return regra['id'], 'Operacao declarada como decisao humana.'
            if c['tipo'] == 'camada':
                if len(segmentos) != 1 or composto:
                    return regra['id'], 'Comando composto pode mudar o contexto de resolucao da camada.'
                if len(valores) != 1 or not valores[0] or P.etapa(pb, valores[0]) is None:
                    return regra['id'], 'Etapa alvo ausente, ambigua ou desconhecida.'
                camada = P.camada(pb, valores[0], st.get('nivel'))
                if camada in c['camadas']:
                    return regra['id'], f"Etapa {valores[0]}, camada {camada}, nivel {st.get('nivel')}: encerramento humano."
            if c['tipo'] == 'arquivo':
                if len(segmentos) != 1 or composto:
                    return regra['id'], 'Comando composto pode alterar o candidato antes da decisao.'
                arquivos = _argumento(args, c['argumento'])
                if len(arquivos) != 1 or not arquivos[0]:
                    return regra['id'], 'Caminho do candidato ausente ou ambiguo.'
                candidato = pathlib.Path(c['diretorio']) / pathlib.Path(arquivos[0]).name
                if not candidato.resolve().is_relative_to(pathlib.Path.cwd().resolve()):
                    return regra['id'], 'Candidato fora do caso.'
                try:
                    dados = X.carregar_yaml(candidato.read_text(encoding='utf-8'))
                    if not isinstance(dados, dict):
                        raise ValueError('candidato precisa ser objeto')
                except (OSError, UnicodeError, ValueError, X.yaml.YAMLError if X.yaml else X.ErroYaml) as exc:
                    return regra['id'], f'Candidato {candidato} nao inspecionavel: {exc}'
                valor = dados.get(c['campo'])
                if 'preparacao' in c and valor not in c['preparacao']:
                    return regra['id'], f"Candidato {candidato}: campo {c['campo']} nao caracteriza preparacao permitida."
                if (c['operador'] == 'igual' and valor == c['valor']) or (c['operador'] == 'preenchido' and bool(valor)):
                    return regra['id'], f"Candidato {candidato}: campo {c['campo']} caracteriza decisao humana."
    return None
