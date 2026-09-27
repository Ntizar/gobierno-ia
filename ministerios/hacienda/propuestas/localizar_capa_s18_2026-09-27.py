# -*- coding: utf-8 -*-
# Sesion 18/30 - localizar QUE capa del vivo contiene el canon completo (a112 y sanity de a81/a68)
import json, re, unicodedata, os
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
parts = re.split(r'(?m)^(## \[[a-z0-9\-]+\][^\n]*)$', raw)
blocks = {}
for i in range(1, len(parts), 2):
    tag = re.match(r'## \[([a-z0-9\-]+)\]', parts[i]).group(1)
    blocks[tag] = (parts[i], parts[i+1])
for tag in ['a81', 'a68', 'a112']:
    cab, body = blocks[tag]
    head = next(l.strip() for l in body.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    ctext = arts[tag]['texto'].strip(); ncanon = norm(ctext)
    apertura = ctext.split('\n')[0].strip()[:60]
    occ = [m.start() for m in re.finditer(re.escape(apertura), body)]
    print('====', tag, '| aperturas en el vivo:', len(occ), '| head:', repr(head[:40]))
    for j, s0 in enumerate(occ):
        e0 = occ[j+1] if j+1 < len(occ) else len(body)
        seg = body[s0:e0]
        print(f'   capa {j+1}: {len(seg.split())} pal | canon_contenido_en_capa={ncanon in norm(seg)}')
