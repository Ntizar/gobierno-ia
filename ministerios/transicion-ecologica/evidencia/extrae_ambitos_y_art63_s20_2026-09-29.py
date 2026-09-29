import re, html, json

# 1) lista de ambitos del NdP oficial archivado en el repo
p = 'C:/Users/d_ant/Projects/gobierno-ia/ministerios/transicion-ecologica/evidencia/agua_miteco_reserva_hidrica_60-3_2026-09-28.html'
t = open(p, encoding='utf-8', errors='ignore').read()
tx = re.sub(r'<[^>]+>', '\n', t)
tx = html.unescape(tx)
tx = re.sub(r'[ \t\xa0]+', ' ', tx)
lines = [l.strip() for l in tx.split('\n') if l.strip()]

i = None
for k, l in enumerate(lines):
    if 'al 60,3' in l and 'española' not in l.lower():
        i = k
if i is not None:
    for l in lines[i:i+40]:
        print(repr(l))
print('=== art 63 LGP ===')
p2 = 'C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html'
t2 = open(p2, encoding='utf-8', errors='ignore').read()
t2 = html.unescape(re.sub(r'<[^>]+>', ' ', t2))
t2 = re.sub(r'[ \t\xa0]+', ' ', t2)
j = t2.find('Artículo 63. Competencias')
print(t2[j:j+1400].strip())
