# -*- coding: utf-8 -*-
# Sesion 18/30 - METRICA B v2 (estricta, misma normalizacion a ambos lados, sondeo de
# falsos positivos incluido). F1 ACTUALIZADO: frases de la redaccion vigente del
# consolidado archivado (filtrada de aparato) que NO viven en el fichero vivo.
# Cada caso se clasifica: REAL (esta en la fuente canon data/raw) o PHANTOM (en ninguna parte).
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('\u00a0', ' ').replace('\u202f', ' ').replace('\u00ad', '')
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'&[a-zA-Z#0-9]+;', lambda m: {'&uacute;':'ú','&oacute;':'ó','&aacute;':'á','&ntilde;':'ñ',
        '&iacute;':'í','&eacute;':'é','&Iacute;':'Í','&Aacute;':'Á','&Uacute;':'Ú','&ccedil;':'ç','&nbsp;':' ',
        '&iquest;':'¿','&raquo;':'»','&laquo;':'«','&Eacute;':'É','&egrave;':'è','&egrave;':'è'}.get(m.group(0), ' '), s)
    s = s.replace('\u2019', "'").replace('’', "'")
    return re.sub(r'\s+', ' ', s).strip().lower()

html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
tx = re.sub(r'<br\s*/?>', '\n', html); tx = re.sub(r'</p>', '\n', tx)
lns = [re.sub(r'\s+', ' ', l).strip() for l in tx.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')
APAR = re.compile(r'(seleccionar redacci|última actualizaci|modificación de apartado|publicada el|publicado el|en vigor|ref\. bolet|ref\. boe|boe-a-20|subir \[|subir sección|subir título|se añade|se modifica|se renumera|renumeran|téngase en cuenta|jurisprudencia|texto original|único\.\d|\d+\.\d+ de la ley \d|real decreto|disposición transitoria|se deroga|\(derogad)', re.I)

def seccion_vigente(artno):
    idx = [i for i, l in enumerate(lns) if re.match(rf'Artículo {artno}\. ', l)]
    if not idx: return ''
    i = idx[-1]; j = i + 1
    while j < len(lns) and not END.match(lns[j]): j += 1
    keep = []
    for l in lns[i:j]:
        ls = l.strip()
        if not ls or ls.startswith('#') or ls.startswith('['): continue
        if APAR.search(ls): continue
        if re.match(r'^\d+\.\d*\.?\s*(de la|por el)', ls, re.I): continue
        keep.append(ls)
    return ' '.join(keep)

vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())
src = norm(open('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html', encoding='utf-8', errors='ignore').read())
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
ids = [a['id'] for a in canon['articulos']]
real = {}; phantom = {}
for tag in ids:
    art = re.sub(r'\D', '', tag)
    if not art: continue
    sv = seccion_vigente(int(art))
    if not sv: continue
    nsv = norm(sv)
    for f in [x.strip() for x in re.split(r'(?<=[.;:])\s+', nsv) if len(x.strip()) >= 30]:
        if f in vivo: continue
        rec = real if f in src else phantom
        rec.setdefault(tag, []).append((f[:100], len(f.split())))
tot_real = sum(len(v) for v in real.values()); pal_real = sum(w for v in real.values() for _, w in v)
tot_ph = sum(len(v) for v in phantom.values())
out = {'metrica_B_v2': {'unidad': 'frase (>=30 chars) de la redaccion vigente del consolidado archivado, filtrada de aparato editorial, ausente del vivo',
        'preceptos_afectados': len(real), 'casos': tot_real, 'palabras': pal_real,
        'phantom': {'preceptos': len(phantom), 'casos': tot_ph, 'nota': 'frase vigente-segun-consolidado ausente TAMBIEN de la fuente canon data/raw: sospecha de aparato no filtrado, no de norma perdida'},
        'detalle': {k: [x[0] for x in v] for k, v in list(real.items())}} ,
       'metrica_A': {'preceptos_con_texto': 292, 'de': 292, 'frases_ausentes': 0}}
json.dump(out, open('ministerios/hacienda/evidencia/recuento_f1_B_v2_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('REAL:', len(real), 'preceptos,', tot_real, 'casos,', pal_real, 'palabras')
for k, v in list(real.items())[:30]:
    print('  ', k, len(v), '|', v[0][0][:80])
print('PHANTOM:', len(phantom), 'preceptos,', tot_ph, 'casos')
for k, v in list(phantom.items())[:10]:
    print('  ph', k, '|', v[0][0][:80])
