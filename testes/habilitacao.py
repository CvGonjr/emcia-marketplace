"""Travas do expediente de habilitação; dados exclusivamente sintéticos."""
import importlib.util
import json
import pathlib
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

    def prepare(self):
        self.source()
        self.run_action("consolidar", campos={"organizacao": {"valor": "Exemplo", "fonte": "S1"}})
        self.run_action("revisar", decisor="Pessoa Engenheira", motivo="Conferência sintética",
                        evidencia=str(self.base / "S1.json"), qualificacao_0a=True, conteudo_conferido=True)
        templates = self.base / "templates"
        templates.mkdir(exist_ok=True)
        for filename in H.TEMPLATES.values():
            (templates / filename).write_text("# Exemplo\n{{organizacao}} {{caso_id}}\n")
        with patch.object(H, "pdf_bytes", return_value=b"%PDF-1.7\nsintetico\n%%EOF"):
            self.run_action("gerar", templates=str(templates))

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
        filename = self.base / "templates" / H.TEMPLATES["HAB-03"]
        filename.write_text("{{campo_ausente}}")
        with patch.object(H, "pdf_bytes", return_value=b"%PDF-1.7\n%%EOF"):
            self.refused("gerar", templates=str(self.base / "templates"))
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


if __name__ == "__main__":
    unittest.main()
