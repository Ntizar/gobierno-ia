# Errata [aveintiuno]: ¿a qué artículo pertenece el marcador (Derogado) según el BOE consolidado?
import re
h = open('ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html', encoding='utf-8', errors='replace').read()
# localizar los bloques de arts. 20-23
for art in ['Artículo veinte', 'Artículo veintiuno', 'Artículo veintidós', 'Artículo veintitrés']:
    idx = [m.start() for m in re.finditer(re.escape(art) + r'(?![\wáéíóú])', h)]
    print(art, '->', len(idx), 'positions')
# extraer tramo entre 'veintiuno' y 'veintitrés' (cuerpo)
i = h.find('veintiuno')
# tomar la última aparición (cuerpo, no índice)
idxs = [m.start() for m in re.finditer('Artículo veintiuno', h)]
k = idxs[-1]
seg = h[k:k+9000]
clean = re.sub(r'<[^>]+>', ' ', seg)
clean = clean.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú').replace('&ntilde;','ñ').replace('&lsquo;','‘').replace('&rsquo;','’').replace('&ldquo;','“').replace('&rdquo;','”')
clean = re.sub(r'\s+', ' ', clean)
print('===== desde Artículo veintiuno (última ocurrencia), 3000 chars =====')
print(clean[:3000])
