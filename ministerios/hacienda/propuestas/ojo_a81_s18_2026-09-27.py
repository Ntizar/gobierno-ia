# -*- coding: utf-8 -*-
# Sesion 18/30 - verificacion OJO: las 7 frases del consolidado ausentes de la cola [a81],
# ¿son texto VIGENTE o capas historicas dentro de la seccion? Comparar con cada version del HTML.
import re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
# localizar el bloque del art 81 y las etiquetas "Vigente desde" / "Redacción dada por"
i = html.find('Artículo 81.')
seg = html[i:i+90000]
# ¿la frase conflictiva esta bajo una nota de vigencia o dentro del texto?
for fr in ['durante la tramitación de los procedimientos de aplicación de los tributos',
           'embargo preventivo de dinero y mercancías',
           'ingresos de los espectáculos públicos',
           'que se conviertan en embargos en el procedimiento de apremio']:
    j = seg.find(fr)
    print('==', fr[:60], '| pos en seg:', j)
    if j >= 0:
        ctx = re.sub(r'<[^>]+>', ' ', seg[max(0,j-400):j+200])
        ctx = re.sub(r'\s+', ' ', ctx)
        print('   ctx:', ctx[-360:])
