"""A7: recusas primeiro; regra de apuração declarada no playbook do caso."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / "eiac-nucleo/scripts/avancar.py"


class TriagemA7(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.caso = pathlib.Path(self.tmp.name)
        shutil.copytree(RAIZ / "eiac-campo/template-caso/registro", self.caso / "registro")
        self.estado = self.caso / "registro/estado.json"
        st = json.loads(self.estado.read_text())
        st["responsavel"] = "Celso do Vale"
        self.estado.write_text(json.dumps(st))
        self.playbook = self.caso / "registro/playbook.json"

    def configurar(self, editar):
        pb = json.loads(self.playbook.read_text())
        editar(pb)
        self.playbook.write_text(json.dumps(pb))

    def executar(self, nivel, eixos, autor="Celso do Vale"):
        args = ["python3", str(SCRIPT), "--apurar-nivel", nivel, "--autor", autor]
        if eixos is not None:
            args += ["--eixos", eixos]
        return subprocess.run(args, cwd=self.caso, text=True, capture_output=True)

    def recusa(self, nivel, eixos, mensagem, autor="Celso do Vale"):
        antes = self.estado.read_bytes()
        result = self.executar(nivel, eixos, autor)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(mensagem, result.stderr)
        self.assertEqual(self.estado.read_bytes(), antes)
        evento = json.loads((self.caso / "registro/eventos.jsonl").read_text().splitlines()[-1])
        self.assertEqual(evento["evento"], "TentativaNegada")
        self.assertEqual(evento["autor"], "Celso do Vale")
        self.assertIn(mensagem, evento["motivo"])

    def positivo(self, nivel, eixos):
        result = self.executar(nivel, eixos)
        self.assertEqual(result.returncode, 0, result.stderr)
        st = json.loads(self.estado.read_text())
        self.assertEqual(st["nivel"], nivel)
        self.assertEqual(st["cumprimentos"]["F0"]["eixos"], eixos)
        evento = json.loads((self.caso / "registro/eventos.jsonl").read_text().splitlines()[-1])
        self.assertEqual(evento["evento"], "NivelApurado")
        self.assertEqual(evento["nivel"], nivel)

    def test_00_eixo_ausente(self):
        self.recusa("N2", "DAD 5, GOV 3", "eixos ausentes: CRI")

    def test_01_eixo_desconhecido(self):
        self.recusa("N2", "DAD 5, GOV 3, CRI 6, OUTRO 5", "eixo desconhecido: OUTRO")

    def test_02_fora_da_escala_A7(self):
        self.recusa("N2", "DAD 2, GOV 1, CRI 2", "DAD 2 fora da faixa 3 a 9")

    def test_03_nivel_divergente_maximo_nunca_media(self):
        self.recusa("N1", "DAD 5, GOV 3, CRI 6", "maior eixo CRI 6 -> N2; informado N1")

    def test_04_eixo_duplicado(self):
        self.recusa("N2", "DAD 5, GOV 3, CRI 6, DAD 5", "eixo duplicado: DAD")

    def test_05_formato(self):
        self.recusa("N2", "DAD=5, GOV=3, CRI=6", "formato dos eixos")

    def test_06_sem_eixos(self):
        self.recusa("N2", None, "eixos obrigatorios")

    def test_07_sem_regra(self):
        self.configurar(lambda pb: pb.pop("apuracao_nivel", None))
        self.recusa("N2", "DAD 5, GOV 3, CRI 6", "regra de apuracao_nivel ausente")

    def test_08_agregacao_desconhecida(self):
        self.configurar(lambda pb: pb["apuracao_nivel"].update(agregacao="media"))
        self.recusa("N2", "DAD 5, GOV 3, CRI 6", "agregacao nao suportada")

    def test_09_faixas_sobrepostas(self):
        self.configurar(lambda pb: pb["apuracao_nivel"]["faixas"][1].update(minimo=4))
        self.recusa("N2", "DAD 5, GOV 3, CRI 6", "faixas sobrepostas ou incompletas")

    def test_10_lacuna_entre_faixas(self):
        self.configurar(lambda pb: pb["apuracao_nivel"]["faixas"][1].update(minimo=6))
        self.recusa("N2", "DAD 5, GOV 3, CRI 6", "faixas sobrepostas ou incompletas")

    def test_11_autor_agente_recusa_com_evento_humano(self):
        self.recusa("N2", "DAD 5, GOV 3, CRI 6", "autor precisa ser pessoa nomeada", "AG-01")

    def test_12_nivel_desconhecido(self):
        self.recusa("N9", "DAD 5, GOV 3, CRI 6", "nao existe no playbook")

    def test_13_acima_da_faixa(self):
        self.recusa("N3", "DAD 4, GOV 3, CRI 10", "CRI 10 fora da faixa 3 a 9")

    def test_14_fracao_recusada(self):
        self.recusa("N2", "DAD 5.5, GOV 3, CRI 6", "formato dos eixos")

    def test_90_n2(self):
        self.positivo("N2", "DAD 5, GOV 3, CRI 6")

    def test_91_n3(self):
        self.positivo("N3", "DAD 4, GOV 3, CRI 8")

    def test_92_limite_3(self):
        self.positivo("N1", "DAD 3, GOV 3, CRI 3")

    def test_93_limite_4(self):
        self.positivo("N1", "DAD 4, GOV 3, CRI 3")

    def test_94_limite_5(self):
        self.positivo("N2", "DAD 5, GOV 3, CRI 3")

    def test_95_limite_7(self):
        self.positivo("N2", "DAD 3, GOV 7, CRI 3")

    def test_96_limite_8(self):
        self.positivo("N3", "DAD 3, GOV 3, CRI 8")

    def test_97_limite_9(self):
        self.positivo("N3", "DAD 9, GOV 3, CRI 3")

    def test_98_regra_alternativa_sem_valores_do_metodo_no_nucleo(self):
        def editar(pb):
            pb["apuracao_nivel"] = {
                "eixos": {e: {"minimo": 10, "maximo": 19} for e in ("X", "Y", "Z")},
                "agregacao": "maximo",
                "faixas": [{"minimo": 10, "maximo": 12, "nivel": "N1"},
                           {"minimo": 13, "maximo": 15, "nivel": "N2"},
                           {"minimo": 16, "maximo": 19, "nivel": "N3"}],
            }
        self.configurar(editar)
        self.positivo("N2", "X 14, Y 10, Z 11")


if __name__ == "__main__":
    unittest.main(verbosity=2)
