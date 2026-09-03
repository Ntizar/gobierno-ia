# Bloques F1 desde el JSON TOTAL del 09-01 (registro con clave "v") y del manifiesto de hoy
import json, io, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

d = json.load(open("../evidencia/fidelidad_LGT_total_2026-09-01.json", encoding="utf-8"))
reg = d["registro"] if isinstance(d, dict) and "registro" in d else (d["casos"] if isinstance(d, dict) and "casos" in d else d)
bloq = {r.get("bloque") for r in reg if r.get("v") == "contenido_perdido"}
print("TOTAL 09-01: casos:", sum(1 for r in reg if r.get('v')=='contenido_perdido'), "| bloques F1 distintos:", len(bloq))

m = json.load(open("../evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
mm = m["manifiesto"]
bloq2 = {b for b, o in mm.items() if o["v"] == "contenido_perdido"}
print("MANIFIESTO 09-02: casos F1:", sum(1 for b,o in mm.items() if o['v']=='contenido_perdido'), "| bloques F1 distintos:", len(bloq2))
print("igualdad de conjuntos:", bloq == bloq2)
print("ejemplos:", sorted(bloq2)[:8])
