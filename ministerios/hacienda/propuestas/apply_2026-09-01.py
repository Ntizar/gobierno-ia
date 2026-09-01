# Aplicacion de los diffs corregidos del Consejo 2026-08-31 — sesion 4/30 — Hacienda
# 1) [a271] -> corregido: la duplicacion vive en 8 bloques propios de DAs (informe Auditoria
#    2026-08-31, veredicto 1). Se aplica bloque de DA por bloque de DA: suprimir toda copia
#    literal posterior conservando la primera ocurrencia. Manifiesto sha256 por parrafo.
# 2) [a150] -> corregido: conservar EXCLUSIVAMENTE la redaccion vigente que coincide con el
#    BOE consolidado (la unica copia que incluye el 3.º del Impuesto Complementario, letra f)
#    de suspension del apartado 3 y parrafo «En el caso contemplado en la letra f)»).
#    Suprimir las 2 redacciones antiguas (12+12) y las 2 copias incompletas de la nueva.
# Ejecutable:  python ministerios/hacienda/propuestas/apply_2026-09-01.py
import re, hashlib, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# (el fichero vive en ministerios/hacienda/propuestas/ -> cuatro niveles arriba es la raiz)
LAW = os.path.join(ROOT, 'ministerios', 'hacienda', 'leyes', 'BOE-A-2003-23186.md')

def norm(p): return re.sub(r'\s+', ' ', p).strip()
def wc(s): return len(s.split())
def sha(p): return hashlib.sha256(norm(p).encode()).hexdigest()

txt = open(LAW, encoding='utf-8').read().replace('\r\n', '\n')
parts = re.split(r'^(## \[[^\]]+\][^\n]*)$', txt, flags=re.M)
head = {}   # bid -> (header_line, raw_body)
order = []
for i, seg in enumerate(parts):
    m = re.match(r'^## (\[[^\]]+\])', seg)
    if m:
        bid = m.group(1)
        head[bid] = (seg, parts[i+1] if i+1 < len(parts) else '')
        order.append(bid)

DA8 = ['[daquinta]','[dasexta]','[daundecima]','[dadecimoctava]','[davigesima]',
       '[davigesimosegunda]','[da]','[da-2]']

manifest = {'generado': '2026-09-01', 'ley': 'BOE-A-2003-23186', 'eliminaciones': {}}

# ---------- 1) DAs: suprimir copias literales, conservar primera ocurrencia ----------
for bid in DA8:
    hdr, body = head[bid]
    paras = body.split('\n\n')
    seen, keep, removed = set(), [], []
    for idx, p in enumerate(paras):
        if not norm(p):
            keep.append(p); continue
        h = sha(p)
        if h in seen:
            removed.append({'idx': idx, 'sha256': h, 'palabras': wc(p), 'inicio': norm(p)[:70]})
        else:
            seen.add(h); keep.append(p)
    manifest['eliminaciones'][bid] = {'n_eliminados': len(removed),
        'palabras_eliminadas': sum(r['palabras'] for r in removed), 'detalle': removed}
    head[bid] = (hdr, '\n\n'.join(keep))

# ---------- 2) [a150]: conservacion de la copia vigente ----------
hdr, body = head['[a150]']
paras = body.split('\n\n')
def at(k): return norm(paras[k]) if k < len(paras) else ''
# estructura medida del bloque (split por parrafos):
#  0='' | 1..5 = 'Articulo 150...' x5 (cabeceras duplicadas) | 6..15 = antigua v1 (12+12)
#  16..42 = copia nueva A (incompleta) | 43..71 = copia nueva B (incompleta)
#  72..81 = antigua v2 | 82..112 = copia nueva C (vigente, coincide con BOE)
# guarda de idempotencia: si el diff ya esta aplicado, salir limpio, no re-escribir
if 'plazo de 12 meses contado' not in body:
    print('El diff ya esta aplicado sobre este fichero (no hay redaccion antigua en [a150]). Nada que hacer.')
    sys.exit(0)
# verificaciones previas (assert antes de tocar nada)
assert 'Artículo 150' in at(1)
assert 'plazo de 12 meses contado' in at(6), at(6)[:60]           # antigua v1
assert 'plazo de 12 meses contado' in at(72), at(72)[:60]         # antigua v2
assert 'deberán concluir en el plazo de:' in at(16)               # copia nueva A
assert 'deberán concluir en el plazo de:' in at(43)               # copia nueva B
assert 'deberán concluir en el plazo de:' in at(82)               # copia nueva C (vigente)
assert '3.º Que el objeto del procedimiento sea la comprobación o investigación del Impuesto Complementario' in at(85)
assert 'f) La comunicación a las Administraciones afectadas' in at(97)
assert 'En el caso contemplado en la letra f)' in at(101)
# ELIMINAR: 0 (vacio), 2..5 (cabeceras duplicadas), 6..81 (antigua v1, copias A y B,
# antigua v2). CONSERVAR: parrafo 1 (titulo del articulo) + 82..fin (copia vigente C,
# la unica con el 3.º del Impuesto Complementario y la letra f) de suspension, que es
# exactamente lo que publica el BOE consolidado consultado hoy).
keep = ['\n', paras[1]] + paras[82:]
removed = [{'idx': k, 'sha256': sha(paras[k]), 'palabras': wc(paras[k]), 'inicio': norm(paras[k])[:70]}
           for k in ([0] + list(range(2, 82))) if norm(paras[k])]
manifest['eliminaciones']['[a150]'] = {'n_eliminados': len(removed),
    'palabras_eliminadas': sum(r['palabras'] for r in removed), 'detalle': removed,
    'criterio': 'conservada copia vigente = unica coincidente con BOE consolidado 01-09-2026 (3.º Impuesto Complementario)'}
head['[a150]'] = (hdr, '\n\n'.join(keep))

# ---------- reescribir ----------
out = []
for bid in order:
    hdr, body = head[bid]
    out.append(hdr + body)
pre = parts[0]  # cabecera del fichero
new = pre + ''.join(out)
# normalizar triples saltos de linea generados
new = re.sub(r'\n{3,}', '\n\n', new)
shutil.copy(LAW, LAW + '.bak-2026-09-01')
open(LAW, 'w', encoding='utf-8', newline='\n').write(new)

tot_w = sum(v['palabras_eliminadas'] for v in manifest['eliminaciones'].values())
tot_p = sum(v['n_eliminados'] for v in manifest['eliminaciones'].values())
print(json.dumps({k: {'paras': v['n_eliminados'], 'palabras': v['palabras_eliminadas']}
                  for k, v in manifest['eliminaciones'].items()}, ensure_ascii=False))
print('TOTAL parrafos eliminados:', tot_p, '| palabras eliminadas:', tot_w)
mvp = os.path.join(ROOT, 'ministerios', 'hacienda', 'evidencia',
                   'manifiesto_aplicacion_2026-09-01.json')
json.dump(manifest, open(mvp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('manifiesto:', mvp)
