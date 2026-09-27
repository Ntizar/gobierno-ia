# -*- coding: utf-8 -*-
# Sesion 18/30 - inspeccion fina de los bloques candidatos a propuesta:
# que sale del fichero si consolidamos contra canon (capas duplicadas vs marcadores de derogado)
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

for tag in ['a81', 'a68', 'a112', 'a233', 'a199', 'a65']:
    cab, body = blocks[tag]
    ncanon = norm(arts[tag]['texto'])
    print('====', tag, '| vivo', len((cab+body).split()), 'pal | canon', len(arts[tag]['texto'].split()), 'pal ====')
    print('  rotulo:', cab.strip())
    # parrafos del vivo no contenidos en el canon (sedimento que saldria)
    fuera = []
    for p in body.split('\n\n'):
        n = norm(p)
        if not n: continue
        if n in ncanon or (ncanon and n and (n in ncanon or ncanon in n)): continue
        fuera.append(p.strip())
    marcadores = [p for p in fuera if '>' in p[:3] or 'Derogad' in p or 'derogada' in p or 'BOE-A-' in p or 'Consolidaci' in p]
    print('  parrafos fuera del canon:', len(fuera), '| con marcador/aparato:', len(marcadores))
    for m in marcadores[:4]:
        print('    MARK:', m[:110].replace('\n', ' '))
    for p in fuera[:6]:
        if p not in marcadores:
            print('    SALDRIA:', p[:150].replace('\n', ' '))
