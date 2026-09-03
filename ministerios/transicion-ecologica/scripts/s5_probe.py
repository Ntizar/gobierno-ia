# Sesion 5: extrae los textos BOE completos de la evidencia y los escribe en un
# JSON de trabajo (no vuelca nada grande a stdout).
import json, re

d = json.load(open("evidencia/verificacion_fidelidad_BOE_2026-09-01.json", encoding="utf-8"))
print("filas:", len(d), "| longitudes texto_a:", [len(r.get("texto_a","")) for r in d][:5], "... max:", max(len(r.get("texto_a","")) for r in d))

o = json.load(open("evidencia/omisiones_repositorio_2026-09-01.json", encoding="utf-8"))
om = o["omisiones"]
print("omisiones:", len(om), "| keys:", list(om[0].keys()))
# mostrar solo bloque+linea+palabras (metadatos) de las 64
for i, row in enumerate(om):
    print(i, row.get("bloque"), row.get("linea"), row.get("palabras"), "| len:", max(len(str(v)) for v in row.values()))
