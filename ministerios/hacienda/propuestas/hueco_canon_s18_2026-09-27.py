# -*- coding: utf-8 -*-
# Sesion 18/30 - ¿huecos del propio canon JSON? Las frases "vigentes ausentes" del test
# se buscan en: canon[tag], canon de OTROS preceptos, source.html crudo.
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('&uacute;', 'ú').replace('&oacute;', 'ó').replace('&aacute;', 'á')
    return re.sub(r'\s+', ' ', s).strip().lower()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: norm(a['texto']) for a in canon['articulos']}
todo_canon = ' '.join(arts.values())
src = norm(open('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html', encoding='utf-8', errors='ignore').read())
src = re.sub(r'<[^>]+>', ' ', src); src = re.sub(r'\s+', ' ', src)
vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())

PROB = {
 'a81': ['Las medidas cautelares reguladas en este artículo podrán adoptarse durante la tramitación de los procedimientos',
         'Cuando en la tramitación de una solicitud de suspensión con otras garantías distintas',
         'Que se conviertan en embargos en el procedimiento de apremio',
         'Si con posterioridad a su adopción, se solicitara al órgano judicial penal competente la suspensión contemplada en el artículo 305.5',
         'Se podrá acordar el embargo preventivo de dinero y mercancías en cuantía suficiente para asegurar el pago de la deuda',
         'Asimismo, podrá acordarse el embargo preventivo de los ingresos de los espectáculos públicos'],
 'a68': ['Por cualquier acción de la Administración tributaria, realizada con conocimiento formal del obligado tributario, conducente al reconocimiento',
         'El plazo de prescripción del derecho a que se refiere el párrafo b) del artículo 66 de esta Ley se interrumpe',
         'El plazo de prescripción del derecho al que se refers (dummy)',
         'Las actuaciones a las que se refieren los apartados anteriores y las de naturaleza análoga producirán los efectos'],
 'a65': ['a) Aquellas cuya exacción se realice por medio de efectos timbrados'],
}
for tag, frs in PROB.items():
    print(f'== {tag} ==')
    for f in frs:
        n = norm(f)
        if 'dummy' in f: continue
        print(f'  {f[:64]}...')
        print(f'    en canon[{tag}]: {n in arts[tag]} | en canon (otro precepto): {n in todo_canon and n not in arts[tag]} | en source.html: {n in src} | en vivo repo: {n in vivo}')
