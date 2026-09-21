import json, sys

p = "ministerios/hacienda/evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json"
with open(p, encoding="utf-8") as f:
    m = json.load(f)

def walk(obj, depth=0, path=""):
    if depth > 2:
        return
    if isinstance(obj, dict):
        for k in list(obj.keys())[:25]:
            v = obj[k]
            info = f"{type(v).__name__}"
            if hasattr(v, "__len__") and not isinstance(v, str):
                info += f" len={len(v)}"
            print("  " * depth + f"{k}: {info}")
            if isinstance(v, (dict, list)) and depth < 1:
                walk(v, depth + 1, path + "/" + k)
    elif isinstance(obj, list) and obj:
        print("  " * depth + f"[0..{len(obj)-1}] first item:")
        walk(obj[0], depth + 1, path + "/[0]")

walk(m)
