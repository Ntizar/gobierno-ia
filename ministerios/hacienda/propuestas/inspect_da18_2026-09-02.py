# Inspeccion forense de [dadecimoctava]: grupos duplicados + trazabilidad contra el BOE archivado
# (grieta senalada por el Auditor 2026-09-01, acuerdo 11 con observaciones; orden presidencial 2026-09-02)
import hashlib, re, json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = "../"
LAW = ROOT + "leyes/BOE-A-2003-23186.md"
BOE = ROOT + "evidencia/boe_consolidado_BOE-A-2003-23186.html"

src = open(LAW, encoding="utf-8").read().replace("\r\n", "\n")
# re.split por TODOS los encabezados (convencion 335, leccion 2026-08-31)
blocks = re.split(r"\n(?=## \[)", src)
da18 = next(b for b in blocks if b.startswith("## [dadecimoctava]"))

paras = [l.strip() for l in da18.split("\n") if l.strip() and len(l.strip()) > 40 and not l.strip().startswith("## [")]
seen, groups = {}, []
for i, p in enumerate(paras):
    key = hashlib.sha256(re.sub(r"\s+", " ", p).lower().encode()).hexdigest()
    seen.setdefault(key, []).append(i)
total_dup = 0
print("=== GRUPOS DUPLICADOS EN [dadecimoctava] (normalizado, case-insensitive) ===")
for key, idxs in seen.items():
    if len(idxs) > 1:
        p = paras[idxs[0]]
        w = len(p.split())
        total_dup += (len(idxs) - 1) * w
        print(f"x{len(idxs)} ({w} pal) idxs={idxs} | {p[:110]}")
print(f"-- dup_words_DA18 = {total_dup} | paras_total = {len(paras)}")

# sensibilidad a normalizacion: mismo escaneo case-SENSITIVE (metodo del scan oficial)
seen2 = {}
for i, p in enumerate(paras):
    key = hashlib.sha256(re.sub(r"\s+", " ", p).encode()).hexdigest()
    seen2.setdefault(key, []).append(i)
d2 = sum((len(v)-1)*len(paras[v[0]].split()) for v in seen2.values() if len(v) > 1)
print(f"-- dup_words case-sensitive (metodo manifiesto) = {d2}")

print("\n=== TRAZABILIDAD CONTRA BOE ARCHIVADO ===")
boe = open(BOE, encoding="utf-8", errors="replace").read()
nb = re.sub(r"\s+", " ", boe)
nb_lower = nb.lower()
nb_nbsp = re.sub(r"\s+", " ", boe.replace("\xa0", " "))
probes = [
    "referidos a una misma cuenta",
    "Obligación de información sobre bienes y derechos situados en el extranjero",
    "monedas virtuales situadas en el extranjero",
    "multa pecuniaria fija de 5.000 euros por cada dato",
    "serán incompatibles con las establecidas en los artículos 198 y 199",
    "titulares reales",
    "El Tribunal de Cuentas",
    "depuración",
]
for pr in probes:
    print(f"'{pr[:70]}': exacto={nb.count(pr)} insensitive={nb_lower.count(pr.lower())} nbsp_ok={nb_nbsp.count(pr)}")

# localizar el bloque DA18 en el BOE HTML para ver su estructura real
m = re.search(r"Disposici[oó]n adicional decimoctativa", boe, re.I)
print("\nPrimera menciona DA18 en BOE en offset:", m.start() if m else None)
if m:
    seg = re.sub(r"<[^>]+>", " ", boe[m.start():m.start()+18000])
    seg = re.sub(r"\s+", " ", seg)
    # contar cuantas veces aparece la frase de la intro y la sancion en esa region
    for pr in ["Los obligados tributarios deberán suministrar", "100 euros por cada dato o conjunto de datos referidos a una misma cuenta", "5.000 euros por cada dato", "150 euros por cada dato"]:
        print(f"  BOE-region x{seg.count(pr)} | {pr[:60]}")
    print("  --- primer trozo de la DA18 en el BOE ---")
    print(" ", seg[:600])
