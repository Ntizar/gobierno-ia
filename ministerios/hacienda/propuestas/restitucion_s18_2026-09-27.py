# -*- coding: utf-8 -*-
# Sesion 18/30 - PROPUESTAS Fase 2 (metodo [a203]+[a82] del 25-09, sin repetir el vicio de [a12]):
# propuesto = capa vigente del bloque vivo (ultima copia del precepto)
#             + letras vigentes del propio sedimento que la copia actual perdio (insertadas,
#             ancladas en la b) que las sigue en la seccion vigente del BOE consolidado archivado).
# Verificaciones: canon ⊆ propuesto; seccion-vigente ⊆ propuesto (frases); 1 copia de head.
import json, re, os, unicodedata, hashlib
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')

def shablock(s): return hashlib.sha256(s.rstrip('\n').replace('\r\n', '\n').encode('utf-8')).hexdigest()
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()

raw_html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
txt = re.sub(r'<br\s*/?>', '\n', raw_html)
txt = re.sub(r'</p>', '\n', txt)
txt = re.sub(r'<[^>]+>', ' ', txt)
lines = [re.sub(r'\s+', ' ', l).strip() for l in txt.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')

def seccion_vigente(artno):
    idx = [i for i, l in enumerate(lines) if re.match(rf'Artículo {artno}\. ', l)]
    i = idx[-1]
    j = i + 1
    while j < len(lines) and not END.match(lines[j]):
        j += 1
    return ' '.join(lines[i:j])

vivo_raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}

CAND = [('a81', 81, '1. Para asegurar el cobro de las deudas para cuya recaudación sea competente'),
        ('a68', 68, '1. El plazo de prescripción del derecho a que se refiere el párrafo a) del artículo 66 de esta Ley se interrumpe:'),
        ('a65', 65, '1. Las deudas tributarias que se encuentren en período voluntario o ejecutivo podrán aplazarse')]

REP = {}
for tag, artno, apertura in CAND:
    m = re.search(r'(?m)^(## \[' + tag + r'\][^\n]*)\n(.*?)(?=\n## \[|\Z)', vivo_raw, re.S)
    cab, body = m.group(1), m.group(2)
    vivo = cab + '\n' + body
    head = next(l.strip() for l in body.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    p = body.rfind(apertura)
    cola = body[p:]
    ncola = norm(cola)
    sv = seccion_vigente(artno)
    nsv = norm(sv)
    # letras sueltas del sedimento que la cola perdio y el consolidado mantiene
    cand = []
    for par in body.split('\n\n'):
        s = par.strip()
        if not s.startswith('a)'): continue
        ns = norm(s)
        if ns in ncola: continue
        if ns in nsv: cand.append(s)
    cand = list(dict.fromkeys(cand))
    nuevo = cola
    insertadas = []
    for c in cand:
        i_sv = sv.find(c[:60].strip())
        if i_sv < 0:
            mm = re.search(re.escape(norm(c[:40])), nsv)
            if not mm: continue
            i_sv = sv.lower().find(c[:40].lower())
        m2 = re.search(r'b\) [A-ZÁÉÍÓÚ].{0,240}?[.;:]', sv[i_sv:i_sv + 1400])
        if not m2: continue
        bstart = m2.group(0)[:60]
        for par in nuevo.split('\n\n'):
            if par.strip().startswith(bstart[:45].strip()):
                nuevo = nuevo.replace(par, c + '\n\n' + par.strip(), 1)
                insertadas.append(c[:70])
                break
    prop = cab + '\n\n' + head + '\n\n' + nuevo.rstrip() + '\n\n' + \
        ('> Consolidación 2026-09-27 (Ministerio de Hacienda): capa vigente — se retiran las capas históricas '
         'del precepto; la letra del sedimento que la copia actual había perdido se restituye en su posición '
         '(insertada literalmente desde el propio bloque, anclada contra la sección vigente del BOE consolidado '
         'archivado). Aparato del repo, no norma.\n')
    nprop = norm(prop)
    frases_sv = [f.strip() for f in re.split(r'(?<=[.;:])\s+', nsv) if len(f.strip()) >= 15]
    aus_sv = [f[:80] for f in frases_sv if f not in nprop]
    ncanon = norm(arts[tag]['texto'])
    frases_c = [f.strip() for f in re.split(r'(?<=[.;:])\s+', ncanon) if len(f.strip()) >= 15]
    aus_c = [f[:80] for f in frases_c if f not in nprop]
    REP[tag] = {
        'vivo_pal': len(vivo.split()), 'prop_pal': len(prop.split()),
        'delta': len(prop.split()) - len(vivo.split()),
        'sha_vivo': shablock(vivo), 'sha_prop': shablock(prop),
        'letras_restituidas': insertadas,
        'canon_substring_en_propuesto': ncanon in nprop,
        'frases_canon_ausentes': aus_c,
        'frases_vigente_consolidado_ausentes': aus_sv,
        'copias_head_en_propuesto': prop.count(head),
        'copias_head_en_vivo': vivo.count(head),
    }
    open(f'ministerios/hacienda/evidencia/bloque_vivo_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(vivo.rstrip('\n') + '\n')
    open(f'ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(prop)
json.dump(REP, open('ministerios/hacienda/evidencia/propuestas_fase2_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(REP, ensure_ascii=False, indent=1))
