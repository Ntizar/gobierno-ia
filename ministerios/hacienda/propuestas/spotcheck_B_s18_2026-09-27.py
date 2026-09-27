# -*- coding: utf-8 -*-
# Sesion 18/30 - spot-check metrica B: ¿los 3 primeros huecos son reales o artefacto de
# normalizacion (NBSP, sangrado)? Buscar variantes relajadas en el vivo.
import re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm2(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('\u00a0', ' ').replace('\u202f', ' ').replace('\u00ad', '')
    s = re.sub(r'<[^>]+>', ' ', s)
    for a, b in [('&uacute;','ú'),('&oacute;','ó'),('&aacute;','á'),('&ntilde;','ñ'),('&iacute;','í'),('&eacute;','é'),('&nbsp;',' ')]:
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip().lower()
vivo = norm2(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())
for f in ['esta ley establece los principios y las normas jurídicas generales',
          'las normas tributarias se interpretarán con arreglo a lo dispuesto',
          'por cualquier acción de la administración tributaria, realizada con conocimiento formal del obligado tributario, conducente al reconocimiento',
          'el incumplimiento de cualquiera de estas circunstancias determinará la exigencia']:
    n = norm2(f)
    # relaxed: sin espacios para matar sangrados
    nr = n.replace(' ', '')
    vr = vivo.replace(' ', '')
    print(f'{f[:66]:68s} | norm2: {n in vivo} | sin-espacios: {nr in vr}')
