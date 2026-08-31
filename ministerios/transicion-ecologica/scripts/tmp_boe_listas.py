import re, html
t = open(r'C:/Users/d_ant/AppData/Local/Temp/ley7.html', encoding='utf-8').read()
t = html.unescape(re.sub(r'<[^>]+>', '\n', t))
t = re.sub(r'\n\s*\n+', '\n', t)
lines = [l.strip() for l in t.split('\n') if l.strip()]

# extraer lista de letras por zona alrededor de anclas
anclas = [
    ('art2', 'Principios rectores'),
    ('art3', 'Se establecen los siguientes objetivos mínimos nacionales'),
    ('art4.3', 'revisar al alza los objetivos establecidos'),
    ('art4.4', 'incluirán, al menos, el siguiente contenido'),
    ('art6', 'Entre las referidas acciones se incluirán'),
    ('art13.2', 'podrán prever, entre otras, las siguientes medidas'),
    ('art16.4', 'a través de Puertos del Estado y de las Autoridades Portuarias'),
    ('DF11', 'presentarán una propuesta de reforma del marco normativo en materia de energía'),
]
for name, anc in anclas:
    for i, l in enumerate(lines):
        if anc in l:
            seg = []
            for j in range(i, min(i + 30, len(lines))):
                if re.match(r'^[a-zñ]\) ', lines[j]) or lines[j] == seg and False:
                    seg.append(lines[j])
                elif seg:
                    break
            print(f'== {name} ({len(seg)} letras):')
            for s in seg:
                print('   ', s[:90])
            break
