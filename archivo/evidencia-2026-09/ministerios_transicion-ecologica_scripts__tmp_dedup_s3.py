import re, hashlib
p = 'C:/Users/d_ant/Projects/gobierno-ia/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md'
t = open(p, encoding='utf-8').read()
print('palabras totales:', len(t.split()))
parts = re.split(r'\n(?=## \[)', t)
blocks = []
for part in parts:
    m = re.match(r'## \[([^\]]+)\]', part)
    if m:
        blocks.append((m.group(1), part))
print('bloques:', len(blocks))

def norm(x):
    x = re.sub(r'<[^>]+>', '', x)  # tags html
    x = re.sub(r'\s+', ' ', x).strip().lower()
    x = x.replace('veintiún', 'veintiuno').replace('27', 'veintisiete')
    return x

tot = 0
for n, body in blocks:
    paras = [l.strip() for l in body.split('\n') if len(l.strip()) > 80]
    seen = {}
    for x in paras:
        h = hashlib.sha256(x.encode()).hexdigest()
        seen.setdefault(h, []).append(x)
    dw = sum(len(v[0].split()) * (len(v) - 1) for v in seen.values() if len(v) > 1)
    if dw and n != 'a1-7':
        print(f'[{n}]: {dw} palabras dup literal')
        for v in seen.values():
            if len(v) > 1:
                print('   x%d:' % len(v), v[0][:130])
    tot += dw
print('total dup literal intra-bloque (excl. a1-7):', tot if False else 'ver arriba')

# difusos: párrafos casi idénticos dentro del mismo bloque (distancia de palabra <5%)
import difflib
for n, body in blocks:
    if n == 'a1-7':
        continue
    paras = [re.sub(r'<[^>]+>', '', l.strip()) for l in body.split('\n') if len(l.strip()) > 120]
    seen_norm = {}
    for x in paras:
        seen_norm.setdefault(norm(x), []).append(x)
    for k, v in seen_norm.items():
        if len(v) > 1:
            print(f'[{n}] DUP DIFUSO x{len(v)}: {v[0][:130]}')
# entre bloques (normalizado)
g = {}
for n, body in blocks:
    for l in body.split('\n'):
        l2 = re.sub(r'<[^>]+>', '', l.strip())
        if len(l2) > 150:
            g.setdefault(norm(l2), []).append((n, l2))
cross = {k: v for k, v in g.items() if len({b for b, _ in v}) > 1}
print('párrafos dup ENTRE bloques (normalizado):', len(cross))
for k, v in list(cross.items())[:15]:
    print('  ', sorted({b for b, _ in v}), '|', v[0][1][:120])
