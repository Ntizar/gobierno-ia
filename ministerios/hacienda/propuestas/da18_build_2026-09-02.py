# Reparacion DA18: construir bloque propuesto (titulo + 6 parrafos legales del BOE vigente),
# diff unificado, hashes y script de aplicacion listo (NO se ejecuta sin mandato del Consejo).
import re, io, sys, json, hashlib, difflib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def norm(p): return re.sub(r"\s+", " ", p).strip()
def wc(s): return len(s.split())
def shaN(s): return hashlib.sha256(norm(s).encode()).hexdigest()
def shaC(s): return hashlib.sha256(s.encode()).hexdigest()

boe = json.load(open("../evidencia/da18_boe_full_2026-09-02.json", encoding="utf-8"))
legales = [p["text"].strip() for p in boe if p["class"] in ("parrafo", "parrafo_2")]
assert len(legales) == 6, f"esperaba 6 parrafos legales, hay {len(legales)}"

txt = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^(## \[dadecimoctava\][^\n]*\n)(.*?)(?=^## \[)", txt, flags=re.S | re.M)
head, old_body = m.group(1), m.group(2)
title_line = "Disposición adicional decimoctava. Obligación de información sobre bienes y derechos situados en el extranjero."
new_body = title_line + "\n\n" + "\n\n".join(legales) + "\n"

old_pars = [p for p in re.split(r"\n\s*\n", old_body) if norm(p)]
new_pars = [title_line] + legales

print("=== CIFRAS ===")
print(f"bloque actual: {len(old_pars)} parrafos | {wc(old_body)} palabras")
print(f"bloque propuesto: {len(new_pars)} parrafos | {wc(new_body)} palabras")
print(f"delta: {wc(new_body)-wc(old_body)} palabras ({100*(wc(new_body)-wc(old_body))/wc(old_body):.1f}%)")
sup = [p for p in old_pars if shaN(p) not in {shaN(x) for x in new_pars}]
rest = [p for p in new_pars if shaN(p) not in {shaN(x) for x in old_pars}]
print(f"parrafos suprimidos (sin traza BOE): {len(sup)} | {sum(wc(p) for p in sup)} palabras")
print(f"parrafos restituidos/vers. vigente: {len(rest)} | {sum(wc(p) for p in rest)} palabras")
print(f"sha256 actual   norm: {shaN(old_body)}")
print(f"sha256 propuesto norm: {shaN(new_body)}")

# fragmento con el bloque propuesto, para el acta
with open("../evidencia/reparacion_DA18_bloque_propuesto_2026-09-02.md", "w", encoding="utf-8") as f:
    f.write("<!-- BLOQUE PROPUESTO PARA [dadecimoctava] — verificado contra BOE consolidado\n")
    f.write("     archivado 2026-09-01 (sha256 b29db001...) y descargado 2026-09-02 (sha256 a2f3fe1f...),\n")
    f.write("     contenido identico en ambos. Firma: Arcadi España, 2026-09-02. -->\n\n")
    f.write(head + new_body)

# diff unificado (lineas no vacias) para lectura en sala
old_l = [l for l in old_body.split("\n")]
new_l = new_body.split("\n")
ud = difflib.unified_diff(old_l, new_l, fromfile="leyes/BOE-A-2003-23186.md [dadecimoctava] ACTUAL",
                          tofile="[dadecimoctava] PROPUESTO (BOE vigente)", lineterm="")
with open("../evidencia/diff_reparacion_DA18_2026-09-02.md", "w", encoding="utf-8") as f:
    f.write("# Diff de reparacion de [dadecimoctava] — Ley 58/2003 (BOE-A-2003-23186)\n")
    f.write(f"# Generado 2026-09-02. Actual: {len(old_pars)} parrafos / {wc(old_body)} palabras. ")
    f.write(f"Propuesto: {len(new_pars)} parrafos / {wc(new_body)} palabras. Delta: {wc(new_body)-wc(old_body)}.\n")
    f.write("# sha256(norm) actual: " + shaN(old_body) + "\n")
    f.write("# sha256(norm) propuesto: " + shaN(new_body) + "\n\n")
    f.write("\n".join(ud) + "\n")

# script de aplicacion, listo para ejecutar SOLO con mandato del Consejo
ap = '''# Aplicar reparacion [dadecimoctava] — SOLO tras mandato expreso del Consejo de Ministros
# de 2026-09-02 (regla aprobada en el acta de 2026-09-01, orden presidencial 02-09:
# "restitucion verificada no autoriza aplicacion anticipada; el mandato cierra el diff").
# Si el Consejo no lo vota esta noche: NO ejecutar. Archivar con constancia.
import re, hashlib, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SRC = "leyes/BOE-A-2003-23186.md"
SHA_ACTUAL = "%(sha_actual)s"   # sha256(norm) del bloque tal y como debe estar en el fichero
def norm(p): return re.sub(r"\\s+", " ", p).strip()
txt = open(SRC, encoding="utf-8").read().replace("\\r\\n", "\\n")
m = re.search(r"^(## \\[dadecimoctava\\][^\\n]*\\n)(.*?)(?=^## \\[)", txt, flags=re.S | re.M)
assert m, "bloque [dadecimoctava] no encontrado"
cur = hashlib.sha256(norm(m.group(2)).encode()).hexdigest()
assert cur == SHA_ACTUAL, f"precondicion fallida: el fichero cambio desde la verificacion ({cur[:12]} != {SHA_ACTUAL[:12]})"
nuevo = open("evidencia/reparacion_DA18_bloque_propuesto_2026-09-02.md", encoding="utf-8").read()
m2 = re.search(r"^## \\[dadecimoctava\\][^\\n]*\\n(.*?)$", nuevo, flags=re.S | re.M)
body = m2.group(1)
shutil.copy(SRC, SRC + ".bak-2026-09-02-da18")
out = txt[:m.start()] + m.group(1) + body + txt[m.end():]
open(SRC, "w", encoding="utf-8", newline="\\n").write(out)
print("DA18 reparada. Verificacion:", "OK" if hashlib.sha256(norm(body).encode()).hexdigest() == "%(sha_prop)s" else "FALLO")
''' % {"sha_actual": shaN(old_body), "sha_prop": shaN(new_body)}
open("apply_da18_2026-09-02.py", "w", encoding="utf-8").write(ap)
print("\nEscritos: evidencia/reparacion_DA18_bloque_propuesto_2026-09-02.md, evidencia/diff_reparacion_DA18_2026-09-02.md, propuestas/apply_da18_2026-09-02.py")
