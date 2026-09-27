# -*- coding: utf-8 -*-
# Sesion 18/30 - triangulacion: B v2 (estricta) da 0 huecos; el spot-check del a27 decia False.
# ¿Donde esta la verdad? Probar la frase conflictiva con 3 normas y en 4 fuentes.
import re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def n1(s):  # norma del pareo canon (la del cierre 292/292)
    s = unicodedata.normalize('NFC', s); s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()
def n2(s):  # norma estricta con NBSP/plano
    s = unicodedata.normalize('NFC', s); s = s.replace('\u00a0', ' ').replace('\u202f', ' ').replace('\u00ad', '')
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
def n3(s):  # solo letras minusculas, sin espacios (ultima instancia)
    s = unicodedata.normalize('NFD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())
FR = ['El incumplimiento de cualquiera de estas circunstancias determinará la exigencia del porcentaje de recargo que corresponda de acuerdo con lo dispuesto en los artículos 27.1.a) o 27.1.b) de esta ley',
      'Esta Ley establece los principios y las normas jurídicas generales',
      'Por cualquier acción de la Administración tributaria, realizada con conocimiento formal del obligado tributario, conducente al reconocimiento']
vivo_raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
src_raw = open('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html', encoding='utf-8', errors='ignore').read()
cons_raw = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
for f in FR:
    print('==', f[:70])
    for label, raw in [('vivo', vivo_raw), ('source', src_raw), ('consolidado', cons_raw)]:
        print(f'   {label:11s} n1={n1(f) in n1(raw)}  n2={n2(f) in n2(raw)}  n3={n3(f) in n3(raw)}')
