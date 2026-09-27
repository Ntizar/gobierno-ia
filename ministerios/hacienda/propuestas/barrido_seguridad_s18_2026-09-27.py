# -*- coding: utf-8 -*-
# Sesion 18/30 - BARRIDO DE SEGURIDAD anti-[a229] para los bloques con sedimento:
# un dedupe a la ultima capa es SEGURO solo si TODA frase vigente del consolidado archivado
# (filtrada de aparato) cabe en esa capa. Si falta alguna -> bandera, no va a voto.
import json, re, os, unicodedata, hashlib
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')

def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    s = s.replace('&uacute;', 'ú').replace('&oacute;', 'ó').replace('&aacute;', 'á').replace('&ntilde;', 'ñ')
    s = re.sub(r'&[a-z]+;', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
tx = re.sub(r'<br\s*/?>', '\n', html); tx = re.sub(r'</p>', '\n', tx); tx = re.sub(r'<[^>]+>', ' ', tx)
lns = [re.sub(r'\s+', ' ', l).strip() for l in tx.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')
APAR = re.compile(r'(seleccionar redacci|última actualizaci|modificación|publicada|publicado|en vigor|ref\. boletin|ref\. boe|boe-a-\d|subir \[|se añade|se modifica|se renumera|renumeran|téngase en cuenta|jurisprudencia|texto original|único\.\d|\b[ab]\.\d+ de la ley\b|de la [Ll]ey \d)', re.I)

def secciones(artno):
    idx = [i for i, l in enumerate(lns) if re.match(rf'Artículo {artno}\. ', l)]
    out = []
    for i in idx:
        j = i + 1
        while j < len(lns) and not END.match(lns[j]): j += 1
        out.append(' '.join(lns[i:j]))
    return out

vivo_raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()

def bloque(tag):
    m = re.search(r'(?m)^## \[' + tag + r'\].*?(?=^## \[|\Z)', vivo_raw, re.S)
    return m.group(0) if m else ''

RES = {}
for tag, artno in [('a26', 26), ('a29', 29), ('a65', 65), ('a67', 67), ('a81', 81), ('a99', 99),
                   ('a112', 112), ('a135', 135), ('a174', 174), ('a180', 180), ('a199', 199),
                   ('a200', 200), ('a211', 211), ('a221', 221), ('a233', 233), ('a239', 239),
                   ('a27', 27), ('a198', 198), ('a41', 41), ('a224', 224)]:
    b = bloque(tag)
    if not b: continue
    head_m = re.search(r'(?m)^Art[íi]culo ' + str(artno) + r'\.', b)
    if not head_m: continue
    head = head_m.group(0)
    # capas del vivo cortadas por repeticion del encabezamiento exacto (incluye titulo)
    m2 = re.search(r'(?m)^Art[íi]culo ' + str(artno) + r'\..*$', b)
    head_line = m2.group(0).strip()
    occ = [x.start() for x in re.finditer(re.escape(head_line), b)]
    capas = [b[occ[j]+len(head_line): occ[j+1] if j+1 < len(occ) else len(b)] for j in range(len(occ))]
    ult = capas[-1]
    # vigentes: todas las secciones del articulo en el consolidado; la vigente es la que tiene
    # mas frases unicas largas; usamos TODAS las frases de TODAS las secciones filtradas como
    # "superconjunto de norma que vivio", y el test duro es contra la SECCION que el consolidado
    # lista como vigente = la ultima seccion completa (los marcadores de redaccion van aparte)
    secs = secciones(artno)
    if not secs:
        RES[tag] = {'error': 'sin seccion en consolidado'}; continue
    s_txt = secs[-1]
    frases = []
    for l in s_txt.split('\n'):
        pass
    fs = [f.strip() for f in re.split(r'(?<=[.;:])\s+', norm(s_txt))
          if len(f.strip()) >= 20 and not APAR.search(f)]
    nult = norm(ult)
    faltan = [f for f in fs if f not in nult]
    RES[tag] = {'capas': len(occ), 'pal_ultima': len(ult.split()), 'pal_vivo': len(b.split()),
                'frases_vigentes': len(fs), 'frases_vigentes_ausentes_de_ultima_capa': len(faltan),
                'muestra_ausentes': [f[:80] for f in faltan[:3]],
                'DEDUPE_SEGURO': len(faltan) == 0}
json.dump(RES, open('ministerios/hacienda/evidencia/barrido_seguridad_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in RES.items():
    flag = 'SEGURO' if v.get('DEDUPE_SEGURO') else ('BANDERA' if 'frases_vigentes_ausentes_de_ultima_capa' in v else 'ERROR')
    print(k, '|', v.get('capas'), 'capas | ult', v.get('pal_ultima'), 'pal | vigentes', v.get('frases_vigentes'),
          '| ausentes', v.get('frases_vigentes_ausentes_de_ultima_capa'), '|', flag)
    for f in v.get('muestra_ausentes', [])[:2]:
        print('    ·', f)
