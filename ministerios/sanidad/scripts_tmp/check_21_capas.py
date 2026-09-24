# Último check: ¿las letras a)-g) y el apdo 2 del [aveintiuno] del .md tienen respaldo en las 3 fuentes?
import re

md = open('ministerios/sanidad/leyes/BOE-A-1986-10499.md', encoding='utf-8').read()
lines = md.splitlines()
# frases extraídas del bloque tal como está (l. 301-345):
frases = [
 'protección de la salud de los trabajadores',
 'vigilancia de los medios',
 'eliminación y control de los agentes',
 'técnicas que afecten a las condiciones de trabajo',
 'control sanitario de los centros de trabajo',
 'dirección de las autoridades sanitarias',
 'estrecha coordinación con las autoridades laborales',
 'seguridad e higiene en',
 'las empresas.',
 'facultades:',
]
SRC = {
 'html': 'ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html',
 'plano': 'ministerios/sanidad/evidencia/boe_texto_plano.txt',
 'canon': 'data/canonical/BOE-A-1986-10499/2026-08-31.json',
}
srcs = {}
for k, p in SRC.items():
    t = open(p, encoding='utf-8', errors='replace').read()
    if k == 'html':
        t = re.sub(r'<[^>]+>', ' ', t)
    srcs[k] = re.sub(r'\s+', ' ', t).lower()
print('== ¿qué frases del bloque existen en las fuentes? ==')
for f in frases:
    fl = f.lower()
    print(f'{f[:55]!r:57} html={srcs["html"].count(fl)} plano={srcs["plano"].count(fl)} canon={srcs["canon"].count(fl)}')
# Volcado compacto del bloque para citar en propuestas lo que REALMENTE dice
print('== BLOQUE 301-345 real ==')
for n in range(301, 346):
    l = lines[n-1].strip()
    if l:
        print(n, '|', l[:96])
