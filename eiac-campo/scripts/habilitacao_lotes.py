"""Conjuntos administrativos com testemunho nominal e aprovação dos bytes exibidos."""
import copy
import json
import pathlib
import re
import shutil
import subprocess
import habilitacao as H
import aprovacao as A


def comando(root, operacao, plano):
    return ['habilitacao-lote', operacao, str(pathlib.Path(root).absolute()), json.dumps(plano, sort_keys=True, ensure_ascii=False)]


def arquivos(root, s, operacao, plano):
    refs = s.get('rascunhos_documentos' if operacao == 'aprovar-documentos' else 'rascunhos_assinaturas')
    H.exigir(refs and set(refs) == set(H.CODIGOS_HAB), 'prepare os três documentos antes da aprovação')
    encontrados = [root/'expediente.json', H.APR]
    def visitar(v):
        if isinstance(v, dict):
            if 'caminho' in v and 'sha256' in v: encontrados.append(root/v['caminho'])
            else:
                for x in v.values(): visitar(x)
        elif isinstance(v, list):
            for x in v: visitar(x)
    visitar(refs)
    if operacao == 'aprovar-documentos': encontrados.append(pathlib.Path(plano['geracao']['config_emcia']))
    return encontrados


def criar_aprovacao(root, operacao, plano, literal):
    H.exigir(operacao in ('aprovar-documentos', 'aprovar-assinaturas'), 'operação de conjunto desconhecida')
    root = H.local_externo(root); s = json.loads((root/'expediente.json').read_text()); H.integridade(root, s)
    resumo = ('Revisão e emissão dos três documentos, qualificação, signatários e painel' if operacao == 'aprovar-documentos'
              else 'Conferência dos três PDFs assinados, associação aos enviados, signatários e evidências')
    return A.criar(operacao, s['responsavel'], s['caso_reservado'], literal, resumo,
                   comando(root, operacao, plano), arquivos(root, s, operacao, plano))


def validar_aprovacao(root, s, operacao, p):
    plano = p.get('plano'); H.exigir(isinstance(plano, dict), 'plano de aprovação ausente')
    r = A.conferir(p.get('testemunho'), operacao, s['responsavel'], s['caso_reservado'], comando(root, operacao, plano))
    for arq in arquivos(root, s, operacao, plano):
        H.exigir(str(arq.absolute()) in r['arquivos'], 'arquivo sem hash na aprovação')
    return plano, r


def registrar_operacao(s, op, payload):
    H.evento(s, 'OperacaoRegistrada', operacao=op, entrada=copy.deepcopy(payload),
             entrada_sha256=H.digest(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()))


def texto_pdf(arquivo):
    exe = shutil.which('pdftotext'); H.exigir(exe, 'instale pdftotext (Poppler) para associar PDFs; alternativa manual disponível')
    r = subprocess.run([exe, '-enc', 'UTF-8', str(arquivo), '-'], capture_output=True, timeout=30)
    H.exigir(r.returncode == 0, 'PDF não conferível; use a alternativa manual com conferência humana')
    t = ' '.join(r.stdout.decode('utf-8').split())
    H.exigir(t, 'PDF sem texto; use a alternativa manual com conferência humana')
    return t


