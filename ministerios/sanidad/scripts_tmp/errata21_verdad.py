# Verificación real del párrafo «3. El ejercicio de las competencias...» en las FUENTES DEL REPO
import re
# 1) HTML consolidado: normalizar (quita tags, colapsa espacios) y buscar
h = open('ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html', encoding='utf-8', errors='replace').read()
txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))
for frase in ['El ejercicio de las competencias enumeradas en este artículo',
              'actuaciones siguientes', 'estrecha coordinación con las autoridades laborales']:
    idxs = [m.start() for m in re.finditer(re.escape(frase), txt)]
    print(frase, '->', len(idxs), 'ocurrencias en HTML consolidado')
    for ix in idxs[:2]:
        print('   ...', txt[max(0,ix-160):ix+140].replace('  ',' ')[:280])
# 2) ¿el art. 21 original de 1986 tenía párrafos 1/2/3? buscar 'Uno. Corresponde' y letras en el plano
p = open('ministerios/sanidad/evidencia/boe_texto_plano.txt', encoding='utf-8').read()
ptxt = re.sub(r'\s+',' ',p)
for frase in ['El ejercicio de las competencias', 'Corresponde a las Administraciones Públicas, en el ámbito de la salud laboral', 'dirección de las autoridades sanitarias']:
    print('PLANO:', frase, '->', ptxt.count(frase))
# 3) canónico
c = re.sub(r'\s+',' ',open('data/canonical/BOE-A-1986-10499/2026-08-31.json', encoding='utf-8').read())
for frase in ['El ejercicio de las competencias', 'dirección de las autoridades sanitarias', 'La acción de las Administraciones Públicas en la protección']:
    print('CANÓNICO:', frase, '->', c.count(frase))
# 4) en el HTML: qué hay justo antes y después de cada 'La protección, promoción y mejora de la salud laboral' (letra g original) y de '(Derogado)' art 21
for m in list(re.finditer(re.escape('La protección, promoción y mejora de la salud laboral'), txt))[:3]:
    ix = m.start(); print('HTML ventana g):', txt[ix-120:ix+260][:360])
