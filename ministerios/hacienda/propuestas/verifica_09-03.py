# Verificar conteo de bloques antes/despues y preparar manifiesto de aplicacion 09-03
import re, hashlib, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SRC = "leyes/BOE-A-2003-23186.md"
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

for f in [SRC + ".bak-2026-09-02-da18", SRC]:
    t = open(f, encoding="utf-8").read()
    n_all = len(re.findall(r"^## \[", t, flags=re.M))
    n_w = len(re.findall(r"^## \[\w+\]", t, flags=re.M))
    print(f, "| encabezados ##[:", n_all, "| con \\w+:", n_w, "| sha:", sha(f)[:16])

# F1 pendientes segun taxonomia/manifiesto: listar casos F1 ordenados
d = json.load(open("evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
casos = d["casos_fidelidad"]
print("total casos:", len(casos), "| ejemplo clave:", list(casos[0].keys()))
from collections import Counter
print(Counter(c.get("tipo") or c.get("familia") or c.get("clase") for c in casos))
hechos = {"[a150]", "[a271]", "[dadecimoctava]"}
f1 = [c for c in casos if (c.get("tipo") or c.get("familia") or c.get("clase")) == "F1"]
f1p = [c for c in f1 if c.get("bloque") not in hechos]
f1p.sort(key=lambda c: -(c.get("palabras_afectadas") or c.get("palabras") or 0))
print("F1 totales:", len(f1), "| F1 pendientes tras DA18:", len(f1p))
for c in f1p[:12]:
    print("  ", c.get("bloque"), "|", (c.get("titulo") or "")[:40], "| pal:", c.get("palabras_afectadas") or c.get("palabras"))
