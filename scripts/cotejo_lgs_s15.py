import re, pathlib, difflib, json

L = pathlib.Path('ministerios/sanidad/leyes/BOE-A-1986-10499.md').read_text(encoding='utf-8').replace('\r\n','\n').split('\n')
idx = [(i, re.match(r'^## \[([^\]]+)\]', l).group(1)) for i,l in enumerate(L) if re.match(r'^## \[([^\]]+)\]', l)]
B = {}
for n,(i,k) in enumerate(idx):
    end = idx[n+1][0] if n+1 < len(idx) else len(L)
    B[k] = (i,end,L[i:end])

C = pathlib.Path('ministerios/sanidad/evidencia/boe_texto_plano.txt').read_text(encoding='utf-8').replace('\r\n','\n').split('\n')
marks = [(i, re.search(r'#([a-z0-9]+)\]', l).group(1)) for i,l in enumerate(C) if re.search(r'\[Bloque \d+: #[a-z0-9]+\]', l)]
CM = {}
for n,(i,k) in enumerate(marks):
    end = marks[n+1][0] if n+1 < len(marks) else len(C)
    CM[k] = C[i+1:end]

APARATO = ('Se modifica','Se deroga','Se convierten','Subir','Última actualización','Seleccionar redacción','Texto original','Se añade','Se declara','Se introduce')
def cuerpo(sl):
    out=[]
    for l in sl:
        t=l.strip()
        if not t: continue
        if t.startswith(APARATO): break
        if re.match(r'^\[?Bloque \d+', t): continue
        out.append(t)
    return out

objetivo = ['aonce','aveintiuno','aveintidos','aveintisiete','atreintaycinco','atreintayseis',
            'acuarentaytres','asesentayuno','aochentaydos','aochentaycuatro','aciento','acientocinco']
res = {}
for k in objetivo:
    if k not in CM:
        print(f"### [{k}] SIN CANON"); continue
    r = cuerpo(B[k][2]); c = cuerpo(CM[k])
    if r == c:
        print(f"### [{k}] IDENTICO al canon ({len(r)} lineas)")
        res[k] = 'identico'
    else:
        print(f"### [{k}] DIFIERE  repo={len(r)} lineas  canon={len(c)} lineas")
        d = list(difflib.unified_diff(c, r, 'canon', 'repo', lineterm='', n=0))
        for l in d[:40]:
            print('   ', l[:170])
        res[k] = 'difiere'
    print()
