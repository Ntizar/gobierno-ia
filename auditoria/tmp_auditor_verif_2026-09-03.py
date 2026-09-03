# -*- coding: utf-8 -*-
# Pasada final del Auditor: consolidado de comprobaciones para el informe 2026-09-03
import io, re, json, hashlib
REPO = "C:/Users/d_ant/Projects/gobierno-ia"

def norm(s):
    return re.sub(r"\s+", " ", s.strip().lower())

# A) LGT: palabras del fichero actual (conv. split), bloques, DA18 backup
lgt = io.open(REPO + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
print("A1) LGT actual: palabras:", len(lgt.split()), "| headers:", len(re.findall(r"(?m)^## \[", lgt)))
bak = io.open(REPO + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-02-da18", encoding="utf-8").read()
mm = re.search(r"(?ms)^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[|\Z)", bak)
paras = [p for p in mm.group(1).split("\n\n") if p.strip()]
print("A2) DA18 en backup 09-02: parrafos:", len(paras), "| palabras:", sum(len(p.split()) for p in paras))

# B) Manifiesto masivo: F1 restantes tras excluir DA18 y tramo 1-30
mf = json.load(io.open(REPO + "/ministerios/hacienda/evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
s = json.dumps(mf)[:120]
# buscar lista de casos
def walk(o):
    if isinstance(o, dict):
        if any(k in o for k in ("casos", "entries", "rows", "items")):
            for k in ("casos", "entries", "rows", "items"):
                if isinstance(o.get(k), list):
                    return o[k]
        for v in o.values():
            r = walk(v)
            if r: return r
    if isinstance(o, list) and o and isinstance(o[0], dict) and len(o) > 50:
        return o
    return None
cases = walk(mf)
print("B) casos en manifiesto:", len(cases) if cases else "estructura no reconocida", "| claves muestra:", list(cases[0].keys()) if cases else list(mf.keys()))
if cases:
    f1 = [c for c in cases if str(c.get("tipo", c.get("category", ""))).lower().find("f1") >= 0 or "perdido" in str(c).lower()[:400]]
    print("   F1 por texto:", len(f1))

# C) LGS: solape entre bloques -2 y sus gemelos (los 42 headers que el regex del ministerio no escanea)
lgs = io.open(REPO + "/ministerios/sanidad/leyes/BOE-A-1986-10499.md", encoding="utf-8").read()
blocks = {}
for blk in re.split(r"(?m)^(?=## \[)", lgs):
    h = re.match(r"## \[([^\]]+)\]", blk)
    if h:
        blocks[h.group(1)] = blk.split("\n", 1)[1] if "\n" in blk else ""
tot_solape = 0
for b2 in sorted(k for k in blocks if k.endswith("-2")):
    base = b2[:-2]
    if base in blocks:
        p1 = [norm(x) for x in blocks[base].splitlines() if len(norm(x).split()) >= 3]
        p2 = [norm(x) for x in blocks[b2].splitlines() if len(norm(x).split()) >= 3]
        common = [x for x in p2 if x in set(p1)]
        w = sum(len(x.split()) for x in common)
        tot_solape += w
        print("C) LGS", b2, "vs", base, ": lineas comunes", len(common), "| palabras comunes", w, "| tam-2:", len(" ".join(p2).split()))
print("C-total) solape artikel-2 no escaneados:", tot_solape, "palabras")

# D) reproducir scan ministerial LGS: 18 bloques / 1924, y adiez/adiecinueve
def scan_block(body):
    seen = {}
    for l in body.splitlines():
        t = norm(l)
        if len(t.split()) < 1: continue
        h = hashlib.sha256(l.strip().encode()).hexdigest()[:12] if l.strip() else ""
        if not l.strip(): continue
        seen.setdefault(h, []).append(l.strip())
    return sum(len(v[0].split()) * (len(v) - 1) for v in seen.values() if len(v) > 1), sum(len(v) - 1 for v in seen.values() if len(v) > 1)
tot, nb, per = 0, 0, {}
for k, v in blocks.items():
    w, e = scan_block(v)
    if e:
        tot += w; nb += 1; per[k] = w
print("D) scan LGS (151 headers): bloques dup:", nb, "| palabras dup:", tot)
print("   adiez:", per.get("adiez"), "| adiecinueve:", per.get("adiecinueve"), "| aveintiuno:", per.get("aveintiuno"))
w25, e25 = scan_block(blocks.get("aveinticinco", "")); w79, e79 = scan_block(blocks.get("asetentaynueve", ""))
print("   arts 25/79 dup:", e25, e79, "| palabras bloque:", len(" ".join(p for p in blocks['aveinticinco'].splitlines() if p.strip()).split()), len(" ".join(p for p in blocks['asetentaynueve'].splitlines() if p.strip()).split()))
print("   discriminatorios x:", len(re.findall("No resultarán discriminatorios", lgs)), "| Cotizaciones sociales x:", len(re.findall("Cotizaciones sociales", lgs)))

# E) L7: checks literales
l7 = io.open(REPO + "/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md", encoding="utf-8").read()
print("E) L7 palabras:", len(l7.split()), "| headers:", len(re.findall(r"(?m)^## \[", l7)), "| 'Artículo 15.' x:", len(re.findall(r"(?m)^Artículo 15\.", l7)))
for s_ in ["embates marinos", "desagregados por sexo", "interfaz urbano-forestal", "perspectiva de género", "control de avenidas"]:
    print("   '", s_, "':", l7.count(s_))
# listas que arrancan en b)
bad = 0
for blk in re.split(r"(?m)^(?=## \[)", l7):
    lines = [l.strip() for l in blk.splitlines() if l.strip()]
    idx = [i for i, l in enumerate(lines) if re.match(r"^[a-z]\.\)", l)]
    first = [l for l in lines if re.match(r"^a\.\)", l)]
print("E2) listas huérfanas b): aproximacion por bloque — usar test ministerial; salto")

# F) evidencia 532: la fila electricidad 83 (DF13) buscar con variante
html = io.open(REPO + "/ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html", encoding="utf-8", errors="replace").read()
i = html.find("metodología retributiva de las actividades reguladas en el sector de la electricidad")
print("F) variante electricidad encontrada:", i > -1)
