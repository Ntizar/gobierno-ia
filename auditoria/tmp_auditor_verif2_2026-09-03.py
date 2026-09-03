# -*- coding: utf-8 -*-
# Ultima pasada: (1) recount duplicados LGT conv. ministerial tras DA18
# (2) ¿las lineas borradas de DA18 existen en el BOE archivado? (prueba X1)
# (3) aritmetica tramo 1-30 del manifiesto con corchetes
import io, re, json, hashlib
REPO = "C:/Users/d_ant/Projects/gobierno-ia"

lgt = io.open(REPO + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
blocks = []
cur = None
for l in lgt.splitlines():
    m = re.match(r"^## \[([^\]]+)\] (.*)$", l)
    if m:
        cur = {"id": m.group(1), "lines": []}
        blocks.append(cur)
    elif cur is not None:
        cur["lines"].append(l)
tot_dup = 0
for b in blocks:
    seen = {}
    for l in b["lines"]:
        if not l.strip(): continue
        h = hashlib.sha256(l.strip().encode()).hexdigest()[:12]
        seen.setdefault(h, []).append(l.strip())
    tot_dup += sum(len(v[0].split()) * (len(v) - 1) for v in seen.values() if len(v) > 1)
print("1) LGT bloques:", len(blocks), "| palabras dup intra-bloque AHORA:", tot_dup, "(KPI declara 44.071 sin actualizar)")

# (2) diff DA18 vs BOE archivado
d = io.open(REPO + "/ministerios/hacienda/evidencia/diff_reparacion_DA18_2026-09-02.md", encoding="utf-8").read()
html = io.open(REPO + "/ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()
ht = re.sub(r"<[^>]+>", " ", html)
ht = (ht.replace("&nbsp;", " ").replace("&#8217;", "'").replace("&#171;", "«").replace("&#187;", "»").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))
ht = re.sub(r"\s+", " ", ht).lower()
deleted = [re.sub(r"\s+", " ", l[1:].strip()).lower() for l in d.splitlines() if l.startswith("-") and not l.startswith("---") and len(l.strip()) > 10]
found = sum(1 for x in deleted if x[:70] in ht)
print("2) lineas borradas DA18:", len(deleted), "| con traza en BOE archivado:", found, "| SIN traza:", len(deleted) - found)
for x in deleted:
    if x[:70] not in ht and len(x.split()) >= 8:
        print("   GHOST:", x[:100])

# (3) tramo
mf = json.load(io.open(REPO + "/ministerios/hacienda/evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
cases = []
def rl(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and "bloque" in o[0]:
        cases.extend(o); return
    if isinstance(o, dict):
        for v in o.values(): rl(v)
    elif isinstance(o, list):
        for v in o: rl(v)
rl(mf)
def catof(c):
    for k in ("tipo", "categoria", "v"):
        if isinstance(c.get(k), str): return c[k]
c1 = [c for c in cases if catof(c) == "contenido_perdido"]
tot = 0
for b in ["[a7]", "[a8]", "[a15]", "[a27]"]:
    sub = [c for c in c1 if c["bloque"] == b]
    w = sum(int(c.get("palabras", 0)) for c in sub)
    tot += w
    print("3)", b, len(sub), "casos", w, "pal")
print("   total tramo:", tot, "pal | declarado: 5+46+38+32=121")
res = [c for c in c1 if c["bloque"] not in ("[a7]", "[a8]", "[a15]", "[a27]", "[dadecimoctava]")]
print("   F1 restantes segun manifiesto:", len(res), "casos,", sum(int(c.get("palabras", 0)) for c in res), "pal,", len(set(c["bloque"] for c in res)), "bloques | declarado: 120/3.192/73")
# casos DA18 en manifiesto (cualquier categoria)
dsub = [c for c in cases if c["bloque"] == "[dadecimoctava]"]
print("   casos DA18 en manifiesto:", len(dsub), "pal", sum(int(c.get("palabras", 0)) for c in dsub), "| categorias:", set(catof(c) for c in dsub))
# ls evidencia sanidad
import os
print("4) evidencia Sanidad:", sorted(os.listdir(REPO + "/ministerios/sanidad/evidencia"))[-12:])
