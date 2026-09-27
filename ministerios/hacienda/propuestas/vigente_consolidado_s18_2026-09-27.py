# -*- coding: utf-8 -*-
# Sesion 18/30 - extraer del consolidado BOE el texto VIGENTE de arts. 68, 81 y 112
# (el canon JSON tiene letras a) caidas por su propia extraccion: hay que ir al ejemplar)
import re, os, json, hashlib, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
raw = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
# trocear en nodos de texto
txt = re.sub(r'<br\s*/?>', '\n', raw)
txt = re.sub(r'</p>', '\n', txt)
txt = re.sub(r'<[^>]+>', '', txt)
lines = [re.sub(r'\s+', ' ', l).strip() for l in txt.split('\n')]
lines = [l for l in lines if l]

def versiones(artno, title):
    # un "articulo" empieza en la linea 'Artículo NNN. Titulo...'
    idx = [i for i, l in enumerate(lines) if l.startswith(f'Artículo {artno}.') and title.lower() in l.lower()]
    out = []
    for k, i in enumerate(idx):
        j = idx[k+1] if k+1 < len(idx) else len(lines)
        # cortar en el siguiente articulo cualquiera
        for m in range(i+1, j):
            if re.match(r'Artículo \d+\.', lines[m]) and m > i:
                j = m; break
        out.append(lines[i:j])
    return out

canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
def norm(s):
    s = unicodedata.normalize('NFC', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

for artno, title, tag in [(68, 'Interrupción', 'a68'), (81, 'Medidas cautelares', 'a81'), (112, 'comparecencia', 'a112')]:
    vs = versiones(artno, title)
    print(f'== art {artno}: {len(vs)} versiones en consolidado ==')
    ncanon = norm(arts[tag]['texto'])
    for k, v in enumerate(vs):
        body = ' '.join(v[1:])
        nb = norm(body)
        letras = len(re.findall(r'(?m)(^|\s)a\)\s+[A-ZÁÉÍÓÚ]', ' \n'.join(v[1:])))
        # ¿es vigente? el consolidado marca tras cada version: buscar nota "Vigente" o "Ref." tras ella
        print(f'  v{k+1}: {len(body.split())} pal | a) x{letras} | canon_substring={ncanon in nb} | arranca: {v[1][:70] if len(v)>1 else ""}')
    # la version que pasa canon_substring
    ok = [k for k, v in enumerate(vs) if ncanon in norm(' '.join(v[1:]))]
    print('  versiones que contienen el canon JSON:', ok)