def aplicar(root, s, op, p):
    if op == 'preparar-documentos':
        H.exigir(s['campos'] and not any(x['estado']=='aberta' for x in s['pendencias'].values()), 'campos ou esclarecimentos pendentes')
        prepared, situacoes = H.preparar_minutas(s, p)
        pdfs = {doc:H.pdf_bytes(md, p.get('navegador', 'google-chrome')) for doc,(raw,md,n,juridica) in prepared.items()}
        s['rascunhos_documentos'] = {doc:dict(versao=n, template=H.guardar(root, raw, '.md'),
             markdown=H.guardar(root, md.encode(), '.md'), pdf=H.guardar(root, pdfs[doc], '.pdf'))
             for doc,(raw,md,n,juridica) in prepared.items()}
        return {'documentos':s['rascunhos_documentos'], 'proximo':'aprovar-documentos'}
    if op == 'preparar-assinaturas':
        import iniciar as I
        from coleta_administrativa import entrada_local
        c = I.ler_config(pathlib.Path(p.get('config_emcia', I.CONFIG)))
        H.exigir(c['responsavel'] == s['responsavel'], 'responsável diverge do expediente')
        base = pathlib.Path(c.get('entrada_dir', pathlib.Path.home()/'emcia-op/entrada'))
        H.exigir(all(s['documentos'].get(d) and s['documentos'][d][-1]['vigente']
                     and s['documentos'][d][-1]['liberacao'] for d in H.CODIGOS_HAB), 'documentos enviados ausentes')
        textos = {d:texto_pdf(root/s['documentos'][d][-1]['pdf']['caminho']) for d in H.CODIGOS_HAB}
        encontrados = {}; arquivos_pdf = sorted(base.glob('*.pdf'))
        for arq in arquivos_pdf:
            arq = entrada_local(arq, base)
            if re.fullmatch(r'HAB-0[123]-relatorio\.pdf', arq.name): continue
            data = arq.read_bytes(); H.exigir(data.startswith(b'%PDF-') and b'%%EOF' in data[-2048:], 'PDF assinado incompleto')
            conteudo = texto_pdf(arq)
            candidatos = [d for d,t in textos.items() if t in conteudo]
            H.exigir(len(candidatos) == 1, 'PDF assinado não corresponde a um único documento enviado')
            doc = candidatos[0]; H.exigir(doc not in encontrados, 'mais de um PDF assinado para o mesmo documento')
            evidencia = base/(doc+'-relatorio.pdf'); evidencia = evidencia if evidencia.exists() else arq
            entrada_local(evidencia, base)
            encontrados[doc] = dict(documento=doc, versao=s['documentos'][doc][-1]['versao'],
                enviado_sha256=s['documentos'][doc][-1]['pdf']['sha256'],
                arquivo=H.guardar(root, data, '.pdf'), evidencia=H.guardar(root, evidencia.read_bytes(), '.pdf'))
        H.exigir(set(encontrados) == set(H.CODIGOS_HAB), 'deposite os três PDFs assinados na pasta de entrada')
        s['rascunhos_assinaturas'] = encontrados
        return {'documentos':encontrados, 'proximo':'aprovar-assinaturas'}
    plano, r = validar_aprovacao(root, s, op, p)
    if op == 'aprovar-documentos':
        revisao = dict(decisor=s['responsavel'], motivo=r['resumo'], qualificacao_0a=plano.get('qualificacao_0a'),
            conteudo_conferido=plano.get('conteudo_conferido'),
            evidencia=str(root/s['rascunhos_documentos']['HAB-01']['markdown']['caminho']))
        H.aplicar(root, s, 'revisar', revisao); registrar_operacao(s, 'revisar', revisao)
        H.aplicar(root, s, 'gerar', plano['geracao']); registrar_operacao(s, 'gerar', plano['geracao'])
        for doc in H.CODIGOS_HAB:
            payload = dict(plano['liberacao'], documento=doc, versao=s['documentos'][doc][-1]['versao'],
                           decisor=s['responsavel'], pdf_conferido=True)
            H.aplicar(root, s, 'liberar', payload); registrar_operacao(s, 'liberar', payload)
    elif op == 'aprovar-assinaturas':
        for doc in H.CODIGOS_HAB:
            reg = s['rascunhos_assinaturas'][doc]; v = s['documentos'][doc][-1]
            H.exigir(reg['enviado_sha256'] == v['pdf']['sha256'] and reg['versao'] == v['versao'], 'PDF enviado mudou; confira novamente as assinaturas')
            payload = dict(documento=doc, versao=v['versao'], decisor=s['responsavel'],
                arquivo=str(root/reg['arquivo']['caminho']), evidencia=str(root/reg['evidencia']['caminho']),
                referencia=H.texto(plano.get('referencia')), conteudo_conferido=True, evidencias_conferidas=True,
                signatarios=plano['signatarios'][doc] if isinstance(plano['signatarios'], dict) else plano['signatarios'])
            H.aplicar(root, s, 'assinatura', payload); registrar_operacao(s, 'assinatura', payload)
        H.aplicar(root, s, 'concluir-0b', {})
    else:
        raise H.Recusa('operação de conjunto desconhecida')
    H.evento(s, 'AprovacaoLoteRegistrada', operacao=op, testemunho=A.evento(r))
    return {'registrado':True, 'operacao':op, 'formalizacao_completa':H.completa(s)}
