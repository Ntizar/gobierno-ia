# -*- coding: utf-8 -*-
"""
ACUERDO 32 — TEST CRUZADO Y CIEGO (Mónica→LGT y Mónica→L7/2021).
Método propio de Fase 1, aplicado a las leyes de OTROS ministerios EN SOLO LECTURA
(no se toca ningún fichero ajeno; el mandato del Consejo autoriza el test, no la edición):
  T1. sha256 por párrafo dentro de cada bloque [aXXX] (misma convención dedup_scan.py,
      normalizado: recorte de espacios; se reporta también la pasada con y sin
      normalización de <tags> y NBSP para detectar duplicados «maquillados» por formato).
  T2. Detección de listas huérfanas: párrafo que empieza por «b)»/«2.» sin su «a)»/«1.»
      inmediatamente anterior — la patología del conversor BOE→repo que ya encontramos
      las tres carteras.
  T3. Cabeceras de artículo duplicadas dentro del bloque (la «doble cabecera» que el
      informe de Sanidad ya denunció para [adiez]).
Ciego: este output se escribe y hashea ANTES de leer el MANIFIESTO_MASIVO_LGT_2026-09-02.json
ni cualquier informe propio de Hacienda/Ecología del día.
"""
import re, hashlib, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
TARGETS = {
    'LGT (hacienda)': os.path.join(REPO, 'ministerios', 'hacienda', 'leyes', 'BOE-A-2003-23186.md'),
    'L7/2021 (transicion)': os.path.join(REPO, 'ministerios', 'transicion-ecologica', 'leyes', 'BOE-A-2021-8447.md'),
}

def sha(p): return hashlib.sha256(p.encode('utf-8')).hexdigest()[:16]
def norm(p):
    p = p.replace('\u00a0', ' ')
    p = re.sub(r'<[^>]+>', '', p)
    return re.sub(r'\s+', ' ', p).strip()

report = {}
for name, path in TARGETS.items():
    raw = open(path, encoding='utf-8').read()
    lines = raw.splitlines()
    blocks, cur = [], None
    for i, l in enumerate(lines, 1):
        m = re.match(r'^## \[([a-z0-9-]+)\] (.*)$', l)
        if m:
            cur = {'id': m.group(1), 'title': m.group(2), 'start': i, 'lines': []}
            blocks.append(cur)
        elif cur is not None:
            cur['lines'].append(l)
    dup_strict = dup_norm = 0
    b_dup_strict = b_dup_norm = 0
    worst = []
    orphan_b, orphan_num, dupcab = [], [], []
    for b in blocks:
        ps = [l.strip() for l in b['lines'] if l.strip()]
        seen, seen_n = {}, {}
        for p in ps:
            seen.setdefault(sha(p), []).append(p)
            seen_n.setdefault(sha(norm(p)), []).append(norm(p))
        ws = sum(len(v[0].split()) * (len(v) - 1) for v in seen.values() if len(v) > 1)
        wn = sum(len(v[0].split()) * (len(v) - 1) for v in seen_n.values() if len(v) > 1)
        dup_strict += ws; dup_norm += wn
        if ws > 0: b_dup_strict += 1
        if wn > 0: b_dup_norm += 1
        if wn > 0: worst.append((b['id'], wn, b['title'][:40]))
        # T2 huérfanas
        for j, p in enumerate(ps):
            if re.match(r'^b\)', p) and (j == 0 or not re.match(r'^a\)', ps[j-1])):
                orphan_b.append((b['id'], ps[j-1][:40] if j else 'INIICIO-BLOQUE'))
            if re.match(r'^2\.', p) and (j == 0 or not re.match(r'^1\.', ps[j-1])):
                # solo si el bloque no es una lista que alterna ordenadamente (heurística: el anterior no es 1.)
                orphan_num.append((b['id'], ps[j-1][:40] if j else 'INIICIO-BLOQUE'))
        # T3 cabecera repetida dentro del bloque
        heads = [p for p in ps if p.startswith(b['title'][:15]) and len(p.split()) < 15]
        if len(heads) > 1:
            dupcab.append((b['id'], len(heads)))
    worst.sort(key=lambda x: -x[1])
    total_words = sum(len(l.split()) for l in lines)
    report[name] = {
        'fichero': os.path.relpath(path, REPO).replace('\\', '/'),
        'sha256_fichero': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
        'bloques': len(blocks), 'palabras_fichero': total_words,
        'T1_dup_literal_estricto': {'palabras': dup_strict, 'bloques': b_dup_strict},
        'T1_dup_normalizado_tags_NBSP': {'palabras': dup_norm, 'bloques': b_dup_norm},
        'T1_mayores_10': worst[:10],
        'T2_huerfanas_b_sin_a': {'total': len(orphan_b), 'muestra': orphan_b[:12]},
        'T2_huerfanas_2_sin_1': {'total': len(orphan_num)},
        'T3_cabeceras_repetidas_en_bloque': {'total': len(dupcab), 'muestra': dupcab[:10]},
    }

out = os.path.join(BASE, 'test_cruzado_ciego_2026-09-04.json')
blob = json.dumps(report, ensure_ascii=False, indent=1)
open(out, 'w', encoding='utf-8').write(blob)
print('sha256 de este output (sellado antes de leer el informe ajeno):', hashlib.sha256(blob.encode()).hexdigest())
print(blob[:6000])
