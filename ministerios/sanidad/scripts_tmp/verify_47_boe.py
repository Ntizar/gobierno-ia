# Verifico el art. 47 contra el BOE consolidado archivado (html + texto plano)
import re
h = open('ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html', encoding='utf-8', errors='replace').read()
t = open('ministerios/sanidad/evidencia/boe_texto_plano.txt', encoding='utf-8', errors='replace').read()

def show(name, txt, needle, span=1800):
    idx = [m.start() for m in re.finditer(re.escape(needle), txt)]
    print(name, 'occurrences of', repr(needle), '->', len(idx))
    return idx

for needle in ['Artículo cuarenta y siete', 'Consejo Interterritorial', 'Comité Consultivo', 'Comite Consultivo', '(Derogado)', 'asociaciones de consumidores']:
    show('HTML', h, needle)
    show('TXT', t, needle)

# extraer sección art 47 del html: buscar el último 'Artículo cuarenta y siete' y limpiar tags
i = h.rfind('Artículo cuarenta y siete')
seg = h[i:i+6000]
clean = re.sub(r'<[^>]+>', '', seg)
clean = re.sub(r'\s+', ' ', clean)
print('=== HTML art47 raw (from last heading, 1600 chars) ===')
print(clean[:1600])

j = t.find('Artículo cuarenta y siete')
print('=== TXT art47 (from first heading, 1800 chars) ===')
print(t[j:j+1800])
