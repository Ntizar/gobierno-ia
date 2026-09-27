# -*- coding: utf-8 -*-
# Sesion 18/30 - ultima duda de vigencia resuelta con el segundo ejemplar BOE (regla del 09-02):
# [a112]: ¿la capa 4 del vivo (sede electronica / Ley 15-2014) esta en el ejemplar descargado
# directo el 02-09 (boe_vivo_LGT_2026-09-02.html)? ¿Y la capa 3 (canon) tambien?
# [a81]: ¿las frases «de mas» del consolidado (apartados 5/8/9) viven en el texto del vivo?
import re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'")
    for a, b in [('&uacute;','ú'),('&oacute;','ó'),('&aacute;','á'),('&ntilde;','ñ'),('&iacute;','í'),('&eacute;','é'),('&Iacute;','Í')]:
        s = s.replace(a, b)
    s = re.sub(r'&[a-zA-Z]+;', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
v2 = norm(re.sub(r'<[^>]+>', ' ', open('ministerios/hacienda/evidencia/boe_vivo_LGT_2026-09-02.html', encoding='utf-8', errors='ignore').read()))
cons = norm(re.sub(r'<[^>]+>', ' ', open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()))
vivo_raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
nvivo = norm(vivo_raw)

PROBES_A112 = [
 ('capa4? Agencia publicara por este medio', 'La Agencia Estatal de Administración Tributaria publicará por este medio los anuncios correspondientes'),
 ('capa3/canon? oficina de la Administracion correspondiente', 'Estos anuncios podrán exponerse asimismo en la oficina de la Administración tributaria correspondiente'),
 ('capa4? sede electronica (BOE digital)', 'sin perjuicio de su publicación' ),
 ('canon? publicacion lunes miercoles viernes', 'La publicación en el «Boletín Oficial del Estado» se efectuará los lunes, miércoles y viernes de cada semana.'),
 ('canon? comparecencia 15 dias naturales', 'En todo caso, la comparecencia deberá producirse en el plazo de 15 días naturales'),
]
print('== [a112] en el ejemplar vivo descargado 02-09 ==')
for lab, fr in PROBES_A112:
    print(f'  {lab[:52]:54s} vivo09-02={norm(fr) in v2} | consolidado={norm(fr) in cons} | ley_repo={norm(fr) in nvivo}')

print('== [a81] ¿apartados del consolidado viven en el repo? ==')
for fr in ['Las medidas cautelares reguladas en este artículo podrán adoptarse durante la tramitación de los procedimientos de aplicación de los tributos',
           'Se podrá acordar el embargo preventivo de dinero y mercancías en cuantía suficiente',
           'podrá acordarse el embargo preventivo de los ingresos de los espectáculos públicos',
           'Que se conviertan en embargos en el procedimiento de apremio',
           'Cuando en la tramitación de una solicitud de suspensión con otras garantías distintas']:
    n = norm(fr)
    print(f'  {fr[:56]:58s} repo={n in nvivo} | vivo09-02={n in v2}')
