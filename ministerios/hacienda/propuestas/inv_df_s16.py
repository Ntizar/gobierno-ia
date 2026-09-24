# Inventario DF completo s16: estado vivo de TODAS las disposiciones finales.
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
raw = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8", newline="").read()

# todas las etiquetas de bloque df*
labels = re.findall(r"^## \[(df[a-z]+)\]", raw, flags=re.M)
print("etiquetas df:", labels)

parts = re.split(r"(?m)^## \[", raw)
for p in parts[1:]:
    lab = p.split("]")[0]
    if not lab.startswith("df"):
        continue
    nl = p.find("\n")
    body = p[nl+1:] if nl >= 0 else ""
    words = len(body.split())
    print(lab, "| palabras:", words, "| truncado:", body.rstrip().endswith(":"))
