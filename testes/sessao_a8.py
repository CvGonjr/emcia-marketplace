"""A8: sessão da etapa corrente conforme camada declarada no caso."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / "eiac-nucleo/scripts/avancar.py"
REGRAS = {"EX1": False, "EX2": False, "EX3": True, "EX4": True}


class SessaoA8(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.caso = pathlib.Path(self.tmp.name)
        shutil.copytree(RAIZ / "eiac-campo/template-caso/registro", self.caso / "registro")
        self.estado = self.caso / "registro/estado.json"
        self.playbook = self.caso / "registro/playbook.json"
        # A regra explícita na fixture permite exercitar o motor anterior,
        # que a ignorava. O teste 18 confere também o template de produção.
        self.configurar(lambda pb: pb.update(encerramento_por_camada=REGRAS.copy()))
        self.posicionar("P3a", "N2")

    def configurar(self, editar):
        pb = json.loads(self.playbook.read_text())
        editar(pb)
        self.playbook.write_text(json.dumps(pb))

    def posicionar(self, etapa, nivel):
        pb = json.loads(self.playbook.read_text())
        st = json.loads(self.estado.read_text())
        st.update(responsavel="Celso do Vale", etapa_atual=etapa, nivel=nivel)
        st["cumprimentos"] = {}
        for et in pb["etapas"]:
            if et["id"] == etapa:
                st.update(camada_atual=et["camada"][nivel], modalidade_atual=et["modalidade"])
                break
            st["cumprimentos"][et["id"]] = {"cumprido": True}
        self.estado.write_text(json.dumps(st))

    def alterar_estado(self, editar):
        st = json.loads(self.estado.read_text())
        editar(st)
        self.estado.write_text(json.dumps(st))

    def executar(self, acao, etapa):
        return subprocess.run(["python3", str(SCRIPT), acao, etapa, "--autor", "Celso do Vale",
                               "--participantes", "Celso do Vale, Pessoa Cliente"],
                              cwd=self.caso, text=True, capture_output=True)

    def ultimo_evento(self):
        return json.loads((self.caso / "registro/eventos.jsonl").read_text().splitlines()[-1])

    def recusa(self, acao, etapa, partes, evento="TentativaNegada"):
        antes = self.estado.read_bytes()
        result = self.executar(acao, etapa)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        for parte in partes:
            self.assertIn(parte, result.stderr)
        self.assertEqual(self.estado.read_bytes(), antes)
        registro = self.ultimo_evento()
        self.assertEqual(registro["evento"], evento)
        self.assertEqual(registro["autor"], "Celso do Vale")
        for parte in partes:
            self.assertIn(parte, registro["motivo"])

    def sessao(self, etapa):
        result = self.executar("--registrar-sessao", etapa)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.ultimo_evento()["evento"], "SessaoDeCampoRegistrada")

    def encerramento(self, etapa):
        result = self.executar("--encerrar", etapa)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(self.estado.read_text())["cumprimentos"][etapa]["cumprido"])
        self.assertEqual(self.ultimo_evento()["evento"], "EtapaEncerrada")

    def test_00_ex3_sem_sessao(self):
        self.recusa("--encerrar", "P3a", ["P3a", "EX3", "N2", "remoto", "sessao"])

    def test_01_sessao_de_outra_etapa_nao_libera(self):
        self.alterar_estado(lambda st: st["cumprimentos"]["P2"].update(
            sessao={"autor": "Celso do Vale", "participantes": "Pessoa Cliente"}))
        self.recusa("--encerrar", "P3a", ["P3a", "EX3", "sessao"])

    def test_02_sessao_futura(self):
        self.recusa("--registrar-sessao", "P4", ["P4", "P3a", "etapa corrente"])

    def test_03_sessao_passada(self):
        self.recusa("--registrar-sessao", "P2", ["P2", "P3a", "etapa corrente"])

    def test_04_sessao_etapa_final_ja_encerrada(self):
        self.posicionar("P10", "N2")
        self.alterar_estado(lambda st: st["cumprimentos"].update(P10={"cumprido": True}))
        self.recusa("--registrar-sessao", "P10", ["P10", "ja encerrada"])

    def test_05_sessao_conferida_antes_do_selo(self):
        self.posicionar("P3b", "N2")
        self.recusa("--encerrar", "P3b", ["P3b", "EX4", "N2", "presencial", "sessao"])

    def test_06_sessao_nao_substitui_selo(self):
        self.posicionar("P3b", "N2")
        self.sessao("P3b")
        self.recusa("--encerrar", "P3b", ["exige selo posterior", "P2"], "RecusaMaquina")

    def test_07_regra_ausente(self):
        self.configurar(lambda pb: pb.pop("encerramento_por_camada"))
        self.recusa("--encerrar", "P3a", ["encerramento_por_camada"])

    def test_08_camada_sem_declaracao(self):
        self.configurar(lambda pb: pb["encerramento_por_camada"].pop("EX3"))
        self.recusa("--encerrar", "P3a", ["encerramento_por_camada", "EX3"])

    def test_09_regra_nao_booleana(self):
        self.configurar(lambda pb: pb["encerramento_por_camada"].update(EX3="sim"))
        self.recusa("--encerrar", "P3a", ["encerramento_por_camada", "EX3"])

    def test_10_outra_regra_exige_sessao_em_outra_camada(self):
        self.posicionar("P1", "N2")
        self.configurar(lambda pb: pb["encerramento_por_camada"].update(EX2=True))
        self.recusa("--encerrar", "P1", ["P1", "EX2", "N2", "video", "sessao"])

    def test_11_sessao_etapa_desconhecida(self):
        self.recusa("--registrar-sessao", "OUTRA", ["OUTRA", "P3a", "etapa corrente"])

    def test_12_ex2_sem_sessao(self):
        self.posicionar("P1", "N2")
        self.encerramento("P1")

    def test_13_ex3_com_sessao_propria(self):
        self.sessao("P3a")
        self.encerramento("P3a")

    def test_14_mesma_etapa_ex2_em_n1(self):
        self.posicionar("P3a", "N1")
        self.encerramento("P3a")

    def test_15_ex4_sessao_e_selo(self):
        self.posicionar("P3b", "N2")
        self.sessao("P3b")
        # Fixture da ordem da trilha; a suíte por estados exercita o selo real.
        with (self.caso / "registro/eventos.jsonl").open("a") as log:
            for evento in [{"evento": "EtapaEncerrada", "etapa": "P2"},
                           {"evento": "SeloAplicado"}]:
                evento["autor"] = "Celso do Vale"
                log.write(json.dumps(evento) + "\n")
        self.encerramento("P3b")

    def test_16_ex1_sem_sessao(self):
        self.posicionar("F0", "N2")
        self.encerramento("F0")

    def test_17_regra_alternativa_lida_do_caso(self):
        self.configurar(lambda pb: pb["encerramento_por_camada"].update(EX3=False))
        self.encerramento("P3a")

    def test_18_template_declara_regra(self):
        pb = json.loads((RAIZ / "eiac-campo/template-caso/registro/playbook.json").read_text())
        self.assertEqual(pb.get("encerramento_por_camada"), REGRAS)

    def test_19_camada_resolvida_nao_cache_do_estado(self):
        self.alterar_estado(lambda st: st.update(camada_atual="EX2"))
        self.recusa("--encerrar", "P3a", ["P3a", "EX3", "N2", "sessao"])

    def test_20_p3d_ex3(self):
        self.posicionar("P3d", "N2")
        self.recusa("--encerrar", "P3d", ["P3d", "EX3", "N2", "remoto", "sessao"])

    def test_21_p4_ex3(self):
        self.posicionar("P4", "N2")
        self.recusa("--encerrar", "P4", ["P4", "EX3", "N2", "video", "sessao"])

    def test_22_p5_ex3(self):
        self.posicionar("P5", "N2")
        self.recusa("--encerrar", "P5", ["P5", "EX3", "N2", "video", "sessao"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
