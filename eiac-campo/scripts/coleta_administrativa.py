"""Entrada local filtrada antes da escrita; nunca preserva o lote de outros casos."""
import csv
import io
import pathlib
import habilitacao as H


def entrada_local(arquivo, pasta):
    import aprovacao as A
    p = pathlib.Path(arquivo).expanduser().absolute(); base = pathlib.Path(pasta).expanduser().absolute()
    H.local_externo(base)
    H.exigir(p.is_relative_to(base), 'arquivo deve estar na pasta de entrada')
    A.hash_arquivo(p)  # Recusa symlinks, inclusive nos ancestrais.
    return p


def filtrar(raw, caso, coluna_id='Submission ID', submissao=None):
    try:
        leitor = csv.DictReader(io.StringIO(raw.decode('utf-8-sig'), newline=''), strict=True)
        cols = leitor.fieldnames
        H.exigir(cols and len(set(cols)) == len(cols) and 'caso' in cols and coluna_id in cols,
                 'CSV exige cabeçalho único, caso e coluna de submissão declarada')
        linhas = []
        for linha in leitor:
            # Antes de consultar qualquer outro campo ou emitir diagnóstico.
            if linha.get('caso') != caso: continue
            H.exigir(None not in linha and all(v is not None for v in linha.values()), 'linha do caso inválida')
            H.texto(linha[coluna_id]); linhas.append(linha)
        H.exigir(linhas, 'nenhuma submissão do caso; deposite a exportação correta e indique qual vale')
        if submissao is not None:
            linhas = [l for l in linhas if l[coluna_id] == submissao]
        H.exigir(len(linhas) == 1, 'indique qual submissão do caso vale; nenhuma escolha automática')
        out = io.StringIO(newline=''); w = csv.DictWriter(out, fieldnames=cols, lineterminator='\n')
        w.writeheader(); w.writerows(linhas)
        return out.getvalue().encode('utf-8'), linhas[0]
    except (UnicodeError, csv.Error) as exc:
        raise H.Recusa('CSV não conferível; verifique formato UTF-8 e cabeçalho') from exc


def receber_exportacao(root, s, p):
    import iniciar as I
    import formularios_permanentes as F
    config = pathlib.Path(p.get('config_emcia', I.CONFIG)); c = I.ler_config(config)
    H.exigir(c['responsavel'] == s['responsavel'], 'responsável da configuração diverge do expediente')
    reg = F.validar(config, c, 'habilitacao')
    H.exigir(s.get('tratamento'), 'tratamento administrativo deve preceder a coleta')
    arquivo = entrada_local(p['arquivo'], c.get('entrada_dir', pathlib.Path.home()/'emcia-op/entrada'))
    raw = arquivo.read_bytes()
    filtrado, linha = filtrar(raw, s['caso_reservado'], p.get('coluna_submissao', 'Submission ID'), p.get('submissao'))
    for coluna, valor in [('formId', reg['formId']), ('workspaceId', c['workspace_tally'])]:
        H.exigir(coluna not in linha or linha[coluna] == valor, 'formulário/workspace da linha do caso diverge da configuração')
    ident = H.identificador(p['id']); submission = linha[p.get('coluna_submissao', 'Submission ID')]
    H.exigir(ident not in s['fontes'], 'fonte já registrada')
    H.exigir(not any(f['formulario'] == reg['formId'] and f['submissao'] == submission for f in s['fontes'].values()), 'submissão duplicada')
    respondente = H.pessoa(linha.get(p.get('coluna_respondente', 'Respondente')) or p.get('respondente'))
    s['fontes'][ident] = dict(formulario=reg['formId'], submissao=submission, rodada=0,
        canal='tally-exportacao', respondente=respondente, versao_perguntas=reg['versao_contrato'],
        workspace_id=c['workspace_tally'], recebido_em=H.agora(),
        original_sha256=H.digest(raw), arquivo=H.guardar(root, filtrado, '.csv'),
        conferencia_sha256=reg['relatorio_sha256'])
    H.invalidar(s)


def receber_mensagem(root, s, p):
    H.exigir(s.get('tratamento') and s['fontes'], 'mensagem exige tratamento e coleta inicial')
    ident = H.identificador(p['id']); H.exigir(ident not in s['fontes'], 'fonte já registrada')
    texto = H.texto(p.get('texto')); pergunta = H.texto(p.get('pergunta')); respondente = H.pessoa(p.get('respondente'))
    origem = p.get('origem') or next(iter(s['fontes']))
    H.exigir(origem in s['fontes'], 'origem da mensagem ausente')
    rodada = max(f['rodada'] for f in s['fontes'].values())+1
    reg = dict(caso=s['caso_reservado'], rodada=rodada, pergunta=pergunta, texto=texto, respondente=respondente)
    import json
    s['fontes'][ident] = dict(formulario=s['fontes'][origem]['formulario'], submissao='mensagem-'+ident,
        rodada=rodada, canal='manual', respondente=respondente, origem=origem,
        versao_perguntas=s['fontes'][origem]['versao_perguntas'], recebido_em=H.agora(),
        arquivo=H.guardar(root, json.dumps(reg, ensure_ascii=False).encode(), '.json'))
    H.invalidar(s)
