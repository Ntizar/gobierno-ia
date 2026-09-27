# -*- coding: utf-8 -*-
# Sesion 18/30 - (a) recuento F1 actualizado: los casos "contenido_perdido" del manifiesto
# masivo (02-09) re-localizados caso por caso contra el texto VIVO de hoy.
# (b) criterio anti-[a12]/[a229] para dedupes seguros: la capa final del vivo debe contener
#     el texto VIGENTE COMPLETO del ejemplar consolidado archivado (canon + letras a) vivas),
#     no solo el canon JSON (que pierde letras por artefacto de su propia extraccion).
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')

def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('\u00a0', ' ').replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()

LAW = 'ministerios/hacienda/leyes/BOE-A-2003-23186.md'
raw = open(LAW, encoding='utf-8').read()
nraw = norm(raw)
parts = re.split(r'(?m)^(## \[[a-z0-9\-]+\][^\n]*)$', raw)
blocks = {}
for i in range(1, len(parts), 2):
    tag = re.match(r'## \[([a-z0-9\-]+)\]', parts[i]).group(1)
    blocks[tag] = parts[i] + parts[i+1]

# ---- (a) F1 re-localizado ----
m = json.load(open('ministerios/hacienda/evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json', encoding='utf-8'))
casos = [c for c in m['casos_fidelidad'] if c.get('v') == 'contenido_perdido']
abiertos = []
for c in casos:
    tag = c['bloque'].strip('[]')
    frag = norm(c.get('texto') or c.get('fragmento') or c.get('letra') or '')
    if not frag:
        abiertos.append((c['bloque'], '(sin fragmento en manifiesto)', 0)); continue
    vivo = norm(blocks.get(tag, ''))
    if frag in vivo or frag[:200] in vivo:
        continue
    abiertos.append((c['bloque'], frag[:90], len(frag.split())))
print('F1 del manifiesto 02-09:', len(casos), 'casos /', len({c["bloque"] for c in casos}), 'bloques')
print('RE-LOCALIZADOS HOY como pendientes:', len(abiertos), 'casos /', len({a[0] for a in abiertos}), 'bloques /', sum(a[2] for a in abiertos), 'palabras')
for a in abiertos[:15]:
    print('  ·', a[0], '|', a[2], 'pal |', a[1][:70])

# ---- (b) criterio de capa vigente contra el consolidado archivado ----
html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
txt = re.sub(r'<br\s*/?>', '\n', html); txt = re.sub(r'</p>', '\n', txt); txt = re.sub(r'<[^>]+>', '', txt)
lines = [re.sub(r'\s+', ' ', l).strip() for l in txt.split('\n') if l.strip()]

def vigentes_consolidado(artno):
    idx = [i for i, l in enumerate(lines) if re.match(rf'Artículo {artno}\. ', l)]
    out = []
    for k, i in enumerate(idx):
        j = i + 1
        while j < len(lines) and not re.match(r'Artículo \d+\. |TÍTULO|CAPÍTULO|SECCIÓN|Disposición', lines[j]):
            j += 1
        out.append(' '.join(lines[i:j]))
    return out

report = {}
for tag in ['a229', 'a81', 'a68', 'a112', 'a233', 'a199', 'a65', 'a26', 'a29']:
    artno = int(re.sub(r'\D', '', tag))
    vs = vigentes_consolidado(artno)
    body = blocks[tag]
    head = next(l.strip() for l in body.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    occ = [x.start() for x in re.finditer(re.escape(head), body)]
    ult = body[occ[-1]+len(head):]
    nul = norm(ult)
    cub = [i+1 for i, v in enumerate(vs) if norm(v) in nul]
    report[tag] = {'n_versiones_consolidado': len(vs), 'pal_versions': [len(v.split()) for v in vs],
                   'pal_ultima_capa_vivo': len(ult.split()),
                   'versiones_consolidado_contenidas_en_ultima_capa': cub,
                   'DEDUPE_SEGURO': len(vs) in (1, 2) and all((i+1) in cub for i in range(len(vs)) if len(vs[i].split()) > 40)}
json.dump({'f1_relocalizado': {'casos_manifiesto': len(casos), 'pendientes_hoy': len(abiertos),
           'pendientes_lista': abiertos}, 'capas': report},
          open('ministerios/hacienda/evidencia/f1_y_capas_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(report, ensure_ascii=False, indent=1))
