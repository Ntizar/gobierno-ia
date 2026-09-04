# TEST CRUZADO Y CIEGO (acuerdo 32) — Arcadi (Hacienda) sobre la LEY 7/2021 de Sara (Transición Ecológica)
# Corre mi método — el mismo del manifiesto masivo LGT: convención de encabezados, sha256 por párrafo
# normalizado, dup LITERAL intra-bloque, y test de letras huérfanas contra el BOE archivado.
# CIEGO: no leo el manifiesto de Sara ANTES de barrer; su evidencia solo se contrasta al final, en claro.
# SOLO LECTURA: no toco el fichero de otro ministerio (prohibido por la Constitución del repo).
import re, io, sys, json, hashlib, collections, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

L7 = "../transicion-ecologica/leyes/BOE-A-2021-8447.md"
BOE7 = "../transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html"

def norm(p): return re.sub(r'\s+', ' ', p).strip()
def wc(s): return len(s.split())
def sha(s): return hashlib.sha256(norm(s).encode()).hexdigest()

txt = open(L7, encoding='utf-8').read().replace('\r\n', '\n')
parts = re.split(r'(?m)^(## \[[^\]]+\][^\n]*)$', txt)
head = {}
order = []
for i, seg in enumerate(parts):
    m = re.match(r'^## (\[[^\]]+\])', seg)
    if m:
        head[m.group(1)] = (seg, parts[i+1] if i+1 < len(parts) else '')
        order.append(m.group(1))
print("== BARRIDO CIEGO ==")
print("bloques detectados:", len(order), "| palabras fichero:", wc(re.sub(r'(?m)^## \[[^\]]+\]', '', txt)))

# 1) duplicación literal intra-bloque (mi definición D1)
tot_dp = tot_dw = 0
dups = []
for bid in order:
    _, body = head[bid]
    paras = [p for p in re.split(r'\n\s*\n', body) if norm(p)]
    cnt = collections.Counter(sha(p) for p in paras)
    d = {k: c for k, c in cnt.items() if c >= 2}
    dp = sum(c-1 for c in d.values())
    dw = 0; seen = set()
    for p in paras:
        h = sha(p)
        if h in d:
            if h in seen: dw += wc(p)
            else: seen.add(h)
    tot_dp += dp; tot_dw += dw
    if dp: dups.append((bid, dp, dw))
print(f"D1 dup literal: {tot_dp} parrafos suprimibles / {tot_dw} palabras en {len(dups)} bloques")
for b in dups[:10]: print("   ", b)

# 2) test de letras huérfanas: párrafos que empiezan por «b)» sin su «a)» en la ley BOE
#    (mi método de LGT aplicado a su ley — busco listas que arranquen en b) tras barrido)
boe = open(BOE7, encoding='utf-8', errors='replace').read()
def clean(seg):
    seg = re.sub(r'<[^>]+>', '', seg)
    return re.sub(r'\s+', ' ', seg).strip()
# parrafos BOE -> set normalizado (prefijo 60 chars, tolerante a entidades)
boe_par = set()
for t in re.findall(r'<p class="[^"]*">(.*?)</p>', boe, re.S):
    c = unicodedata.normalize('NFC', clean(t))
    if len(c) > 12: boe_par.add(c[:90])
print("parrafos BOE indexados:", len(boe_par))

# 3) para cada bloque del repo: ¿su texto (normalizado) traza en BOE? muestreo por parrafo largo
fantasmas = []  # parrafos del repo SIN traza en el BOE archivado (test X1 de Hacienda)
for bid in order:
    _, body = head[bid]
    paras = [p for p in re.split(r'\n\s*\n', body) if norm(p)]
    for j, p in enumerate(paras):
        c = unicodedata.normalize('NFC', norm(p))
        if wc(c) < 15: continue  # los cortos dan falsos positivos por anclaje
        pref = c[:90]
        if pref not in boe_par:
            fantasmas.append((bid, j, wc(c), c[:110]))
print("\n== PARRAFOS >15 PAL SIN TRAZA EN BOE ARCHIVADO ==")
for f in fantasmas: print(f"   {f[0]} par.{f[1]} ({f[2]} pal): {f[3]}")
print("total:", len(fantasmas))

# 4) listas huérfanas «b)» — el test que Presidencia usó: bloque con párrafo «b)...» cuyo «a)...»
#    existe en BOE pero no en el bloque del repo
orph = []
for bid in order:
    _, body = head[bid]
    paras = [norm(p) for p in re.split(r'\n\s*\n', body) if norm(p)]
    has_a = any(p.startswith('a)') for p in paras)
    n_b = sum(1 for p in paras if p.startswith('b)'))
    if n_b and not has_a:
        orph.append((bid, n_b))
print("\n== BLOQUES CON 'b)' SIN SU 'a)' ==", orph if orph else "0 — limpio")

# 5) rótulos duplicados: la segunda línea «Artículo N» dentro del cuerpo (hallazgo LGT; ¿aquí también?)
dup_label = 0
for bid in order:
    h, body = head[bid]
    mt = re.search(r'Art[íi]culo\s+[\w\-áéíóú]+', h)
    if mt:
        label = mt.group(0)
        oc = len(re.findall(re.escape(label) + r'\.', body))
        if oc >= 2: dup_label += 1
print("bloques con el rótulo 'Artículo ...' 2+ veces en el cuerpo:", dup_label)

json.dump({"test": "cruzado Hacienda->L7", "fecha": "2026-09-04",
           "bloques": len(order),
           "D1_parrafos": tot_dp, "D1_palabras": tot_dw, "D1_bloques": [b[0] for b in dups],
           "fantasmas_boe": [{"bloque": f[0], "parrafo": f[1], "palabras": f[2], "texto": f[3]} for f in fantasmas],
           "b_huerfanas": orph, "rotulos_dup": dup_label},
          open("evidencia/test_cruzado_L7_2026-09-04.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nguardado evidencia/test_cruzado_L7_2026-09-04.json")
