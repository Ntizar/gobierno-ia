# -*- coding: utf-8 -*-
# Pasada de cierre: hash DA18 vigente, palabras totales LGT, dup-bloques LGS, tramo adiez/adiecinueve, L7 residuales
import io, re, json, hashlib
from collections import Counter
REPO = "C:/Users/d_ant/Projects/gobierno-ia"

def norm(s): return re.sub(r"\s+", " ", s.strip().lower())

def blocks(text):
    out = []
    cur = None
    for l in text.splitlines():
        m = re.match(r"^## \[([^\]]+)\] (.*)$", l)
        if m:
            cur = {"id": m.group(1), "lines": []}
            out.append(cur)
        elif cur is not None:
            cur["lines"].append(l)
    return out

lgt = io.open(REPO + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
bs = blocks(lgt)
d18 = next(b for b in bs if b["id"] == "dadecimoctava")
body = "\n".join(d18["lines"])
print("A) DA18 vigente: paras(no vac):", len([l for l in d18['lines'] if l.strip()]), "| palabras:", len(body.split()), "| sha256(norm):", hashlib.sha256(norm(body).encode()).hexdigest()[:12], "(decl:11c84ad1...)")
print("B) LGT palabras totales fichero:", len(lgt.split()), "(decl:142.992)")

lgs = io.open(REPO + "/ministerios/sanidad/leyes/BOE-A-1986-10499.md", encoding="utf-8").read()
dupb = 0
for b in blocks(lgs):
    seen = set(); dup = False
    for l in b["lines"]:
        if not l.strip(): continue
        h = hashlib.sha256(l.strip().encode()).hexdigest()[:12]
        if h in seen: dup = True
        seen.add(h)
    dupb += dup
print("C) LGS bloques con dup ahora:", dupb, "(decl:18)")

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
for b in ["[adiez]", "[adiecinueve]"]:
    sub = [c for c in cases if c["bloque"] == b and catof(c) == "contenido_perdido"]
    print("D)", b, len(sub), "casos F1,", sum(int(c.get("palabras", 0)) for c in sub), "pal (decl: 692 y 92)")

l7 = io.open(REPO + "/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md", encoding="utf-8").read()
for b in blocks(l7):
    seen = Counter()
    for l in b["lines"]:
        if l.strip(): seen[l.strip()] += 1
    for k, v in seen.items():
        if v > 1:
            print("E) L7 dup residual en", b["id"], "x", v, ":", k[:70], "| palabras repetidas:", len(k.split()) * (v - 1))
