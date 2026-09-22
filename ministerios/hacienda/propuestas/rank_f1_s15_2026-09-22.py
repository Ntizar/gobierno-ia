# -*- coding: utf-8 -*-
"""Vuelco ordenado del ranking F1 abierto (evidencia/f1_abiertos_2026-09-21.json)."""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
d = json.load(open("ministerios/hacienda/evidencia/f1_abiertos_2026-09-21.json", encoding="utf-8"))
b = d["bloques"]
print("tipo bloques:", type(b))
if isinstance(b, dict):
    items = list(b.items())
    print("n bloques:", len(items))
    print("clave ejemplo:", json.dumps(items[0], ensure_ascii=False)[:500])
    def palabra(v):
        if isinstance(v, dict):
            return v.get("palabras", 0)
        if isinstance(v, (int, float)):
            return v
        return 0
    def casos(v):
        if isinstance(v, dict):
            c = v.get("casos")
            return len(c) if isinstance(c, list) else (c or 0)
        return 0
    rows = sorted(items, key=lambda kv: -palabra(kv[1]))
    tot_p = sum(palabra(v) for _, v in items)
    tot_c = sum(casos(v) for _, v in items)
    print("TOTAL palabras:", tot_p, "| casos:", tot_c, "| bloques:", len(items))
    for k, v in rows[:20]:
        print("%-16s casos=%-3s pal=%-5s" % (k, casos(v), palabra(v)))
elif isinstance(b, list):
    print("n entradas:", len(b))
    print(json.dumps(b[:3], ensure_ascii=False)[:800])
