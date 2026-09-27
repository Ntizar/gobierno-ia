# -*- coding: utf-8 -*-
# Sesion 18/30 - PRUEBA DECISIVA por bloque: ¿el texto VIGENTE del consolidado archivado
# (seccion 'Artículo N.' terminada en la siguiente cabecera) cabe CONTIGUO en una capa del vivo?
# Solo se propone el dedupe SI: canon ⊆ vigente-consolidado ⊆ capa única del vivo.
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()

raw_html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
txt = re.sub(r'<br\s*/?>', '\n', raw_html); txt = re.sub(r'</p>', '\n', txt); txt = re.sub(r'<[^>]+>', ' ', txt)
lines = [re.sub(r'\s+', ' ', l).strip() for l in txt.split('\n') if l.strip()]

# las secciones del BOE consolidado: 'Artículo N.' arranca version; la version vigente es la que
# lleva la marca 'Vigente desde' o es la ultima antes del siguiente encabezado
START = re.compile(r'^Artículo (\d+)\.')
END = re.compile(r'^(Artículo \d+\.|T[íi]tulo|CAP[ÍI]TULO|SECCI[ÓO]N|Disposici[óo]n|Anexo)')
def secciones(artno):
    idx = [i for i, l in enumerate(lines) if START.match(l) and int(START.match(l).group(1)) == artno]
    out = []
    for k, i in enumerate(idx):
        j = i + 1
        while j < len(lines) and not END.match(lines[j]):
            j += 1
        out.append(' '.join(lines[i:j]))
    return out

vivo = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
parts = re.split(r'(?m)^(## \[[a-z0-9\-]+\][^\n]*)$', vivo)
blocks = {}
for i in range(1, len(parts), 2):
    tag = re.match(r'## \[([a-z0-9\-]+)\]', parts[i]).group(1)
    blocks[tag] = parts[i] + parts[i+1]

canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}

for tag, artno in [('a112', 112), ('a81', 81), ('a68', 68), ('a150', 150)]:
    secs = secciones(artno)
    ncanon = norm(arts[tag]['texto'])
    body = blocks[tag]
    head = next(l.strip() for l in body.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    occ = [x.start() for x in re.finditer(re.escape(head), body)]
    capas = []
    for j, s0 in enumerate(occ):
        e0 = occ[j+1] if j+1 < len(occ) else len(body)
        capas.append(body[s0+len(head):e0])
    print(f'== {tag}: {len(secs)} secciones en consolidado, {len(capas)} capas en vivo ==')
    for k, s in enumerate(secs):
        ns = norm(s)
        incanon = ns in ncanon or ncanon in ns
        capas_ok = [j+1 for j, c in enumerate(capas) if ns in norm(c)]
        print(f'  sec {k+1}: {len(s.split())} pal | canon-superconjunto? {ncanon in ns} | capas del vivo que la contienen: {capas_ok}')
