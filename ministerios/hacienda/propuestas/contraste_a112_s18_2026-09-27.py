# -*- coding: utf-8 -*-
# Sesion 18/30 - contraste a112 capa 4 contra los dos ejemplares BOE archivados
# (regla 2026-09-02: si un texto no esta en NINGUNO de los dos, es invencion de la conversion)
import re, json, unicodedata, os
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    return re.sub(r'[\s]+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip().lower()
html1 = norm(open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read())
p2 = 'ministerios/hacienda/evidencia/boe_vivo_LGT_2026-09-02.html'
html2 = norm(open(p2, encoding='utf-8', errors='ignore').read()) if os.path.exists(p2) else ''
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
a112 = next(a for a in canon['articulos'] if a['id'] == 'a112')
raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
m = re.search(r'(?m)^## \[a112\].*?(?=^## \[|\Z)', raw, re.S)
head = 'Artículo 112. Notificación por comparecencia.'
body = m.group(0)
occ = [x.start() for x in re.finditer(re.escape(head), body)]
# las 4 capas y su huella en los dos ejemplares
for j, s0 in enumerate(occ):
    e0 = occ[j+1] if j+1 < len(occ) else len(body)
    cap = body[s0+len(head):e0]
    probes = [re.sub(r'\s+', ' ', norm(p))[:70] for p in cap.split('\n') if len(p.split()) >= 10]
    h1 = sum(1 for pr in probes if pr and pr in html1)
    h2 = sum(1 for pr in probes if pr and pr in html2)
    print(f'capa {j+1}: {len(cap.split())} pal | {len(probes)} probes | huella consolidado {h1}/{len(probes)} | huella vivo-09-02 {h2}/{len(probes)}')
# canon como probe
ncap = re.sub(r'\s+', ' ', norm(a112['texto']))
print('canon a112 en consolidado:', ncap[:400] in html1, '| cola canon en consolidado:', ncap[-400:] in html1)
print('canon a112 en vivo-09-02:', ncap[:400] in html2)
