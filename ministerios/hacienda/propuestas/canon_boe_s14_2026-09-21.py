import re, html, hashlib

def extrae(path, num):
    t = open(path, encoding='utf-8', errors='replace').read()
    pat = re.compile(r'<h5 class="articulo">\s*Art[íi]culo\s+%d\.\s*(.*?)</h5>' % num, re.S)
    ms = list(pat.finditer(t))
    m = ms[0]
    start = m.end()
    nxt = re.search(r'<h5 class="articulo">', t[start:])
    end = start + nxt.start() if nxt else len(t)
    chunk = t[m.start():end]
    # conservar solo los parrafos de norma (divs con clase parrafo*), descartar aparato editorial
    paras = re.findall(r'<(?:div|p) class="(?:parrafo[_\d]*|articulo)"[^>]*>(.*?)</(?:div|p)>', chunk, re.S)
    out = []
    for p in paras:
        p = re.sub(r'<[^>]+>', '', p)
        p = html.unescape(p).replace('\xa0', ' ')
        p = re.sub(r'\s+', ' ', p).strip()
        if not p:
            continue
        if re.match(r'^(Se (añade|modifica|deroga|añaden|modifica|suprime)|Ref\. BOE|Última actualización|Modificación publicada|Véase|Subir|\[Bloque)', p):
            continue
        out.append(p)
    return out

def wc(s):
    return len(re.findall(r"\S+", s))

HTML = "ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html"
dest = "ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt"
with open(dest, "w", encoding="utf-8") as f:
    for n in (93, 101, 187):
        ps = extrae(HTML, n)
        canon = "\n\n".join(ps)
        h = hashlib.sha256(canon.encode("utf-8")).hexdigest()
        f.write("=" * 90 + "\n## [a%d] — TEXTO CANÓNICO (BOE consolidado archivado, aparato editorial excluido)\npalabras: %d | sha256: %s\n" % (n, wc(canon), h))
        f.write(canon + "\n\n")
        print("[a%d] parrafos: %d | palabras canon: %d | sha: %s" % (n, len(ps), wc(canon), h[:16]))
print("escrito", dest)
