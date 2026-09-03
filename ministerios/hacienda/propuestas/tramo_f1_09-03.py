# Tramo F1 (contenido_perdido) siguiente, excluyendo los bloques ya intervenidos
import json, io, sys
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
d = json.load(open("evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
hechos = {"[a150]", "[a271]", "[dadecimoctava]"}  # ya reparados (restituciones 09-01 y DA18 09-03)
casos = [c for c in d["casos_fidelidad"] if c["v"] == "contenido_perdido" and c["bloque"] not in hechos]
por_bloque = defaultdict(lambda: [0, 0])
for c in casos:
    por_bloque[c["bloque"]][0] += 1
    por_bloque[c["bloque"]][1] += c["palabras"]
print("casos F1 pendientes:", len(casos), "| bloques F1 pendientes:", len(por_bloque),
      "| palabras F1 pendientes:", sum(v[1] for v in por_bloque.values()))
orden = sorted(por_bloque.items(), key=lambda kv: (-kv[1][1], kv[0]))
def art_num(b):
    import re
    m = re.match(r"\[a(\d+)\]", b)
    return int(m.group(1)) if m else 10**9
orden_art = [(b, v) for b, v in por_bloque.items() if b.startswith("[a") and art_num(b) <= 30]
print("\n-- Tramo proposed: arts. 1-30 (orden numerico) --")
for b, v in sorted(orden_art, key=lambda kv: art_num(kv[0])):
    print(f"  {b}: {v[0]} casos, {v[1]} palabras")
print("\n-- Top 15 bloques por palabras perdidas --")
for b, v in orden[:15]:
    print(f"  {b}: {v[0]} casos, {v[1]} palabras")
