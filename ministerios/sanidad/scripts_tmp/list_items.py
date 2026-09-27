import re, sys
h = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
items = re.findall(r'<h3[^>]*>\s*<a href="([^"]+)"[^>]*>([^<]+)</a>', h)
for u, t in items[:20]:
    print(t.strip()[:110], '|', u[:110])
times = re.findall(r'(\d\d:\d\d)h[^\n]{0,20}', h)
print('HORAS EN PORTADA:', times[:10])
