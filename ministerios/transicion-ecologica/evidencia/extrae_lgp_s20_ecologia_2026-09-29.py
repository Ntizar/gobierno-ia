import re, html

p = 'C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html'
t = open(p, encoding='utf-8', errors='ignore').read()
t = re.sub(r'<[^>]+>', ' ', t)
t = html.unescape(t)
t = re.sub(r'[ \t\xa0]+', ' ', t)
t = re.sub(r'\n+', '\n', t)

heads = ['Artículo 52. Transferencias de crédito',
         'Artículo 61. ',
         'Artículo 62. Competencias',
         'Artículo 63. Competencias']
for h in heads:
    i = t.find(h)
    print('#### BUSCANDO:', h, '=> idx', i)
    if i >= 0:
        print(t[i:i+1800].strip())
        print('-----')
# bloque de apartados 52.x, 62.1, 63.1
for pat in [r'52\.2\.[^\n]{0,600}', r'62\.1\.[^\n]{0,600}', r'63\.1\.[^\n]{0,600}', r'52\.1\.[^\n]{0,600}']:
    for m in re.finditer(pat, t):
        print('>>>', m.group(0)[:700].strip())
        print()
