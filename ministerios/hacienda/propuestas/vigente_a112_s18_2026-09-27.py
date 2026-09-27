# -*- coding: utf-8 -*-
# Sesion 18/30 - que capa es la VIGENTE segun el BOE consolidado archivado (a112)
# y que piezas vigentes faltan en la ultima capa del vivo (a81, a68)
import re, os, unicodedata, json
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
cons = norm(open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read())
vivo = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()

# a112: localizar cada "Artículo 112" en el consolidado con su "Ref. / vigente desde"
idxs = [m.start() for m in re.finditer('artículo 112', cons)]
print('apariciones de "artículo 112" en consolidado:', len(idxs))
for i, s0 in enumerate(idxs):
    e0 = idxs[i+1] if i+1 < len(idxs) else len(cons)
    frag = cons[s0:e0]
    vig = re.findall(r'vigente desde [^(]*\)', frag[:1200].replace(')', ')', 1)) if 'vigente desde' in frag[:200] else []
    head40 = frag[:100]
    print(f'  #{i+1}: {head40}')
    j = frag.find('vigente desde')
    if j >= 0: print('      vigente:', frag[j:j+60])
    k = frag.find('cuando no sea posible')
    if k >= 0: print('      apertura:', frag[k:k+90])

# capas del vivo a112: cotejar cada una contra el consolidado (¿existe como texto?)
m = re.search(r'(?m)^## \[a112\].*?(?=^## \[|\Z)', vivo, re.S)
body = m.group(0)
head = 'Artículo 112. Notificación por comparecencia.'
occ = [x.start() for x in re.finditer(re.escape(head), body)]
for j, s0 in enumerate(occ):
    e0 = occ[j+1] if j+1 < len(occ) else len(body)
    cap = norm(body[s0+len(head):e0])
    probes = [cap[i:i+80] for i in range(0, min(len(cap), 700), 120)]
    hits = sum(1 for p in probes if p and p in cons)
    print(f'capa {j+1}: probes {hits}/{len(probes)} en consolidado')
