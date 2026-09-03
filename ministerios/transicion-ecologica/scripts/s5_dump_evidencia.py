# Sesion 5: volcar SOLO lo necesario para construir los diffs de restitucion.
import json, re

d = json.load(open("evidencia/verificacion_fidelidad_BOE_2026-09-01.json", encoding="utf-8"))
print("=== 23 filas fidelidad (22 letras a + df4) ===")
for i, row in enumerate(d):
    print(f"[{i}] repo={row.get('repo')} palabras={row.get('palabras')}")
    print("    boe_head:", str(row.get("boe_head"))[:90])
    print("    texto_a:", str(row.get("texto_a"))[:160])

o = json.load(open("evidencia/omisiones_repositorio_2026-09-01.json", encoding="utf-8"))
print("\n=== omisiones keys ===", list(o["omisiones"][0].keys()))
# filtrar df-4, df-5, df-9
for row in o["omisiones"]:
    b = str(row.get("bloque", ""))
    if "df" in b.lower() and re.search(r"df[ -]?[459]|cuarta|quinta|novena", b.lower()):
        print("---", json.dumps({k: (str(v)[:220]) for k, v in row.items()}, ensure_ascii=False))
