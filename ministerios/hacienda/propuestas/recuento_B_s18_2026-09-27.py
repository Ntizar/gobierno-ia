# -*- coding: utf-8 -*-
# Sesion 18/30 - RECUENTO F1 ACTUALIZADO, metrica B honesta:
# para cada precepto, las frases de la REDACCION VIGENTE del ejemplar consolidado archivado
# (ultima seccion 'Articulo N.', filtrada de aparato) que NO estan en los DOS ejemplares
# (fuente canon data/raw source.html) ni en el vivo. Las que faltan en los DOS y ademas
# no viven en el repo = phantom; las que viven en el ejemplar pero no en el repo = hueco real.
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    for a, b in [('&uacute;','ú'),('&oacute;','ó'),('&aacute;','á'),('&ntilde;','ñ'),('&iacute;','í'),('&eacute;','é'),
                 ('&Iacute;','Í'),('&Aacute;','Á'),('&Uacute;','Ú'),('&ccedil;','ç'),('&nbsp;',' '),('&iquest;','¿'),('&agrave;','à')]:
        s = s.replace(a, b)
    s = re.sub(r'&[a-zA-Z]+;', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
tx = re.sub(r'<br\s*/?>', '\n', html); tx = re.sub(r'</p>', '\n', tx); tx = re.sub(r'<[^>]+>', ' ', tx)
lns = [re.sub(r'\s+', ' ', l).strip() for l in tx.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')
APAR = re.compile(r'(seleccionar redacci|última actualizaci|modificación|publicada|publicado|en vigor|ref\. boletin|ref\. boe|boe-a-\d|subir \[|se añade|se modifica|se renumera|renumeran|téngase en cuenta|jurisprudencia|texto original|único\.\d|de la [Ll]ey \d|real decreto|disposición transitoria|se deroga|derogado|\[\d+\]|<)', re.I)

def seccion_vigente(artno):
    idx = [i for i, l in enumerate(lns) if re.match(rf'Artículo {artno}\. ', l)]
    if not idx: return ''
    i = idx[-1]; j = i + 1
    while j < len(lns) and not END.match(lns[j]): j += 1
    keep = [l for l in lns[i:j] if not APAR.search(l) and not l.startswith('#') and not l.startswith('[')]
    return ' '.join(keep)

vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())
src = norm(re.sub(r'<[^>]+>', ' ', open('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html', encoding='utf-8', errors='ignore').read()))
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
ids = [a['id'] for a in canon['articulos']]

huecos = {}
phantom = {}
for tag in ids:
    artno = re.sub(r'\D', '', tag)
    sv = seccion_vigente(int(artno)) if artno else ''
    if not sv: continue
    nsv = norm(sv)
    frases = [f.strip() for f in re.split(r'(?<=[.;:])\s+', nsv) if len(f.strip()) >= 25]
    falt_vivo = [f for f in frases if f not in vivo]
    reales = [f for f in falt_vivo if f in src]
    phant = [f for f in falt_vivo if f not in src]
    if reales: huecos[tag] = (len(reales), sum(len(f.split()) for f in reales), [f[:70] for f in reales[:2]])
    if phant: phantom[tag] = (len(phant), [f[:70] for f in phant[:2]])

tot_r = sum(v[0] for v in huecos.values()); tot_pr = sum(v[1] for v in huecos.values())
tot_p = sum(v[0] for v in phantom.values())
res = {'metrica_B': {'definicion': 'frases (>=25 chars) de la redaccion vigente del consolidado archivado (filtrada de aparato), ausentes del fichero vivo PERO presentes en la fuente canon source.html (hueco real) o ausentes de ambos (phantom: no es norma del BOE archivado — doctrina X1)',
      'preceptos_con_hueco_real': len(huecos), 'casos_hueco_real': tot_r, 'palabras_hueco_real': tot_pr,
      'preceptos_con_phantom': len(phantom), 'casos_phantom': tot_p,
      'detalle_huecos': huecos},
     'metrica_A': {'preceptos_con_texto': 292, 'de': 292, 'frases_ausentes': 0, 'fuente': 'pareo_frases_total_s18_2026-09-26.json (reproducido hoy con estado_sesion18_2026-09-27.py, hash a5e63375 inalterado)'}}
json.dump(res, open('ministerios/hacienda/evidencia/recuento_f1_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('METRICA B: hueco real =', len(huecos), 'preceptos,', tot_r, 'casos,', tot_pr, 'palabras')
print('METRICA B: phantom =', len(phantom), 'preceptos,', tot_p, 'casos')
for k, v in list(huecos.items())[:20]:
    print('  HUECO', k, v[0], 'casos', v[1], 'pal |', v[2][0][:66])
for k, v in list(phantom.items())[:12]:
    print('  PHANTOM', k, v[0], '|', v[1][0][:66])
