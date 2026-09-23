import re, pathlib, collections

P = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md'
t = pathlib.Path(P).read_text(encoding='utf-8').replace('\r\n', '\n')
lines = t.split('\n')
idx = [(i, re.match(r'^## \[([^\]]+)\]', l).group(1)) for i, l in enumerate(lines) if re.match(r'^## \[([^\]]+)\]', l)]
B = {}
for n, (i, k) in enumerate(idx):
    end = idx[n+1][0] if n+1 < len(idx) else len(lines)
    B[k] = (i, end, lines[i:end])

def paras(sl):
    out, cur = [], []
    for l in sl:
        if l.strip() == '':
            if cur: out.append(cur); cur = []
        else:
            cur.append(l)
    if cur: out.append(cur)
    return out

for k in ['aonce','aochentaycuatro','atreintayseis','aciento','aochentaydos','acientocinco']:
    i, e, sl = B[k]
    print(f"########## [{k}] l.{i+1}-{e} ##########")
    ps = paras(sl)
    cnt = collections.Counter('\n'.join(p).strip() for p in ps)
    for j, p in enumerate(ps):
        txt = '\n'.join(p)
        dup = '<<<DUP' if cnt['\n'.join(p).strip()] > 1 and len('\n'.join(p).strip())>3 else ''
        print(f"  [p{j}]{dup} {txt[:150]}")
    print()
