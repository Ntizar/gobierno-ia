# -*- coding: utf-8 -*-
"""Verificación pre-sesión 14 (2026-09-22): sha256 del fichero de ley, rótulos
únicos en los bloques ejecutados la noche del 21-09 ([a12], [a93], [a101],
[a187]), y conteo de rótulos duplicados en todo el fichero."""
import hashlib, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

p = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
raw = open(p, encoding="utf-8").read()
print("sha256:", hashlib.sha256(raw.encode("utf-8")).hexdigest())
print("bytes:", len(raw.encode("utf-8")), "palabras:", len(raw.split()))

heads = re.findall(r"(?m)^## \[([a-z0-9\-]+)\][^\n]*$", raw)
from collections import Counter
c = Counter(heads)
print("total encabezados:", len(heads), "| duplicados:", {k: v for k, v in c.items() if v > 1} or "ninguno")

for slug, art in (("a12", "Artículo 12."), ("a93", "Artículo 93."),
                  ("a101", "Artículo 101."), ("a187", "Artículo 187.")):
    m = re.search(r"(?m)^## \[%s\][^\n]*\n(.*?)(?=^## \[|\Z)" % slug, raw, re.S)
    body = m.group(1)
    n_labels = body.count(art)
    print("[%s] rótulos en cuerpo: %d | palabras bloque: %d" % (slug, n_labels, len(body.split())))

# ¿contiene ya cada bloque ejecutado su pie de consolidación?
for slug in ("a12", "a93", "a101", "a187"):
    m = re.search(r"(?m)^## \[%s\][^\n]*\n(.*?)(?=^## \[|\Z)" % slug, raw, re.S)
    print("[%s] pie consolidación 2026-09-21 presente:" % slug, "Consolidación 2026-09-21" in m.group(1) or "Ronda 3" in m.group(1))
