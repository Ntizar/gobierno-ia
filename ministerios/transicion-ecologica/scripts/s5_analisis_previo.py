# Sesion 5 (2026-09-03): analisis previo a la ejecucion de los acuerdos 15 y 16
# Imprime SOLO resumenes y cifras, nunca ficheros enteros.
import hashlib, json, re, io, sys

BASE = ""  # run with cwd = ministerios/transicion-ecologica
LEY = BASE + "leyes/BOE-A-2021-8447.md"

raw = open(LEY, "rb").read()
print("SHA256_ANTES:", hashlib.sha256(raw).hexdigest())
lines = raw.decode("utf-8").split("\n")
print("LINEAS:", len(lines), "BYTES:", len(raw))
words_total = len(re.findall(r"\S+", raw.decode("utf-8")))
print("PALABRAS_TOTAL_LEY:", words_total)

# 1) Mapa del bloque [a1-7] (art. 15)
def wc(seg): return len(re.findall(r"\S+", "\n".join(seg)))
print("\n-- ENTORNOS BLOQUE a1-7 --")
for i, l in enumerate(lines, 1):
    if re.match(r"^## \[", l) and 375 <= i <= 480:
        print(i, repr(l[:70]))
print("L379:", repr(lines[378][:70]))
print("L382:", repr(lines[381][:70]))
print("L444:", repr(lines[443][:70]))
print("L445:", repr(lines[444][:70]))
print("L473:", repr(lines[472][:70]))
print("L474:", repr(lines[473][:70]))
seg_v1v2 = lines[381:444]  # lineas 382..444 inclusive
print("PALABRAS_A_ELIMINAR_382_444:", wc(seg_v1v2))
seg_v3 = lines[444:473]    # lineas 445..473
print("PALABRAS_V3_445_473:", wc(seg_v3))

# 2) Bloques DF 4a, 5a, 9a
print("\n-- BLOQUES DF --")
for i, l in enumerate(lines, 1):
    if re.match(r"^## \[(df|da)", l):
        print(i, repr(l[:60]))

# 3) Estructura de los JSON de evidencia (claves y counts, sin volcar)
for jf in ["evidencia/verificacion_fidelidad_BOE_2026-09-01.json",
           "evidencia/omisiones_repositorio_2026-09-01.json",
           "evidencia/lineas_ausentes_BOE_vs_repo_2026-09-01.json"]:
    d = json.load(open(BASE + jf, encoding="utf-8"))
    print("\nJSON:", jf, "type:", type(d).__name__)
    if isinstance(d, dict):
        for k, v in d.items():
            print("  key:", k, type(v).__name__, (len(v) if hasattr(v, "__len__") else v))
    elif isinstance(d, list):
        print("  len:", len(d), "elem0 keys:", list(d[0].keys()) if d and isinstance(d[0], dict) else d[:1])
