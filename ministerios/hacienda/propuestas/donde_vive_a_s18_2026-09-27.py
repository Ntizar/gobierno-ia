# -*- coding: utf-8 -*-
# Sesion 18/30 - donde vive exactamente la letra a) del 68.1 y del 81.4 en canon y consolidado
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
for tag in ['a81', 'a68', 'a112']:
    t = norm(arts[tag]['texto'])
    print(f'== canon {tag}: "Por cualquier acción"={t.count("por cualquier acción")}, "retención del pago de devoluciones"={t.count("retención del pago de devoluciones")}, "a) "={t.count("a) ")}')
html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
h = norm(re.sub(r'<[^>]+>', ' ', html))
h = re.sub(r'\s+', ' ', h)
print('consolidado(sin tags): Por cualquier acción =', h.count('por cualquier acción'), '| retención del pago de devoluciones =', h.count('retención del pago de devoluciones'))
# contexto de cada ocurrencia de la letra a) del 68.1 en el consolidado
for m in re.finditer('conducente al reconocimiento', h):
    print('  ctx68:', h[max(0, m.start()-160):m.start()+60])
# ¿cuantos articulos 68/81/112 hay en el consolidado (las capas que el BOE muestra)?
for arto in ['Artículo 68.', 'Artículo 81.', 'Artículo 112.']:
    print(arto, 'apariciones en consolidado:', h.count(arto.lower()))
