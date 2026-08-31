# Detalle de duplicados de [a271] DA 5a y [a150], sesion 2026-08-31
import re, hashlib
src = open("leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
for aid in ("a271", "a150"):
    b = [x for x in re.split(r'\n(?=## \[a\d+\])', src) if x.startswith(f'## [{aid}]')][0]
    paras = [l.strip() for l in b.split('\n') if l.strip() and len(l.strip()) > 40 and not l.startswith('## [')]
    groups = {}
    for p in paras:
        k = hashlib.sha256(re.sub(r'\s+', ' ', p).encode()).hexdigest()
        groups.setdefault(k, []).append(p)
    print(f"===== {aid} =====")
    for v in groups.values():
        if len(v) > 1:
            print(f"--x{len(v)}: {v[0][:220]}")
    # variantes no literales: lineas con redaccion antigua/nueva del art 150
    if aid == "a150":
        print("--- variantes 'dias' / 'SIX' ---")
        for l in paras:
            if "seis meses" in l or "seis" in l and "días" in l:
                print("*", l[:220])
