# Titulos normativos del sumario BOE 02-09 (bloque MINISTERIO DE HACIENDA)
import re, io, sys, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open(r"C:\Users\d_ant\AppData\Local\Temp\boe_0902.html", encoding="utf-8", errors="replace").read()
# localizar el bloque de HACIENDA
i = raw.find("MINISTERIO DE HACIENDA")
j = raw.find("MINISTERIO DE", i+10)
seg = raw[i: j if j>0 else i+12000]
# los titulos suelen estar en <span class="titulo"> o justo antes del enlace pdf
for m in re.finditer(r'titulo[^>]*>(.*?)</[^>]+>|<h3[^>]*>(.*?)</h3>', seg, flags=re.S|re.I):
    t = m.group(1) or m.group(2)
    t = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t))).strip()
    if t:
        print("T:", t[:300])
