import hashlib, io, sys, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
LAW = 'leyes/BOE-A-2021-8447.md'
lines = io.open(LAW, encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')
hdrs = [(i, l) for i, l in enumerate(lines) if l.startswith('## [')]
def show(tag):
    pos = next(k for k, (j, l) in enumerate(hdrs) if l.startswith('## [' + tag + ']'))
    start = hdrs[pos][0]
    end = hdrs[pos + 1][0] if pos + 1 < len(hdrs) else len(lines)
    seg = lines[start:end]
    while seg and seg[-1].strip() == '':
        seg.pop()
    text = '\n'.join(seg)
    print('====', tag, 'lineas', start + 1, '-', start + len(seg), '| palabras', len(text.split()),
          '| sha256', hashlib.sha256(text.encode('utf-8')).hexdigest())
    print(text)
    print()
for t in sys.argv[1:]:
    show(t)
