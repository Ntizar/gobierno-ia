#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Limpieza del aparato editorial del BOE que se colo en la restitucion de [a12] (2026-09-21)."""
import hashlib, json, pathlib, re, shutil

repo = pathlib.Path(r'C:\Users\d_ant\Projects\gobierno-ia')
ley = repo / 'ministerios/hacienda/leyes/BOE-A-2003-23186.md'
ev = repo / 'ministerios/hacienda/evidencia'
raw_before = ley.read_bytes(); sha_before = hashlib.sha256(raw_before).hexdigest()
lines = raw_before.decode('utf-8').split('\r\n')

html = (ev / 'boe_consolidado_BOE-A-2003-23186.html').read_bytes().decode('utf-8', 'ignore')
p = re.sub(r'<[^>]+>', ' ', html).replace('&nbsp;', ' ').replace('&#8203;', '')
p = re.sub(r'\s+', ' ', p)
i = p.index('Artículo 12. Interpretación de las normas tributarias.')
j = p.index('Artículo 13.', i)
s = re.sub(r'\s+([.,;:])', r'\1', p[i:j]).strip()
corte = re.search(r'(Se modifica el apartado|Se a\u00f1ade por|\[Bloque|Jurisprudencia|Seleccionar redacci|Texto original, publicado|Subir)', s)
print('corte en:', corte.group(0) if corte else None, 'pos', corte.start() if corte else None)
if corte:
    s = s[:corte.start()].strip()
rot = 'Artículo 12. Interpretación de las normas tributarias.'
s = s[len(rot):].strip() if s.startswith(rot) else s
s = re.sub(r'\s+([.,;:])', r'\1', s)
bodies = [b.strip() for b in re.split(r'(?<=[.;])\s+(?=[123]\.\s)', s) if b.strip()]
print('apartados:', len(bodies), 'palabras:', len(' '.join(bodies).split()))
for b in bodies[:3]:
    print('  -', b[:90], '...')
pie = ('> Restitución 2026-09-21 (Presidencia, acuerdo de la sesión 13/30): texto íntegro del BOE '
       'consolidado (incluye las disposiciones interpretativas o aclaratorias del apartado 3). Se anula '
       'la redacción divergente aprobada por el Consejo el 08-09 y nunca ratificada. Fidelidad; ahorro 0.')
idx = [k for k, l in enumerate(lines) if re.match(r'## \[a\d+\] Artículo', l)]
i0 = next(k for k in idx if lines[k].startswith('## [a12] '))
j0 = next((k for k in idx if k > i0), len(lines))
cuerpo_antes = lines[i0+1:j0]
nuevo = [lines[i0], '', rot, '']
for b in bodies:
    nuevo += [b, '']
nuevo += [pie]
lines[i0:j0] = nuevo
ley.write_bytes('\r\n'.join(lines).encode('utf-8'))
raw_after = ley.read_bytes()
l2 = raw_after.decode('utf-8').split('\r\n')
idx2 = [k for k, l in enumerate(l2) if re.match(r'## \[a\d+\] Artículo', l)]
i1 = next(k for k in idx2 if l2[k].startswith('## [a12] '))
j1 = next((k for k in idx2 if k > i1), len(l2))
cd = l2[i1+1:j1]
junk = [m for m in ['Se modifica', '[Bloque', 'Jurisprudencia', 'Seleccionar', 'actualizaci'] if any(m in l for l in cd)]
print('--- CUERPO FINAL [a12] ---'); print('\n'.join(cd)); print('--- FIN ---')
print('palabras:', len(' '.join(cd).split()), 'rotulos:', sum(1 for l in cd if l.strip().startswith('Artículo 12.')))
print('junk restante:', junk, '| bloques:', len(idx2))
print('sha_antes', sha_before); print('sha_despues', hashlib.sha256(raw_after).hexdigest())
man = json.loads((ev / 'manifiesto_ronda3b_a12_2026-09-21.json').read_text(encoding='utf-8'))
man.update({'correccion_posterior': 'limpieza del aparato editorial del BOE (marcadores de bloque, notas de modificación y jurisprudencia) que se colaron en la primera pasada; el cuerpo queda solo con la norma',
            'sha256_fichero_antes_limpieza': sha_before, 'sha256_fichero_despues_limpieza': hashlib.sha256(raw_after).hexdigest(),
            'palabras_cuerpo_final': len(' '.join(cd).split()), 'apartados_finales': len(bodies)})
(ev / 'manifiesto_ronda3b_a12_2026-09-21.json').write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding='utf-8')
with (ev / 'SHA256SUMS_2026-09-21.txt').open('a', encoding='utf-8', newline='') as f:
    f.write('%s *leyes/BOE-A-2003-23186.md\n' % hashlib.sha256(raw_after).hexdigest())
    f.write('%s *evidencia/manifiesto_ronda3b_a12_2026-09-21.json\n' % hashlib.sha256((ev / 'manifiesto_ronda3b_a12_2026-09-21.json').read_bytes()).hexdigest())
