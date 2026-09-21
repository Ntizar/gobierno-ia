# -*- coding: utf-8 -*-
"""Verificación post-aplicación (sesión 13/30, 2026-09-21):
 - fidelidad párrafo a párrafo contra el BOE consolidado archivado
 - recuento de copias por artículo (art. 3 y art. 6 deben tener UNA sola)
 - re-escaneo de duplicados intra-bloque
 - test cruzado ciego (versión conservada vs. versión eliminada)"""
import re, hashlib, json, os, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
SAN  = os.path.dirname(BASE)
LEY  = os.path.join(SAN, 'leyes', 'BOE-A-1986-10499.md')
BOE  = os.path.join(BASE, 'boe_texto_plano.txt')

def sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def nn(p):
    p = p.replace('\u00a0', ' ')
    p = p.replace('"', '"').replace('"', '"').replace('"', '"').replace('"', '"')
    p = re.sub(r'<[^>]+>', '', p)
    return re.sub(r'\s+', ' ', p).strip()

L = open(LEY, encoding='utf-8').read().splitlines()
boe_raw = open(BOE, encoding='utf-8').read()
boe_n = nn(boe_raw)                     # una sola cadena normalizada
boe_set = set(nn(x) for x in boe_raw.split('\n') if nn(x))

def blk(bid):
    s = [i for i, l in enumerate(L) if re.match(r'^## \[' + bid + r'\]', l)][0]
    e = len(L)
    for j in range(s + 1, len(L)):
        if re.match(r'^## \[a\w+\]', L[j]):
            e = j; break
    return s, e

def paras(ls): return [l.strip() for l in ls if l.strip()]

def fidelidad(bid, sin_rotulo=True):
    s, e = blk(bid)
    ps = paras(L[s:e])
    if sin_rotulo: ps = ps[1:]          # quita la cabecera ##
    res = []
    for p in ps:
        exacto = p in boe_set
        # tolera el número de apartado que el BOE añade al rótulo de la intro
        suelto = re.sub(r'^\d+\.\s*', '', p)
        en_linea = (nn(p) in boe_n) or (nn(suelto) in boe_n)
        res.append((p[:70], exacto, en_linea))
    return res

print('================= FIDELIDAD vs BOE CONSOLIDADO ARCHIVADO =================')
tot_ok = tot = 0
for bid, lab in [('atres', 'art. 3'), ('aseis', 'art. 6'), ('adieciseis', 'art. 16'), ('aveinte', 'art. 20')]:
    print(f'\n--- [{bid}] {lab} ---')
    for txt, exacto, en_linea in fidelidad(bid):
        tot += 1; tot_ok += 1 if en_linea else 0
        marca = 'EXACTO' if exacto else ('OK(substr)' if en_linea else '*** NO EN BOE ***')
        print(f'   [{marca:11s}] {txt}')
print(f'\n>>> párrafos conservados presentes en el BOE: {tot_ok}/{tot}')

print('\n================= COPIA ÚNICA art. 3 y art. 6 =================')
full = '\n'.join(L)
for txt, lab in [('1. Los medios y actuaciones del sistema sanitario', 'art.3.1'),
                 ('2. La asistencia sanitaria pública se extenderá', 'art.3.2'),
                 ('3. La política de salud estará orientada', 'art.3.3'),
                 ('4. Las políticas, estrategias y programas de salud', 'art.3.4'),
                 ('Las actuaciones de las Administraciones Públicas Sanitarias estarán orientadas:', 'art.6.intro'),
                 ('1. A la promoción de la salud.', 'art.6.1'),
                 ('2. A promover el interés individual', 'art.6.2'),
                 ('3. A garantizar que cuantas acciones', 'art.6.3'),
                 ('4. A garantizar la asistencia sanitaria en todos los casos', 'art.6.4'),
                 ('5. A promover las acciones necesarias', 'art.6.5'),
                 ('2. En la ejecución de lo previsto en el apartado anterior', 'art.6.igualdad')]:
    print(f'   {lab:22s} copias = {full.count(txt)}')

print('\n================= RE-ESCANEO DUP INTRA-BLOQUE =================')
blocks, cur = [], None
for i, l in enumerate(L):
    m = re.match(r'^## \[(a\w+)\] (.*)$', l)
    if m:
        cur = {'id': m.group(1), 'lines': []}; blocks.append(cur)
    elif cur is not None:
        cur['lines'].append(l)
per = {}; tot_w = 0
for b in blocks:
    seen = {}
    for p in [x.strip() for x in b['lines'] if x.strip()]:
        seen.setdefault(sha(p), []).append(p)
    w = sum(len(v[0].split()) * (len(v) - 1) for v in seen.values() if len(v) > 1)
    per[b['id']] = w; tot_w += w
print(f'   bloques: {len(blocks)} | palabras duplicadas (scan): {tot_w}')
print(f'   [atres]={per.get("atres")}  [aseis]={per.get("aseis")}  [aveinte]={per.get("aveinte")}  [adieciseis]={per.get("adieciseis")}')
top = {k: v for k, v in sorted(per.items(), key=lambda x: -x[1]) if v > 0}
print('   top dup restante:', dict(list(top.items())[:12]))

print('\n================= TEST CRUZADO CIEGO [atres]/[aseis]/[aveinte] =================')
s3, e3 = blk('atres')
kept3 = [p for p in paras(L[s3:e3])][1:]
elim3 = ['Artículo tres',
 '1. Los medios y actuaciones del sistema sanitario estarán orientados prioritariamente a la promoción de la salud y a la prevención de las enfermedades.',
 '2. La asistencia sanitaria pública se extenderá a toda la población española. El acceso y las prestaciones sanitarias se realizarán en condiciones de igualdad efectiva.',
 '3. La política de salud estará orientada a la superación de los desequilibrios territoriales y sociales.']
k3 = sum(1 for p in kept3 if nn(p) in boe_n or nn(re.sub(r'^\d+\.\s*','',p)) in boe_n)
e3c = sum(1 for p in elim3 if nn(p) in boe_n or nn(re.sub(r'^\d+\.\s*','',p)) in boe_n)
print(f'   [atres]  conservado {k3}/{len(kept3)} en BOE   |   eliminado {e3c}/{len(elim3)} en BOE   (el conservado incluye 3.4)')
print('   -> 3.4 (igualdad) presente en BOE:', nn([p for p in kept3 if p.startswith('4.')][0]) in boe_n)
print('\n[fin verificación]')
