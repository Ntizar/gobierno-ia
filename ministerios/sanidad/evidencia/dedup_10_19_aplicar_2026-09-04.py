# -*- coding: utf-8 -*-
"""
Acuerdo 27 (Consejo 2026-09-03): deduplicación EJECUTADA de [adiez] (692 dup por
scan) y [adiecinueve] (92 dup por scan) sobre leyes/BOE-A-1986-10499.md.
Reglas de la casa:
 - manifiesto sha256 antes/después (fichero completo + bloque + párrafos)
 - el bloque conservado debe coincidir PÁRRAFO A PÁRRAFO con el BOE consolidado
   (evidencia/boe_texto_plano.txt, BOE-A-1986-10499, consolidación 02/08/2011
   para el art. 10 y 05/10/2011 para el art. 19)
 - fidelidad registrada APARTE del ahorro (acuerdo del Consejo 2026-09-01)
 - backup .bak antes de tocar
"""
import re, hashlib, json, shutil, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))          # .../sanidad/evidencia
SAN  = os.path.dirname(BASE)                                # .../sanidad
LEY  = os.path.join(SAN, 'leyes', 'BOE-A-1986-10499.md')
BAK  = LEY + '.bak-2026-09-04-pre-10-19'
BOE  = os.path.join(BASE, 'boe_texto_plano.txt')

def sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def sha_file(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def norm(p):
    """normalización para matching BOE: quita tags, NBSP, espacios sobrantes"""
    p = p.replace('\u00a0', ' ')
    p = re.sub(r'<[^>]+>', '', p)
    return re.sub(r'\s+', ' ', p).strip()

raw = open(LEY, encoding='utf-8').read()
crlf = '\r\n' in raw
lines = raw.splitlines()

# ---------- parseo de bloques (misma convención que dedup_scan.py) ----------
def block_range(lines, bid):
    starts = [i for i, l in enumerate(lines)
              if re.match(r'^## \[' + bid + r'\]', l)]
    assert len(starts) == 1, f'{bid}: {len(starts)} cabeceras'
    s = starts[0]
    e = len(lines)
    for j in range(s + 1, len(lines)):
        if re.match(r'^## \[a\w+\]', lines[j]):
            e = j; break
    return s, e   # [s, e)

def paras(lns): return [l.strip() for l in lns if l.strip()]

def wc(lns): return sum(len(p.split()) for p in paras(lns))

manifiesto = {}
manifiesto['fecha'] = '2026-09-04'
manifiesto['acuerdo'] = 27
manifiesto['ley'] = 'BOE-A-1986-10499.md'
manifiesto['sha256_fichero_antes'] = sha_file(LEY)   # hash de bytes, cadena de custodia

# ---------- BOE vigente: párrafos por artículo, para fidelidad ----------
boe = open(BOE, encoding='utf-8').read()
def boe_article(bid, title, nxt):
    # el plano BOE repite el título en el índice; tomar la 2ª ocurrencia = cuerpo
    idx = [m.start() for m in re.finditer(re.escape(title), boe)]
    body = None
    for st in idx[1:]:
        en = boe.find(nxt, st)
        seg = boe[st:en if en > 0 else st + 4000]
        if len(seg) > 100: body = seg; break
    ps = [norm(x) for x in body.split('\n') if norm(x)]
    ps = [p for p in ps if not p.startswith('[') and 'Se modifican' not in p
          and 'Se derogan' not in p and 'Seleccionar' not in p and 'publicada el' not in p
          and 'Última actualización' not in p and 'Texto original' not in p
          and p not in ('Subir',) and not p.startswith('Sección') and 'en vigor' not in p]
    return set(ps)

boe10 = boe_article('adiez', 'Artículo diez', 'Artículo once')
boe19 = boe_article('adiecinueve', 'Artículo diecinueve', 'CAPÍTULO III')

# ============================================================ [adiez]
s, e = block_range(lines, 'adiez')
before = lines[s:e]
# párrafos del bloque
ps = paras(before)
# la COPIA VIGENTE (Ley 26/2011) es la que empieza por el 3er «Todos tienen los siguientes derechos»
inicios = [i for i, p in enumerate(ps) if p.startswith('Todos tienen los siguientes derechos')]
assert len(inicios) == 3, f'[adiez] esperaba 3 copias de la lista, hay {len(inicios)}'
vig = ps[inicios[2]:]
# el texto del bloque conserva convención del repo: «<strong>(Derogado)</strong>» — la copia vigente ya la trae
nuevo = ['## [adiez] Artículo diez', '', 'Artículo diez', '']
for p in vig: nuevo += [p, '']
while nuevo and nuevo[-1] == '': nuevo.pop()
after10 = nuevo
words_before_10, words_after_10 = wc(before), wc(after10)
# ============================================================ [adiecinueve]
s2, e2 = block_range(lines, 'adiecinueve')
before2 = lines[s2:e2]
ps2 = paras(before2)
k = [i for i, p in enumerate(ps2) if p.startswith('1.') and 'Derogado' in p]
assert len(k) == 1, f'[adiecinueve] esperaba 1 copia con 1.(Derogado), hay {len(k)}'
vig2 = ps2[k[0]:]
nuevo2 = ['## [adiecinueve] Artículo diecinueve', '', 'Artículo diecinueve', '']
for p in vig2: nuevo2 += [p, '']
while nuevo2 and nuevo2[-1] == '': nuevo2.pop()
after19 = nuevo2
words_before_19, words_after_19 = wc(before2), wc(after19)

# ---------- reconstruir fichero (reemplazo por índice, de abajo arriba) ----------
assert s2 > e  # bloques separados
out = lines[:s] + after10 + lines[e:s2] + after19 + lines[e2:]
newtext = '\n'.join(out) + ('\n' if raw.endswith('\n') else '')
if crlf: newtext = newtext.replace('\n', '\r\n')

# ---------- FIDELIDAD: cada párrafo conservado, con su hash en el BOE ----------
def fidelidad(after, boe_set, skip_header=3):
    keep = [norm(p) for p in paras(after)][1:]  # sin la cabecera ## [..]
    hits = [(p, p in boe_set) for p in keep]
    ok = sum(1 for _, h in hits if h)
    return {'parrafos': len(hits), 'hash_en_BOE': ok,
            'no_coinciden': [p[:90] for p, h in hits if not h]}

fid10 = fidelidad(after10, boe10)
fid19 = fidelidad(after19, boe19)

# ---------- aplicar ----------
shutil.copy(LEY, BAK)
open(LEY, 'w', encoding='utf-8', newline='').write(newtext)
# convención de formato del repo: línea en blanco previa a cada cabecera ##
tmp = open(LEY, encoding='utf-8').read().splitlines()
fix = []
for l in tmp:
    if l.startswith('## [a') and fix and fix[-1].strip() != '':
        fix.append('')
    fix.append(l)
open(LEY, 'w', encoding='utf-8', newline='').write('\n'.join(fix) + '\n')

# ---------- manifiesto después + re-scan + verify restituciones ----------
after_lines = open(LEY, encoding='utf-8').read().splitlines()
manifiesto['sha256_fichero_despues'] = sha_file(LEY)

def scan_dup(ls):
    """mismo método que dedup_scan.py"""
    blocks, cur = [], None
    for i, l in enumerate(ls):
        m = re.match(r'^## \[(a\w+)\] (.*)$', l)
        if m:
            cur = {'id': m.group(1), 'lines': []}; blocks.append(cur)
        elif cur is not None:
            cur['lines'].append(l)
    tot_w = tot_b = nblocks = 0
    per = {}
    for b in blocks:
        nblocks += 1
        seen = {}
        for p in [x.strip() for x in b['lines'] if x.strip()]:
            seen.setdefault(sha(p), []).append(p)
        w = sum(len(v[0].split()) * (len(v) - 1) for v in seen.values() if len(v) > 1)
        per[b['id']] = w
        tot_w += w; tot_b += 1 if w > 0 else 0
    return nblocks, tot_b, tot_w, per

nblocks, blocks_dup, dup_words, per = scan_dup(after_lines)
total_words = sum(len(l.split()) for l in after_lines)

# verify de las restituciones del acuerdo 17/25 (los dos «a)» que estaban en pausa)
full = '\n'.join(after_lines)
a25 = full.count('a) No resultarán discriminatorios')
a79 = len(re.findall(r'^a\) Cotizaciones sociales\.$', full, flags=re.M))
a10_amb = full.count('a) Cuando la no intervención')  # letra a) del 6 del art.10 (capa 1986)
manifiesto['bloques'] = {
 'adiez': {'lineas_antes': e - s, 'lineas_despues': len(after10),
           'palabras_antes': words_before_10, 'palabras_despues': words_after_10,
           'palabras_suprimidas': words_before_10 - words_after_10,
           'dup_scan_antes': 692, 'dup_scan_despues': per.get('adiez', 0),
           'fidelidad': fid10},
 'adiecinueve': {'lineas_antes': e2 - s2, 'lineas_despues': len(after19),
           'palabras_antes': words_before_19, 'palabras_despues': words_after_19,
           'palabras_suprimidas': words_before_19 - words_after_19,
           'dup_scan_antes': 92, 'dup_scan_despues': per.get('adiecinueve', 0),
           'fidelidad': fid19},
}
manifiesto['ley_despues'] = {'bloques': nblocks, 'bloques_con_dup': blocks_dup,
                             'palabras_dup_scan': dup_words,
                             'palabras_totales_fichero': total_words,
                             'tasa_dup': round(100.0 * dup_words / total_words, 2)}
manifiesto['inventario_dup_restante'] = {k: v for k, v in sorted(per.items(), key=lambda x: -x[1]) if v > 0}
manifiesto['verify_restituciones'] = {
    'a_no_discriminatorios_art25_copias': a25,
    'a_cotizaciones_art79_copias': a79,
    'a_cuando_no_intervencion_art10_capa1986': a10_amb,
    'nota': ('Las dos restituciones EN PAUSA del acuerdo 17 eran las letras a) de [aveinticinco] y '
             '[asetentaynueve] (el «24» fue error de transcripción del 09-02, corregido el 09-03 y '
             'ratificado en el acta). Ambas aterrizaron AYER; hoy se re-verifica copia única. La letra '
             'a) del apartado 6 del art. 10 vive solo en la capa de 1986 que hoy se retira: en la '
             'redacción vigente el apartado 6 está (Derogado) por la Ley 41/2002, y el BOE no la lista.')
}
json.dump(manifiesto, open(os.path.join(BASE, 'manifiesto_10_19_2026-09-04.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(json.dumps(manifiesto, ensure_ascii=False, indent=1))
