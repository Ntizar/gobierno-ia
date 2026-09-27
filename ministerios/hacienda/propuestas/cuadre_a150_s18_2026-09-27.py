# -*- coding: utf-8 -*-
# Sesion 18/30 - cuadre definitivo de los 2 casos F1 de [a150]: ¿texto real del manifiesto y donde vive?
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()
m = json.load(open('ministerios/hacienda/evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json', encoding='utf-8'))
casos = [c for c in m['casos_fidelidad'] if c.get('v') == 'contenido_perdido' and 'a150' in str(c.get('bloque', ''))]
vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())
cons = norm(re.sub(r'<[^>]+>', ' ', open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()))
print('casos a150 en manifiesto:', len(casos))
for c in casos:
    print(json.dumps(c, ensure_ascii=False)[:400])
    for k in ('texto', 'fragmento', 'letra', 'pieza'):
        if c.get(k):
            n = norm(c[k])
            print(f'  campo {k}: len {len(n.split())} | en vivo: {n in vivo} | en consolidado: {n in cons}')
            # probar sin la letra "b)" y recortado
            nn = re.sub(r'^b\)\s*', '', n)
            print('  sin b): en vivo:', nn in vivo, '| en consolidado:', nn in cons)
