import re, pathlib

L = pathlib.Path('ministerios/sanidad/leyes/BOE-A-1986-10499.md').read_text(encoding='utf-8').replace('\r\n','\n').split('\n')
idx = [(i, re.match(r'^## \[([^\]]+)\]', l).group(1)) for i,l in enumerate(L) if re.match(r'^## \[([^\]]+)\]', l)]
B = {}
for n,(i,k) in enumerate(idx):
    end = idx[n+1][0] if n+1 < len(idx) else len(L)
    B[k] = (i,end,L[i:end])

C = pathlib.Path('ministerios/sanidad/evidencia/boe_texto_plano.txt').read_text(encoding='utf-8').replace('\r\n','\n').split('\n')

def canon(tag, n=30):
    for i,l in enumerate(C):
        if f'#{tag}]' in l:
            return '\n'.join(C[i:i+n])
    return 'NO ENCONTRADO'

for k,tag in [('aonce','aonce'),('aochentaycuatro','aochentaycuatro'),('aciento','aciento')]:
    i,e,sl = B[k]
    print(f"=========== REPO [{k}] l.{i+1}-{e} ===========")
    for j,l in enumerate(sl): print(f"{j}|{l}")
    print(f"----------- CANON {tag} -----------")
    print(canon(tag))
    print()
