# Verificación definitiva de la errata [aveintiuno]: ¿a qué artículo pertenece el marcador (Derogado)?
import re, html
h = open('ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html', encoding='utf-8', errors='replace').read()
clean = html.unescape(re.sub(r'<[^>]+>', ' ', h))
clean = re.sub(r'\s+', ' ', clean)
# 1) dónde cae "El ejercicio de las competencias..." en el cuerpo consolidado: ¿art. 20 o 21?
for m in re.finditer('El ejercicio de las competencias enumeradas', clean):
    k = m.start()
    antes = clean[max(0,k-3000):k]
    arts = re.findall(r'Art[íi]culo (veinti[úu]no|veinte|veintid[óo]s)', antes)
    print('OCURRENCIA en', k, '-> último artículo citado antes:', arts[-2:] if arts else 'ninguno')
    print('   tras:', clean[k:k+240])
# 2) notas oficiales: derogaciones de art. 20 y 21
for art in ['Artículo veinte', 'Artículo veintiuno']:
    for m in re.finditer(re.escape(art) + r' \(Derogad', clean):
        k = m.start()
        print('NOTA', art, ':', clean[k:k+200])
# 3) ¿qué es el art. 21 en el cuerpo del consolidado y qué es el art. 20?
k20 = clean.rfind('Artículo veinte.', 0, clean.find('El ejercicio de las competencias enumeradas'))
print('== art. 20 cuerpo ==', clean[k20:k20+200])
k21 = clean.rfind('Artículo veintiuno', 0, clean.find('El ejercicio de las competencias enumeradas'))
print('== art. 21 cuerpo ==', clean[k21:k21+260])
