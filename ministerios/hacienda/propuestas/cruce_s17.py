# ¿Qué ausencias grandes (palabra a palabra) caen dentro del inventario F1 vivo? (s17)
import json, re

d = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json", encoding="utf-8"))
inv = {k: v for k, v in d["preceptos_afectados"].items() if not k.startswith("_")}
grandes = {"a229":384,"a199":255,"a27":185,"a135":151,"a243":138,"a239":85,"a67":70,"a26":62,"a233":62,"a211":55,"a40":54,"a81":44}
keys = [k for k in d if not k.startswith("_")]
print("claves:", list(d.keys()))
tot = d.get("resumen") or d.get("totales") or d.get("total") or {}
print("resumen:", tot)
for t in sorted(grandes, key=lambda x: -grandes[x]):
    v = inv.get(t)
    print(f"  {t}: ausentes {grandes[t]} | F1 vivo: {v['casos'] if v else 0} casos / {v['palabras'] if v else 0} pal | {v['tipos'] if v else ''}")
