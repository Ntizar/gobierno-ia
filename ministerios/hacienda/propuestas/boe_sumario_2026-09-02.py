# Localizar en el sumario BOE 02-09-2026 la Resolucion de Subsecretaria (libre designacion) y su PDF
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open(r"C:/Users/d_ant/AppData/Local/Temp/boe_0902.html", encoding="utf-8", errors="replace").read()
i = raw.find("MINISTERIO DE HACIENDA")
j = raw.find("MINISTERIO DE INCLUSI", i)
sec = raw[i:j]
# pares de (id BOE, href pdf) junto a titulos
for m in re.finditer(r'href="(/boe/dias/2026/09/02/pdfs/([A-Z0-9\-]+)\.pdf)"[^>]*>([^<]{5,300})', sec):
    print(m.group(2), "|", m.group(3)[:160])
