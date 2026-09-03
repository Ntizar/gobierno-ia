# Que tags y clases hay realmente entre las anclas dadecimoctava/dadecimonovena
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open("../evidencia/boe_vivo_LGT_2026-09-02.html", encoding="utf-8", errors="replace").read()
i = raw.find('id="dadecimoctava"')
j = raw.find('id="dadecimonovena"', i + 10)
print("anclas:", i, j, "longitud seccion:", j - i)
sec = raw[i:j]
tags = re.findall(r"<([a-zA-Z]+)\b", sec)
from collections import Counter
print(Counter(t.lower() for t in tags).most_common(15))
print("=== muestra 600 chars tras el titulo ===")
k = sec.find("extranjero")
print(repr(sec[k-200:k+700]) if k > 0 else "no encontrado")
