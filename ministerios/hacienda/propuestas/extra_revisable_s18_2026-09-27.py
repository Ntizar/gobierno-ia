# -*- coding: utf-8 -*-
# Sesion 18/30 - que sobra en el propuesto aparte del canon (cola literal): clasificar el extra
import json, re, unicodedata, os
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
for tag in ['a81', 'a68', 'a112']:
    prop = open(f'ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-27.txt', encoding='utf-8').read()
    vivo = open(f'ministerios/hacienda/evidencia/bloque_vivo_{tag}_2026-09-27.txt', encoding='utf-8').read()
    nc = norm(arts[tag]['texto']); ncanon = nc
    print('====', tag, '====')
    for p in prop.split('\n\n'):
        n = norm(p)
        if not n: continue
        if n in ncanon: continue
        # ¿parrafos del canon que contienen a este?
        parts = [s for s in ncanon.split('. ') ]
        lab = 'EXTRA'
        if n in ncanon or any(n in seg for seg in [ncanon]): pass
        print(f'  [{lab}] ({len(p.split())} pal):', p[:120].replace('\n', ' '))
    # ¿el extra vive tambien ANTES de la cola en el vivo? (sedimento duplicado que NO hubo que tocar)
print('OK')
