# Pareo canon↔vivo, párrafo a párrafo, sobre TODO el fichero (sesión 17, 25-09)
# Criterio del cierre de Fase 2 (acuerdo 67): preceptos CON TEXTO, no rótulos.
import json, re

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = canon["articulos"]
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()

def bloque(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0) if m else None

ids = [a["id"] for a in arts]
print("canon items:", len(ids), "| primeras:", ids[:5], "| últimas:", ids[-5:])

con_texto, sin_texto, ausentes = [], [], []
for a in arts:
    tag = a["id"]
    b = bloque(tag)
    if b is None:
        ausentes.append(tag)
        continue
    bn = norm(re.sub(r"^## \[.*?\][^\n]*\n", "", b))
    tx = (a.get("texto") or "").strip()
    if not tx:
        continue
    falt = [p for p in tx.split("\n") if p.strip() and norm(p) not in bn]
    fw = sum(len(p.split()) for p in falt)
    if fw == 0:
        con_texto.append(tag)
    else:
        sin_texto.append((tag, fw, len(falt)))

print("PRECEPTOS CON TEXTO COMPLETO:", len(con_texto))
print("PRECEPTOS CON PÁRRAFOS AUSENTES:", len(sin_texto), "| palabras ausentes:", sum(x[1] for x in sin_texto))
for t in sorted(sin_texto, key=lambda x: -x[1])[:15]:
    print("  -", t[0], "faltan", t[1], "pal en", t[2], "párrafos")
print("BLOQUES VIVOS SIN PRECEPTO EN CANON O AL REVÉS (canon sin bloque):", len(ausentes), ausentes[:10])
