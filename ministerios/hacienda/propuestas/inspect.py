# Inspeccion de bloques: cuenta repeticiones por parrafo
import hashlib, re, json, sys

src = open("leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
blocks = re.split(r'\n(?=## \[)', src)

def inspect(target):
    for b in blocks:
        m = re.match(r'## \[(\w+)\]', b)
        if not m or m.group(1) != target:
            continue
        title = b.split('\n')[0]
        print(f"=== {title} ===")
        paras = [l.strip() for l in b.split('\n') if l.strip() and len(l.strip()) > 40 and not l.strip().startswith('## [')]
        seen = {}
        for p in paras:
            key = hashlib.sha256(re.sub(r'\s+', ' ', p).encode()).hexdigest()
            seen.setdefault(key, [p, 0])
            seen[key][1] += 1
        total_dup = 0
        for p, n in seen.values():
            if n > 1:
                total_dup += (n - 1) * len(p.split())
                print(f"x{n} | {p[:150]}")
        tw = sum(len(p.split()) for p in paras)
        print(f"-- dup_words={total_dup} total_words={tw} ratio={total_dup/tw*100:.0f}% paras={len(paras)}")
        return

for t in sys.argv[1:]:
    inspect(t)
