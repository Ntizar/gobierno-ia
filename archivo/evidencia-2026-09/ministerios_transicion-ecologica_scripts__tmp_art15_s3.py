import re
p = 'C:/Users/d_ant/Projects/gobierno-ia/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md'
lines = open(p, encoding='utf-8').read().split('\n')[379:474]
runs = [(387, 414), (415, 443), (445, 473)]  # líneas 1-based dentro del fichero
for si, (a, b) in enumerate(runs):
    seg = lines[a - 380: b - 380]
    w = sum(len(l.split()) for l in seg if l.strip())
    print(f'cuerpo {si+1} (líneas {a}-{b}): {w} palabras')
# palabras de los rótulos
print('rótulos x3: 8 palabras c/u => 16 de sobra (1 real + 2 duplicadas)')
# dup exactas entre cuerpos (ya sabidas): 1996 palabras en copias literales
# total de sobra si conservamos solo la versión 3 (la más reciente):
total = 0
for si, (a, b) in enumerate(runs):
    seg = lines[a - 380: b - 380]
    w = sum(len(l.split()) for l in seg if l.strip())
    total += w
print('total bloque art.15 (sin rótulos):', total)
v1 = sum(len(l.split()) for l in lines[387-380:414-380] if l.strip())
v2 = sum(len(l.split()) for l in lines[415-380:443-380] if l.strip())
print('ahorro si se conserva solo v3 y se eliminan v1+v2:', v1 + v2)
