# Reconocimiento del JSON LGT total + manifiesto de letras a del 09-01 (para reejecutar metodo hoy)
import json, io, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open("../evidencia/fidelidad_LGT_total_2026-09-01.json", encoding="utf-8"))
print("=== LGT_total tipo:", type(d).__name__)
if isinstance(d, dict):
    for k, v in d.items():
        print(" clave:", k, "->", type(v).__name__, (len(v) if hasattr(v, "__len__") else v))
recs = d if isinstance(d, list) else None
if recs is None:
    for k in ("registros","bloques","casos","items"):
        if k in d: recs = d[k]; break
print("num registros:", len(recs) if recs else 0)
if recs:
    ks = collections.Counter()
    for r in recs[:500]: ks.update(r.keys())
    print("campos:", dict(ks))
    print("ejemplo:", json.dumps(recs[0], ensure_ascii=False)[:500])
    bl = collections.Counter(str(r.get("bloque")) for r in recs)
    print("bloques distintos:", len(bl), "top:", bl.most_common(5))
