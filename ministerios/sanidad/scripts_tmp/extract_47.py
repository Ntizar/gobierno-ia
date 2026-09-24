# Extraigo del HTML consolidado la redacción completa del art. 47 (bloque de cuerpo, no el de notas)
import re
h = open('ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html', encoding='utf-8', errors='replace').read()
idx = [m.start() for m in re.finditer('Artículo cuarenta y siete', h)]
print('positions:', idx)
for k, i in enumerate(idx):
    seg = h[i:i+4500]
    clean = re.sub(r'<[^>]+>', ' ', seg)
    clean = re.sub(r'&aacute;|&eacute;|&iacute;|&oacute;|&uacute;', lambda m: {'&aacute;':'á','&eacute;':'é','&iacute;':'í','&oacute;':'ó','&uacute;':'ú'}[m.group(0)], clean)
    clean = re.sub(r'\s+', ' ', clean)
    print(f'----- occurrence {k} -----')
    print(clean[:2200])
    print()
