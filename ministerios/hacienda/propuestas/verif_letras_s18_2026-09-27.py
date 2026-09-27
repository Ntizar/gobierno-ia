# -*- coding: utf-8 -*-
# Sesion 18/30 - comprobacion de que las proposiciones no pierden letras vigentes
# contra el ejemplar BOE consolidado archivado (evidencia/boe_consolidado_*.html)
import re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
cons = norm(open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read())
vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8', errors='ignore').read())

def probe(label, frase):
    f = norm(frase)
    print(f'{label:55s} | consolidado={f in cons} | vivo={f in vivo}')

probe('a81.a) retencion devoluciones (¿vigente?)', 'La retención del pago de devoluciones tributarias o de otros pagos')
probe('a68.1.a) accionAdmin (¿vigente?)', 'Por cualquier acción de la Administración tributaria, realizada con conocimiento formal del obligado tributario, conducente al reconocimiento')
probe('a112 variante “según la Administración que dicte”', 'según la Administración que dicte')
probe('a112 variante Agencia publica', 'publicará por este medio los anuncios')
probe('a112 canon apertura', 'Cuando no sea posible efectuar la notificación al interesado o a su representante por causas no imputables a la Administración tributaria e intentada al menos dos veces')
# ¿el texto vigente del BOE tiene una sola de estas variantes o ambas?
print()
print('consolidado: ocurrencias "Cuando no sea posible efectuar la notificación":', cons.count('Cuando no sea posible efectuar la notificación'))
print('consolidado: ocurrencias "retención del pago de devoluciones":', cons.count('retención del pago de devoluciones'))
print('consolidado: ocurrencias "Por cualquier acción de la Administración tributaria":', cons.count('Por cualquier acción de la Administración tributaria'))
