# Cita decisiva para el acuerdo 37: ¿a qué artículo pertenece «El ejercicio de las competencias…» EN EL BOE CONSOLIDADO?
import re
SRC = {'html': 'ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html',
       'plano': 'ministerios/sanidad/evidencia/boe_texto_plano.txt',
       'canon': 'data/canonical/BOE-A-1986-10499/2026-08-31.json'}
for k, p in SRC.items():
    t = open(p, encoding='utf-8', errors='replace').read()
    if k == 'html':
        t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    print(f'==== {k} ====')
    for m in re.finditer(r'jercicio de las competencias', t, re.I):
        i = m.start()
        before = t[:i]
        arts = re.findall(r'Art[íi]culo (veinti[oa]|veintiuno|diecinueve|veintid[oó]s)\b', before)
        print('  último rótulo antes:', arts[-1] if arts else '?')
        print('  ventana:', t[max(0,i-180):i+300][:480])
        print('  ---')
    # ¿existe el texto actual del bloque [aveintiuno] (salud laboral, letras a-g) en esta fuente?
    probe = re.sub(r'\s+', ' ', 'La actuacion sanitaria en el ambito de la salud laboral').lower()
    tt = t.replace('ú','u').replace('ó','o').replace('é','e').replace('à','a').lower()
    print('  probe salud-laboral(1ª frase, sin acentos):', tt.count(probe))
# y en el .md: ¿el bloque [aveinte] (285-300) lleva el párrafo «El ejercicio…»?
md = open('ministerios/sanidad/leyes/BOE-A-1986-10499.md', encoding='utf-8').read().splitlines()
print('== [aveinte] (285-300) ==')
for n in range(285, 301):
    s = md[n-1].strip()
    if s: print(n, '|', s[:92])
print('ocurrencias «El ejercicio de las competencias» en TODO el .md:',
      sum(1 for l in md if 'El ejercicio de las competencias' in l))
