import re, html
p = 'C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html'
t = open(p, encoding='utf-8', errors='ignore').read()
t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
t = re.sub(r'[ \t\xa0]+', ' ', t)
for key in ['El carácter limitativo y vinculante', 'Artículo 46.', 'Artículo 27.']:
    for m in re.finditer(re.escape(key), t):
        i = m.start()
        prev = [x for x in re.finditer(r'Artículo \d+\. [A-ZÁÉÍÓÚ][^.]{0,70}\.', t[:i])]
        cab = prev[-1].group(0) if prev else '(sin cabecera previa)'
        print('>>> KEY:', key)
        print('   artículo contenedor:', cab)
        print('   texto:', t[i:i+420].strip().replace('\n', ' ')[:420])
        print()
