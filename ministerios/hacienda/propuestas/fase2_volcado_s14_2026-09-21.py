import re, html

def extrae(path, num):
    t = open(path, encoding='utf-8', errors='replace').read()
    pat = re.compile(r'<h5 class="articulo">\s*Art[íi]culo\s+%d\.\s*(.*?)</h5>' % num, re.S)
    ms = list(pat.finditer(t))
    out = []
    for m in ms:
        start = m.end()
        nxt = re.search(r'<h5 class="articulo">', t[start:])
        end = start + nxt.start() if nxt else len(t)
        chunk = t[m.start():end]
        chunk = re.sub(r'<script.*?</script>', '', chunk, flags=re.S)
        chunk = re.sub(r'<form.*?</form>', '', chunk, flags=re.S)
        chunk = re.sub(r'<[^>]+>', '\n', chunk)
        chunk = html.unescape(chunk).replace('\xa0', ' ')
        lines = [l.strip() for l in chunk.split('\n')]
        out.append([l for l in lines if l])
    return out

boe = {}
for n in (93, 101, 187):
    r = extrae("ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", n)
    boe[n] = r[0] if r else []

# fichero repo, bloques
with open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8") as f:
    txt = f.read()
parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", txt)
repo = {}
for i in range(1, len(parts), 2):
    lab = re.match(r"## (\[[a-z0-9\-]+\])", parts[i]).group(1)
    repo[lab] = parts[i + 1]

def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-záéíóúüñ\s]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()

def squashed(s):
    return norm(s).replace(" ", "")

with open("ministerios/hacienda/evidencia/volcado_fase2_2026-09-21.txt", "w", encoding="utf-8") as out:
    for n, lab in ((93, "[a93]"), (101, "[a101]"), (187, "[a187]")):
        rb = repo[lab]
        out.write("#" * 90 + "\n" + lab + " — PÁRRAFOS DEL BOE FALTANTES EN EL BLOQUE DEL REPO\n")
        for line in boe[n]:
            if line.startswith("Artículo"):
                continue
            if squashed(line) in squashed(rb):
                continue
            out.write("[FALTA] " + line + "\n")
        out.write("\n" + "=" * 90 + "\n" + lab + " — CUERPO ACTUAL DEL REPO\n")
        out.write(rb + "\n")
print("escrito ministerios/hacienda/evidencia/volcado_fase2_2026-09-21.txt")
