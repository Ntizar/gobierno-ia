# Verificacion final s16: cleanup artefactos HTML, re-hash convencion Auditor,
# copia unica por rotulo, huella vivo vs prop, sha256 ley al cierre.
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
EVID = BASE + "/ministerios/hacienda/evidencia/"

def auditor(t):
    return hashlib.sha256(t.strip("\n").replace("\r\n", "\n").encode("utf-8")).hexdigest()

WS = re.compile(r"\S+")

for slug in ["dfquinta", "dfsexta", "dfoctava"]:
    p = EVID + "bloque_propuesto_" + slug + "_2026-09-24.txt"
    t = open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    t = re.sub(r"\s+([,;:])", r"\1", t)
    t = t.replace("\n\n\n", "\n\n")
    open(p, "w", encoding="utf-8", newline="\n").write(t)
    v = open(EVID + "bloque_vivo_" + slug + "_2026-09-24.txt", encoding="utf-8", newline="").read()
    print(slug)
    print("  vivo:", len(WS.findall(v)), "pal", auditor(v))
    print("  prop:", len(WS.findall(t)), "pal", auditor(t))

# copia unica por rotulo en la ley
raw = open(BASE + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8", newline="").read()
for slug in ["dfquinta", "dfsexta", "dfoctava"]:
    n = raw.count("## [" + slug + "]")
    print("copias", slug, "=", n)
open(BASE + "/ministerios/hacienda/evidencia/SHA256SUMS_s16_cierre_2026-09-24.txt", "w", encoding="utf-8", newline="\n").write(
    auditor(raw) + "  leyes/BOE-A-2003-23186.md (completo, sin normalizar: " +
    hashlib.sha256(raw.encode("utf-8")).hexdigest() + ")\n")
print("sha256 crudo ley:", hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16])
