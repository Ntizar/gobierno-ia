# Ver claves reales de un registro del JSON letras_a
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
d = json.load(open("../evidencia/fidelidad_letras_a_2026-09-01.json", encoding="utf-8"))
reg = d["registro"] if isinstance(d, dict) and "registro" in d else (d["casos"] if isinstance(d, dict) and "casos" in d else d)
print("total:", len(reg))
print("claves:", sorted(reg[0].keys()))
print("ejemplo:", json.dumps(reg[0], ensure_ascii=False)[:300])
import collections
cnt = collections.Counter()
bloq = collections.defaultdict(set)
for r in reg:
    cat = None
    for k in ("categoria", "v", "clase", "tipo"):
        if k in r: cat = r[k]; break
    b = None
    for k in ("bloque", "b", "slug"):
        if k in r: b = r[k]; break
    cnt[cat]+=1; bloq[cat].add(b)
print(cnt)
print("bloques F1:", len(bloq.get("contenido_perdido", set())))
