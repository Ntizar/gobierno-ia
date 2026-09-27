# -*- coding: utf-8 -*-
# Sesion 18/30 - VERSION FINAL de las propuestas: dedupe puro a la ULTIMA capa del vivo
# (metodo [a203]/[a188] aprobado el 25-09: sin reensamblar, sin insertar; canon ⊆ propuesto
#  verificado como substring y frase a frase). Las letras que la copia vigente perdio se
# DECLARAN como hallazgo de fidelidad aparte (doctrina [a82]: se restituye en su propia
# propuesta, no colada dentro de un dedupe).
import json, re, os, unicodedata, hashlib
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')

def shablock(s): return hashlib.sha256(s.rstrip('\n').replace('\r\n', '\n').encode('utf-8')).hexdigest()
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    s = s.replace('&uacute;', 'ú').replace('&oacute;', 'ó').replace('&aacute;', 'á')
    return re.sub(r'\s+', ' ', s).strip().lower()

vivo_raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}

# seccion del consolidado archivado, FILTRADA de aparato (selector de redacciones, refs)
raw_html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
tx = re.sub(r'<br\s*/?>', '\n', raw_html); tx = re.sub(r'</p>', '\n', tx); tx = re.sub(r'<[^>]+>', ' ', tx)
lns = [re.sub(r'\s+', ' ', l).strip() for l in tx.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')
APAR = re.compile(r'(seleccionar redacci|última actualizaci|modificaci|publicada|publicado|en vigor|ref\. boletin|ref\. boe|boe-a-20|subir \[|se añade|se modifica|se renumera|renumeran|téngase en cuenta|jurisprudencia|texto original|único\.\d)', re.I)
def seccion_vigente(artno):
    idx = [i for i, l in enumerate(lns) if re.match(rf'Artículo {artno}\. ', l)]
    i = idx[-1]; j = i + 1
    while j < len(lns) and not END.match(lns[j]): j += 1
    keep = []
    for l in lns[i:j]:
        if APAR.search(l): continue
        if re.match(r'^\d+\.\d*\.\s', l): continue
        keep.append(l)
    return ' '.join(keep)

REP = {}
for tag, artno, apertura in [('a81', 81, '1. Para asegurar el cobro de las deudas para cuya recaudación sea competente'),
                             ('a68', 68, '1. El plazo de prescripción del derecho a que se refiere el párrafo a) del artículo 66 de esta Ley se interrumpe:'),
                             ('a65', 65, '1. Las deudas tributarias que se encuentren en período voluntario o ejecutivo podrán aplazarse')]:
    m = re.search(r'(?m)^(## \[' + tag + r'\][^\n]*)\n(.*?)(?=\n## \[|\Z)', vivo_raw, re.S)
    cab, body = m.group(1), m.group(2)
    vivo = cab + '\n' + body
    head = next(l.strip() for l in body.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    p = body.rfind(apertura)
    cola = body[p:].rstrip()
    ncola = norm(cola)
    prop = cab + '\n\n' + head + '\n\n' + cola + '\n\n' + \
        ('> Consolidación 2026-09-27 (Ministerio de Hacienda): de la última copia del precepto en el bloque '
         '(la capa más reciente del BOE consolidado, texto vigente) — se retiran las capas históricas. '
         'canon ⊆ propuesto verificado como substring y frase a frase. Aparato del repo, no norma.\n')
    nprop = norm(prop)
    ncanon = norm(arts[tag]['texto'])
    frases_c = [f.strip() for f in re.split(r'(?<=[.;:])\s+', ncanon) if len(f.strip()) >= 15]
    sv = seccion_vigente(artno); nsv = norm(sv)
    frases_v = [f.strip() for f in re.split(r'(?<=[.;:])\s+', nsv) if len(f.strip()) >= 15]
    letras_vivas_faltan = [f[:110] for f in frases_v if f.startswith('a)') and f not in ncola]
    REP[tag] = {
        'vivo_pal': len(vivo.split()), 'prop_pal': len(prop.split()),
        'delta': len(prop.split()) - len(vivo.split()),
        'sha_vivo': shablock(vivo), 'sha_prop': shablock(prop),
        'canon_substring_en_propuesto': ncanon in nprop,
        'frases_canon': len(frases_c), 'frases_canon_ausentes': sum(1 for f in frases_c if f not in nprop),
        'frases_vigente_consolidado': len(frases_v),
        'frases_vigente_ausentes_del_propuesto': [f[:110] for f in frases_v if f not in nprop],
        'letras_a_vigentes_que_faltan_en_la_copia': letras_vivas_faltan,
        'copias_head_vivo': vivo.count(head),
    }
    open(f'ministerios/hacienda/evidencia/bloque_vivo_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(vivo.rstrip('\n') + '\n')
    open(f'ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(prop)
json.dump(REP, open('ministerios/hacienda/evidencia/propuestas_definitivas_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(REP, ensure_ascii=False, indent=1))
