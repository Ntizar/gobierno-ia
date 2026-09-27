# -*- coding: utf-8 -*-
# Sesion 18/30 - donde vive la letra a) (81.4 y 68.1) en los dos ejemplares BOE archivados
import re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
for f in ['ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html',
          'data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html']:
    p = f
    if not os.path.exists(p):
        print('NO EXISTE:', p); continue
    h = norm(open(p, encoding='utf-8', errors='ignore').read())
    print('====', p, '====', len(h), 'chars')
    a81 = [m.start() for m in re.finditer('artículo 81', h)]
    la = [m.start() for m in re.finditer('retención del pago de devoluciones', h)]
    print('  occ art81:', len(a81), '| occ letra a) 81.4:', len(la))
    a68 = [m.start() for m in re.finditer('artículo 68', h)]
    lb = [m.start() for m in re.finditer('conducente al reconocimiento', h)]
    print('  occ art68:', len(a68), '| occ letra a) 68.1:', len(lb))
    for pos in la + lb:
        back = h[max(0, pos-1500):pos]
        vig = re.findall(r'vigente desde el [^ .]{1,12}', back)
        ref = re.findall(r'ref\.\s*boe[-a-z0-9./ ]{1,40}', back)
        ult_vig = vig[-1] if vig else 'sin-marca'
        ult_ref = ref[-1][:50] if ref else 'sin-ref'
        print(f'  pos {pos}: ultimo vigente-before = {ult_vig} | ultima ref = {ult_ref}')
# ademas: ¿el canon data/canonical 2026-08-31 viene de source.html? mirar esquema
import json
c = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
print('esquema canon: version', c.get('schema_version'), '| source_sha256', str(c.get('source_sha256'))[:16], '| fecha_consulta', c.get('fecha_consulta'))
import hashlib
if os.path.exists('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html'):
    print('sha256 source.html:', hashlib.sha256(open('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html','rb').read()).hexdigest()[:16])
