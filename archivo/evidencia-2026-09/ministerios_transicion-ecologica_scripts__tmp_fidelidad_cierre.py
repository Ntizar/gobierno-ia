# -*- coding: utf-8 -*-
"""Sesion 4 - CIERRE del test de fidelidad BOE (3 checks deterministas)."""
import re, html
from collections import Counter

MD = "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
BOE = "ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html"

def norm(s):
    s = s.replace("\u00a0", " ").replace("\r", " ")
    s = re.sub(r"[«»\"'’`´]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def load_lines(path):
    h = open(path, encoding="utf-8").read()
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    hu = html.unescape(re.sub(r"<[^>]+>", "\n", h))
    return [norm(l) for l in hu.split("\n") if l.strip()]

boe = load_lines(BOE); md = load_lines(MD)

# ---- CHECK 1: titulos de articulos/disposiciones (unicos) ----
HEAD = re.compile(r"^(Art[íi]culo \d+[^\d]|Disposici[óo]n (adicional|transitoria|final|regulatoria) \w+\.|T[íi]tulo [IVXL]+\.|TÍTULO [IVXL]+)«")
def titles(lines):
    t = []
    for x in lines:
        m = re.match(r"^(Art[íi]culo \d+\.|Disposici[óo]n (?:adicional|transitoria|final|regulatoria) \w+\.|T[íi]tulo [IVXL]+\.|TÍTULO [IVXL]+) ", x)
        if m and len(x) < 160:
            t.append(norm(x))
    return t
bt, mt = set(titles(boe)), set(titles(md))
print("CHECK 1 titulos de bloque: BOE", len(bt), "| repo", len(mt),
      "| faltan en repo:", len([x for x in bt if x.split('.')[0] not in " ".join(mt)]))
for x in sorted(bt):
    if x not in mt:
        print("   -", x[:80])

# ---- CHECK 2: secuencia de letras ----
LET = "abcdefghilmnoprstuv"
pat = re.compile(r"^([%s]\)) " % LET)
def seq(lines):
    return [pat.match(x).group(1) for x in lines if pat.match(x)]
bseq, mseq = seq(boe), seq(md)
cb, cm = Counter(bseq), Counter(mseq)
solo_repo = {k: cm[k] - cb.get(k, 0) for k in cm if cm[k] > cb.get(k, 0)}
solo_boe = {k: cb[k] - cm.get(k, 0) for k in cb if cm.get(k, 0) < cb[k]}
print("CHECK 2 letras a)-v): BOE", len(bseq), "| repo", len(mseq))
print("   exceso en repo (lineas de versiones duplicadas del art.15):", solo_repo or "0")
print("   faltan en repo respecto al BOE:", solo_boe or "0")

# ---- CHECK 3: truncamientos (preambulo si, cuerpo no) ----
print("CHECK 3 truncamientos:")
for probe, desc, body in [
    ("quedan redactados en los siguientes términos", "df-4 preámbulo", "Las sociedades que realizan actividades reguladas no podrán otorgar préstamos"),
    ("El objeto de la presente ley es", "art.2", None),
    ("Desarrollo sostenible", "objeto DF-15/9", None),
    ("Antes de 2050", "art.3.2", None),
]:
    in_boe = any(probe in x for x in boe); in_repo = any(probe in x for x in md)
    line = "   %-18s BOE=%s repo=%s" % (desc, in_boe, in_repo)
    if body:
        line += " | cuerpo en repo=%s" % any(body in x for x in md)
    print(line)
