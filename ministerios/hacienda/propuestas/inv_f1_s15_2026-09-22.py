# -*- coding: utf-8 -*-
"""Ranking F1 abierto a 2026-09-22 (sesión 14): reconstruye el ranking desde
evidencia/f1_abiertos_2026-09-21.json y lo ordena por palabras por bloque."""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

p = "ministerios/hacienda/evidencia/f1_abiertos_2026-09-21.json"
d = json.load(open(p, encoding="utf-8"))
print("top-level keys:", list(d.keys()) if isinstance(d, dict) else "LISTA len=%d" % len(d))

# intentos genéricos de localizar el ranking por bloque
def as_blocks(obj):
    if isinstance(obj, list):
        return obj
    for k in ("bloques", "por_bloque", "ranking", "casos", "f1", "items"):
        if isinstance(obj, dict) and k in obj:
            v = obj[k]
            return v if isinstance(v, list) else as_blocks(v)
    return None

blocks = as_blocks(d)
if blocks:
    print("n_entries:", len(blocks))
    print("sample[0]:", json.dumps(blocks[0], ensure_ascii=False)[:600])
    # agrupar por bloque si los casos son planos
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0])
    for b in blocks:
        if isinstance(b, dict):
            key = b.get("bloque") or b.get("id") or b.get("slug")
            w = b.get("palabras") or b.get("words") or 0
            if key:
                agg[key][0] += 1
                agg[key][1] += w
    rows = sorted(agg.items(), key=lambda kv: -kv[1][1])
    tot_casos = sum(v[0] for v in agg.values())
    tot_pals = sum(v[1] for v in agg.values())
    print("TOTAL casos=%d bloques=%d palabras=%d" % (tot_casos, len(agg), tot_pals))
    for k, (c, w) in rows[:25]:
        print("%-18s casos=%-3d pal=%-5d" % (k, c, w))
