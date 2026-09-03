# Imprimir todo el sumario BOE del dia (texto plano) para localizar bloque HACIENDA y su titulo
import re, io, sys, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open(r"C:\Users\d_ant\AppData\Local\Temp\boe_0902.html", encoding="utf-8", errors="replace").read()
txt = H.unescape(re.sub(r"<[^>]+>", "\n", raw))
lines = [l.strip() for l in txt.split("\n") if l.strip()]
# localizar la seccion de HACIENDA
idxs = [i for i, l in enumerate(lines) if "HACIENDA" in l.upper()]
print("lineas con HACIENDA:", idxs)
for i in idxs:
    print("--- contexto", i, "---")
    print("\n".join(lines[i:i+18]))
