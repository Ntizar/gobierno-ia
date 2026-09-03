# Clasificar casos del manifiesto por familia (campo v) y sacar tramo F1 pendiente
import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
d = json.load(open("evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
print("resumen:", json.dumps(d["resumen"], ensure_ascii=False)[:600])
from collections import Counter
casos = d["casos_fidelidad"]
print("valores campo v:", Counter(str(c.get("v")) for c in casos))
print("ejemplo caso:", json.dumps(casos[0], ensure_ascii=False)[:300])
