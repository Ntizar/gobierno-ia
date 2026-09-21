#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ejecucion ronda 3 (Presidencia, 2026-09-21 sesion 13/30):
consolidaciones [a93] [a101] [a187] sobre la LGT desde el texto canonico del BOE archivado.
Agente de Hacienda caido por timeout -> ejecuta Presidencia con evidencia completa.
"""
import hashlib, json, pathlib, re, shutil, datetime

repo = pathlib.Path(r'C:\Users\d_ant\Projects\gobierno-ia')
ley = repo / 'ministerios/hacienda/leyes/BOE-A-2003-23186.md'
can_path = repo / 'ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt'
ev = repo / 'ministerios/hacienda/evidencia'

raw_before = ley.read_bytes()
sha_before = hashlib.sha256(raw_before).hexdigest()
text = raw_before.decode('utf-8')
assert text.count('\r\n') > 0, 'se esperaba CRLF'
lines = text.split('\r\n')

# --- texto canonico por bloque ---
can = can_path.read_bytes().decode('utf-8').replace('\r\n', '\n')
secs, cur = {}, None
for l in can.split('\n'):
    m = re.match(r'## \[(a\d+)\] — TEXTO CANÓNICO', l)
    if m:
        cur = m.group(1); secs[cur] = []; continue
    if l.startswith('====='):
        continue
    if cur is None:
        continue
    if l.startswith('palabras:') and not secs[cur]:
        continue
    secs[cur].append(l)
for k in secs:
    v = secs[k]
    while v and not v[0].strip(): v.pop(0)
    while v and not v[-1].strip(): v.pop()

pies = {
 'a93': "> Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado (últ. mod. vigente: Ley 13/2023, que añade la letra e) del apartado 1). Órgano de aplicación: la Administración tributaria, a cuyo efecto las obligaciones del apartado 2 se cumplen en la forma y plazos que determine la disposición reglamentaria correspondiente; los requerimientos individualizados del apartado 3 exigen autorización del órgano reglamentariamente determinado.",
 'a101': "> Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado (últ. mod. vigente: Ley 34/2015, que añade la letra c) del apartado 4). La comprobación e investigación de la totalidad de los elementos (apartado 3.a) corresponde al procedimiento inspector del título II; la regla general de duración del procedimiento es el plazo máximo de seis meses del artículo 104.",
 'a187': "> Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado. Los incrementos del apartado 1 operan sobre la sanción mínima y son de aplicación simultánea (apartado 2); su gestión corresponde a los órganos de la Administración tributaria competentes para la imposición de sanciones (título IV).",
}
targets = {'a93': 'Artículo 93. Obligaciones de información.',
           'a101': 'Artículo 101. Las liquidaciones tributarias: concepto y clases.',
           'a187': 'Artículo 187. Criterios de graduación de las sanciones tributarias.'}

# comprobacion previa del canonico
can_report = {}
for k, v in secs.items():
    j = '\n'.join(v)
    can_report[k] = {'palabras': len(j.split()),
                     'sha256_nl': hashlib.sha256(j.encode()).hexdigest(),
                     'sha256_crlf': hashlib.sha256('\r\n'.join(v).encode()).hexdigest()[:16],
                     'lineas': len(v)}
print('CANONICO:', json.dumps(can_report, ensure_ascii=False))

idx = [i for i, l in enumerate(lines) if re.match(r'## \[a\d+\] Artículo', l)]
print('bloques antes:', len(idx))
detalle = []
for key in ['a93', 'a101', 'a187']:
    i = next(i for i in idx if lines[i].startswith('## [%s]' % key))
    j = next((x for x in idx if x > i), len(lines))
    cuerpo_antes = lines[i+1:j]
    palabras_antes = len(' '.join(cuerpo_antes).split())
    sha_antes = hashlib.sha256('\n'.join(cuerpo_antes).encode()).hexdigest()
    # rotulo del propio bloque
    rot = next(l for l in cuerpo_antes if l.strip() == targets[key])
    nuevo = [lines[i], '', rot, ''] + secs[key] + ['', pies[key]]
    palabras_despues = len(' '.join(nuevo[1:]).split())
    sha_despues = hashlib.sha256('\n'.join(nuevo[1:]).encode()).hexdigest()
    detalle.append({'bloque': key, 'linea_antes': i+1, 'linea_despues': i+1,
                    'lineas_bloque_antes': j-i, 'lineas_bloque_despues': len(nuevo),
                    'palabras_cuerpo_antes': palabras_antes, 'palabras_cuerpo_despues': palabras_despues,
                    'palabras_canonico': can_report[key]['palabras'],
                    'rotulos_antes': sum(1 for l in cuerpo_antes if l.strip() == targets[key]),
                    'rotulos_despues': 1,
                    'sha256_cuerpo_antes': sha_antes, 'sha256_cuerpo_despues': sha_despues,
                    'texto': nuevo})

# aplicar de abajo arriba para no desplazar indices
for d in sorted(detalle, key=lambda x: -x['linea_antes']):
    i = d['linea_antes'] - 1
    j = i + d['lineas_bloque_antes']
    lines[i:j] = d['texto']
new_text = '\r\n'.join(lines)
shutil.copy2(ley, ley.with_name(ley.name + '.bak-2026-09-21-ronda3'))
ley.write_bytes(new_text.encode('utf-8'))
raw_after = ley.read_bytes()
sha_after = hashlib.sha256(raw_after).hexdigest()

# verificacion posterior
t2 = raw_after.decode('utf-8')
l2 = t2.split('\r\n')
idx2 = [i for i, l in enumerate(l2) if re.match(r'## \[a\d+\] Artículo', l)]
verif = []
for d in detalle:
    i = next(i for i in idx2 if l2[i].startswith('## [%s]' % d['bloque']))
    j = next((x for x in idx2 if x > i), len(l2))
    cuerpo = l2[i+1:j]
    canon = secs[d['bloque']]
    verif.append({'bloque': d['bloque'], 'rotulos': sum(1 for l in cuerpo if l.strip() == targets[d['bloque']]),
                  'palabras_cuerpo': len(' '.join(cuerpo).split()),
                  'canonico_presente_literal': all(c in cuerpo for c in canon),
                  'canonico_lineas': len(canon), 'lineas_bloque': j-i})
print('bloques despues:', len(idx2))
print('VERIFICACION:', json.dumps(verif, ensure_ascii=False))

man = {
 'ley': 'Ley 58/2003 General Tributaria (BOE-A-2003-23186)', 'fecha': '2026-09-21', 'sesion': '13/30',
 'ministerio': 'hacienda',
 'ejecutor': 'Presidencia (Mastermind) — el agente del ministro de Hacienda fallo por timeout en dos intentos a las 23:05 y 23:20; Presidencia ejecuta los acuerdos aprobados en la ronda 3 de la sesion 13 con el texto canonico verificado',
 'fichero': 'ministerios/hacienda/leyes/BOE-A-2003-23186.md',
 'fuente_verdad_fidelidad': 'ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt (canonico BOE archivado)',
 'fuente_acuerdo': 'consejo/actas/2026-09-21.md (ronda 3, sesion 13/30)',
 'copia_seguridad': 'ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-21-ronda3',
 'sha256_fichero_antes': sha_before, 'sha256_fichero_despues': sha_after,
 'eol': 'CRLF preservado (split/join con CRLF)',
 'canonico_comprobado': can_report, 'bloques': detalle, 'verificacion': verif,
}
for d in man['bloques']:
    d.pop('texto', None)
(ev / 'manifiesto_ronda3_2026-09-21.json').write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding='utf-8')
with (ev / 'SHA256SUMS_2026-09-21.txt').open('a', encoding='utf-8', newline='') as f:
    f.write('%s *leyes/BOE-A-2003-23186.md\n' % sha_after)
    f.write('%s *leyes/BOE-A-2003-23186.md.bak-2026-09-21-ronda3\n' % sha_before)
    f.write('%s *evidencia/manifiesto_ronda3_2026-09-21.json\n' % hashlib.sha256((ev / 'manifiesto_ronda3_2026-09-21.json').read_bytes()).hexdigest())
print('sha_antes:', sha_before)
print('sha_despues:', sha_after)

# --- intento de extraccion del art. 12 (BOE consolidado archivado) para la restitucion pendiente ---
html = (ev / 'boe_consolidado_BOE-A-2003-23186.html').read_bytes().decode('utf-8', 'ignore')
plano = re.sub(r'<[^>]+>', ' ', html)
plano = re.sub(r'&nbsp;', ' ', plano)
plano = re.sub(r'\s+', ' ', plano)
m = re.search(r'Artículo 12\.\s*Interpretación de las normas tributarias', plano)
print('art12 encontrado:', bool(m))
if m:
    print('EXTRACTO art12:', plano[m.start():m.start()+1400])
