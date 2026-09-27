# -*- coding: utf-8 -*-
# Sesion 18/30 - test final con FILTRO DE APARATO: secciones vigentes del consolidado vs propuestos
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    s = s.replace('&uacute;', 'ú').replace('&oacute;', 'ó').replace('&aacute;', 'á').replace('&igrave;', 'ì')
    return re.sub(r'\s+', ' ', s).strip().lower()
APARATO = re.compile(r'(seleccionar redacci|última actualizaci|modificaci|publicada el|publicado el|en vigor|ref\. boletin|ref\. boe|boe-a-20|subir \[|se añade|se modifica|se renumera|renumeran|téngase en cuenta|único\.\d|\d\.\d+ de la ley|disposición transitoria única|texto original)', re.I)

vivo_raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
print('a150 letra completa "reanudación de las actuaciones" en vivo:', norm('Los ingresos realizados desde el inicio del procedimiento hasta la reanudación de las actuaciones') in norm(vivo_raw))
print('a65 letra "aquellas cuya exacción" en vivo:', norm('aquellas cuya exacción se realice por medio de efectos timbrados') in norm(vivo_raw))

raw_html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
txt = re.sub(r'<br\s*/?>', '\n', raw_html); txt = re.sub(r'</p>', '\n', txt); txt = re.sub(r'<[^>]+>', ' ', txt)
lines = [re.sub(r'\s+', ' ', l).strip() for l in txt.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')
def seccion(artno):
    idx = [i for i, l in enumerate(lines) if re.match(rf'Artículo {artno}\. ', l)]
    i = idx[-1]; j = i + 1
    while j < len(lines) and not END.match(lines[j]): j += 1
    return ' '.join(lines[i:j])

for tag in ['a81', 'a68', 'a65', 'a112']:
    prop_path = f'ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-27.txt'
    if not os.path.exists(prop_path):
        print(tag, 'sin propuesto'); continue
    artno = int(re.sub(r'\D', '', tag))
    sv = seccion(artno); nsv = norm(sv)
    nprop = norm(open(prop_path, encoding='utf-8').read())
    frases = [f.strip() for f in re.split(r'(?<=[.;:])\s+', nsv) if len(f.strip()) >= 15]
    aus = [f for f in frases if f not in nprop and not APARATO.search(f)]
    print(f'== {tag}: frases vigentes (sin aparato) ausentes del propuesto: {len(aus)} ==')
    for f in aus:
        print('   ·', f[:110])
