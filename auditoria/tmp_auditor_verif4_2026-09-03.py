# -*- coding: utf-8 -*-
import io, re, json
REPO = "C:/Users/d_ant/Projects/gobierno-ia"
html = io.open(REPO + "/ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()
ht = re.sub(r"<[^>]+>", " ", html)
ht = (ht.replace("&nbsp;", " ").replace("&#8217;", "'").replace("&#171;", "«").replace("&#187;", "»").replace("&amp;", "&"))
ht = re.sub(r"\s+", " ", ht).lower()
bak = io.open(REPO + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-02-da18", encoding="utf-8").read()
m = re.search(r"(?ms)^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[|\Z)", bak)
body = m.group(1)
paras = [re.sub(r"\s+", " ", p.strip()) for p in body.split("\n\n") if p.strip() and p.strip() != "## [dadecimoctava]"]
ghost_w = 0; ghost_n = 0
for p in paras:
    pl = p.lower()
    probe = pl[:80]
    if probe not in ht:
        ghost_n += 1; ghost_w += len(p.split())
print("DA18 antiguo: parrafos:", len(paras), "| SIN traza en BOE:", ghost_n, "parrafos,", ghost_w, "palabras")
# 532 coverage
h7 = io.open(REPO + "/ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html", encoding="utf-8", errors="replace").read()
h7t = re.sub(r"<[^>]+>", " ", h7)
h7t = re.sub(r"&#\d+;", "", h7t)
h7t = (h7t.replace("&nbsp;", " ").replace("&#8217;", "'").replace("&amp;", "&"))
h7t = re.sub(r"\s+", " ", h7t).lower()
j = json.load(io.open(REPO + "/ministerios/transicion-ecologica/evidencia/clasificacion_deuda_55_lineas_2026-09-03.json", encoding="utf-8"))
g = j["omision_real_fuerza_obligatoria"] if "omision_real_fuerza_obligatoria" in j else None
if g:
    rows = g if isinstance(g, list) else g.get("lineas", [])
    hit = 0; tot = 0; miss = []
    for r in rows:
        txt = r if isinstance(r, str) else (r.get("texto") or r.get("linea") or "")
        t = re.sub(r"\s+", " ", txt.strip().lower())
        if len(t.split()) < 4: continue
        tot += 1
        if t[:70] in h7t: hit += 1
        else: miss.append(txt[:60])
    print("532-JSON: filas con texto:", tot, "| localizadas en BOE:", hit, "| no:", len(miss))
    for x in miss[:5]: print("   MISS70:", x)
