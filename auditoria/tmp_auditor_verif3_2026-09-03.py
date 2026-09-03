# -*- coding: utf-8 -*-
# Pasada de precision antes de firmar: categorias del manifiesto, hash DA18 conv exacta, sonda larga 939
import io, re, json, hashlib
from collections import Counter
REPO = "C:/Users/d_ant/Projects/gobierno-ia"

# 1) categorias del manifiesto
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
cnt = Counter((c["bloque"], catof(c)) for c in cases)
by_cat = Counter(catof(c) for c in cases)
print("1) categorias globales:", dict(by_cat))
print("   total casos:", len(cases))
# F1 = contenido_perdido + variantes? ver clave del manifiesto
print("   claves raiz JSON:", list(mf)[:8] if isinstance(mf, dict) else "lista")
d18c = [c for c in cases if c["bloque"] == "[dadecimoctava]"]
print("   DA18:", len(d18c), "casos ->", dict(Counter(catof(c) for c in d18c)))

# 2) hash DA18 vigente con la convencion EXACTA del ministerio (sin minusculas)
lgt = io.open(REPO + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
m = re.search(r"(?ms)^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[|\Z)", lgt)
body = m.group(1)
conv = re.sub(r"\s+", " ", body).strip()
print("2) sha256 norm(sin lower):", hashlib.sha256(conv.encode()).hexdigest()[:16])
# conv con minusculas del ministerio? buscar en el script
sc = io.open(REPO + "/ministerios/hacienda/propuestas/apply_da18_2026-09-03.py", encoding="utf-8").read()
print("   funcion norm del script:", re.search(r"def norm.*", sc).group(0))

# 3) sonda larga de palabras fantasma DA18 (150 chars)
html = io.open(REPO + "/ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()
ht = re.sub(r"<[^>]+>", " ", html)
ht = (ht.replace("&nbsp;", " ").replace("&#8217;", "'").replace("&#171;", "«").replace("&#187;", "»").replace("&amp;", "&"))
ht = re.sub(r"\s+", " ", ht).lower()
bak = io.open(REPO + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-02-da18", encoding="utf-8").read()
mb = re.search(r"(?ms)^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[|\Z)", bak)
paras = [re.sub(r"\s+", " ", p.strip()).lower() for p in mb.group(1).split("\n\n") if len(p.strip()) > 20]
for probe in (120, 150, 200, len_max:=300):
    ghost = [p for p in paras if p[:probe] not in ht]
    print("3) probe", probe, "-> sin traza:", len(ghost), "parrafos,", sum(len(g.split()) for g in ghost), "palabras")
