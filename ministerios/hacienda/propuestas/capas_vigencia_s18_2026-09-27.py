# -*- coding: utf-8 -*-
# Sesion 18/30 - propuesta con patron [a203]: proposed = copia VIGENTE del vivo que contiene
# todo el canon, no el canon JSON a secas (el canon 2026-08-31 tiene letras 'a)' caidas por
# artefacto de su propia extraccion; tomarlo literal mataria norma vigente = vicio de [a12]).
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

OUT = {}
for tag in ['a81', 'a68', 'a112']:
    cab, body = blocks[tag]
    vivo = cab + body
    head = next(l.strip() for l in body.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    ncanon = norm(arts[tag]['texto'])
    # capas: se cortan en cada repeticion del encabezamiento oficial
    idx = [m.start() for m in re.finditer(re.escape(head), body)]
    capas = []
    for j, s0 in enumerate(idx):
        e0 = idx[j+1] if j+1 < len(idx) else len(body)
        capas.append(body[s0+len(head):e0])
    # capa vigente = ultima que contiene el canon completo (normalizado)
    ok_layers = [j for j, c in enumerate(capas) if ncanon in norm(c)]
    frases = [f for f in re.split(r'(?<=[.;:])\s+', ncanon) if len(f.strip()) >= 15]
    frases_in = [j for j, c in enumerate(capas) if all(f in norm(c) for f in frases)]
    OUT[tag] = {
        'n_capas': len(capas), 'pal_capas': [len(c.split()) for c in capas],
        'capas_con_canon_completo_substring': ok_layers,
        'capas_con_todas_las_frases': frases_in,
    }
    picks = frases_in or ok_layers
    if picks:
        j = picks[-1]
        capa = capas[j].strip()
        prop = (cab.rstrip('\n') + '\n\n' + head + '\n\n' + capa +
                '\n\n> Consolidación 2026-09-27 (Ministerio de Hacienda): capa ' + str(j+1) + ' de ' + str(len(capas)) +
                ' — se retiran las copias históricas del precepto; el cuerpo es íntegramente texto vigente del BOE consolidado'
                ' (canon ⊆ propuesto verificado frase a frase, ' + str(len(frases)) + ' frases). Aparato del repo, no norma.\n')
        nprop = norm(prop)
        OUT[tag].update({
            'capa_elegida': j+1, 'prop_pal': len(prop.split()),
            'delta_vs_vivo': len(prop.split()) - len(vivo.split()),
            'sha_prop': shablock(prop), 'sha_vivo': shablock(vivo),
            'frases_ausentes_en_propuesto': sum(1 for f in frases if f not in nprop),
            'letras_a_en_propuesto': len(re.findall(r'(?m)^a\)', prop)),
            'letras_a_en_capa': len(re.findall(r'(?m)^a\)', capa)),
            'letras_a_fuera_del_vivo_completo': len(re.findall(r'(?m)^a\)', vivo)),
        })
        open(f'ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(prop)
json.dump(OUT, open('ministerios/hacienda/evidencia/capas_vigencia_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(OUT, ensure_ascii=False, indent=1))
