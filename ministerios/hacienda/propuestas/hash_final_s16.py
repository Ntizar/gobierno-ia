# Hashes definitivos s16: normaliza los 6 ficheros de evidencia a LF exactos
# (bytes hasheados == bytes en disco), sin saltos finales, y verifica que el
# bloque VIVO coincide con lo que esta escrito en la ley (contencion literal).
import os
import sys
import io
import hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
EVID = os.path.join(BASE, "ministerios/hacienda/evidencia")
LEY = os.path.join(BASE, "ministerios/hacienda/leyes/BOE-A-2003-23186.md")

ley = open(LEY, "rb").read().replace(b"\r\n", b"\n")
print("LEY (LF) sha256:", hashlib.sha256(ley).hexdigest())

for s in ["dfquinta", "dfsexta", "dfoctava"]:
    for kind in ["vivo", "propuesto"]:
        p = os.path.join(EVID, "bloque_%s_%s_2026-09-24.txt" % (kind, s))
        b = open(p, "rb").read().replace(b"\r\n", b"\n").rstrip(b"\n")
        open(p, "wb").write(b)
        t = b.decode("utf-8")
        inside = b in ley
        print("%s %s | pal=%d | sha256=%s | en_ley=%s" % (
            kind, s, len(t.split()), hashlib.sha256(b).hexdigest(), inside))
