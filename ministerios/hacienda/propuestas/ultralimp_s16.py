# Ultra-limpieza s16: quita artefactos de enlaces inline del BOE (" ." -> "."),
# recomprime espacio triple, re-hash convencion Auditor.
import re
import sys
import io
import hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
EVID = BASE + "/ministerios/hacienda/evidencia/"


def auditor(t):
    t = t.strip("\n").replace("\r\n", "\n")
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


for slug in ["dfquinta", "dfsexta", "dfoctava"]:
    p = EVID + "bloque_propuesto_" + slug + "_2026-09-24.txt"
    with open(p, encoding="utf-8", newline="") as f:
        t = f.read().replace("\r\n", "\n")
    t = re.sub(r"\s+([.;:,])", r"\1", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    n = len(t.split())
    h = auditor(t)
    print(slug, "| pal", n, "| hash", h)
