# -*- coding: utf-8 -*-
"""Sesion 21/30 (2026-09-30) - Ministerio de Transicion Ecologica (Sara Aagesen).
Extraccion PROPIA y reproducible de la Ley 47/2003 General Presupuestaria desde el fichero
que YA esta en el repo (descarga de Hacienda, acuerdo 100 de la sesion 19).
Deja el texto limpio en evidencia/lgp_texto_limpio_s21_ecologia_2026-09-30.txt para que
cualquier cita «fichero y linea» sea reproducible por el Auditor sin volver a parsear el HTML.
Uso:  python extrae_lgp_s21_ecologia_2026-09-30.py
"""
import hashlib, html as H, io, os, re

REPO = "C:/Users/d_ant/Projects/gobierno-ia"
SRC = os.path.join(REPO, "ministerios/hacienda/evidencia",
                   "ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html")
DST = os.path.join(REPO, "ministerios/transicion-ecologica/evidencia",
                   "lgp_texto_limpio_s21_ecologia_2026-09-30.txt")

raw = io.open(SRC, "rb").read()
print("fichero fuente:", SRC)
print("bytes:", len(raw), "| sha256:", hashlib.sha256(raw).hexdigest())
m = re.search(r"<title>(.*?)</title>", raw.decode("utf-8", "replace"), re.S)
print("title:", " ".join(m.group(1).split()) if m else None)

txt = re.sub(r"<script.*?</script>", " ", raw.decode("utf-8", "replace"), flags=re.S)
txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
txt = H.unescape(re.sub(r"<[^>]+>", "\n", txt))
lines = [l for l in (" ".join(x.split()) for x in txt.split("\n")) if l]
io.open(DST, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("texto limpio ->", DST, "| lineas:", len(lines))

idx = {}
for i, l in enumerate(lines):
    mm = re.match(r"^Artículo (\d+)\.\s*(.*)$", l)
    if mm and int(mm.group(1)) not in idx:
        idx[int(mm.group(1))] = i
CITADOS = [42, 45, 46, 49, 52, 58, 61, 62, 63]
print("\nLINEAS DE LOS ARTICULOS CITADOS HOY (fichero y linea):")
for n in CITADOS:
    print(f"  art. {n}: linea {idx.get(n)} | {lines[idx[n]][:88]}")
print("\nTEXTO LITERAL QUE SOSTIENE LA PROPUESTA DE HOY:")
for n, hi in ((42, 1), (45, 1), (46, 1), (49, 3), (52, 10), (58, 2), (62, 2), (63, 3)):
    print("\n--- art.", n)
    for i in range(idx[n], min(idx[n] + hi + 1, len(lines))):
        print(f"[{i}] {lines[i][:300]}")
