# REVOCACIÓN de mi errata del [aveintiuno] (acuerdo 37): el marcador (Derogado) NO es huérfano,
# es el derogatorio del PROPIO art. 21 (Ley 33/2011, DF ú, Ref. BOE-A-2011-15623 — nota visible en
# las 3 fuentes del repo). Lo que sí es un artefacto de la fusión del 22-09 es el párrafo
# «3. El ejercicio de las competencias…» (apartado 3 del art. 20) colocado DESPUÉS del cuerpo del 21.
# Acción: restaurar el fichero desde el .bak de sesión con SOLO el dedup del 47 (estado sha 92ef…).
import hashlib, json, subprocess, sys

BAK = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md.bak-2026-09-23'
PATH = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md'

# 1) restaurar PATH desde el .bak de sesión (estado inicial eb54…) y re-aplicar SOLO el dedup 47
import shutil
shutil.copyfile(BAK, PATH)
r = subprocess.run([sys.executable, 'ministerios/sanidad/scripts_tmp/apply_acuarentaysiete_2026-09-23.py'],
                   capture_output=True, text=True)
print('re-apply 47:', r.stdout.strip()[:200], r.returncode)
sha_after47 = hashlib.sha256(open(PATH,'rb').read()).hexdigest()
print('sha tras solo-47:', sha_after47)
assert sha_after47 == '92ef137244a82d6406f4a6acae5754e11ed58d3769f1092e9ce1597f42ec3542', 'no coincide con el estado verificado del dedup 47'

# 2) verificar estado: 12 marcadores, el del 21 presente tras el párrafo misplaced
data = open(PATH, 'rb').read()
i = data.find('## [aveintiuno]'.encode()); j = data.find('## [aveintidos]'.encode())
seg = data[i:j]
print('marcadores totales:', data.count(b'(Derogado)'))
print('marcador en [aveintiuno]:', seg.count(b'(Derogado)'))
print('párrafo 20.3 presente:', b'El ejercicio de las competencias enumeradas en este art' in seg)

# 3) ¿dónde termina el cuerpo del art. 20? cabeceras cercanas
lines = data.decode('utf-8').splitlines()
for n, l in enumerate(lines[:340], 1):
    if l.startswith('## [avein') or l.startswith('## [adiecinueve]'):
        print('cabecera', n, l[:60])
# texto del bloque [aveinte] si existe
k = [idx for idx, l in enumerate(lines, 1) if l.startswith('## [aveinte]')]
if k:
    k0 = k[0]
    k1 = [idx for idx, l in enumerate(lines, 1) if l.startswith('## [') and idx > k0][0]
    print('== BLOQUE [aveinte]', k0, '-', k1-1, '==')
    for n in range(k0, k1):
        s = lines[n-1].strip()
        if s: print(n, '|', s[:92])

# 4) scan residual con marcador restaurado
out = subprocess.run([sys.executable, 'ministerios/sanidad/propuestas/dedup_scan.py'],
                     capture_output=True, text=True).stdout
tots = [l for l in out.splitlines() if 'TOTAL' in l.upper() or 'RESIDUAL' in l.upper()][:6]
print('== SCAN =='); [print(t[:160]) for t in tots]

# 5) manifiesto de revocación
rev = {
 'fecha': '2026-09-23', 'sesion': '15/30',
 'actuacion': 'REVOCACIÓN de la retirada del marcador (Derogado) de [aveintiuno] ejecutada a las 13:19 por esta ministra',
 'motivo': ('Comprobación con las 3 fuentes BOE del repo (evidencia/boe_consolidado_BOE-A-1986-10499.html, '
   'evidencia/boe_texto_plano.txt l.4018-4042, data/canonical/BOE-A-1986-10499/2026-08-31.json): el '
   'marcador es la nota de derogación del PROPIO artículo veintiuno («Se deroga por la disposición '
   'derogatoria única de la Ley 33/2011… Ref. BOE-A-2011-15623»). Retirarlo habría eliminado una '
   'derogación vigente. El artefacto real de la fusión del 22-09 es otro: el párrafo «3. El ejercicio '
   'de las competencias enumeradas en este artículo…» es el apartado 3 del art. 20 (encadenado en las '
   'fuentes tras «2. Las actividades de fomento sobre salud laboral…» del 20) y quedó descolocado '
   'después del cuerpo del 21, lo que hacía parecer huérfano al marcador.'),
 'regla_aplicada': 'Acuerdo 37 del acta 2026-09-22: «con cita, o no se borra». La cita dice lo contrario de lo que mi primer vistazo interpretó: NO se borra.',
 'estado_final': {'sha256': sha_after47, 'marcadores_totales': data.count(b'(Derogado)'),
   'errata_37': 'ABIERTA — propuesta como reubicación del párrafo 20.3 en propuestas/2026-09-23.md, no ejecutada'},
 'anulados': {'manifiesto': 'ministerios/sanidad/evidencia/manifiesto_errata_aveintiuno_2026-09-23.json',
   'nota': 'queda en el repo como registro del error; el estado del fichero NO es el que describe'},
}
json.dump(rev, open('ministerios/sanidad/evidencia/manifiesto_errata_aveintiuno_REVOCADO_2026-09-23.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('OK revocación registrada')
