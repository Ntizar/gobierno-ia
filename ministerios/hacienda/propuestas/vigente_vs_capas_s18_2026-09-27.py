# -*- coding: utf-8 -*-
# Sesion 18/30 - [a112] y [a68]/[a81]: cual capa del vivo es exactamente la VIGENTE del consolidado
import re, os, json, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()
raw = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
txt = re.sub(r'<br\s*/?>', '\n', raw); txt = re.sub(r'</p>', '\n', txt); txt = re.sub(r'<[^>]+>', '', txt)
lines = [re.sub(r'\s+', ' ', l).strip() for l in txt.split('\n') if l.strip()]

def vigente(artno, title):
    idx = [i for i, l in enumerate(lines) if l.startswith(f'Artículo {artno}.') and title.lower() in l.lower()]
    i = idx[-1]  # el consolidado archivado muestra la version vigente al final de cada articulo? mejor: la que sigue a 'Artículo N. Titulo.'
    # tomar la version completa: desde i hasta el siguiente Articulo
    j = i + 1
    while j < len(lines) and not re.match(r'Artículo \d+\.', lines[j]):
        j += 1
    return ' '.join(lines[i+1:j])

vivo = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
for tag, artno, title in [('a112', 112, 'comparecencia'), ('a68', 68, 'Interrupción'), ('a81', 81, 'Medidas cautelares')]:
    v = vigente(artno, title); nv = norm(v)
    m = re.search(r'(?m)^## \[' + tag + r'\].*?(?=^## \[|\Z)', vivo, re.S)
    b = m.group(0)
    head = next(l.strip() for l in b.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    occ = [x.start() for x in re.finditer(re.escape(head), b)]
    print(f'== {tag}: vigente-consolidado {len(v.split())} pal | canon {len(arts[tag]["texto"].split())} pal ==')
    print('   canon substring del vigente:', norm(arts[tag]['texto']) in nv)
    for j, s0 in enumerate(occ):
        e0 = occ[j+1] if j+1 < len(occ) else len(b)
        cap = b[s0+len(head):e0]
        print(f'   capa {j+1}: {len(cap.split())} pal | vigente in capa: {nv in norm(cap)} | capa in vigente: {norm(cap) in nv}')
