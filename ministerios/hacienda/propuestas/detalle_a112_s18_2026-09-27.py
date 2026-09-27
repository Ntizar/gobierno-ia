# -*- coding: utf-8 -*-
# Sesion 18/30 - que hay despues de la capa canonica (capa 3) en [a112]: es la 4 (2536->cola)
import json, re, unicodedata, os
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
m = re.search(r'(?m)^## \[a112\].*?(?=^## \[|\Z)', raw, re.S)
body = m.group(0)
head = 'Artículo 112. Notificación por comparecencia.'
ncanon = norm(arts['a112']['texto'])
occ = [x.start() for x in re.finditer(re.escape(head), body)]
print('aperturas de head:', len(occ))
for j, s0 in enumerate(occ):
    e0 = occ[j+1] if j+1 < len(occ) else len(body)
    cap = body[s0+len(head):e0]
    print(f'capa {j+1}: {len(cap.split())} pal | canon_en_capa={ncanon in norm(cap)} | primera frase: ' + (cap.strip().split(chr(10))[0][:90] if cap.strip() else '(vacia)'))
# la capa posterior a la canonica (si canon=capa3): mostrar texto
cap4 = body[occ[3]+len(head):]
print('== CAPA 4 (posterior a la canonica) 500 chars ==')
print(cap4[:600])
