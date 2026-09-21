import json

p = "ministerios/hacienda/evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json"
with open(p, encoding="utf-8") as f:
    m = json.load(f)

targets = ["[a101]", "[a93]", "[a104]", "[a187]", "[daundecima]", "[a82]"]
for c in m["casos_fidelidad"]:
    if c["v"] == "contenido_perdido" and c["bloque"] in targets:
        print("=" * 100)
        print(c["bloque"], "idx", c["idx"], "| palabras:", c["palabras"], "| letra_a:", repr(c.get("letra_a")))
        print(c["texto"][:900])
