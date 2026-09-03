# Cifras para el manifiesto: palabras totales ley antes/despues + clase de los casos DA18
import re, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def total_words(p):
    t = open(p, encoding="utf-8").read()
    return len(t.split())
bak = "leyes/BOE-A-2003-23186.md.bak-2026-09-02-da18"
cur = "leyes/BOE-A-2003-23186.md"
print("palabras ley antes:", total_words(bak), "| despues:", total_words(cur))
d = json.load(open("evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
da18 = [c for c in d["casos_fidelidad"] if c["bloque"] == "[dadecimoctava]"]
from collections import Counter
print("casos DA18 por familia:", Counter(c["v"] for c in da18), "| total:", len(da18))
