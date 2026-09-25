# Medida exacta de duplicados/rótulos obsoletos en los 5 mayores bloques F1 vivos (s17, 25-09)
import json, re

ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

def bloque(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0)

for tag in ("a229", "a203", "a188", "a150", "a81", "a48"):
    b = bloque(tag)
    lines = [l for l in b.split("\n")]
    body = [l.strip() for l in lines if l.strip() and not l.startswith("## [")]
    # líneas no únicas dentro del bloque
    seen, dups = {}, []
    for l in body:
        seen[l] = seen.get(l, 0) + 1
    for l, c in seen.items():
        if c > 1:
            dups.append((c, len(l.split()), l[:100]))
    # líneas de rótulo "Artículo NNN."
    titulos = [l for l in body if re.match(r"^Artículo \d+\.", l)]
    print("=" * 72)
    print(f"BLOQUE [{tag}] | palabras totales: {len(b.split())} | líneas de rótulo: {len(titulos)}")
    for t in titulos:
        print("   TÍTULO:", t[:110])
    print(f"   LÍNEAS DUPLICADAS: {len(dups)} | palabras duplicadas (exceso): {sum((c-1)*w for c,w,l in dups)}")
    for c, w, l in sorted(dups, key=lambda x: -x[1])[:6]:
        print(f"     x{c} ({w} pal): {l}")
