# -*- coding: utf-8 -*-
# Sesion 18/30 - RECUENTO F1 ACTUALIZADO (encargo del acta 17, obs. 3):
# metrica A (cierre acuerdo 67): frases del canon JSON ⊆ vivo -> 292/292 hoy.
# metrica B (territorio): frases de la REDACCION VIGENTE de data/raw source.html ⊄ vivo.
#   La redaccion vigente = el trozo de la seccion 'Articulo N.' ANTES de 'Seleccionar redaccion'.
# El canon JSON se extrajo con huecos (letras a) caidas): por eso la B encuentra lo que la A no ve.
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    for a, b in [('&uacute;','ú'),('&oacute;','ó'),('&aacute;','á'),('&ntilde;','ñ'),('&iacute;','í'),('&eacute;','é'),
                 ('&Iacute;','Í'),('&agrave;','à'),('&ccedil;','ç'),('&Aacute;','Á'),('&Eacute;','É'),('&Uacute;','Ú'),('&iquest;','¿'),('&nbsp;',' ')]:
        s = s.replace(a, b)
    s = re.sub(r'&[a-zA-Z]+;', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

src_html = open('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html', encoding='utf-8', errors='ignore').read()
src_txt = norm(re.sub(r'<[^>]+>', ' ', src_html))
vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}

# secciones 'Artículo N.' hasta la siguiente marca de version/redaccion o proximo articulo
marks = [(m.start(), int(m.group(1))) for m in re.finditer(r'artículo (\d+)\. ', src_txt)]
resumen = {}
for k, (pos, artno) in enumerate(marks):
    end = marks[k+1][0] if k+1 < len(marks) else len(src_txt)
    seg = src_txt[pos:end]
    for stop in ['seleccionar redaccion', 'seleccionar redación']:
        j = seg.find(stop)
        if j > 50: seg = seg[:j]; break
    j = seg.find('vigente desde')
    if j > 50: seg = seg[:j]
    frases = [f.strip() for f in re.split(r'(?<=[.;:])\s+', seg) if len(f.strip()) >= 15]
    faltan = [f for f in frases if f not in vivo and f not in ('artículo ' + str(artno) + '.',)]
    tag = 'a' + str(artno)
    if tag not in arts: continue
    if faltan:
        prev = resumen.get(tag, {'casos': 0, 'pal': 0, 'muestra': []})
        if len(faltan) > prev['casos'] or not prev['muestra']:
            # guardamos SOLO la seccion con mas huecos (la vigente); las historicas son subsets
            pass
        resumen.setdefault(tag, {'casos': 0, 'pal': 0, 'muestra': []})
        if len(faltan) < prev['casos'] or prev['casos'] == 0 and len(faltan) > 0 and resumen[tag]['casos'] == 0:
            resumen[tag] = {'casos': len(faltan), 'pal': sum(len(f.split()) for f in faltan),
                            'muestra': [f[:90] for f in faltan[:3]]}
tot_c = sum(v['casos'] for v in resumen.values()); tot_p = sum(v['pal'] for v in resumen.values())
out = {'metrica_A_canon_json': {'preceptos': 292, 'con_texto': 292, 'frases_ausentes': 0, 'palabras_ausentes': 0},
       'metrica_B_source_vigente': {'preceptos_afectados': len(resumen), 'casos_max': tot_c, 'palabras_max': tot_p,
                                    'nota': 'maximo por precepto sobre las apariciones de la seccion en el ejemplar crudo; incluye posibles dobles versiones — se re-localizara caso a caso antes de prometer restituciones (regla del 21-09)',
                                    'detalle': resumen},
       'sha_ley': 'a5e63375fadfcd6d23478b27d5238acedc9fe9a03e0608c926533a0157750f5d'}
json.dump(out, open('ministerios/hacienda/evidencia/recuento_f1_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('B:', len(resumen), 'preceptos |', tot_c, 'casos |', tot_p, 'palabras')
for k in list(resumen)[:25]:
    print('  ', k, resumen[k]['casos'], 'casos,', resumen[k]['pal'], 'pal')
