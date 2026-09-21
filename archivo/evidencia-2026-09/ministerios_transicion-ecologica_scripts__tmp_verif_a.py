import re, html
h = open(r'C:/Users/d_ant/AppData/Local/Temp/ley7.html', encoding='utf-8').read()
h = html.unescape(re.sub(r'<[^>]+>', '\n', h))
h = re.sub(r'\n\s*\n+', '\n', h)
hl = [l.strip() for l in h.split('\n') if l.strip()]

repo = open(r'C:/Users/d_ant/Projects/gobierno-ia/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md', encoding='utf-8').read().split('\n')
faltan = []
for i, l in enumerate(repo):
    if l.strip().startswith('b) '):
        prev = '\n'.join(repo[max(0, i-5):i])
        if not re.search(r'^a\) ', prev, re.M):
            faltan.append(i + 1)
print('listas con a) ausente en repo:', len(faltan), faltan)

# para cada una, buscar la letra a) correspondiente en el BOE: la a) que precede a esa b) en hl
ok, no = 0, []
idx_map = {}
# indexar letras b) del BOE
for n in faltan:
    blinea = repo[n-1].strip()[:60]
    cand = [j for j, x in enumerate(hl) if x.startswith('b) ') and x[3:60].strip() == blinea[3:60].strip()]
    if not cand:
        no.append((n, blinea))
        continue
    j = cand[0]
    # buscar la a) inmediatamente anterior
    for k in range(j - 1, max(0, j - 4), -1):
        if hl[k].startswith('a) '):
            print(f'repo L{n}: BOE a) = {hl[k][:95]}')
            ok += 1
            break
    else:
        no.append((n, blinea))
print('verificadas contra BOE:', ok, '| no encontradas:', len(no))
for x in no:
    print('SIN MATCH:', x)
