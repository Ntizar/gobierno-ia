import re, html, sys
src = open("ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html", encoding="utf-8").read()
# bloques por encabezado de articulo
partes = re.split(r'(<h5 class="articulo">)', src)
arts = {}
for i in range(1, len(partes), 2):
    chunk = partes[i] + (partes[i+1] if i+1 < len(partes) else "")
    m = re.match(r'<h5 class="articulo">(.*?)</h5>', chunk, re.S)
    if not m: continue
    titulo = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
    cuerpo = re.sub(r'<[^>]+>', ' ', chunk)
    cuerpo = html.unescape(cuerpo)
    cuerpo = re.sub(r'[ \t]+', ' ', cuerpo)
    cuerpo = re.sub(r'\n\s*\n+', '\n', cuerpo).strip()
    n = re.match(r'Artículo (\d+)', titulo)
    if n: arts.setdefault(n.group(1), (titulo, cuerpo))
for a in ["42","46","47","50","52","61","62","63"]:
    if a in arts:
        t, c = arts[a]
        print("="*20, t, "="*20)
        print(c[:2600])
        print()
    else:
        print("!! no encontrado art", a)
