"""Travas do expediente de habilitação; dados exclusivamente sintéticos."""
import importlib.util
import hashlib
import json
import pathlib
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("habilitacao", ROOT / "eiac-campo/scripts/habilitacao.py")
H = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(H)


class Habilitacao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name)
        self.root = self.base / "expediente"
        H.iniciar(self.root, "HAB-TESTE", "Pessoa Responsavel")
        self.templates = self.base / 'templates'
        shutil.copytree(ROOT / 'testes/apoio/templates-hab-v1', self.templates)
        self.addCleanup(patch.stopall)
        patch.object(H, 'APR', self.templates / 'EMCIA-APR-01-registro-de-aprovacoes.md', create=True).start()

    def run_action(self, action, **data):
        return H.executar(self.root, action, data)

    def state(self):
        return json.loads((self.root / "expediente.json").read_text())

    def refused(self, action, **data):
        with self.assertRaises(H.Recusa):
            self.run_action(action, **data)
        self.assertEqual(self.state()["eventos"][-1]["tipo"], "Recusado")
        self.assertEqual(self.state()["eventos"][-1]["autor"], "Pessoa Responsavel")

    def source(self, name="S1"):
        p = self.base / (name + ".json")
        p.write_text('{"resposta": "declaracao sintetica"}')
        self.run_action("receber", id=name, arquivo=str(p), formulario="F1",
                        submissao=name, respondente="Pessoa Cliente", versao_perguntas="v1", rodada=0)

    def test_01_no_case_or_tool_repository(self):
        with self.assertRaises(H.Recusa):
            H.iniciar(ROOT / "expediente-teste", "H1", "Pessoa Responsavel")
        self.assertFalse((ROOT / "expediente-teste").exists())

    def test_02_author_cannot_be_agent_or_changed(self):
        with self.assertRaises(H.Recusa):
            H.iniciar(self.base / "outro", "H1", "AG-01")
        self.refused("receber", autor="Outra Pessoa")

    def test_03_signature_without_release(self):
        self.refused("assinatura", documento="HAB-01", versao=1)

    def test_04_no_silent_denial(self):
        self.refused("inexistente")
        self.refused("consolidar", campos={})

    def test_05_duplicate_submission(self):
        self.source()
        self.refused("receber", id="S2", arquivo=str(self.base / "S1.json"),
                     formulario="F1", submissao="S1", respondente="Pessoa Cliente",
                     versao_perguntas="v1", rodada=0)
        self.assertEqual(len(self.state()["fontes"]), 1)

    def test_06_round_and_human_resolution(self):
        self.source()
        self.run_action("pendencia", id="P1", origem="S1", pergunta="Qual limite?",
                        efeito="carta", rodada=1)
        self.refused("resolver", id="P1", resposta="S1", decisor="Pessoa Engenheira", motivo="ok")
        self.refused("receber", id="S2", arquivo=str(self.base / "S1.json"),
                     formulario="F2", submissao="R2", respondente="Pessoa Cliente",
                     versao_perguntas="v1", rodada=2)

    def test_07_unresolved_pending_blocks_consolidation(self):
        self.source()
        self.run_action("pendencia", id="P1", origem="S1", pergunta="Qual limite?",
                        efeito="carta", rodada=1)
        self.refused("consolidar", campos={"organizacao": {"valor": "Exemplo", "fonte": "S1"}})

    def test_08_tampered_original(self):
        self.source()
        f = self.state()["fontes"]["S1"]["arquivo"]
        (self.root / f["caminho"]).write_text("alterado")
        self.refused("consolidar", campos={"organizacao": {"valor": "Exemplo", "fonte": "S1"}})

    def test_09_no_automatic_0b(self):
        result = self.run_action("estado")
        self.assertFalse(result["formalizacao_completa"])
        self.refused("concluir-0b")

    def test_10_originals_and_actor_recorded(self):
        self.source()
        self.run_action("consolidar", campos={"organizacao": {"valor": "Exemplo", "fonte": "S1"}})
        self.assertEqual(self.state()["campos"]["organizacao"]["fonte"], "S1")
        self.assertTrue(all(e["autor"] == "Pessoa Responsavel" for e in self.state()["eventos"]))

    def revisao_juridica(self, documentos=None, **mudancas):
        dados = dict(revisor='Pessoa Jurista', decisor='Pessoa Engenheira', data='2026-10-04',
                     resultado='aprovado',
                     documentos=({doc: hashlib.sha256((self.templates / H.TEMPLATES[doc]).read_bytes()).hexdigest()
                                  for doc in ('HAB-02', 'HAB-03')} if documentos is None else documentos),
                     evidencia=str(self.base / 'S1.json'))
        dados.update(mudancas)
        return dados

    def prepare(self, gerar=True, juridica=True):
        self.source()
        campos = {k: {'valor': 'Controle sintético ' + k, 'fonte': 'S1'}
                  for f in H.TEMPLATES.values() for k in H.TOKEN.findall((self.templates / f).read_text())}
        campos['organizacao']['valor'] = 'Organização Sintética'
        campos['signatario']['valor'] = 'Pessoa Cliente'
        self.run_action("consolidar", campos=campos)
        self.run_action("revisar", decisor="Pessoa Engenheira", motivo="Conferência sintética",
                        evidencia=str(self.base / "S1.json"), qualificacao_0a=True, conteudo_conferido=True)
        if juridica:
            self.run_action('revisao-juridica', **self.revisao_juridica())
        if gerar:
            with patch.object(H, "pdf_bytes", return_value=b"%PDF-1.7\nsintetico\n%%EOF"):
                self.run_action("gerar", templates=str(self.templates))

    def release(self, doc="HAB-01", version=1):
        self.run_action("liberar", documento=doc, versao=version, decisor="Pessoa Engenheira",
                        pdf_conferido=True, ferramenta="Painel escolhido", operador="Pessoa Cliente",
                        signatarios=[{"nome": "Pessoa Cliente", "papel": "organizacao", "competencia": "Representante"},
                                     {"nome": "Pessoa Responsavel", "papel": "emcia", "competencia": "Responsável"}])

    def signature(self, doc="HAB-01", version=1):
        pdf = self.base / "assinado.pdf"
        pdf.write_bytes(b"%PDF-1.7\nassinado sintetico diferente\n%%EOF")
        return dict(documento=doc, versao=version, decisor="Pessoa Engenheira", arquivo=str(pdf),
                    evidencia=str(self.base / "S1.json"), referencia="Solicitação sintética",
                    conteudo_conferido=True, evidencias_conferidas=True,
                    signatarios=[{"nome": "Pessoa Cliente", "papel": "organizacao", "data": "2026-09-25"},
                                 {"nome": "Pessoa Responsavel", "papel": "emcia", "data": "2026-09-25"}])

    def test_11_partial_or_wrong_signer(self):
        self.prepare()
        self.release()
        data = self.signature()
        data["signatarios"].pop()
        self.refused("assinatura", **data)
        data = self.signature()
        data["signatarios"][0]["nome"] = "Outra Pessoa"
        self.refused("assinatura", **data)
        self.assertIsNone(self.state()["documentos"]["HAB-01"][-1]["assinatura"])

    def test_12_stale_version(self):
        self.prepare()
        self.release()
        self.run_action("assinatura", **self.signature())
        self.run_action("consolidar", campos={"organizacao": {"valor": "Nova", "fonte": "S1"}})
        self.refused("assinatura", **self.signature())
        self.refused("concluir-0b")

    def test_13_three_docs_both_parties_and_different_hashes(self):
        self.prepare()
        for doc in H.TEMPLATES:
            self.release(doc)
            self.run_action("assinatura", **self.signature(doc))
        self.assertTrue(self.run_action("concluir-0b")["formalizacao_completa"])
        self.refused("preparar-0d")
        self.run_action("acessos", patrocinador="Pessoa Cliente", executor="Pessoa Executora",
                        decisor="Pessoa Engenheira", autoridade_patrocinador="Responsável pelo processo",
                        executor_liberado=True, agenda_reservada=True, data_sessao="2026-10-01",
                        itens=[{"item": "Fonte A", "status": "concedido", "evidencia": "Leitura conferida"}])
        self.assertTrue(self.run_action("preparar-0d")["pronto_para_0d"])
        self.assertFalse(self.state()["caso_aberto"])

    def test_14_unsigned_or_unreviewed_pdf(self):
        self.prepare()
        self.refused("assinatura", **self.signature())
        self.release()
        data = self.signature()
        data["evidencias_conferidas"] = False
        self.refused("assinatura", **data)
        data = self.signature()
        pathlib.Path(data["arquivo"]).write_text("não é PDF")
        self.refused("assinatura", **data)

    def test_15_mcp_requires_prior_treatment(self):
        p = self.base / "source.json"
        p.write_text("{}")
        data = dict(id="S1", arquivo=str(p), formulario="F1", submissao="R1", respondente="Pessoa Cliente",
                    versao_perguntas="v1", rodada=0, canal="tally-mcp")
        self.refused("receber", **data)
        self.run_action("tratamento", escopo="administrativo", condicoes="Condições sintéticas",
                        provedor="Ambiente autorizado", decisor="Pessoa Engenheira", evidencia=str(p))
        self.run_action("receber", **data)
        data.update(id="S2", submissao="R2", escopo="operacional")
        self.refused("receber", **data)

    def test_16_invalid_json_produces_event(self):
        p = self.base / "invalid.json"
        p.write_text("{")
        with self.assertRaises(H.Recusa):
            H.executar(self.root, "receber", p)
        self.assertEqual(self.state()["eventos"][-1]["tipo"], "Recusado")

    def test_17_missing_field_and_pdf_failure_do_not_publish_versions(self):
        self.prepare()
        campos = self.state()['campos']
        del campos['processo_alvo']
        self.run_action('consolidar', campos=campos)
        self.run_action('revisar', decisor='Pessoa Engenheira', motivo='Conferência sintética',
                        evidencia=str(self.base / 'S1.json'), qualificacao_0a=True, conteudo_conferido=True)
        with patch.object(H, "pdf_bytes", return_value=b"%PDF-1.7\n%%EOF"):
            with self.assertRaisesRegex(H.Recusa, 'campos ausentes'):
                self.run_action('gerar', templates=str(self.templates))
        self.assertTrue(all(len(v) == 1 for v in self.state()["documentos"].values()))

    def test_18_expiration_blocks_completion(self):
        self.prepare()
        self.release()
        self.run_action("ocorrencia", documento="HAB-01", versao=1, decisor="Pessoa Engenheira",
                        status="expirado", motivo="Prazo encerrado")
        self.refused("assinatura", **self.signature())

    def test_19_round_trip_and_reopening_preserve_history(self):
        self.source()
        self.run_action("pendencia", id="P1", origem="S1", pergunta="Qual limite?", efeito="carta", rodada=1)
        self.run_action("receber", id="S2", arquivo=str(self.base / "S1.json"), formulario="F2",
                        submissao="R2", respondente="Pessoa Cliente", versao_perguntas="v1", rodada=1)
        self.run_action("resolver", id="P1", resposta="S2", decisor="Pessoa Engenheira", motivo="Esclarecido")
        self.run_action("reabrir", id="P1", rodada=2, decisor="Pessoa Engenheira", motivo="Nova divergência")
        self.refused("resolver", id="P1", resposta="S2", decisor="Pessoa Engenheira", motivo="Resposta antiga")
        self.assertEqual(len(self.state()["pendencias"]["P1"]["decisoes"]), 2)

    def test_20_gerar_sem_revisao_juridica_recusa_antes_do_pdf(self):
        self.prepare(gerar=False, juridica=False)
        with patch.object(H, 'pdf_bytes') as pdf:
            with self.assertRaisesRegex(H.Recusa, 'revisao-juridica.*HAB-02'):
                self.run_action('gerar', templates=str(self.templates))
            pdf.assert_not_called()
        self.assertEqual(self.state()['documentos'], {})
        self.assertEqual(self.state()['eventos'][-1]['tipo'], 'Recusado')

    def test_21_cobertura_so_de_hab02_nao_autoriza_hab03(self):
        self.prepare(gerar=False, juridica=False)
        sha = self.revisao_juridica()['documentos']['HAB-02']
        self.run_action('revisao-juridica', **self.revisao_juridica(documentos={'HAB-02': sha}))
        with patch.object(H, 'pdf_bytes') as pdf:
            with self.assertRaisesRegex(H.Recusa, 'revisao-juridica.*HAB-03'):
                self.run_action('gerar', templates=str(self.templates))
            pdf.assert_not_called()
        self.assertEqual(self.state()['documentos'], {})

    def test_22_revisao_exige_hash_aprovado_pessoa_data_e_evidencia(self):
        self.source()
        for mudanca in ({'revisor': 'AG-01'}, {'decisor': 'AG-02'}, {'data': '2026-02-30'},
                        {'documentos': {'HAB-02': '0' * 64}}, {'documentos': {'OUTRO': '0' * 64}},
                        {'documentos': []}, {'evidencia': str(self.base / 'ausente')}, {'dispensa': True}):
            with self.subTest(mudanca=mudanca):
                self.refused('revisao-juridica', **self.revisao_juridica(**mudanca))
        self.assertFalse(self.state().get('revisoes_juridicas'))

    def test_23_evidencia_juridica_adulterada_bloqueia_gerar(self):
        self.prepare(gerar=False)
        ref = self.state()['revisoes_juridicas'][0]['evidencia']
        (self.root / ref['caminho']).write_text('adulterada')
        self.refused('gerar', templates=str(self.templates))

    def test_24_hash_do_template_alterado_nao_herda_revisao(self):
        self.prepare(gerar=False)
        p = self.templates / H.TEMPLATES['HAB-03']
        p.write_bytes(p.read_bytes() + b'\nAlteracao de clausula.\n')
        with self.assertRaisesRegex(H.Recusa, 'APR-01.*HAB-03'):
            self.run_action('gerar', templates=str(self.templates))
        self.assertEqual(self.state()['documentos'], {})

    def test_25_documentos_emitidos_preservam_contrato_e_identificacao(self):
        self.prepare(gerar=False)
        with patch.object(H, 'pdf_bytes', side_effect=lambda md, browser: b'%PDF-1.7\n' + md.encode() + b'\n%%EOF'):
            self.run_action('gerar', templates=str(self.templates))
        s = self.state()
        for doc, nome in H.TEMPLATES.items():
            with self.subTest(doc=doc):
                v = s['documentos'][doc][-1]
                raw = (self.templates / nome).read_bytes()
                md = H.ler_arquivo(self.root, v['markdown']).decode()
                pdf = H.ler_arquivo(self.root, v['pdf']).decode()
                for emitido in (md, pdf):
                    for interno in ('Controle do modelo', 'Revisão jurídica', 'Histórico de revisões do modelo',
                                    '**Aprovação**', 'Celso do Vale'):
                        self.assertNotIn(interno, emitido)
                    self.assertIn('Estado de emissão: Para assinatura', emitido)
                    self.assertIn('## Identificação do caso', emitido)
                    self.assertIn('Organização Sintética', emitido)
                    self.assertIn('HAB-TESTE', emitido)
                contrato = '## 1. Objetivo' + raw.decode().split('## 1. Objetivo', 1)[1].split('## 10. Histórico de revisões do modelo', 1)[0]
                aviso = next((l for l in contrato.splitlines(keepends=True) if l.startswith('> **Revisão jurídica:**')), '')
                contrato = contrato.replace(aviso, '')
                campos = {k: val['valor'] for k, val in s['campos'].items()}
                campos.update(caso_id='HAB-TESTE', responsavel_emcia='Pessoa Responsavel',
                              status_assinatura='Aguardando assinatura', versao_assinada='Pendente',
                              evidencia_assinatura='Pendente', data_assinatura_cliente='A registrar na assinatura',
                              data_assinatura_emcia='A registrar na assinatura')
                esperado = H.TOKEN.sub(lambda m: campos[m[1]], contrato).strip()
                self.assertIn(esperado, md)
                self.assertEqual(H.ler_arquivo(self.root, v['template']), raw)
                self.assertEqual(v['template']['sha256'], hashlib.sha256(raw).hexdigest())
                self.assertEqual(v['markdown']['sha256'], hashlib.sha256(md.encode()).hexdigest())
                if doc != 'HAB-01':
                    self.assertEqual(v['revisao_juridica']['documentos'][doc], v['template']['sha256'])

    def test_26_marcas_ausentes_recusam_com_motivo_sem_publicar(self):
        self.prepare(gerar=False)
        nome = H.TEMPLATES['HAB-02']
        original = (self.templates / nome).read_text()
        for marca in ('## Controle do modelo', '## Identificação do caso', '> **Revisão jurídica:**',
                      '## 10. Histórico de revisões do modelo'):
            with self.subTest(marca=marca):
                alterado = original.replace(marca, 'MARCA AUSENTE')
                (self.templates / nome).write_text(alterado)
                # Isola a checagem estrutural: APR sintético conserva a mesma linha,
                # somente o hash da mutação é registrado nesta cópia temporária.
                apr = self.templates / 'EMCIA-APR-01-registro-de-aprovacoes.md'
                registro = (ROOT / 'testes/apoio/templates-hab-v1' / apr.name).read_text()
                registro = registro.replace(hashlib.sha256(original.encode()).hexdigest(), hashlib.sha256(alterado.encode()).hexdigest())
                apr.write_text(registro)
                self.run_action('revisao-juridica', **self.revisao_juridica())
                with self.assertRaisesRegex(H.Recusa, 'marcas.*HAB-02'):
                    self.run_action('gerar', templates=str(self.templates))
                self.assertEqual(self.state()['documentos'], {})

    def test_27_blocos_juridicos_multilinha_sao_retirados_sem_comer_contrato(self):
        self.prepare(gerar=False)
        nome = H.TEMPLATES['HAB-03']
        p = self.templates / nome
        raw = p.read_bytes()
        novo = raw.decode().replace('> **Revisão jurídica:**', '> **Revisão jurídica:**\n> Continuação interna.\n>')
        p.write_text(novo)
        apr = self.templates / 'EMCIA-APR-01-registro-de-aprovacoes.md'
        apr.write_text(apr.read_text().replace(hashlib.sha256(raw).hexdigest(), hashlib.sha256(novo.encode()).hexdigest()))
        self.run_action('revisao-juridica', **self.revisao_juridica())
        with patch.object(H, 'pdf_bytes', return_value=b'%PDF-1.7\n%%EOF'):
            self.run_action('gerar', templates=str(self.templates))
        md = H.ler_arquivo(self.root, self.state()['documentos']['HAB-03'][-1]['markdown']).decode()
        self.assertNotIn('Continuação interna', md)
        self.assertIn('## 2. Identificação', md)

    def test_28_nova_revisao_preserva_a_anterior_e_mostra_cobertura(self):
        self.prepare(gerar=False)
        self.run_action('revisao-juridica', **self.revisao_juridica(revisor='Outra Jurista', data='2026-10-05'))
        s = self.state()
        self.assertEqual(len(s['revisoes_juridicas']), 2)
        self.assertEqual(s['revisoes_juridicas'][0]['revisor'], 'Pessoa Jurista')
        self.assertEqual(s['revisoes_juridicas'][1]['revisor'], 'Outra Jurista')
        self.assertEqual(self.run_action('estado')['revisoes_juridicas'], s['revisoes_juridicas'])

    def test_29_falha_no_pdf_nao_publica_versoes_parciais(self):
        self.prepare(gerar=False)
        with patch.object(H, 'pdf_bytes', side_effect=[b'%PDF-1.7\n%%EOF', H.Recusa('falha sintética de PDF')]):
            self.refused('gerar', templates=str(self.templates))
        self.assertEqual(self.state()['documentos'], {})
        self.assertEqual(self.state()['eventos'][-1]['motivo'], 'falha sintética de PDF')

    def test_30_revisao_sem_resultado_recusa_com_evento(self):
        self.source()
        dados = self.revisao_juridica()
        del dados['resultado']
        self.refused('revisao-juridica', **dados)
        self.assertIn('resultado', self.state()['eventos'][-1]['motivo'])
        self.assertFalse(self.state().get('revisoes_juridicas'))

    def test_31_somente_resultado_literal_aprovado_e_aceito(self):
        self.source()
        for resultado in ('condicionado', 'reprovado', 'Texto livre', 'Aprovado', ' aprovado ', '', None, True):
            with self.subTest(resultado=resultado):
                self.refused('revisao-juridica', **self.revisao_juridica(resultado=resultado))
                self.assertIn('resultado', self.state()['eventos'][-1]['motivo'])
                self.assertFalse(self.state().get('revisoes_juridicas'))

    def test_32_aprovado_preserva_resultado_ciclo_hashes_e_evidencia(self):
        self.source()
        dados = self.revisao_juridica(ciclo='2026-10-ciclo-2')
        self.run_action('revisao-juridica', **dados)
        revisao = self.state()['revisoes_juridicas'][0]
        self.assertEqual(revisao['resultado'], 'aprovado')
        self.assertEqual(revisao['ciclo'], '2026-10-ciclo-2')
        self.assertEqual(revisao['documentos'], dados['documentos'])
        self.assertEqual(revisao['evidencia']['sha256'], hashlib.sha256((self.base / 'S1.json').read_bytes()).hexdigest())
        self.assertEqual(self.state()['eventos'][-1]['entrada'], dados)
        self.run_action('revisao-juridica', **self.revisao_juridica())
        self.assertEqual(self.state()['revisoes_juridicas'][-1]['resultado'], 'aprovado')
        self.assertNotIn('ciclo', self.state()['revisoes_juridicas'][-1])

    def test_33_ciclo_invalido_recusa_sem_dispensa(self):
        self.source()
        for ciclo in (None, True, 2, [], '', '   '):
            with self.subTest(ciclo=ciclo):
                self.refused('revisao-juridica', **self.revisao_juridica(ciclo=ciclo))
        self.assertFalse(self.state().get('revisoes_juridicas'))

    def test_34_gerar_ignora_revisoes_legadas_ou_nao_aprovadas(self):
        # Simula registros preservados de versões anteriores, sem usar uma
        # operação que já deve recusar o resultado. Não toca nas evidências.
        self.prepare(gerar=False, juridica=False)
        dados = self.revisao_juridica()
        original = self.state()
        original['revisoes_juridicas'] = [dict(revisor=dados['revisor'], decisor=dados['decisor'],
            data=dados['data'], documentos=dados['documentos'], evidencia=original['fontes']['S1']['arquivo'])]
        for resultado in (None, 'condicionado', 'reprovado', 'texto livre'):
            with self.subTest(resultado=resultado):
                registro = json.loads(json.dumps(original))
                if resultado is not None:
                    registro['revisoes_juridicas'][0]['resultado'] = resultado
                (self.root / 'expediente.json').write_text(json.dumps(registro))
                with patch.object(H, 'pdf_bytes') as pdf:
                    with self.assertRaisesRegex(H.Recusa, 'revisao-juridica.*HAB-02'):
                        self.run_action('gerar', templates=str(self.templates))
                    pdf.assert_not_called()
                self.assertEqual(self.state()['documentos'], {})
                self.assertEqual(self.state()['eventos'][-1]['tipo'], 'Recusado')
                self.assertEqual(self.state()['eventos'][-1]['autor'], 'Pessoa Responsavel')

    def test_35_gerar_seleciona_somente_registro_aprovado(self):
        self.prepare(gerar=False)
        registro = self.state()
        condicionado = json.loads(json.dumps(registro['revisoes_juridicas'][0]))
        condicionado.update(resultado='condicionado', revisor='Outra Jurista')
        registro['revisoes_juridicas'].append(condicionado)
        (self.root / 'expediente.json').write_text(json.dumps(registro))
        with patch.object(H, 'pdf_bytes', return_value=b'%PDF-1.7\n%%EOF'):
            self.run_action('gerar', templates=str(self.templates))
        for doc in ('HAB-02', 'HAB-03'):
            r = self.state()['documentos'][doc][-1]['revisao_juridica']
            self.assertEqual(r['resultado'], 'aprovado')
            self.assertEqual(r['revisor'], 'Pessoa Jurista')


if __name__ == "__main__":
    unittest.main()
