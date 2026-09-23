# Verificación case-insensitive de la errata [aveintiuno] + lectura final del bloque 36 + scan residual
import re

SRC = {
 'html': 'ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html',
 'plano': 'ministerios/sanidad/evidencia/boe_texto_plano.txt',
 'canon': 'data/canonical/BOE-A-1986-10499/2026-08-31.json',
}
texts = {}
for k, p in SRC.items():
    t = open(p, encoding='utf-8', errors='replace').read()
    t = re.sub(r'<[^>]+>', ' ', t) if k == 'html' else t
    texts[k] = re.sub(r'\s+', ' ', t).lower()

claves = [
 'el ejercicio de las competencias',
 'estrecha coordinación con las autoridades laborales',
 'dirección de las autoridades sanitarias',
 'órganos de participación, inspección y control de las condiciones de trabajo',
 'corresponde a las administraciones públicas, en el ámbito de la salud laboral',
 'la acción de las administraciones públicas en la protección',
 'se añaden las letras f) y g) al apartado 1',
]
print('== BÚSQUEDA CASE-INSENSITIVE (normalizada) ==')
for c in claves:
    print(f'{c[:60]!r:62} html={texts["html"].count(c)} plano={texts["plano"].count(c)} canon={texts["canon"].count(c)}')

print('== BLOQUE 36 (528-557) ==')
md = open('ministerios/sanidad/leyes/BOE-A-1986-10499.md', encoding='utf-8').read()
lines = md.splitlines()
for n in range(528, 558):
    l = lines[n-1]
    if l.strip():
        print(n, '|', len(l.split()), 'w |', l.strip()[:88])

print('== SCAN RESIDUAL ==')
import subprocess, json
out = subprocess.run(['python', 'ministerios/sanidad/propuestas/dedup_scan.py'], capture_output=True, text=True).stdout
tail = out.splitlines()[-16:]
print('\n'.join(tail))
