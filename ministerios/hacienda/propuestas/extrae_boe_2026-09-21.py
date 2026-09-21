# -*- coding: utf-8 -*-
"""Extrae de los HTML del BOE consolidado el texto de un articulo concreto.
Uso: python extrae_boe_2026-09-21.py <num_articulo> [ruta_html]
"""
import re, sys, html, unicodedata

def extrae(path, num):
    t = open(path, encoding='utf-8', errors='replace').read()
    # localizar el h5 del articulo
    pat = re.compile(r'<h5 class="articulo">\s*Art[íi]culo\s+%d\.\s*(.*?)</h5>' % num, re.S)
    ms = list(pat.finditer(t))
    out = []
    for m in ms:
        start = m.end()
        nxt = re.search(r'<h5 class="articulo">', t[start:])
        end = start + nxt.start() if nxt else len(t)
        chunk = t[m.start():end]
        # limpiar
        chunk = re.sub(r'<script.*?</script>', '', chunk, flags=re.S)
        chunk = re.sub(r'<form.*?</form>', '', chunk, flags=re.S)
        chunk = re.sub(r'<[^>]+>', '\n', chunk)
        chunk = html.unescape(chunk)
        chunk = chunk.replace('\xa0', ' ')
        lines = [l.strip() for l in chunk.split('\n')]
        lines = [l for l in lines if l]
        out.append('\n'.join(lines))
    return out

if __name__ == '__main__':
    num = int(sys.argv[1])
    path = sys.argv[2] if len(sys.argv) > 2 else 'boe_consolidado_BOE-A-2003-23186.html'
    res = extrae(path, num)
    print('### ocurrencias:', len(res))
    for i, r in enumerate(res, 1):
        print('===== BLOQUE %d (chars %d) =====' % (i, len(r)))
        print(r)
