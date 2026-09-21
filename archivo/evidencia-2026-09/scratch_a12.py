import re
p = r'ministerios/hacienda/leyes/BOE-A-2003-23186.md'
raw = open(p, 'rb').read()
print("CRLF:", raw.count(b"\r\n"), "LF-only:", raw.count(b"\n") - raw.count(b"\r\n"))
txt = raw.decode('utf8')
m = re.search(r'^## \[a12\].*?(?=^## \[a13\])', txt, re.S | re.M)
blk = m.group(0)
paras = [x for x in blk.split('\n\n') if x.strip()]
for i, pp in enumerate(paras):
    print(i, len(pp.split()), repr(pp[:75]))
print("TOTAL WORDS a12:", len(blk.split()))
a = open(r'ministerios/hacienda/agenda.md', 'rb').read()
print("agenda CRLF:", a.count(b"\r\n"), "LF-only:", a.count(b"\n") - a.count(b"\r\n"), "tail:", repr(a[-15:]))
k = open(r'ministerios/hacienda/kpis.md', 'rb').read()
print("kpis CRLF:", k.count(b"\r\n"), "LF-only:", k.count(b"\n") - k.count(b"\r\n"))
