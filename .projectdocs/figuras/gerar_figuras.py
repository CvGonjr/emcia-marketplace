"""Gera as figuras-tabela do PFC a partir de dados/*.json.

Uso:
    python gerar_figuras.py            # gera todas
    python gerar_figuras.py fig45      # gera só uma

Saída em saida/: <fig>.png (2x, para o Word) e <fig>.html (para conferência).
Requer: pip install playwright && python -m playwright install chromium
"""
import html
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).parent
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "saida"

# Identidade dos documentos controlados: Calibri, azul-petróleo, bordas finas.
CSS = """
:root { --petroleo:#1F3A4D; --tinta:#E9EFF3; --borda:#B7C3CC; --texto:#1E2A33;
        --neutro:#6B7780; --alerta:#8A4B0F; }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; color:var(--texto);
       background:#fff; padding:16px; width:max-content; }
table { border-collapse:collapse; font-size:15px; line-height:1.35; table-layout:fixed; }
th { background:var(--petroleo); color:#fff; font-weight:700; text-align:left;
     padding:8px 10px; border:1px solid var(--petroleo); vertical-align:bottom; }
td { padding:7px 10px; border:1px solid var(--borda); vertical-align:top; }
tr.grupo td { background:var(--tinta); color:var(--petroleo); font-weight:700; }
td.chave { font-weight:700; }
.ok { color:var(--petroleo); font-weight:700; }
.diverge { color:var(--alerta); font-weight:700; }
.pendente { color:var(--neutro); font-style:italic; }
strong { font-weight:700; }
"""

CLASSE_SITUACAO = [
    (re.compile(r"^(Confirmado|Coincide)"), "ok"),
    (re.compile(r"^(Diverge|Não previsto)"), "diverge"),
    (re.compile(r"^Não apurado"), "pendente"),
]


def formatar(texto: str) -> str:
    """Escapa HTML e converte **negrito** e quebras de linha."""
    t = html.escape(texto)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t.replace("\n", "<br>")


def celula_situacao(texto: str) -> str:
    for padrao, classe in CLASSE_SITUACAO:
        if padrao.match(texto):
            return f'<td class="{classe}">{formatar(texto)}</td>'
    return f"<td>{formatar(texto)}</td>"


def montar_html(fig: dict) -> str:
    colunas = fig["colunas"]
    col_sit = fig.get("coluna_situacao")
    largura = "".join(f'<col style="width:{c["largura"]}px">' for c in colunas)
    cab = "".join(f"<th>{formatar(c['titulo'])}</th>" for c in colunas)
    linhas = []
    for linha in fig["linhas"]:
        if "grupo" in linha:
            linhas.append(f'<tr class="grupo"><td colspan="{len(colunas)}">'
                          f'{formatar(linha["grupo"])}</td></tr>')
            continue
        tds = []
        for i, valor in enumerate(linha["celulas"]):
            if i == col_sit:
                tds.append(celula_situacao(valor))
            elif i == 0:
                tds.append(f'<td class="chave">{formatar(valor)}</td>')
            else:
                tds.append(f"<td>{formatar(valor)}</td>")
        linhas.append("<tr>" + "".join(tds) + "</tr>")
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f"<style>{CSS}</style></head><body><table><colgroup>{largura}</colgroup>"
            f"<thead><tr>{cab}</tr></thead><tbody>{''.join(linhas)}</tbody>"
            f"</table></body></html>")


def gerar(nomes: list[str]) -> None:
    SAIDA.mkdir(exist_ok=True)
    arquivos = [DADOS / f"{n}.json" for n in nomes] if nomes else sorted(DADOS.glob("*.json"))
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(device_scale_factor=2)
        for arq in arquivos:
            fig = json.loads(arq.read_text(encoding="utf-8"))
            doc = montar_html(fig)
            (SAIDA / f"{arq.stem}.html").write_text(doc, encoding="utf-8")
            pagina.set_content(doc, wait_until="networkidle")
            pagina.locator("body").screenshot(path=str(SAIDA / f"{arq.stem}.png"))
            print(f"ok  {arq.stem}.png")
        navegador.close()


if __name__ == "__main__":
    gerar(sys.argv[1:])
