# Sesion 5 — verificacion fina del estado de los bloques DF 10-14 (donde viven
# las omisiones reales de contenido) + cifra final de palabras.
import re, json
raw = open("leyes/BOE-A-2021-8447.md", encoding="utf-8").read()
print("PALABRAS_FINALES:", len(re.findall(r"\S+", raw)), "| LINEAS:", raw.count("\n") + 1)
import hashlib
print("SHA_FINAL:", hashlib.sha256(raw.encode("utf-8")).hexdigest())
# localizar cabeceras de df-10..df-14 y volcar SOLO sus primeras 260 caracteres por linea
i0 = raw.find("## [df-10]"); i1 = raw.find("## [df-15]")
seg = raw[i0:i1].split("\n")
for l in seg:
    s = l.strip()
    if s:
        print((s[:150] + ("…" if len(s) > 150 else "")))
