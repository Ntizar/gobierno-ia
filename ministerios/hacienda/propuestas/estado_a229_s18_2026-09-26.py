# -*- coding: utf-8 -*-
# Sesion 18 - estado del bloque [a229] y comprobaciones de no-reaplicacion
# Arcadi Espana, 2026-09-26
import hashlib, json, os
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')

def norm(s): return s.rstrip('\n').replace('\r\n', '\n')
def shastr(s): return hashlib.sha256(norm(s).encode('utf-8')).hexdigest()
def shafile(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

law = 'ministerios/hacienda/leyes/BOE-A-2003-23186.md'
print('SHA256 LEY HOCA:', shafile(law))

blocks = {}
cur = None
for line in open(law, encoding='utf-8'):
    if line.startswith('## ['):
        cur = line.strip().split(']')[0][4:]
        blocks[cur] = []
    if cur is not None:
        blocks[cur].append(line)

out = {'n_bloques': len(blocks)}
for tag in ['a229']:
    vivo = ''.join(blocks[tag])
    yest = open('ministerios/hacienda/evidencia/bloque_vivo_%s_2026-09-25.txt' % tag, encoding='utf-8').read()
    prop = open('ministerios/hacienda/evidencia/bloque_propuesto_%s_2026-09-25.txt' % tag, encoding='utf-8').read()
    out[tag] = {
        'vivo_hoy_sha8': shastr(vivo)[:8], 'vivo_hoy_pal': len(vivo.split()),
        'vivo_ayer_sha8': shastr(yest)[:8], 'vivo_ayer_pal': len(yest.split()),
        'propuesto_sha8': shastr(prop)[:8], 'propuesto_pal': len(prop.split()),
        'INTACTO_vivo_hoy_igual_vivo_ayer': shastr(vivo) == shastr(yest),
        'APLICADO_vivo_hoy_igual_propuesto': shastr(vivo) == shastr(prop),
    }
print(json.dumps(out, indent=1, ensure_ascii=False))
