# Escaneo TOTAL canon↔vivo a nivel de palabra (292 preceptes) — verdad para el cierre de Fase 2 (s17)
import json, re, difflib

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = canon["articulos"]
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

def bloque(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0) if m else ""

def words(s):
    return re.findall(r"\S+", re.sub(r"\s+", " ", s).strip())

res = []
for a in arts:
    tag = a["id"]
    b = bloque(tag)
    if not b:
        continue
    body = re.sub(r"^## \[.*?\][^\n]*\n", "", b)
    body = re.sub(r"^\s*>?\s*\*\*(Nota|Notas al bloque|Fuente|Aplicación|Cierre)[^\n]*", "", body, flags=re.M)
    body = body.replace("<sup>", "").replace("</sup>", "")
    cw, vw = words(a["texto"]), words(body)
    sm = difflib.SequenceMatcher(None, cw, vw)
    missing = sum(i2-i1 for op, i1, i2, j1, j2 in sm.get_opcodes() if op in ("delete", "replace"))
    extra = sum(j2-j1 for op, i1, i2, j1, j2 in sm.get_opcodes() if op in ("insert", "replace"))
    if missing:
        res.append((tag, missing, extra, len(cw)))

res.sort(key=lambda x: -x[1])
print("PRECEPTOS CON PALABRAS DEL CANON AUSENTES EN EL VIVO (criterio estricto palabra a palabra):", len(res), "de 292")
for t in res:
    print(f"  {t[0]}: faltan {t[1]} pal (canon {t[3]}), sobran {t[2]}")
tot = sum(r[1] for r in res)
print("TOTAL palabras canónicas ausentes:", tot)
