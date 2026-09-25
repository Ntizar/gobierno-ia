# Ranking F1 vivo (s15) ordenado por palabras — de dónde salgo hoy (2026-09-25)
import json

d = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json", encoding="utf-8"))
inv = {k: v for k, v in d["preceptos_afectados"].items()}
rows = sorted(((k, v["casos"], v["palabras"], v.get("ejemplos", [])) for k, v in inv.items()), key=lambda x: -x[2])
print("bloques F1 vivos:", len(rows), "| casos:", sum(r[1] for r in rows), "| palabras:", sum(r[2] for r in rows))
for r in rows[:25]:
    print(f"  {r[0]}: {r[1]} casos / {r[2]} pal | ej: {(r[3][0][:70] if r[3] else '')}")
