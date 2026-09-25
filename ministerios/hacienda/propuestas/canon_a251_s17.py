# Estructura de 'articulos' y búsqueda del 250-251 en el canon (sesión 17, 25-09)
import json

p = r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json"
d = json.load(open(p, encoding="utf-8"))
arts = d["articulos"]
print("type:", type(arts), "len:", len(arts) if hasattr(arts, "__len__") else "?")
if isinstance(arts, list):
    print("first item:", json.dumps(arts[0], ensure_ascii=False)[:300])
    for a in arts:
        num = a.get("numero") or a.get("n") or a.get("articulo")
        if str(num) in ("249", "250", "251", "252", "253"):
            print("=====", num, "keys:", list(a.keys()))
            s = json.dumps(a, ensure_ascii=False)
            print(s[:500])
elif isinstance(arts, dict):
    print("keys sample:", list(arts.keys())[:10])
    for k in ("250", "251", "249", "252"):
        if k in arts:
            print("=====", k, json.dumps(arts[k], ensure_ascii=False)[:400])
