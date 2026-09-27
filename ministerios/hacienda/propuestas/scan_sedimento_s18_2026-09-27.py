# -*- coding: utf-8 -*-
# Sesion 18/30 - scan de sedimento restante por bloque (cabeceras repetidas y parrafos duplicados)
import re, hashlib, json
raw = open('C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
parts = re.split(r'(?m)^(## \[[a-z0-9\-]+\][^\n]*)$', raw)
blocks = {}
for i in range(1, len(parts), 2):
    tag = re.match(r'## \[([a-z0-9\-]+)\]', parts[i]).group(1)
    blocks[tag] = parts[i] + parts[i+1]

def normline(s):
    return re.sub(r'\s+', ' ', s.replace('\u00a0',' ')).strip().lower()

rows = []
for tag, body in blocks.items():
    cab = len(re.findall(r'(?m)^Art[íi]culo \d', body)) + len(re.findall(r'(?m)^(Disposici[oó]n|SECCI|[Cc]ap[íi]TUL|T[íi]TULO)', body))
    paras = [normline(p) for p in body.split('\n\n') if len(normline(p).split()) >= 12]
    seen = {}
    dupw = 0
    for p in paras:
        h = hashlib.sha256(p.encode()).hexdigest()
        if h in seen:
            dupw += len(p.split())
        seen[h] = True
    nh = body.rstrip('\n').split('\n\n')[0]
    pal = len(body.split())
    if dupw > 40 or cab > 1:
        rows.append((tag, pal, cab, dupw))
rows.sort(key=lambda r: -r[3])
print('tag | palabras_bloque | cabeceras | palabras_parrafos_repetidos')
for r in rows[:25]:
    print(r[0], r[1], r[2], r[3])
print('total bloques con sospecha:', len(rows), '| suma pal repetidas:', sum(r[3] for r in rows))
