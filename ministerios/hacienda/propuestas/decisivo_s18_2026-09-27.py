# -*- coding: utf-8 -*-
# Sesion 18/30 - TEST DECISIVO canon-JSON vs realidad, por frase:
# ¿fuente canon source.html? ¿consolidado archivado? ¿fichero vivo? -> decide que se propone.
import re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    for a, b in [('&uacute;','ú'),('&oacute;','ó'),('&aacute;','á'),('&ntilde;','ñ'),('&iacute;','í'),('&eacute;','é'),('&Iacute;','Í'),('&agrave;','à'),('&ccedil;','ç'),('&Aacute;','Á'),('&Ó','Ó')]:
        s = s.replace(a, b)
    s = re.sub(r'&[a-zA-Z]+;', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
src = norm(re.sub(r'<[^>]+>', ' ', open('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html', encoding='utf-8', errors='ignore').read()))
cons = norm(re.sub(r'<[^>]+>', ' ', open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()))
vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())
import json
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: norm(a['texto']) for a in canon['articulos']}

FR = {
 'a81': ['Las medidas cautelares reguladas en este artículo podrán adoptarse durante la tramitación de los procedimientos de aplicación de los tributos',
         'Cuando en la tramitación de una solicitud de suspensión con otras garantías distintas de las necesarias para obtener la suspensión automática',
         'Que se conviertan en embargos en el procedimiento de apremio',
         'Si con posterioridad a su adopción, se solicitara al órgano judicial penal competente la suspensión contemplada en el artículo 305.5 del Código Penal',
         'Se podrá acordar el embargo preventivo de dinero y mercancías en cuantía suficiente para asegurar el pago de la deuda tributaria que proceda exigir por actividades lucrativas ejercidas sin establecimiento',
         'Podrá acordarse el embargo preventivo de los ingresos de los espectáculos públicos',
         'a) La retención del pago de devoluciones tributarias o de otros pagos'],
 'a68': ['Por cualquier acción de la Administración tributaria, realizada con conocimiento formal del obligado tributario, conducente al reconocimiento, regularización, comprobación, inspección y recaudación',
         'El plazo de prescripción del derecho a que se refiere el párrafo b) del artículo 66 de esta Ley se interrumpe',
         'El plazo de prescripción del derecho al que se refiere el párrafo c) del artículo 66 de esta Ley',
         'El plazo de prescripción del derecho al que se refiere el párrafo d) del artículo 66 de esta Ley',
         'Las actuaciones a las que se refieren los apartados anteriores y las de naturaleza análoga producirán los efectos'],
 'a65': ['a) Aquellas cuya exacción se realice por medio de efectos timbrados'],
}
for tag, frs in FR.items():
    print(f'== {tag} ==')
    for f in frs:
        n = norm(f)
        print(f'  src={int(n in src)} cons={int(n in cons)} vivo={int(n in vivo)} canon={int(n in arts[tag])} | {f[:64]}')
