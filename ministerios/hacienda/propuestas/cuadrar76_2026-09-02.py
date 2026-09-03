# Cuadrar bloques F1 distintos (para la cifra 161/76 que pide el orden del dia)
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
d = json.load(open("../evidencia/fidelidad_letras_a_2026-09-01.json", encoding="utf-8"))
reg = d["registro"] if isinstance(d, dict) and "registro" in d else (d["casos"] if isinstance(d, dict) and "casos" in d else d)
bloques = {}
for r in reg:
    b = r.get("bloque")
    bloques.setdefault(b, []).append(r.get("categoria") or r.get("v"))
f1_bloques = sorted({b for b, vs in bloques.items() if "contenido_perdido" in vs})
print("bloques distintos con >=1 F1:", len(f1_bloques))
print("bloques totales tocados:", len(set(bloques)))
print("ejemplos:", f1_bloques[:5])
