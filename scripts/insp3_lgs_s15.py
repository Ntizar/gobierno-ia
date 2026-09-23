import re, pathlib
L = pathlib.Path('ministerios/sanidad/leyes/BOE-A-1986-10499.md').read_text(encoding='utf-8').replace('\r\n','\n').split('\n')
idx = [(i, re.match(r'^## \[([^\]]+)\]', l).group(1)) for i,l in enumerate(L) if re.match(r'^## \[([^\]]+)\]', l)]
B = {}
for n,(i,k) in enumerate(idx):
    end = idx[n+1][0] if n+1 < len(idx) else len(L)
    B[k] = (i,end,L[i:end])

for k in ['aveintidos','aveintisiete','asesentayuno','acuarentaytres','atreintaycinco','aveintiuno','acientocinco']:
    i,e,sl = B[k]
    print(f"===== [{k}] l.{i+1}-{e} =====")
    for j,l in enumerate(sl[:26]):
        print(f"{j}|{l}")
    print()

# C.3: parrafo huerfano
frase = "El ejercicio de las competencias enumeradas en este artículo se llevará a cabo bajo la dirección de las autoridades sanitarias"
def norm(s):
    import unicodedata
    s = unicodedata.normalize('NFKD', s.lower())
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', s)).strip()
frags = ['ejercicio de las competencias enumeradas en este articulo se llevara a cabo bajo la direccion']
for p in ['ministerios/sanidad/evidencia/boe_texto_plano.txt','ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html','data/canonical/BOE-A-1986-10499/2026-08-31.json']:
    t = norm(pathlib.Path(p).read_text(encoding='utf-8', errors='replace'))
    print(f"{p}: coincidencias = {sum(t.count(f) for f in frags)}")
