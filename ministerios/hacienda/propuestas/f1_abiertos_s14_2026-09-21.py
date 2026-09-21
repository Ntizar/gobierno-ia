import json, re
from collections import defaultdict

p = "ministerios/hacienda/evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json"
with open(p, encoding="utf-8") as f:
    m = json.load(f)

# F1 = contenido_perdido
f1 = [c for c in m["casos_fidelidad"] if c["v"] == "contenido_perdido"]
print("F1 manifiesto 09-02:", len(f1), "casos,", sum(c["palabras"] for c in f1), "pal,", len({c['bloque'] for c in f1}), "bloques")

# cerrados verificados 09-04 (del reconciliacion)
per_bloque = {"[a7]":1,"[a8]":1,"[a15]":2,"[a27]":1,"[a150]":11,"[a271]":1,"[dadecimoctava]":3}
def closed_count(b, casos):
    want = per_bloque.get(b, 0)
    return want
# remove them (by first-N per block, order = manifiesto order)
seen = defaultdict(int)
rest = []
for c in f1:
    b = c["bloque"]
    if b in per_bloque and seen[b] < per_bloque[b]:
        seen[b] += 1
        continue
    rest.append(c)
print("tras cerrar 09-04:", len(rest), "casos,", sum(c["palabras"] for c in rest), "pal,", len({c['bloque'] for c in rest}), "bloques")

# Los 4 acuerdos ejecutados de Hacienda: ¿llevaban casos F1?
acuerdos = ["[a12]", "[a62]", "[a95]", "[a43]"]
byb = defaultdict(lambda: [0, 0, []])
for c in rest:
    byb[c["bloque"]][0] += 1
    byb[c["bloque"]][1] += c["palabras"]
    byb[c["bloque"]][2].append(c)
for a in acuerdos:
    d = byb.get(a)
    print(a, "->", (d[0], d[1]) if d else "sin casos F1")

inv = {b: (d[0], d[1]) for b, d in byb.items()}
print("total abiertos:", sum(v[0] for v in inv.values()), "casos /", len(inv), "bloques /", sum(v[1] for v in inv.values()), "pal")

# ranking por bloque
def keynum(b):
    mm = re.match(r"\[a(\d+)\]", b)
    return (0, int(mm.group(1))) if mm else (1, 0)
ranked = sorted(inv.items(), key=lambda kv: (-kv[1][1], keynum(kv[0])))
print("\nTOP 20 bloques F1 abiertos (por palabras):")
for b, (n, w) in ranked[:20]:
    print(f"{b}: {n} casos / {w} pal")

# guardar inventario para consulta posterior
out = {b: {"casos": n, "palabras": w} for b, (n, w) in ranked}
with open("ministerios/hacienda/evidencia/f1_abiertos_2026-09-21.json", "w", encoding="utf-8") as f:
    json.dump({"fuente": "MANIFIESTO_MASIVO_LGT_2026-09-02.json (F1=contenido_perdido) menos 20 casos/734 pal cerrados y verificados el 2026-09-04",
               "total": {"casos": sum(v[0] for v in inv.values()), "bloques": len(inv), "palabras": sum(v[1] for v in inv.values())},
               "bloques": out}, f, ensure_ascii=False, indent=1)
print("\nescrito evidencia/f1_abiertos_2026-09-21.json")
