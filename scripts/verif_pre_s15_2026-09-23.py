import hashlib, re, pathlib

def bloques(path):
    t = pathlib.Path(path).read_text(encoding='utf-8').replace('\r\n', '\n')
    lines = t.split('\n')
    idx = [(i, re.match(r'^## \[([^\]]+)\]', l).group(1)) for i, l in enumerate(lines) if re.match(r'^## \[([^\]]+)\]', l)]
    out = {}
    for n, (i, key) in enumerate(idx):
        end = idx[n+1][0] if n+1 < len(idx) else len(lines)
        out[key] = (i, end, lines[i:end])
    return lines, out

def medida(sl):
    body = '\n'.join(sl)
    pal = len([w for w in re.split(r'\s+', body.strip()) if w])
    return pal, hashlib.sha256(body.encode('utf-8')).hexdigest()

print("=== LGT ===")
L, B = bloques('ministerios/hacienda/leyes/BOE-A-2003-23186.md')
print("bloques:", len(B))
for k, decl in [('a82', 'c02c984fafb02ea8'), ('a104', 'c4e64d770d916fcd')]:
    i, e, s = B[k]
    p, h = medida(s)
    rot = len([x for x in s if re.match(r'^Artículo \d', x.strip())])
    print(f"[{k}] l.{i+1}-{e} palabras={p} sha={h[:16]} declarado={decl} rotulos_cuerpo={rot}")

print()
print("=== LGS ===")
L2, B2 = bloques('ministerios/sanidad/leyes/BOE-A-1986-10499.md')
print("bloques:", len(B2))
for k in ['aonce','aveintiuno','aveintidos','aveintisiete','atreintaycinco','atreintayseis','acuarentaytres','asesentayuno','aochentaydos','aochentaycuatro','aciento','acientocinco','acuarentaysiete']:
    if k in B2:
        i, e, s = B2[k]
        p, h = medida(s)
        print(f"[{k}] l.{i+1}-{e} palabras={p}")
    else:
        print(f"[{k}] NO EXISTE")

print()
print("=== L7 ===")
L3, B3 = bloques('ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md')
print("bloques:", len(B3))

print()
print("=== canonico Hacienda declarado ===")
c = pathlib.Path('ministerios/hacienda/evidencia/bloque_propuesto_a82_2026-09-23.txt').read_text(encoding='utf-8').replace('\r\n','\n')
print("a82 propuesto:", len([w for w in re.split(r'\s+', c.strip()) if w]), "lineas", c.count('\n')+1)
print("primeras lineas:", c.split('\n')[:2])
