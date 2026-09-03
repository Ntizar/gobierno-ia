# Aplicar reparacion [dadecimoctava] — SOLO tras mandato expreso del Consejo de Ministros
# de 2026-09-02 (regla aprobada en el acta de 2026-09-01, orden presidencial 02-09:
# "restitucion verificada no autoriza aplicacion anticipada; el mandato cierra el diff").
# Si el Consejo no lo vota esta noche: NO ejecutar. Archivar con constancia.
import re, hashlib, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
SRC = "leyes/BOE-A-2003-23186.md"
SHA_ACTUAL = "574ad589ebb449387923d02ebdc7f42d6c7a2d621c896af8cf6b9290da6f6bdc"   # sha256(norm) del bloque tal y como debe estar en el fichero
def norm(p): return re.sub(r"\s+", " ", p).strip()
txt = open(SRC, encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^(## \[dadecimoctava\][^\n]*\n)(.*?)(?=^## \[)", txt, flags=re.S | re.M)
assert m, "bloque [dadecimoctava] no encontrado"
cur = hashlib.sha256(norm(m.group(2)).encode()).hexdigest()
assert cur == SHA_ACTUAL, f"precondicion fallida: el fichero cambio desde la verificacion ({cur[:12]} != {SHA_ACTUAL[:12]})"
nuevo = open("evidencia/reparacion_DA18_bloque_propuesto_2026-09-02.md", encoding="utf-8").read()
m2 = re.search(r"^## \[dadecimoctava\][^\n]*\n(.*?)$", nuevo, flags=re.S | re.M)
body = m2.group(1)
shutil.copy(SRC, SRC + ".bak-2026-09-02-da18")
out = txt[:m.start()] + m.group(1) + body + txt[m.end():]
open(SRC, "w", encoding="utf-8", newline="\n").write(out)
print("DA18 reparada. Verificacion:", "OK" if hashlib.sha256(norm(body).encode()).hexdigest() == "11c84ad13a5dc5f9b452456bc5fff1bca87e155ba8164ae18e414a03d6fab889" else "FALLO")
