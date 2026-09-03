# MANIFIESTO MASIVO LGT — 335 bloques — cierre de Fase 1 (sesion 5/30, 2026-09-02)
# Cumplimiento del acuerdo 13 del Consejo 2026-09-01 (APROBADO CON CONDICION):
#   condicion = taxonomia de Hacienda firmada ANTES de ejecutar el barrido.
# Metodo (convencion declarada 335, identica al escaneo 08-29..09-01):
#   - re.split por TODOS los encabezados "## [bid]" (lecion 2026-08-31: nunca regex solo numerico)
#   - parrafos separados por linea en blanco, normalizados (\s+ -> ' '), sha256 por parrafo
#   - duplicacion LITERAL = mismo sha256 >=2 veces DENTRO del bloque
#   - huella por bloque = sha256 del bloque normalizado completo + sha256 crudo
#   - clasificacion de fidelidad = los 161 casos del test contra BOE archivado (v)
# SOLO LECTURA sobre la ley: no modifica el fichero (restituciones: otra tramitacion, acuerdo 12).
import re, json, hashlib, io, sys, collections, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
LAW = "../leyes/BOE-A-2003-23186.md"
BOE01 = "../evidencia/boe_consolidado_BOE-A-2003-23186.html"
BOE02 = "../evidencia/boe_vivo_LGT_2026-09-02.html"

def norm(p): return re.sub(r'\s+', ' ', p).strip()
def wc(s): return len(s.split())
def sha(s): return hashlib.sha256(norm(s).encode()).hexdigest()
def shac(s): return hashlib.sha256(s.encode() if isinstance(s, str) else s).hexdigest()

txt = open(LAW, encoding='utf-8').read().replace('\r\n', '\n')
parts = re.split(r'^(## \[[^\]]+\][^\n]*)$', txt, flags=re.M)
head, order = {}, []
for i, seg in enumerate(parts):
    m = re.match(r'^## (\[[^\]]+\])', seg)
    if m:
        bid = m.group(1)
        head[bid] = (seg, parts[i+1] if i+1 < len(parts) else '')
        order.append(bid)
print("bloques detectados:", len(order))
assert len(order) == 335, f"CONVENCION 335 ROTA: {len(order)}"

manifesto = {}
tot_par = tot_dup_par = tot_dup_w = 0
blocks_with_dup = []
for bid in order:
    hline, body = head[bid]
    titulo = hline[3:].strip()
    paras = [p for p in re.split(r'\n\s*\n', body) if norm(p)]
    cnt = collections.Counter(sha(p) for p in paras)
    dups = {k: c for k, c in cnt.items() if c >= 2}
    dup_par = sum(c - 1 for c in dups.values())
    dup_w = 0
    seen = set()
    for p in paras:
        h = sha(p)
        if h in dups:
            if h in seen:
                dup_w += wc(p)
            else:
                seen.add(h)
    manifesto[bid] = {
        "titulo": titulo,
        "palabras": wc(body),
        "parrafos": len(paras),
        "parrafos_dup": dup_par,
        "palabras_dup": dup_w,
        "sha256_bloque_norm": sha(body),
        "sha256_bloque_crudo": shac(body),
        "hashes_parrafo": [sha(p) for p in paras],
    }
    tot_par += len(paras)
    tot_dup_par += dup_par
    tot_dup_w += dup_w
    if dup_par: blocks_with_dup.append((bid, dup_par, dup_w))

# fidelidad: 161 casos clasificados contra BOE archivado (09-01) + huella hoy
fidel = json.load(open("../evidencia/fidelidad_LGT_total_2026-09-01.json", encoding="utf-8"))
vcount = collections.Counter(r["v"] for r in fidel)
for r in fidel:
    r["sha256_texto"] = sha(r["texto"])
fidel_bloques = sorted(set(r["bloque"] for r in fidel))
# re-verificacion: cada caso "contenido_perdido" sigue ausente del bloque hoy
resv = {}
for r in fidel:
    b = manifesto.get(r["bloque"])
    resv[r["v"]] = resv.get(r["v"], 0) + (1 if b and r["sha256_texto"] not in b["hashes_parrafo"] else 0)

boe01sha = shac(open(BOE01, "rb").read())
boe02sha = shac(open(BOE02, "rb").read())
a01 = open(BOE01, encoding="utf-8", errors="replace").read()
a02 = open(BOE02, encoding="utf-8", errors="replace").read()
diffpos = [i for i in range(min(len(a01), len(a02))) if a01[i] != a02[i]][:3]

out = {
 "ley": "BOE-A-2003-23186 (Ley 58/2003 General Tributaria)",
 "fecha": "2026-09-02", "sesion": "5/30 (cierre Fase 1)",
 "mandato": "Acuerdo 13 Consejo 2026-09-01 (APROBADO CON CONDICION) + acuerdo 10 (denominador 335)",
 "condicion_satisfecha": "Taxonomia de Hacienda firmada el 2026-09-02 en evidencia/TAXONOMIA_LGT_FIRMADA_2026-09-02.md, ANTES de este barrido",
 "metodo": {
   "convencion_denominador": 335,
   "split": "re.split por TODOS los encabezados '^## [bid]' (no solo numericos)",
   "normalizacion": "colapsar \\s+ a un espacio + strip; sha256 hex sobre UTF-8",
   "duplicacion": "LITERAL intra-bloque (mismo sha256 >=2 en el bloque); las no literales se clasifican aparte (test de fidelidad)",
   "fidelidad": "161 casos del test contra BOE archivado (SHA-256 en SHA256SUMS_2026-09-01), re-verificados contra el barrido de hoy"
 },
 "boe_cadena_custodia": {
   "archivado_2026-09-01": {"sha256": boe01sha, "bytes": len(a01.encode())},
   "descargado_2026-09-02": {"sha256": boe02sha, "bytes": len(a02.encode())},
   "primera_diferencia_offset": (diffpos[0] if diffpos else None)
 },
 "resumen": {
   "bloques_barridos": len(manifesto),
   "parrafos_totales": tot_par,
   "bloques_con_dup_literal": len(blocks_with_dup),
   "parrafos_dup_suprimibles": tot_dup_par,
   "palabras_dup": tot_dup_w,
   "casos_fidelidad": len(fidel),
   "casos_por_categoria": dict(vcount),
   "bloques_con_defecto_fidelidad": len(fidel_bloques),
   "reverificacion_2026-09-02_siguen_ausentes": resv
 },
 "bloques": manifesto,
 "casos_fidelidad": fidel,
}
json.dump(out, open("../evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("CATEGORIAS v:", dict(vcount))
print("palabras por categoria:", {k: sum(int(r.get("palabras") or 0) for r in fidel if r["v"] == k) for k in vcount})
print("bloques defecto:", len(fidel_bloques))
print("resumen dup hoy:", len(blocks_with_dup), "bloques /", tot_dup_par, "parrafos /", tot_dup_w, "palabras")
print("boe diff offsets:", diffpos)
print("byte a01@a:", a01[diffpos[0]-30:diffpos[0]+30] if diffpos else "identicos")
print("byte a02@a:", a02[diffpos[0]-30:diffpos[0]+30] if diffpos else "")
