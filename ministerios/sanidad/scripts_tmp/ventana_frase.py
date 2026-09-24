# Contexto exacto de la única frase real: 'El ejercicio de las competencias' en las 3 fuentes BOE del repo
import re

SRC = {
 'html': 'ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html',
 'plano': 'ministerios/sanidad/evidencia/boe_texto_plano.txt',
 'canon': 'data/canonical/BOE-A-1986-10499/2026-08-31.json',
}
frase = 'El ejercicio de las competencias'
for k, p in SRC.items():
    t = open(p, encoding='utf-8', errors='replace').read()
    if k == 'html':
        t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    print(f'==== {k} ====')
    for m in re.finditer(re.escape(frase), t, re.I):
        i = m.start()
        print('  ...' + t[max(0,i-260):i+420])
        print('  ----')
