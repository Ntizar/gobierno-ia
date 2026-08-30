# -*- coding: utf-8 -*-
"""Deduplicación de BOE-A-2021-8447 (Ley 7/2021): hash por párrafo dentro de cada bloque.
Detecta copias literales repetidas y calcula palabras ahorrables."""
import re, hashlib, json
from collections import OrderedDict

F = "C:/Users/d_ant/Projects/gobierno-ia/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
lines = open(F, encoding="utf-8").read().splitlines()

# Cortar por bloques '## [x]'
bloques = []  # (ref, titulo, start, end)
cur = None
for i, l in enumerate(lines):
    m = re.match(r"^##\s+\[([^\]]+)\]\s*(.*)$", l)
    if m:
        if cur: cur[3] = i
        cur = [m.group(1), m.group(2), i, None]
        bloques.append(cur)
if cur: cur[3] = len(lines)

total_palabras = 0
dup_palabras = 0
resumen = []
for ref, titulo, s, e in bloques:
    cuerpo = lines[s+1:e]
    vistos = {}   # hash -> primera linea idx
    dups = []     # lineas repetidas (indices en cuerpo)
    for j, linea in enumerate(cuerpo):
        t = linea.strip()
        if not t:
            continue
        h = hashlib.sha256(re.sub(r"\s+", " ", t).encode()).hexdigest()
        if h in vistos:
            dups.append(j)
        else:
            vistos[h] = j
    palabras = sum(len(l.split()) for l in cuerpo)
    dup_pal = sum(len(cuerpo[j].split()) for j in dups)
    total_palabras += palabras
    dup_palabras += dup_pal
    if dups:
        resumen.append({"ref": ref, "titulo": titulo, "lineas_fichero": (s+1, s+1+e-s-1),
                        "parr_dups": len(dups), "palabras": palabras, "palabras_dup": dup_pal,
                        "primeras_dups": [cuerpo[j][:90] for j in dups[:3]]})

print(f"Bloques: {len(bloques)} | Palabras totales: {total_palabras} | Duplicadas: {dup_palabras} ({100*dup_palabras/total_palabras:.1f}%)")
print(f"Bloques con duplicados: {len(resumen)}")
for r in resumen:
    print(f"  [{r['ref']}] {r['titulo']} | líneas {r['lineas_fichero']} | dups={r['parr_dups']} | palabras dup={r['palabras_dup']}")
    for d in r["primeras_dups"]:
        print(f"      » {d}")
json.dump(resumen, open("C:/Users/d_ant/Projects/gobierno-ia/scripts/tmp_dedup_tecologica.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
