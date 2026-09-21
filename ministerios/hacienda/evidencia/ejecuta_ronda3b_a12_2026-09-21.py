#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[a12] LGT: restitucion al texto canonico del BOE (acuerdo ronda 3, sesion 13/30, 2026-09-21).
Anula la redaccion divergente aprobada en la sesion 9 y conserva UNA sola copia del articulo 12.
Ejecuta Presidencia (agente de Hacienda caido por timeout). Registrado como FIDELIDAD (ahorro 0).
"""
import hashlib, json, pathlib, re, shutil

repo = pathlib.Path(r'C:\Users\d_ant\Projects\gobierno-ia')
ley = repo / 'ministerios/hacienda/leyes/BOE-A-2003-23186.md'
ev = repo / 'ministerios/hacienda/evidencia'

raw_before = ley.read_bytes(); sha_before = hashlib.sha256(raw_before).hexdigest()
lines = raw_before.decode('utf-8').split('\r\n')

html = (ev / 'boe_consolidado_BOE-A-2003-23186.html').read_bytes().decode('utf-8', 'ignore')
p = re.sub(r'<[^>]+>', ' ', html)
p = p.replace('&nbsp;', ' ').replace('&#8203;', '')
p = re.sub(r'\s+', ' ', p)
i = p.index('Artículo 12. Interpretación de las normas tributarias.')
j = p.index('Artículo 13.', i)
slice_ = p[i:j]
slice_ = re.sub(r'\s+([.,;:])', r'\1', slice_).strip()
# apartados
parts = re.split(r'(?<=[.;])\s+(?=[123]\.\s)', slice_)
bodies = []
for k, pa in enumerate(parts):
    pa = re.sub(r'\s+', ' ', pa).strip()
    if y := pa.strip():
        bodies.append(y)
# el primer elemento incluye el rotulo (Artículo 12. ...) -> separar
rot = 'Artículo 12. Interpretación de las normas tributarias.'
if bodies[0].startswith(rot):
    bodies[0] = bodies[0][len(rot):].strip()
if not bodies[0]:
    bodies.pop(0)
pie = ('> Restitución 2026-09-21 (Presidencia, acuerdo de la sesión 13/30): texto íntegro del BOE '
       'consolidado (incluye las disposiciones interpretativas o aclaratorias del apartado 3). Se anula '
       'la redacción divergente aprobada por el Consejo el 08-09 y nunca ratificada. Fidelidad; ahorro 0.')

idx = [k for k, l in enumerate(lines) if re.match(r'## \[a\d+\] Artículo', l)]
i0 = next(k for k in idx if lines[k].startswith('## [a12] '))
j0 = next((k for k in idx if k > i0), len(lines))
cuerpo_antes = lines[i0+1:j0]
pal_antes = len(' '.join(cuerpo_antes).split())
sha_cuerpo_antes = hashlib.sha256('\n'.join(cuerpo_antes).encode()).hexdigest()
rotulos = sum(1 for l in cuerpo_antes if l.strip().startswith('Artículo 12.'))

nuevo = [lines[i0], '', rot, ''] + [b + '\n' for b in bodies]
# separar parrafos con linea en blanco
nuevo = [lines[i0], '', rot, '']
for b in bodies:
    nuevo += [b, '']
nuevo += [pie]
lines[i0:j0] = nuevo
ley.write_bytes('\r\n'.join(lines).encode('utf-8'))
raw_after = ley.read_bytes(); sha_after = hashlib.sha256(raw_after).hexdigest()

l2 = raw_after.decode('utf-8').split('\r\n')
idx2 = [k for k, l in enumerate(l2) if re.match(r'## \[a\d+\] Artículo', l)]
i1 = next(k for k in idx2 if l2[k].startswith('## [a12] '))
j1 = next((k for k in idx2 if k > i1), len(l2))
cuerpo_despues = l2[i1+1:j1]
print('--- CUERPO NUEVO [a12] ---')
print('\n'.join(cuerpo_despues))
print('--- FIN ---')
print('palabras antes/despues:', pal_antes, len(' '.join(cuerpo_despues).split()))
print('rotulos antes/despues:', rotulos, sum(1 for l in cuerpo_despues if l.strip().startswith('Artículo 12.')))
print('bloques:', len(idx), '->', len(idx2))
print('canonico presente literal:', all(b in cuerpo_despues for b in bodies))
man = {
 'ley': 'Ley 58/2003 General Tributaria (BOE-A-2003-23186)', 'fecha': '2026-09-21', 'sesion': '13/30',
 'bloque': '[a12] Artículo 12', 'operacion': 'restitución de fidelidad (anula la reforma no ratificada del 08-09)',
 'ejecutor': 'Presidencia (Mastermind) — agente de Hacienda caído por timeout; ejecuta Presidencia con el BOE consolidado archivado',
 'fuente_verdad': 'ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html (art. 12 completo, apartados 1-3)',
 'fuente_acuerdo': 'consejo/actas/2026-09-21.md (ronda 3, sesión 13/30)',
 'copia_seguridad': 'ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-21-ronda3b-a12',
 'sha256_fichero_antes': sha_before, 'sha256_fichero_despues': sha_after,
 'palabras_cuerpo_antes': pal_antes, 'palabras_cuerpo_despues': len(' '.join(cuerpo_despues).split()),
 'rotulos_antes': rotulos, 'rotulos_despues': 1, 'sha256_cuerpo_antes': sha_cuerpo_antes,
 'sha256_cuerpo_despues': hashlib.sha256('\n'.join(cuerpo_despues).encode()).hexdigest(),
 'ahorro_palabras': 0, 'fidelidad': 'restitución íntegra del apartado 3 (disposiciones interpretativas o aclaratorias)',
 'apartados_restituidos': len(bodies), 'eol': 'CRLF preservado',
}
shutil.copy2(ley.with_name(ley.name + '.bak-2026-09-21-ronda3'), ley.with_name(ley.name + '.bak-2026-09-21-ronda3b-a12'))
(ev / 'manifiesto_ronda3b_a12_2026-09-21.json').write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding='utf-8')
with (ev / 'SHA256SUMS_2026-09-21.txt').open('a', encoding='utf-8', newline='') as f:
    f.write('%s *leyes/BOE-A-2003-23186.md\n' % sha_after)
    f.write('%s *evidencia/manifiesto_ronda3b_a12_2026-09-21.json\n' % hashlib.sha256((ev / 'manifiesto_ronda3b_a12_2026-09-21.json').read_bytes()).hexdigest())
print(json.dumps(man, ensure_ascii=False, indent=1))
