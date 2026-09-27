# -*- coding: utf-8 -*-
# Sesion 18/30 - textos FINALES de las 3 propuestas: [a81] [a68] [a112]
# Regla: la capa vigente es la que contiene el canon COMPLETO (verificado capa a capa).
#  a81 y a68: es la ULTIMA capa -> propuesto = cola literal del vivo desde su apertura
#  a112: es la capa 3 de 4 (la 4 es redaccion historica pendiente/posterior que NO es el
#         canon) -> propuesto = canon byte a byte, y el dato de la capa 4 se declara al Auditor
import hashlib, json, re, unicodedata, os
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')

def shablock(s): return hashlib.sha256(s.rstrip('\n').replace('\r\n', '\n').encode('utf-8')).hexdigest()
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()

canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
parts = re.split(r'(?m)^(## \[[a-z0-9\-]+\][^\n]*)$', raw)
blocks = {}
for i in range(1, len(parts), 2):
    tag = re.match(r'## \[([a-z0-9\-]+)\]', parts[i]).group(1)
    blocks[tag] = (parts[i], parts[i+1])

FOOT = ('> Consolidación 2026-09-27 (Ministerio de Hacienda): se retiran las capas históricas del precepto; '
        'el cuerpo es íntegramente texto vigente del BOE consolidado (data/canonical/BOE-A-2003-23186/2026-08-31.json; '
        'canon ⊆ propuesto verificado frase a frase con el script preparar_textos_s18_2026-09-27.py). Aparato del repo, no norma.\n')

OUT = {}
for tag in ['a81', 'a68', 'a112']:
    cab, body = blocks[tag]
    vivo = cab + body
    head = next(l.strip() for l in body.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    ctext = arts[tag]['texto'].strip()
    ncanon = norm(ctext)
    frases = [f.strip() for f in re.split(r'(?<=[.;:])\s+', ncanon) if len(f.strip()) >= 15]
    apertura = ctext.split('\n')[0].strip()[:80]
    if tag in ('a81', 'a68'):
        p = body.rfind(apertura)
        cuerpo = body[p:].rstrip()
        metodo = 'cola_literal_capa_vigente'
    else:
        cuerpo = ctext
        metodo = 'canon_byte_a_byte_capa3_viva'
    prop = cab.rstrip('\n') + '\n\n' + head + '\n\n' + cuerpo + '\n\n' + FOOT
    nprop = norm(prop)
    # invariantes: para cada hito, ocurrencias en propuesto == ocurrencias en canon (una sola copia del texto)
    hitos = ['Para asegurar el cobro', 'medidas cautelares podrán consistir', 'cesarán en el plazo de seis meses',
             'El plazo de prescripción del derecho', 'Producida la interrupción', 'Interrumpido el plazo',
             'Cuando no sea posible efectuar la notificación', 'plazo de 15 días naturales',
             'se entiendan notificados por no haber comparecido']
    inv = {h: (norm(h) in nprop, nprop.count(norm(h)), ncanon.count(norm(h))) for h in hitos if norm(h) in nprop or norm(h) in ncanon}
    OUT[tag] = {
        'metodo': metodo,
        'vivo_pal': len(vivo.split()), 'prop_pal': len(prop.split()), 'delta': len(prop.split()) - len(vivo.split()),
        'sha_vivo': shablock(vivo), 'sha_prop': shablock(prop),
        'canon_substring_en_propuesto': ncanon in nprop,
        'frases_ausentes': sum(1 for f in frases if f not in nprop), 'frases_total': len(frases),
        'head_unica_en_prop': prop.count(head), 'copias_head_en_vivo': vivo.count(head),
        'hitos_ocurrencias': inv,
    }
    open(f'ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(prop)
    open(f'ministerios/hacienda/evidencia/bloque_vivo_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(vivo.rstrip('\n') + '\n')
json.dump(OUT, open('ministerios/hacienda/evidencia/propuesta_texts_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(OUT, ensure_ascii=False, indent=1))
