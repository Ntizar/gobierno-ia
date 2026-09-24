# Verificacion de cierre s16: hash de la ley, hashes Auditor de bloques propuestos,
# unicidad de rotulos DF, y cola exacta de cada bloque.
import os
import sys
import io
import hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
LEY = os.path.join(BASE, "ministerios/hacienda/leyes/BOE-A-2003-23186.md")
EVID = os.path.join(BASE, "ministerios/hacienda/evidencia")

raw = open(LEY, "rb").read()
print("LEY sha256:", hashlib.sha256(raw).hexdigest())
txt = raw.decode("utf-8")
for cab in ["Disposición final quinta", "Disposición final sexta", "Disposición final octava"]:
    print("copias en ley de", repr(cab), "=", txt.count(cab))

for s in ["dfquinta", "dfsexta", "dfoctava"]:
    p = os.path.join(EVID, "bloque_propuesto_" + s + "_2026-09-24.txt")
    b = open(p, "rb").read().rstrip(b"\r\n")
    t = b.decode("utf-8")
    w = len(t.split())
    h = hashlib.sha256(b).hexdigest()
    print("PROP", s, "| palabras =", w, "| sha256 =", h)
    print("   linea1:", t.split("\n")[0])
    print("   cola:", repr(t[-60:]))

pv = os.path.join(EVID, "bloque_vivo_dfquinta_2026-09-24.txt")
b = open(pv, "rb").read().rstrip(b"\r\n")
t = b.decode("utf-8")
print("VIVO dfquinta | palabras =", len(t.split()), "| sha256 =", hashlib.sha256(b).hexdigest())
print("   cola:", repr(t[-60:]))
