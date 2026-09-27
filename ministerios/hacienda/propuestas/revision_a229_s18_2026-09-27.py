# -*- coding: utf-8 -*-
# Sesion 18/30 - preparacion de la revision linea a linea de [a229] (acuerdo 75, aplazado)
# NO ejecuta nada sobre la ley: deja en evidencia el material para el Auditor y el Consejo.
# 1) extrae el canon del art. 229 (data/canonical 2026-08-31) a fichero con sha256
# 2) coteja linea a linea el bloque vivo (2.263 pal.) contra el canon: vigente / sedimento / extra
# 3) verifica canon <= propuesto_s17 (frases literales) y mide el sedimento que saldria
import hashlib, json, re, unicodedata, os

os.chdir('C:/Users/d_ant/Projects/gobierno-ia')

def shatxt(s): return hashlib.sha256(s.rstrip('\n').replace('\r\n', '\n').encode('utf-8')).hexdigest()
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()

canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
art = next(a for a in canon['articulos'] if a['id'] == 'a229')
canon_txt = art['texto']
open('ministerios/hacienda/evidencia/canon_a229_s18_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(canon_txt)
canon_sha = shatxt(canon_txt)

raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
m = re.search(r'(?m)^## \[a229\].*?(?=^## \[|\Z)', raw, re.S)
vivo = m.group(0)
ncanon = norm(canon_txt)

lineas = [l for l in vivo.split('\n') if l.strip()]
estados = []
for l in lineas:
    n = norm(l)
    if n.startswith('## [a229]'):
        k = 'ROTULO_REPO'
    elif n in ncanon:
        k = 'EN_CANON'
    else:
        k = 'FUERA_DE_CANON'
    estados.append((k, len(l.split()), l[:90]))

en = sum(w for k, w, _ in estados if k == 'EN_CANON')
fuera = sum(w for k, w, _ in estados if k == 'FUERA_DE_CANON')
roto = sum(w for k, w, _ in estados if k == 'ROTULO_REPO')

# canon como unidades: frases del canon localizadas en el vivo, y subsecuencias de canon
frases = [f.strip() for f in re.split(r'(?<=[.;:])\s+', norm(canon_txt)) if len(f.strip()) >= 15]
nvivo = norm(vivo)
aus = [f for f in frases if f not in nvivo]

# propuesto del 25-09 (el retirado del voto): canon <= propuesto?
prop = open('ministerios/hacienda/evidencia/bloque_propuesto_a229_2026-09-25.txt', encoding='utf-8').read()
nprop = norm(prop)
aus_prop = [f for f in frases if f not in nprop]

res = {
    'fecha': '2026-09-27', 'bloque': '[a229]',
    'orden': 'PREPARACION - no ejecutado, no aprobado (acuerdo 75: aplazado, requiere revision linea a linea del Auditor)',
    'canon_a229': {'sha256': canon_sha, 'palabras': len(canon_txt.split()),
                   'fichero': 'ministerios/hacienda/evidencia/canon_a229_s18_2026-09-27.txt'},
    'vivo': {'palabras': len(vivo.split()), 'lineas_no_vacías': len(lineas),
             'palabras_lineas_en_canon': en, 'palabras_lineas_fuera_de_canon': fuera,
             'palabras_rotulo': roto,
             'frases_canon_ausentes_del_vivo': len(aus)},
    'propuesto_s17': {'palabras': len(prop.split()),
                      'frases_canon_ausentes_del_propuesto': len(aus_prop),
                      'ejemplos_ausentes': aus_prop[:5],
                      'canon_incluido_como_subsecuencia_contigua': ncanon in nprop},
    'reordenamiento_detectado': {
        'encabezamientos_repetidos': len(re.findall(r'(?m)^Artículo 229', vivo)),
        'capas': 'tres capas (original 2003, reforma LO 1/2010, reforma Ley 7/2011+34/2015); la vigente NO esta contiguous: le faltan a) del 1, encabezamiento del 2.a) y el encabezamiento del 3 dentro de su capa - el dedupe tiene que reensamblar piezas de capas distintas',
        'letras_o': 'en la capa vigente las letras b) y c) de los apartados 2 y 3 aparecen SIN el encabezamiento que las introduce (lineas 85-87, 91-93): una deduplicacion ingenua por linea mataria norma vigente'
    }
}
json.dump(res, open('ministerios/hacienda/evidencia/revision_a229_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
