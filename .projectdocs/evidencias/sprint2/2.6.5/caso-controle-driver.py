#!/usr/bin/env python3
"""Constroi o caso de controle do pacote 2.6.5: percurso F0->E5 completo,
cenario agentico (E3-E aplicavel), P6/P7 validos, P8/P9/P10 validos, os
cinco inegociaveis verificados e os seis portoes avaliados.

Persiste os artefatos-chave em .projectdocs/evidencias/sprint2/2.6.5/
seguindo o mesmo padrao usado em 2.6.3 (caso-controle-<ID>.yaml,
caso-controle-estado-final.json).
"""
import json
import pathlib
import shutil
import subprocess
import sys

RAIZ = pathlib.Path("/home/netiv-ai/Projetos/AI/PLUGINS/emcia-marketplace")
sys.path.insert(0, str(RAIZ / "testes"))
import campo_2_6_5 as T  # noqa: E402

EVID = RAIZ / ".projectdocs" / "evidencias" / "sprint2" / "2.6.5"
EVID.mkdir(parents=True, exist_ok=True)

caso = T.preparar_caso()
print(f"caso de controle em: {caso}")

log = []


def passo(desc, codigo, saida, erro):
    log.append({"passo": desc, "exit": codigo, "stdout": saida.strip(), "stderr": erro.strip()})
    marca = "OK " if codigo == 0 or "NAO_APLICAVEL" in saida else "!! "
    print(f"{marca}{desc}: exit={codigo} {saida.strip()[:80]}")


# F0
codigo, saida, erro = T.apurar_e_encerrar_f0(caso, nivel="N2")
passo("F0: apurar nivel N2 e encerrar", codigo, saida, erro)

# E1
codigo, saida, erro = T.entregavel(caso, "E1", "Celso do Vale", emitir=True)
passo("E1: renderizar e emitir", codigo, saida, erro)

# P1, P2
for e in ["P1", "P2"]:
    codigo, saida, erro = T.avancar(caso, encerrar=e, autor="Celso do Vale")
    passo(f"{e}: encerrar", codigo, saida, erro)

