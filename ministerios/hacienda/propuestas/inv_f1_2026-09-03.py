# Inventario F1 pendiente: bloques con marcas ausentes, ordenados por palabras, con dup del bloque
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
d = json.load(open("evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
casos = d["casos_fidelidad"]
print("ejemplo de caso:", json.dumps(casos[0], ensure_ascii=False))
pend = [c for c in casos if c.get("clase") == "contenido_perdido" and c.get("reverificado_presente") is not True]
# mirar claves disponibles
print("claves caso:", sorted(casos[0].keys()))
f1 = [c for c in casos if "contenido_perdido" in str(c.get("clase", "")) or c.get("clase") == "F1"]
print("total F1 en JSON:", len(f1))
from collections import defaultdict
por_bloque = defaultdict(list)
for c in f1:
    por_bloque[c.get("bloque")].append(c)
est = "sigue_ausente"
pend_blk = {b: [c for c in cs if c.get(est) is True or ("presente" not in json.dumps(c))] for b, cs in por_bloque.items()}
# resumen del manifiesto para la flag exacta
print("\n-- resumen reverificacion --")
print(json.dumps(d["resumen"].get("reverificacion_2026-09-02_siguen_ausentes"), ensure_ascii=False, indent=1))
# mostrar 2 casos completos
print("\n", json.dumps(casos[1], ensure_ascii=False))
print("\n", json.dumps(casos[60], ensure_ascii=False))
