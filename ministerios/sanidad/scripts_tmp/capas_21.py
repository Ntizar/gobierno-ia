# ¿Qué dice REALMENTE el [aveintiuno] en las 3 fuentes y en el .md HOY? Compara capa a capa.
import re

md = open('ministerios/sanidad/leyes/BOE-A-1986-10499.md', encoding='utf-8').read()
lines = md.splitlines()
# localizar bloque [aveintiuno]
h = [i for i, l in enumerate(lines, 1) if l.startswith('## [aveintiuno]')][0]
nxt = [i for i, l in enumerate(lines, 1) if l.startswith('## [') and i > h][0]
print(f'== BLOQUE .md: {h}..{nxt-1} ==')
for n in range(h, nxt):
    l = lines[n-1].rstrip()
    if l.strip():
        print(n, '|', l.strip()[:98])
print('PALABRAS cuerpo (sin encabezado ##):', sum(len(lines[n-1].split()) for n in range(h+1, nxt)))
print()

SRC = {
 'html': 'ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html',
 'plano': 'ministerios/sanidad/evidencia/boe_texto_plano.txt',
 'canon': 'data/canonical/BOE-A-1986-10499/2026-08-31.json',
}
frases_md = []
for n in range(h+1, nxt):
    l = re.sub(r'<[^>]+>', ' ', lines[n-1]).strip()
    if len(l.split()) >= 6:
        frases_md.append((n, l))
srcs = {}
for k, p in SRC.items():
    t = open(p, encoding='utf-8', errors='replace').read()
    if k == 'html':
        t = re.sub(r'<[^>]+>', ' ', t)
    srcs[k] = re.sub(r'\s+', ' ', t).lower()
print('== ¿cada párrafo del bloque .md tiene respaldo literal en las fuentes? ==')
for n, l in frases_md:
    fr = re.sub(r'\s+', ' ', l).lower()[:70]
    hits = {k: s.count(fr) for k, s in srcs.items()}
    print(n, '|', l[:62].replace('\n', ' '), '->', hits)
