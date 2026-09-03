# Titulos de la seccion MINISTERIO DE HACIENDA en el sumario BOE del 02-09-2026
import re, io, sys, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open(r"C:/Users/d_ant/AppData/Local/Temp/boe_0902.html", encoding="utf-8", errors="replace").read()
# localizar bloque HACIENDA entre dos <h2> de ministerio
mins = [(m.start(), H.unescape(m.group(1))) for m in re.finditer(r">\s*(MINISTERIO DE [^<]+)\s*<", raw)]
for k, (pos, name) in enumerate(mins):
    end = mins[k+1][0] if k+1 < len(mins) else len(raw)
    if "HACIENDA" in name:
        sec = raw[pos:end]
        for m in re.finditer(r'href="(/boe/dias/2026/09/02/pdfs/([A-Z0-9\-]+)\.pdf)"[^>]*>\s*([^<]{5,260})', sec):
            print(m.group(2), "|", H.unescape(m.group(3)).strip()[:200])
