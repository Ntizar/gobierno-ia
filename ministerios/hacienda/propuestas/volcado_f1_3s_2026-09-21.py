import json

p = "ministerios/hacienda/evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json"
with open(p, encoding="utf-8") as f:
    m = json.load(f)

for b in ["[a93]", "[a101]", "[a187]"]:
    print("#" * 100)
    print("BLOQUE", b)
    for c in m["casos_fidelidad"]:
        if c["bloque"] == b and c["v"] == "contenido_perdido":
            print("-" * 90)
            print("idx", c["idx"], "| pal", c["palabras"], "| sha", c["sha256_texto"][:12])
            print(c["texto"])
