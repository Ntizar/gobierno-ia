# -*- coding: utf-8 -*-
# Sesion 18/30 - dos comprobaciones finales:
# 1) [a150]: los 2 casos F1 re-localizados como pendientes, ¿estan realmente ausentes del vivo?
# 2) letras a) vigentes en el consolidado vs canon JSON, por candidato a dedupe
import re, os, json, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()
vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())
cons_raw = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
cons = norm(re.sub(r'<[^>]+>', ' ', cons_raw))
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}

print('1) [a150]:')
f = norm('b) los ingresos realizados desde el inicio del procedimiento hasta la finalización del plazo de ingreso')
print('   fragmento ausente del vivo:', f not in vivo)
print('   fragmento en consolidado:', f in cons)
f2 = norm('los ingresos realizados desde el inicio del procedimiento')
print('   variante corta en vivo:', f2 in vivo)
i = cons.find(f2)
print('   ctx consolidado:', cons[i-60:i+180] if i>=0 else 'NO')

print('2) letras a) del consolidado por articulo, y si viajan en el canon JSON:')
for tag, artno in [('a81', 81), ('a68', 68), ('a112', 112), ('a233', 233), ('a199', 199), ('a65', 65), ('a26', 26), ('a29', 29)]:
    ncanon = norm(arts[tag]['texto'])
    # letra a) del apartado mas cargado del consolidado: buscamos patron "en:\n\na)" -> 'en: a)'
    # tomamos las 3 primeras ocurrencias de ' a)' seguidas de 40+ chars y preguntamos si estan en el canon
    holes = []
    for m in re.finditer(r'a\) ([a-záéíóúñ]{3}.{20,90}?)(?:\.\s|\s\)|,)', cons):
        frag = m.group(0)
        if frag in ncanon: continue
        # ¿pertenece al articulo? ventana: ±2500 chars alrededor
        pos = m.start()
        near_art = re.findall(r'artículo (\d+)\b', cons[max(0,pos-2500):pos])
        if near_art and int(near_art[-1]) == artno:
            holes.append(frag[:70])
    print(f'   [{tag}] letras a) del consolidado cerca del art. {artno} ausentes del canon: {len(set(holes))}')
    for h in list(dict.fromkeys(holes))[:3]:
        print('      ·', h)
