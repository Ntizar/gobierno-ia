# Último cierre de verdad [aveintiuno]: (a) TODAS las notas del 21 en el plano, (b) total scan exacto, (c) ¿la «perspectiva de género» está en fuentes?
import re, subprocess

p = open('ministerios/sanidad/evidencia/boe_texto_plano.txt', encoding='utf-8').read()
plines = p.splitlines()
print('== NOTAS COMPLETAS DEL ART. 21 EN EL PLANO (4018-4042) ==')
for n in range(4018, 4043):
    l = plines[n-1].strip()
    if l:
        print(n, '|', l[:140])

print('== TOTALS SCAN ==')
out = subprocess.run(['python', 'ministerios/sanidad/propuestas/dedup_scan.py'], capture_output=True, text=True).stdout
for l in out.splitlines():
    if 'TOTAL' in l.upper() and ('palabra' in l.lower() or 'bloque' in l.lower()):
        print(l[:200])

srcs = {}
for k, path in {'html': 'ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html',
                'plano': 'ministerios/sanidad/evidencia/boe_texto_plano.txt',
                'canon': 'data/canonical/BOE-A-1986-10499/2026-08-31.json'}.items():
    t = open(path, encoding='utf-8', errors='replace').read()
    if k == 'html':
        t = re.sub(r'<[^>]+>', ' ', t)
    srcs[k] = re.sub(r'\s+', ' ', t).lower()
print('== FRASES DEL BLOQUE ACTUAL .md ==')
for f in ['la actuación sanitaria en el ámbito de la salud laboral',
          'integrará en todo caso la perspectiva de género',
          'salud integral del trabajador',
          'factores de microclima laboral',
          'mapa de riesgos laborales',
          'el ejercicio de las competencias enumeradas en este artículo',
          'llevó a cabo bajo la dirección',
          'registro de morbilidad y mortalidad por patología']:
    print(f'{f[:58]!r:60}', {k: s.count(f.lower()) for k, s in srcs.items()})
