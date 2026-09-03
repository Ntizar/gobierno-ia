# Sesion 5 — CLASIFICACION de la deuda de inventario (55 lineas ~1.090 palabras),
# una a una, con la taxonomia del acuerdo 13 (adaptada): meta-dato de consolidacion /
# artefacto de pagina BOE / rotulo o encabezado / ya restituida hoy / omision real con
# fuerza obligatoria (defecto de conversion) -> candidata a restitucion en Consejo.
import json, re, html

om = json.load(open("evidencia/omisiones_repositorio_2026-09-01.json", encoding="utf-8"))["omisiones"]
# las 9 de DF4/5/9 ya ejecutadas hoy: se excluyen de la deuda (fueron el acuerdo 15)
df_ok = [r for r in om if r["bloque"].startswith(("artículo 20.1", "artículo 26.3", "artículo 38 bis"))]
deuda = [r for r in om if r not in df_ok]
assert len(df_ok) == 9 and len(deuda) == 55, (len(df_ok), len(deuda))

t_repo = open("leyes/BOE-A-2021-8447.md", encoding="utf-8").read()
norm = lambda s: re.sub(r"\s+", " ", s).strip()
repo_set = set(norm(l) for l in t_repo.split("\n") if l.strip())

META = ["Texto original, publicado", "Se modifican", "Se añade por", "Redactado el apartado",
        "Incluye la corrección de errores", "Texto añadido, publicado", "Se deroga por la disposición"]
PAGE = ["Ayúdenos a mejorar", "Servicio de atención", "Sobre la sede electrónica",
        "Sistema Interno de Información", "de Manoteras"]
FORMULA = ["A todos los que la presente vieren", "Esta ley consta de", "Madrid, 20 de mayo de 2021",
           "El Presidente del Gobierno", "PEDRO SÁNCHEZ"]
TITULO = lambda s: bool(re.match(r"^TÍTULO\b", s)) or s.startswith("TÍTULO")

res = {}
for r in deuda:
    s = norm(r["linea"])
    if s in repo_set:
        cat = "ya_restituida_hoy"  # coincidia con una de las 22 letras a)
    elif any(m in s for m in META):
        cat = "metadato_consolidacion"
    elif any(p in s for p in PAGE):
        cat = "artefacto_pagina_boe"
    elif any(f in s for f in FORMULA):
        cat = "formula_promulgacion_preambulo"
    elif TITULO(s):
        cat = "rotulo_titulo"
    else:
        cat = "omision_real_fuerza_obligatoria"
    res.setdefault(cat, []).append({"bloque": r["bloque"][:60], "linea": s[:110], "palabras": r["palabras"]})

for cat, rows in sorted(res.items()):
    w = sum(x["palabras"] for x in rows)
    print(f"{cat}: {len(rows)} lineas, {w} palabras")
    if cat == "omision_real_fuerza_obligatoria":
        for x in rows:
            print("   -", x["bloque"][:42], "|", x["palabras"], "pal |", x["linea"][:80])
json.dump(res, open("evidencia/clasificacion_deuda_55_lineas_2026-09-03.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
tot = sum(sum(x["palabras"] for x in rows) for rows in res.values())
print("TOTAL:", len(deuda), "lineas,", tot, "palabras -> evidencia/clasificacion_deuda_55_lineas_2026-09-03.json")
