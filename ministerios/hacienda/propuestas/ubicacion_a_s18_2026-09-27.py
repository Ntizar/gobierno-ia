# -*- coding: utf-8 -*-
# Sesion 18/30 - donde vive la letra a) (81.4 y 68.1) en el consolidado: vigente o historica
import re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'<[^>]+>', '|', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
for f in ['ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html',
          'data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html']:
    h = norm(open(f, encoding='utf-8', errors='ignore').read())
    print('====', f, '====')
    # marcadores de seccion
    for marker in ['vigente desde', 'ref.', 'redacci'].pass_num if False else ['vigente desde', 'ref. boletin', 'ref.']:
        pass
    # posiciones de Articulo 81 y de la letra a)
    a81 = [m.start() for m in re.finditer('artículo 81', h)]
    la = [m.start() for m in re.finditer('retención del pago de devoluciones', h)]
    print('art81 occ:', len(a81), a81[:8])
    print('letra a) 81.4 occ:', la)
    a68 = [m.start() for m in re.finditer('artículo 68', h)]
    lb = [m.start() for m in re.finditer('conducente al reconocimiento', h)]
    print('art68 occ:', len(a68), a68[:8])
    print('por cualquier accion occ:', lb)
    # contexto de vigente desde mas cercano a cada ocurrencia de letra
    for pos in la + lb:
        # buscar "Ref." o "Vigente" justo antes
        back = h[max(0,pos-1200):pos]
        v = re.findall(r'vigente desde [a-z0-9/\- ]{1,30}', back)
        r = re.findall(r'ref\.\s*bolet[^\|]{0,80}', back)
        print(f'  pos {pos}: vigente={v[-1] if v else None} | ref={r[-1][:60] if r else None}')
