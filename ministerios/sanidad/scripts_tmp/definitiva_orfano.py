# Verificación DEFINITIVA (case-insensitive, espacio normalizado): ¿dónde está
# «El ejercicio de las competencias enumeradas en este artículo se llevará a cabo bajo la
# dirección de las autoridades sanitarias...» en las 3 fuentes BOE del repo?
import re

def norm(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('\u2013', '-').replace('\u2014', '-').replace('\xa0', ' ')
    s = s.replace('«', '"').replace('»', '"')
    return re.sub(r'\s+', ' ', s)

SRC = {
 'plano':  'ministerios/sanidad/evidencia/boe_texto_plano.txt',
 'html':   'ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html',
 'canon':  'data/canonical/BOE-A-1986-10499/2026-08-31.json',
}
frag = norm('El ejercicio de las competencias enumeradas en este artículo se llevará a cabo bajo la dirección de las autoridades sanitarias')
for k, p in SRC.items():
    t = norm(open(p, encoding='utf-8', errors='replace').read())
    hits = [m.start() for m in re.finditer(re.escape(frag), t)]
    print(f"{k}: {len(hits)} coincidencias")
    for pos in hits[:3]:
        print('   ANTES:', t[max(0,pos-240):pos].replace('  ',' ')[-180:])
        print('   EN/HUECO:', t[pos:pos+260])
print()
print("=== ¿El art. 21 original 1986 (plano l.5458+) tiene este párrafo? ventana normalizada de 'Artículo veintiuno' primera aparición: ya comprobada. Ahora 'estrecha coordinación' en cada fuente: ===")
for k, p in SRC.items():
    t = norm(open(p, encoding='utf-8', errors='replace').read())
    n = len(re.findall('estrecha coordinación', t))
    print(f"{k}: 'estrecha coordinación' -> {n}")
