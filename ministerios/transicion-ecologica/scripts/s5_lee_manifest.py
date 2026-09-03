import json
m = json.load(open("evidencia/manifiesto_ejecucion_2026-09-03.json", encoding="utf-8"))
print("claves:", list(m.keys()))
print("acuerdo_16:", m["acuerdo_16_art15"])
print("acuerdo_15:", m["acuerdo_15_restituciones"])
print("letras insertadas:", len(m["acuerdo_22_letras_a"]), "| palabras:", m["palabras_letras_a"])
for x in m["acuerdo_22_letras_a"]: print("  INS", x)
for x in m.get("letras_a_ya_presentes_o_sin_b", []): print("  SKIP", x)
