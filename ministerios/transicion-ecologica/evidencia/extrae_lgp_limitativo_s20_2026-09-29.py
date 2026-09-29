import re, html
p = 'C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html'
t = open(p, encoding='utf-8', errors='ignore').read()
t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
t = re.sub(r'[ \t\xa0]+', ' ', t)
for pat in ['carácter limitativo', 'limitativo', 'Artículo 34.', 'Artículo 38.', 'Artículo 47.', 'Artículo 42.']:
    ms = [m.start() for m in re.finditer(re.escape(pat), t)]
    print('===', pat, 'ocurrencias:', len(ms))
    for i in ms[:3]:
        print('   ...', t[i-160:i+300].strip().replace('\n', ' '))
        print('   ---')
