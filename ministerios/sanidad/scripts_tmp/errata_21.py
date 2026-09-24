# Errata [aveintiuno]: ¿a qué artículo pertenece realmente el marcador (Derogado) huérfano?
# El marcador cuelga tras «3. El ejercicio de las competencias enumeradas en este artículo...» (línea 347 del .md)
import re
h = open('ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html', encoding='utf-8', errors='replace').read()
clean = re.sub(r'<[^>]+>', ' ', h)
for ent in [('á','á'),('é','é'),('í','í'),('ó','ó'),('ú','ú'),('ñ','ñ'),('«','«'),('»','»'),('&nbsp;',' ')]:
    clean = clean.replace(ent[0], ent[1])
clean = re.sub(r'\s+', ' ', clean)
k = clean.find('El ejercicio de las competencias enumeradas en este artículo')
print('== contexto del pasaje en el BOE consolidado ==')
print(clean[max(0,k-120):k+420])
# ¿qué dice la sección de notas (Derogado) del art. 20 y 21?
for art in ['veinte', 'veintiuno']:
    k2 = clean.find('Artículo ' + art + ' (')
    print(f'== nota de derogación Artículo {art} ==', clean[k2:k2+320] if k2!=-1 else 'no encontrado')
# ¿en el fichero .md el bloque [aveinte] existe y termina sin marcador?
d = open('ministerios/sanidad/leyes/BOE-A-1986-10499.md','rb').read().decode('utf-8', errors='replace')
i = d.find('## [aveinte]'); j = d.find('## [aveintiuno]')
seg = d[i:j]
print('== ¿[aveinte] contiene "El ejercicio de las competencias"?', 'El ejercicio de las competencias' in seg)
print('== ¿[aveinte] tiene marcador (Derogado)?', '(Derogado)' in seg)
print('== cola de [aveinte] ==', repr(seg[-260:]))
