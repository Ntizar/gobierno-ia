# ¿Qué dice el BOE CANÓNICO del repo sobre el art. 20/21 LGS y sobre Ley 33/2011?
import json, re
raw = open('data/canonical/BOE-A-1986-10499/2026-08-31.json', encoding='utf-8').read()
print('tam json:', len(raw))
# 1) contexto de los artículos 20/21 en el canónico
for frase in ['salud laboral', 'El ejercicio de las competencias', 'La distribución territorial', 'distribuci\u00f3n territorial']:
    for m in list(re.finditer(re.escape(frase), raw))[:2]:
        k = m.start()
        antes = re.findall(r'Art[íi]culo [a-záéíóúüñ]+', raw[max(0,k-2500):k])
        print(f'>> "{frase}" a {k} | último rótulo antes: {antes[-1] if antes else "ninguno"} | frag: {raw[k:k+110]!r}')
# 2) ¿el canónico guarda notas de vigencia?
for pat in ['33/2011', 'Derogad', '15623']:
    print(f'canónico contiene {pat!r}:', raw.count(pat))
