# -*- coding: utf-8 -*-
# Sesion 18/30 - preparacion de propuestas: verificacion canon contiguo y textos propuestos
# Criterio anti-[a229]: solo va a propuesta el bloque cuya copia canonica esta CONTIGUA en el vivo
# (dedupe = quitar copias, no reensamblar). canon <= propuesto verificado frase a frase y substring.
import hashlib, json, re, unicodedata, os

os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
LAW = 'ministerios/hacienda/leyes/BOE-A-2003-23186.md'

def shablock(s): return hashlib.sha256(s.rstrip('\n').replace('\r\n', '\n').encode('utf-8')).hexdigest()
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()

canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
raw = open(LAW, encoding='utf-8').read()
parts = re.split(r'(?m)^(## \[[a-z0-9\-]+\][^\n]*)$', raw)
blocks = {}
for i in range(1, len(parts), 2):
    tag = re.match(r'## \[([a-z0-9\-]+)\]', parts[i]).group(1)
    blocks[tag] = (parts[i], parts[i+1])

res = {}
for tag in ['a81', 'a26', 'a29', 'a68', 'a233', 'a199', 'a65', 'a112']:
    cab, body = blocks[tag]
    vivo = cab + body
    ncanon = norm(arts[tag]['texto'])
    nvivo = norm(vivo)
    contiguo = ncanon in nvivo
    frases = [f.strip() for f in re.split(r'(?<=[.;:])\s+', ncanon) if len(f.strip()) >= 15]
    # copia canonica localizable en el vivo como parrafos contiguos?
    res[tag] = {
        'pal_vivo': len(vivo.split()),
        'pal_canon': len(arts[tag]['texto'].split()),
        'canon_contiguo_en_vivo': contiguo,
        'frases_canon': len(frases),
        'frases_ausentes': sum(1 for f in frases if f not in nvivo),
        'sha_vivo': shablock(vivo)[:16],
    }
    # material de evidencia: cuerpo canonico en fichero aparte
    if contiguo:
        prop = cab.rstrip('\n') + '\n\n' + arts[tag]['texto'].strip() + \
               '\n\n> Consolidación 2026-09-27 (Ministerio de Hacienda): copias duplicadas del precepto eliminadas; el cuerpo es el texto consolidado vigente del BOE (data/canonical 2026-08-31, byte a byte). Aparato del repo, no norma.\n'
        open(f'ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(prop)
        open(f'ministerios/hacienda/evidencia/bloque_vivo_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(vivo)
        nprop = norm(prop)
        res[tag]['canon_en_propuesto_substring'] = ncanon in nprop
        res[tag]['frases_ausentes_propuesto'] = sum(1 for f in frases if f not in nprop)
        res[tag]['pal_propuesto'] = len(prop.split())
        res[tag]['delta_pal'] = res[tag]['pal_propuesto'] - res[tag]['pal_vivo']
        res[tag]['sha_prop'] = shablock(prop)[:16]
json.dump(res, open('ministerios/hacienda/evidencia/prep_propuestas_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