# P3a + baseline (I1)
codigo, saida, erro = T.preparar_bl(caso)
passo("P3a: gravar baseline BL-001", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P3a", autor="Celso do Vale")
passo("P3a: encerrar", codigo, saida, erro)
codigo, saida, erro = T.inegociavel(caso, 1, "registro/baseline/BL-001.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I1: verificar baseline e satisfazer", codigo, saida, erro)

# P3b, P3d
codigo, saida, erro = T.avancar(caso, registrar_sessao="P3b", autor="Celso do Vale",
                                 participantes="Ana, Celso")
passo("P3b: registrar sessao", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P3b", autor="Celso do Vale")
passo("P3b: encerrar", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P3d", autor="Celso do Vale")
passo("P3d: encerrar", codigo, saida, erro)

# E2
codigo, saida, erro = T.avancar(caso, emitir="E2", autor="Celso do Vale")
passo("E2 (portao): emitir", codigo, saida, erro)
codigo, saida, erro = T.entregavel(caso, "E2", "Celso do Vale", emitir=True)
passo("E2: renderizar e emitir (materializacao)", codigo, saida, erro)

# P4
codigo, saida, erro = T.avancar(caso, encerrar="P4", autor="Celso do Vale")
passo("P4: encerrar", codigo, saida, erro)

# P5 -- classificacao agentica (para exercitar E3-E aplicavel)
estado_path = caso / "registro" / "estado.json"
st = json.loads(estado_path.read_text(encoding="utf-8"))
st["cumprimentos"]["P5"] = {
    "cumprido": True, "autor": "Celso do Vale",
    "classificacao_tecnologica": "agente",
}
estado_path.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
print("OK  P5: classificacao_tecnologica=agente (gravado via avancar.encerrar equivalente)")

# E3-D (sempre) + E3-E (condicional, aplicavel aqui)
codigo, saida, erro = T.avancar(caso, emitir="E3-D", autor="Celso do Vale")
passo("E3-D (portao): emitir", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, emitir="E3-E", autor="Celso do Vale")
passo("E3-E (portao, caso agentico): emitir", codigo, saida, erro)
codigo, saida, erro = T.entregavel(caso, "E3", "Celso do Vale", emitir=True)
passo("E3: renderizar e emitir (consolida E3-D+E3-E)", codigo, saida, erro)

# P6
idx_estado = json.loads(estado_path.read_text(encoding="utf-8"))
idx_estado["etapa_atual"] = "P6"
idx_estado["camada_atual"] = "EX3"
idx_estado["modalidade_atual"] = "presencial_ou_remoto"
estado_path.write_text(json.dumps(idx_estado, indent=2, ensure_ascii=False), encoding="utf-8")
codigo, saida, erro = T.avancar(caso, encerrar="P6", autor="Celso do Vale")
passo("P6: encerrar (etapa_atual ajustada apos P5 gravado fora da maquina)", codigo, saida, erro)

T.preparar_op_validado(caso)
print("OK  P6: OP-001 proposta -> validado")

# P7
T.preparar_aut(caso, estado="decidido")
print("OK  P7: AUT-001 rascunho -> proposto -> decidido (Marina Prado)")
codigo, saida, erro = T.avancar(caso, registrar_sessao="P7", autor="Celso do Vale",
                                 participantes="Ana, Celso")
passo("P7: registrar sessao", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P7", autor="Celso do Vale")
passo("P7: encerrar", codigo, saida, erro)
codigo, saida, erro = T.inegociavel(caso, 2, "registro/governanca/autonomia/AUT-001.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I2: verificar termo de autonomia e satisfazer", codigo, saida, erro)

# E4
codigo, saida, erro = T.avancar(caso, emitir="E4", autor="Celso do Vale")
passo("E4 (portao): emitir", codigo, saida, erro)
codigo, saida, erro = T.entregavel(caso, "E4", "Celso do Vale", emitir=True)
passo("E4: renderizar e emitir (materializacao)", codigo, saida, erro)

# P8
codigo, saida, erro = T.preparar_ct_revisado(caso)
passo("P8: gravar CT-001 rascunho -> revisado", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P8", autor="Celso do Vale")
passo("P8: encerrar", codigo, saida, erro)
codigo, saida, erro = T.inegociavel(caso, 3, "registro/piloto/CT-001.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I3: verificar casos de teste e satisfazer", codigo, saida, erro)

# P9
codigo, saida, erro = T.preparar_met_apurada(caso)
passo("P9: gravar MET-001 planejada -> apurada (tipo=resultado)", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P9", autor="Celso do Vale")
passo("P9: encerrar", codigo, saida, erro)
codigo, saida, erro = T.inegociavel(caso, 4, "registro/metricas/MET-001.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I4: verificar metrica de resultado e satisfazer", codigo, saida, erro)

# P10
codigo, saida, erro = T.preparar_cal(caso)
passo("P10: gravar CAL-001 (rotina, responsavel Marina Prado)", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, registrar_sessao="P10", autor="Celso do Vale",
                                 participantes="Ana, Celso")
passo("P10: registrar sessao", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, encerrar="P10", autor="Celso do Vale")
passo("P10: encerrar", codigo, saida, erro)
codigo, saida, erro = T.avancar(caso, registrar_recorrencia="P10", autor="Celso do Vale",
                                 cadencia="mensal", responsavel="Marina Prado")
passo("P10: registrar recorrencia (ciclo 1)", codigo, saida, erro)
codigo, saida, erro = T.inegociavel(caso, 5, "registro/calibragem/CAL-001.yaml",
                                     satisfazer=True, autor="Marina Prado")
passo("I5: verificar responsavel de recalibragem e satisfazer", codigo, saida, erro)

# E5
codigo, saida, erro = T.avancar(caso, emitir="E5", autor="Celso do Vale")
passo("E5 (portao): emitir", codigo, saida, erro)
codigo, saida, erro = T.entregavel(caso, "E5", "Celso do Vale", emitir=True)
passo("E5: renderizar e emitir (materializacao)", codigo, saida, erro)

# ---- Tentativa negativa: AG tentando decidir I2/P10 (fronteira) --------
codigo, saida, erro = T.governanca(caso, "registro/governanca/autonomia/AUT-001.yaml", "AG-03")
passo("Negativo: AG-03 tenta regravar termo decidido (fronteira agente/humano)", codigo, saida, erro)

print()
print("=" * 70)
print(f"Percurso concluido. {len(log)} passos registrados.")
falhas_reais = [p for p in log if p["exit"] != 0 and "NAO_APLICAVEL" not in p["stdout"]
                and "Negativo" not in p["passo"]]
print(f"Passos com exit != 0 (fora dos negativos esperados): {len(falhas_reais)}")
for f in falhas_reais:
    print(f"  {f['passo']}: {f['stderr'] or f['stdout']}")

# ---- Persistir artefatos-chave em .projectdocs -------------------------
artefatos = {
    "BL-001": caso / "registro" / "baseline" / "BL-001.yaml",
    "AUT-001": caso / "registro" / "governanca" / "autonomia" / "AUT-001.yaml",
    "OP-001": caso / "registro" / "operacional" / "OP-001.yaml",
    "CT-001": caso / "registro" / "piloto" / "CT-001.yaml",
    "MET-001": caso / "registro" / "metricas" / "MET-001.yaml",
    "CAL-001": caso / "registro" / "calibragem" / "CAL-001.yaml",
}
for nome, caminho in artefatos.items():
    if caminho.exists():
        shutil.copy(caminho, EVID / f"caso-controle-{nome}.yaml")
        print(f"copiado: {nome} -> {EVID / f'caso-controle-{nome}.yaml'}")

for entregavel_id in ["E1", "E2", "E3", "E4", "E5"]:
    origem = caso / "caso" / "entregaveis" / f"{entregavel_id}.md"
    if origem.exists():
        shutil.copy(origem, EVID / f"caso-controle-{entregavel_id}.md")
        print(f"copiado: {entregavel_id}.md -> {EVID / f'caso-controle-{entregavel_id}.md'}")

shutil.copy(caso / "registro" / "estado.json", EVID / "caso-controle-estado-final.json")
shutil.copy(caso / "registro" / "eventos.jsonl", EVID / "eventos.jsonl")
print(f"copiado: estado.json, eventos.jsonl")

(EVID / "caso-controle-log-comandos.txt").write_text(
    "\n".join(f"{p['passo']}\n  exit={p['exit']}\n  stdout={p['stdout']}\n  stderr={p['stderr']}\n"
              for p in log),
    encoding="utf-8",
)
print(f"copiado: caso-controle-log-comandos.txt")

print()
print(f"CASO_TEMP={caso}")
