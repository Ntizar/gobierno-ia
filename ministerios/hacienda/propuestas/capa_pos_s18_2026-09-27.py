# -*- coding: utf-8 -*-
# Sesion 18/30 - regla anti-[a12]: el canon debe vivir en la ULTIMA capa del bloque.
# Candidatos a233/a199/a65/a81/a68/a112: posicion de la capa canonica.
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
for tag in ['a233', 'a199', 'a65', 'a81', 'a68', 'a112']:
    cab, body = blocks[tag]
    head = next(l.strip() for l in body.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    ctext = arts[tag]['texto'].strip(); ncanon = norm(ctext)
    apertura = ctext.split('\n')[0].strip()[:80]
    occ = [m.start() for m in re.finditer(re.escape(apertura), body)]
    capas = []
    for j, s0 in enumerate(occ):
        e0 = occ[j+1] if j+1 < len(occ) else len(body)
        capas.append((s0, body[s0:e0]))
    pos = [j+1 for j, (_, c) in enumerate(capas) if ncanon in norm(c)]
    print(f'{tag}: {len(occ)} aperturas | pal capas {[len(c.split()) for _,c in capas]} | capa(s) con canon {pos} / ultima={len(occ)}')
