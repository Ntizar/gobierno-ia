# Sesion 5 (2026-09-03) — EJECUCION de los acuerdos 15 y 16 del Consejo 2026-09-01
# sobre ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md
#  - Acuerdo 16: diff art. 15 -> eliminar lineas 382-444 (v1+v2+rotulos dup), conservar v3 (445-473)
#  - Acuerdo 15: restituir las 9 lineas / 297 palabras de DF 4a/5a/9a (omision total)
#  - Acuerdo 14-ter (restituciones aprobadas 2026-08-31): insertar las 22 letras «a)» verificadas contra el BOE archivado
# Escribe manifiesto JSON con sha256 antes/despes y cada linea tocada. Solo imprime cifras.
import hashlib, json, re, shutil, sys

LEY = "leyes/BOE-A-2021-8447.md"
BAK = "leyes/BOE-A-2021-8447.md.bak-2026-09-03"

raw = open(LEY, "rb").read()
sha_before = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
crlf = "\r\n" in text
NL = "\r\n" if crlf else "\n"
lines = text.split(NL)
wc = lambda seg: len(re.findall(r"\S+", "\n".join(seg)))
words_before = wc(lines)

# backup
shutil.copy2(LEY, BAK)

def sha_of(lst):
    return hashlib.sha256(NL.join(lst).encode("utf-8")).hexdigest()

sha_after_step1 = None
manifest = {"fecha": "2026-09-03", "sha256_antes": sha_before, "palabras_antes": words_before,
            "lineas_antes": len(lines)}

# ---------- PASO 1: acuerdo 16 (diff art. 15) ----------
# Rango verificado hoy: linea 382 (idx 381) a linea 444 (idx 443) inclusive = 2.548 palabras
i0, i1 = 381, 444  # idx corte Python: [381:444] = lineas 382..444
seg = lines[i0:i1]
pal_art15 = wc(seg)
assert pal_art15 == 2548, f"rango art.15 no cuadrado: {pal_art15}"
# comprobaciones de borde: linea 382 en blanco, 445 = inicio v3 «1. El Gobierno...»
assert lines[i0].strip() == "", "L382 no es linea en blanco"
assert lines[i1].startswith("1. El Gobierno"), "L445 no es el inicio de la v3"
new = lines[:i0] + lines[i1:]
sha_after_step1 = sha_of(new)
manifest["acuerdo_16_art15"] = {"eliminan_lineas": "382-444 (antes del diff)", "lineas": 63,
    "palabras_eliminadas": pal_art15, "sha256_tras_paso1": sha_after_step1,
    "v3_conservada_palabras": wc(new[381:410]) and wc(lines[i1:i1+29])}

# ---------- PASO 2: acuerdo 15 (restitucion DF 4a/5a/9a) ----------
om = json.load(open("evidencia/omisiones_repositorio_2026-09-01.json", encoding="utf-8"))["omisiones"]
df4 = [r["linea"] for r in om if r["bloque"].startswith("artículo 20.1 del texto refundido")]
df5 = [r["linea"] for r in om if r["bloque"].startswith("artículo 26.3 de la Ley 50/1997")]
df9 = [r["linea"] for r in om if r["bloque"].startswith("artículo 38 bis de la Ley 25/1964")]
assert len(df4) == 7 and len(df5) == 1 and len(df9) == 1, (len(df4), len(df5), len(df9))

def insert_after_block_end(new_lines, header_prefix, insert_lines):
    """inserta insert_lines antes del siguiente encabezado '## [' tras header_prefix"""
    hi = next(i for i, l in enumerate(new_lines) if l.startswith("## [" + header_prefix))
    # buscar el siguiente encabezado tras hi; insercion justo antes de la linea en blanco previa
    ni = next(i for i in range(hi + 1, len(new_lines)) if new_lines[i].startswith("## [") or new_lines[i].startswith("# "))
    j = ni
    while new_lines[j - 1].strip() == "":
        j -= 1
    return new_lines[:j] + list(insert_lines) + [""] + new_lines[j:], j, hi

pal_restit = 0
for pref, blk in (("df-4", df4), ("df-5", df5), ("df-9", df9)):
    new, pos, hi = insert_after_block_end(new, pref, blk)
    pal_restit += wc(blk)
    manifest.setdefault("acuerdo_15_restituciones", []).append(
        {"bloque": pref, "lineas_insertadas": len(blk), "palabras": wc(blk), "posicion": pos})
assert pal_restit == 297, f"palabras restituidas {pal_restit} != 297"

# ---------- PASO 3: restitucion de las 22 letras «a)» ----------
vf = json.load(open("evidencia/verificacion_fidelidad_BOE_2026-09-01.json", encoding="utf-8"))
filas = [r for r in vf if r.get("repo")]
assert len(filas) == 22, len(filas)
pal_letras = 0
hechas = 0
for r in filas:
    a_txt = r["texto_a"].strip().replace("\r\n", "\n").replace("\n", " ")
    assert a_txt.startswith("a)"), a_txt[:40]
    # localizar el bloque por el prefijo de cabecera
    cab = r["repo"].strip()
    key = re.match(r"^## \[[^\]]+\]", cab).group(0)
    hi = next(i for i, l in enumerate(new) if l.startswith(key))
    ni = next((i for i in range(hi + 1, len(new)) if new[i].startswith("## [") or new[i].startswith("# ")), len(new))
    # primera linea 'b) ' del bloque
    bi = next((i for i in range(hi, ni) if new[i].strip().startswith("b) ")), None)
    if bi is None:
        manifest.setdefault("letras_a_ya_presentes_o_sin_b", []).append({"bloque": key, "nota": "no hay b) tras cabecera"})
        continue
    # evitar doble insercion: si ya hay una 'a)' justo antes, saltar
    if new[bi - 1].strip().startswith("a)"):
        manifest.setdefault("letras_a_ya_presentes_o_sin_b", []).append({"bloque": key, "nota": "ya presente"})
        continue
    new = new[:bi] + [a_txt] + new[bi:]
    pal_letras += wc([a_txt])
    hechas += 1
    manifest.setdefault("acuerdo_22_letras_a", []).append({"bloque": key, "linea_b": bi + 1, "palabras": wc([a_txt])})
manifest["letras_a_insertadas"] = hechas
manifest["palabras_letras_a"] = pal_letras

# ---------- escritura ----------
sha_after = sha_of(new)
palabras_despues = wc(new)
open(LEY, "wb").write((NL.join(new)).encode("utf-8"))
raw2 = open(LEY, "rb").read()
sha_on = hashlib.sha256(raw2).hexdigest()
assert sha_on == sha_after, "sha en disco no coincide"
manifest.update({"sha256_despues": sha_on, "palabras_despues": palabras_despues,
                 "lineas_despues": len(new),
                 "neto_palabras": palabras_despues - words_before})
json.dump(manifest, open("evidencia/manifiesto_ejecucion_2026-09-03.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("SHA_ANTES:", sha_before)
print("SHA_DESPUES:", sha_on)
print("art15 eliminadas:", pal_art15, "| DF restituidas:", pal_restit, "| letras a):", hechas, pal_letras, "palabras")
print("palabras:", words_before, "->", palabras_despues, "neto:", palabras_despues - words_before)
print("manifiesto: evidencia/manifiesto_ejecucion_2026-09-03.json")
