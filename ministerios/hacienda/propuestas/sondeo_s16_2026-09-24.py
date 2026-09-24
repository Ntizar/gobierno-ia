# Sondeo sesión 16/30 (2026-09-24): estado vivo de los bloques del ranking F1 restante
# contra el fichero vivo de la LGT (hash 61fc9fc9...), + convención de hash del Auditor.
import json, re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
LEY = BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md"

raw = open(LEY, encoding="utf-8", newline="").read()

# separar bloques por cabecera ## [etiqueta]
parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", raw)
blocks = {}
order = []
for i in range(1, len(parts) - 1, 2):
    header = parts[i]
    body = parts[i + 1]
    m = re.match(r"## \[([a-z0-9\-]+)\]", header)
    if m:
        slug = m.group(1)
        blocks[slug] = (header, body)
        order.append(slug)
print("bloques en fichero vivo:", len(blocks))

# hash con convención única del Auditor: bloque completo con su cabecera, LF normalizado,
# sin saltos finales (ni al principio ni al final)
def aud_hash(header, body):
    full = (header + body).replace("\r\n", "\n").replace("\r", "\n")
    full = full.strip("\n")
    return hashlib.sha256(full.encode("utf-8")).hexdigest()

def wc(text):
    return len(re.findall(r"\S+", text))

inv = json.load(open(BASE + r"/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json", encoding="utf-8"))
pa = inv["preceptos_afectados"]
print("preceptos_afectados:", type(pa).__name__, len(pa))
if isinstance(pa, dict):
    k0 = list(pa.keys())[0]
    print("muestra:", k0, "->", json.dumps(pa[k0], ensure_ascii=False)[:500])
else:
    print("muestra:", json.dumps(pa[0], ensure_ascii=False)[:500])


# nº de copias por etiqueta (¿se han re-duplicado bloques?)
from collections import Counter
cnt = Counter(re.findall(r"(?m)^## \[([a-z0-9\-]+)\]", raw))
dupes = {k: v for k, v in cnt.items() if v > 1}
print("etiquetas con >1 cabecera:", dupes)

# ranking F1 vivo: para cada precepto afectado, palabras actuales del bloque
rows = []
missing = []
for key, e in pa.items():
    slug = key.strip("[]")
    if slug in blocks:
        h, b = blocks[slug]
        rows.append((wc(h + b), slug, e))
    else:
        missing.append(key)
rows.sort(reverse=True)
print("preceptos del inventario sin bloque en fichero:", missing)
print("\nTOP 15 bloques del reescaneo por palabras actuales (convención Auditor):")
for w, slug, e in rows[:15]:
    hh = aud_hash(*blocks[slug])
    print(f"  [{slug:20s}] {w:5d} pal  casos={e.get('casos')} pal_inv={e.get('palabras')}  hash={hh[:8]}")
print("\ntotal bloques del inventario vivo:", len(rows), " palabras:", sum(r[0] for r in rows))

# ranking por palabras AUSENTES declaradas (pal_inv) — es lo que pesa en F1
rows2 = sorted(rows, key=lambda r: -(r[2].get("palabras") or 0))
print("\nTOP 20 por palabras ausentes (inventario s15):")
tot = 0
for w, slug, e in rows2:
    tot += e.get("palabras", 0)
print("suma palabras inventario:", tot, " casos:", sum(e.get("casos",0) for _,_,e in rows2))
for w, slug, e in rows2[:20]:
    hh = aud_hash(*blocks[slug])
    print(f"  [{slug:20s}] pal_bloque_vivo={w:5d} casos={e.get('casos'):2d} pal_ausentes={e.get('palabras'):4d} hash={hh[:8]}")
    for ex in (e.get("ejemplos") or [])[:3]:
        print(f"        ej: {ex[:140]}")


