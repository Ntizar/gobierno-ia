# Inventario F1 por bloque (tramos) y candidatas para hoy
import json, io, sys, re
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
d = json.load(open("evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
casos = d["casos_fidelidad"]
print("total casos:", len(casos))
by_v = defaultdict(int)
for c in casos:
    by_v[c["v"]] += 1
print(dict(by_v))
f1 = [c for c in casos if c["v"] == "contenido_perdido"]
por_bloque = defaultdict(list)
for c in f1:
    por_bloque[c["bloque"]].append(c)
print("bloques con F1:", len(por_bloque))
# orden numerico de articulos
def keynum(b):
    m = re.match(r"\[a(\d+)\]", b)
    return (0, int(m.group(1))) if m else (1, b)
rows = sorted(por_bloque.items(), key=lambda kv: keynum(kv[0]))
tot_pw = sum(c["palabras"] for c in f1)
print("palabras F1 totales (suma casos):", tot_pw)
print("\nPRIMEROS 30 BLOQUES F1 (por numero de articulo):")
for b, cs in rows[:30]:
    blk = d["bloques"].get(b, {})
    print(f"  {b}: {len(cs)} casos, {sum(c['palabras'] for c in cs)} palabras | dup_bloque={blk.get('parrafos_dup',0)}p/{blk.get('palabras_dup',0)}w | titulo={blk.get('titulo','?')[:48]}")
# tramo 1: primeros bloques a1..a30
tramo = [(b, cs) for b, cs in rows if re.match(r"\[a(\d+)\]", b) and int(re.match(r"\[a(\d+)\]", b).group(1)) <= 30]
print("\nTRAMO a1-a30:", len(tramo), "bloques,", sum(len(cs) for _, cs in tramo), "casos,", sum(c["palabras"] for _, cs in tramo for c in cs), "palabras")
