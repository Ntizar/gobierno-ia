# Probe fino: estructura exacta de las filas para construir el script de ejecucion.
import json
d = json.load(open("evidencia/verificacion_fidelidad_BOE_2026-09-01.json", encoding="utf-8"))
for i, r in enumerate(d):
    print(i, "| repo:", repr(r.get("repo"))[:20], "| pal:", r.get("palabras"), "| head:", repr(str(r.get("boe_head"))[:45]))
o = json.load(open("evidencia/omisiones_repositorio_2026-09-01.json", encoding="utf-8"))
for i in (47,48,53,54,55):
    r = o["omisiones"][i]
    print(i, r["bloque"][:50], "| primera y ultima letra linea:", repr(r["linea"][0]), repr(r["linea"][-1]), "| len", len(r["linea"]))
