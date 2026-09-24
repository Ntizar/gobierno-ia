# Hashes y texto exacto de los bloques VIVOS dfsexta/dfoctava (convencion Auditor:
# bytes del bloque completo con su cabecera, LF, sin saltos finales).
import os
import sys
import io
import hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
EVID = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia"

for s in ["dfsexta", "dfoctava"]:
    p = os.path.join(EVID, "bloque_vivo_" + s + "_2026-09-24.txt")
    raw = open(p, "rb").read().replace(b"\r\n", b"\n").rstrip(b"\n")
    t = raw.decode("utf-8")
    print(s, "| palabras =", len(t.split()), "| sha256 =", hashlib.sha256(raw).hexdigest())
    print(t)
    print("-----")
