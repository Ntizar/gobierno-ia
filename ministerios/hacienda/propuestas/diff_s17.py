# Diff real: primer punto de divergencia canon vs vivo para a8, a150, a117 (sesión 17)
import json, re

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def bloque(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0) if m else ""

for tag in ("a8", "a150", "a117", "a27"):
    a = arts[tag]
    cn = norm(a["texto"])
    bn = norm(re.sub(r"^## \[.*?\][^\n]*\n", "", bloque(tag)))
    # buscar el prefijo común
    i = 0
    while i < min(len(cn), len(bn)) and cn[i] == bn[i]:
        i += 1
    print("=====", tag, "| canon", len(cn.split()), "pal | vivo", len(bn.split()), "pal | prefijo común:", i, "caracteres")
    print("  canon sigue:", repr(cn[i:i+140]))
    print("  vivo  sigue:", repr(bn[i:i+140]))
    # ¿el canon es subsecuencia de palabras del vivo (ignorando el orden de párrafos)?
    cs = set(re.findall(r"\w+", cn.lower()))
    ws = set(re.findall(r"\w+", bn.lower()))
    solo_canon = cs - ws
    print("  palabras del canon NO presentes en el vivo:", len(solo_canon), sorted(solo_canon)[:15])
