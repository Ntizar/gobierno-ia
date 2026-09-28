"""Extrae los articulos relevantes de la Ley 47/2003 General Presupuestaria (BOE-A-2003-21614)
y verifica la disponibilidad de conversion de PDF de la AEAT.
Uso: python extrae_lgp_2026-09-28.py
Salida: stdout (sin escribir ficheros).
"""
import re
import html as _html
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
LGP_HTML = os.path.join(BASE, "ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html")
IART_PDF = os.path.join(BASE, "AEAT-IART-2025-informe-anual-recaudacion-2026-09-28.pdf")

ARTICULOS = ["35", "36", "38", "42", "46", "47", "50", "52", "61", "62", "63", "64"]


def a_texto(raw):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = _html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


with open(LGP_HTML, encoding="utf-8", errors="replace") as fh:
    html = fh.read()
texto = a_texto(html)

print("=== LGP: fichero", os.path.basename(LGP_HTML), "bytes:", len(html), "palabras texto:", len(texto.split()))
print("Preceptos 'Artículo N.' detectados:", len(re.findall(r"(?m)^Artículo \d+\.", texto)))
print("Bloques 'Disposición' detectados:", len(re.findall(r"(?m)^Disposición[a-z ]*", texto)))

marcas = list(re.finditer(r"(?m)^Artículo (\d+)\.", texto))
rangos = {}
for i, m in enumerate(marcas):
    fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(texto)
    rangos[m.group(1)] = texto[m.start():fin]

for art in ARTICULOS:
    cuerpo = rangos.get(art)
    if not cuerpo:
        print("\n--- Artículo %s: NO LOCALIZADO" % art)
        continue
    limpio = re.sub(r"\s+", " ", cuerpo).strip()
    print("\n--- Artículo %s (%d palabras): %s" % (art, len(cuerpo.split()), limpio[:1400]))

print("\n=== IART 2025: fichero", os.path.basename(IART_PDF), "bytes:", os.path.getsize(IART_PDF))
print("pdftotext disponible:", bool(shutil.which("pdftotext")))
for mod in ("pypdf", "PyPDF2", "pdfminer"):
    try:
        __import__(mod)
        print("modulo PDF disponible:", mod)
    except Exception:
        print("modulo PDF NO disponible:", mod)
