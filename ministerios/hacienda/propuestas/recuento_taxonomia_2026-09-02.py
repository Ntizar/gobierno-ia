# Recuento can6n6nico de la taxonom6a LGT desde mi propio JSON del 09-01
# (para cuadrar las cifras 161/76 vs 139/84 antes de firmar, observaci6n del Auditor a13)
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open("../evidencia/fidelidad_LGT_total_2026-09-01.json", encoding="utf-8"))
print("total casos:", len(d))
from collections import Counter, defaultdict
c = Counter(x["v"] for x in d)
print("por veredicto:", dict(c))
pal = defaultdict(int); bloques = defaultdict(set)
for x in d:
    pal[x["v"]] += x.get("palabras", 0)
    bloques[x["v"]].add(x["bloque"])
for v in c:
    print(f"  {v}: {c[v]} casos | {pal[v]} palabras | {len(bloques[v])} bloques distintos")
cp = [x for x in d if x["v"] == "contenido_perdido"]
print("BLOQUES DISTINTOS con contenido_perdido:", len(set(x['bloque'] for x in cp)))
print("PALABRAS contenido_perdido (1ª ocurrencia por bloque+letra):")
seen = set(); tot = 0
for x in cp:
    k = (x["bloque"], x.get("letra_a","")[:60])
    if k in seen: continue
    seen.add(k); tot += x.get("palabras", 0)
print("  ->", tot)
# huérfanas = casos que el BOE sí tiene (contenido_perdido + solo_marca?) — definiciones
print("huérfanas seg6n titular acta: 139 | seg6n JSON: contenido_perdido", c.get("contenido_perdido"))
print("solo_marca:", c.get("solo_marca"), "| boe_sin_a:", c.get("boe_sin_a"), "| no_localizable:", c.get("no_localizable"))
