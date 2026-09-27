# -*- coding: utf-8 -*-
# Sesion 18/30 (domingo 2026-09-27, fecha fatal) - verificacion de apertura y cierre
# 1) sha256/palabras/bloques de la LGT  2) estado de [a229]: no re-aplicar lo no aprobado
# 3) inventario F1 re-medido por pareo de frases literales (convencion del 26-09)
# Autor: Arcadi Espana, Ministerio de Hacienda
import hashlib, json, re, unicodedata, os

os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
LAW = 'ministerios/hacienda/leyes/BOE-A-2003-23186.md'

def shafile(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()

raw = open(LAW, encoding='utf-8').read()
sha = shafile(LAW)
words = len(raw.split())
parts = re.split(r'(?m)^(## \[[a-z0-9\-]+\][^\n]*)$', raw)
headers = [p for p in parts if p.startswith('## [')]

# bloques vivos: re.split deja [pre, cab1, cue1, cab2, cue2, ...] — cabeceras en indices impares
blocks = {}
for i in range(1, len(parts), 2):
    tag = re.match(r'## \[([a-z0-9\-]+)\]', parts[i]).group(1)
    blocks[tag] = parts[i] + parts[i+1]

out = {
    'fecha': '2026-09-27',
    'sha256_ley': sha,
    'palabras': words,
    'n_bloques': len(headers),
    'apertura_esperada': {'sha': 'a5e63375fadfcd6d23478b27d5238acedc9fe9a03e0608c926533a0157750f5d', 'pal': 135180, 'bloques': 335},
    'identico_apertura': sha == 'a5e63375fadfcd6d23478b27d5238acedc9fe9a03e0608c926533a0157750f5d',
}

# [a229]: vivo hoy vs bloque_vivo y bloque_propuesto del 25-09 (no re-aplicar, no aprobar sin Consejo)
def normblock(s): return hashlib.sha256(s.rstrip('\n').replace('\r\n', '\n').encode('utf-8')).hexdigest()
a229 = blocks.get('a229', '')
out['a229'] = {
    'vivo_hoy_sha': normblock(a229), 'vivo_hoy_pal': len(a229.split()),
    'copias_articulo_229': len(re.findall(r'Art[íi]culo 229', a229)),
}
for label, path in [('vivo_25', 'ministerios/hacienda/evidencia/bloque_vivo_a229_2026-09-25.txt'),
                    ('propuesto_25', 'ministerios/hacienda/evidencia/bloque_propuesto_a229_2026-09-25.txt')]:
    if os.path.exists(path):
        t = open(path, encoding='utf-8').read()
        out['a229'][label + '_sha'] = normblock(t)
        out['a229'][label + '_pal'] = len(t.split())
if 'vivo_25_sha' in out['a229']:
    out['a229']['INTACTO_igual_apertura_25'] = out['a229']['vivo_hoy_sha'] == out['a229']['vivo_25_sha']
    out['a229']['APLICADO_igual_propuesto'] = out['a229']['vivo_hoy_sha'] == out['a229']['propuesto_25_sha']

# F1 re-medido: frases literales del canon 2026-08-31 vs fichero vivo (unidad: precepto con texto)
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = canon['articulos']
deficiente, total_frases, frases_ausentes, pal_ausentes = [], 0, 0, 0
for a in arts:
    b = norm(blocks.get(a['id'], ''))
    if not b:
        deficiente.append((a['id'], 'bloque inexistente', 0)); continue
    frases = [f.strip() for f in re.split(r'(?<=[.;:])\s+', norm(a['texto'])) if len(f.strip()) >= 15]
    falt = [f for f in frases if f not in b]
    total_frases += len(frases); frases_ausentes += len(falt)
    fw = sum(len(f.split()) for f in falt); pal_ausentes += fw
    if fw: deficiente.append((a['id'], 'frases ausentes', fw))
out['f1_remedido'] = {
    'convencion': 'frases literales >=15 chars, canon data/canonical 2026-08-31 vs fichero vivo (la del pareo del 26-09, no la del manifiesto masivo por letras)',
    'preceptos_canon': len(arts),
    'preceptos_con_texto': len(arts) - len(deficiente),
    'frases_canon_total': total_frases, 'frases_ausentes': frases_ausentes,
    'palabras_ausentes': pal_ausentes,
    'deficientes': deficiente,
    'bloques_vivo_sin_homologo_en_canon': sorted(set(blocks) - {a['id'] for a in arts}),
}
json.dump(out, open('ministerios/hacienda/evidencia/estado_sesion18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'f1_remedido'}, ensure_ascii=False, indent=1))
f1 = out['f1_remedido']
print('F1:', f1['preceptos_con_texto'], '/', f1['preceptos_canon'], 'con texto | frases', f1['frases_ausentes'], 'ausentes de', f1['frases_canon_total'], '| palabras ausentes', f1['palabras_ausentes'])
print('deficientes:', f1['deficientes'])
print('bloques del repo sin homologo canon:', len(f1['bloques_vivo_sin_homologo_en_canon']))
