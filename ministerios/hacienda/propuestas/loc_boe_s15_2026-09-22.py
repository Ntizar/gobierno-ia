# -*- coding: utf-8 -*-
"""Extrae el texto canónico BOE de la DA undécima y la DA vigésima del HTML
consolidado archivado (evidencia/boe_consolidado_BOE-A-2003-23186.html),
descartando aparato editorial, y lo guarda en evidencia/ con sha256.
Además: diff de párrafos contra los bloques vivos del repo (squash)."""
import io, sys, re, hashlib, html
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

src = "ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html"
raw = open(src, encoding="utf-8", errors="replace").read()
print("HTML bytes:", len(raw))

# localizar la zona de las DAs undécima y vigésima
def find_span(pattern_start, pattern_end):
    m = re.search(pattern_start, raw)
    if not m:
        return None
    i = m.start()
    me = re.search(pattern_end, raw[i:])
    j = i + (me.start() if me else 60000)
    return raw[i:j]

# El BOE usa "disposicionadicional" en ids o "Undécima" en títulos; probamos ambos
seg = find_span(r"und[ée]cima(?!</)", r"duod[ée]cima")
print("span DA11 encontrado:", bool(seg), "len:", len(seg) if seg else 0)
seg20 = find_span(r"vig[ée]cima(?!</)", r"vig[ée]sim[oa] segunda|vig[ée]simaop|un[ée]sima(?=\")")
# fallback más simple: buscar los encabezados por texto
idxs = [m.start() for m in re.finditer(r"(?i)disposici[óo]n adicional (und[ée]cima|duod[ée]cima|decimoquinta|decimosexta|decimos[ée]ptima|vig[ée]cima|vig[ée]sima una|vig[ée]simoprimera|vig[ée]simosegunda)\b", raw)]
print("hits de títulos DA:", len(idxs))
for i in idxs[:40]:
    snippet = re.sub(r"<[^>]+>", " ", raw[i:i+90])
    snippet = re.sub(r"\s+", " ", html.unescape(snippet))
    print(i, "|", snippet[:80])
