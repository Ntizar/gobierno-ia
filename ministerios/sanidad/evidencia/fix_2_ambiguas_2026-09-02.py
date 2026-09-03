# -*- coding: utf-8 -*-
# Fix 2 letras «a)» con ancla ambigua: se inserta SOLO ante la «b)» que NO tiene
# su «a)» delante (el duplicado del bloque ya la conserva).
import re, unicodedata

BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"
LEY = BASE + "/leyes/BOE-A-1986-10499.md"

def norm(s):
    return unicodedata.normalize("NFC", s.replace("\u00a0", " ").replace("\ufeff", "").strip())

lines = open(LEY, encoding="utf-8").read().splitlines()

jobs = [
    ("aveinticinco", "b) Deberán estar justificados en la protección de la salud pública.",
     "a) No resultarán discriminatorios ni directa ni indirectamente en función de la nacionalidad o, por lo que se refiere a sociedades, por razón de ubicación del domicilio social."),
    ("asetentaynueve", "b) Transferencias del Estado, que abarcarán:",
     "a) Cotizaciones sociales."),
]

report = []
for bid, bpre, a_txt in jobs:
    hs = [i for i, l in enumerate(lines) if re.match(r'^## \[a\w+\] ', l)]
    start = next(i for i in hs if f"[{bid}]" in lines[i])
    end = next((i for i in hs if i > start), len(lines))
    cands = [i for i in range(start, end) if norm(lines[i]).startswith(bpre)]
    huérf = [i for i in cands if not (lambda k: norm(lines[k]) == norm(a_txt))(max([j for j in range(0, i) if lines[j].strip()] or [start]))]
    assert len(huérf) == 1, (bid, len(cands), len(huérf))
    i = huérf[0]
    lines[i:i] = [a_txt, ""]
    report.append({"bloque": bid, "candidatas_b": len(cands), "insertada_en_linea": i + 1})

open(LEY, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

# recuento final
a_res = __import__("json").load(open(BASE + "/evidencia/a_restituir_completas_2026-09-01.json", encoding="utf-8"))
ok = 0
missing = []
for r in a_res:
    tgt = norm(r["letra_a_BOE"])
    found = any(norm(l) == tgt for l in lines)
    ok += found
    if not found:
        missing.append(r["linea_repo"])
print(f"21 verificacion: {ok}/{len(a_res)} letras a) BOE presentes", ("faltan:" + str(missing)) if missing else "— TODAS")
