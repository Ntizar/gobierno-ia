# Diff palabra a palabra canon vs vivo (difflib) para los 17 «sospechosos» (sesión 17)
import json, re, difflib

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

def bloque(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0) if m else ""

def words(s):
    return re.findall(r"\S+", re.sub(r"\s+", " ", s).strip())

sus = ["a150","a43","a95","a27","a26","a93","a62","a104","a187","a29","a46","a82","a101","a8","a117","a17","a25"]
for tag in sus:
    a = arts.get(tag)
    if not a:
        print(tag, "NO ESTÁ EN CANON"); continue
    b = bloque(tag)
    # quitar del vivo: cabecera ## [..], y líneas "Nota"/"Fuente"/comentarios我们的 propios
    body = re.sub(r"^## \[.*?\][^\n]*\n", "", b)
    body = re.sub(r"^\s*>?\s*\*\*(Nota|Notas al bloque|Fuente|Aplicación|Cierre)[^\n]*", "", body, flags=re.M)
    cw, vw = words(a["texto"]), words(body)
    sm = difflib.SequenceMatcher(None, cw, vw)
    missing, added = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ("delete", "replace"):
            missing.extend(cw[i1:i2])
        if op in ("insert", "replace"):
            added.extend(vw[j1:j2])
    # ¿qué son las palabras 'added'? probably duplicado de rótulo + notas nuestras
    print(f"== {tag}: canon {len(cw)}p | vivo {len(vw)}p | faltan {len(missing)} | sobran {len(added)}")
    if missing:
        print("   FALTAN EN VIVO:", " ".join(missing[:40]))
    if added:
        print("   SOBRA EN VIVO:", " ".join(added[:40]))
