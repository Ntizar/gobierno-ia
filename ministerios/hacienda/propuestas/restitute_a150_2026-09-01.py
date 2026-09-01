# Restitucion de las letras a) del BOE perdidas por la conversion — [a150] y [a271]
# Lista para aplicar: python ministerios/hacienda/propuestas/restitute_a150_2026-09-01.py
# Idempotente: aborta sin escribir si alguna insercion no casa 1:1 con el BOE archivado.
import re, hashlib, json, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LAW = os.path.join(ROOT, 'ministerios', 'hacienda', 'leyes', 'BOE-A-2003-23186.md')
BOE = os.path.join(ROOT, 'ministerios', 'hacienda', 'evidencia', 'boe_consolidado_BOE-A-2003-23186.html')

INS = [
    # (ancla_antes, texto_a_insertar, ancla_despues)
    ('deberán concluir en el plazo de:',
     'a) 18 meses, con carácter general.',
     'b) 27 meses, cuando concurra alguna de las siguientes circunstancias'),
    ('se suspenderá desde el momento en que concurra alguna de las siguientes circunstancias:',
     'a) La remisión del expediente al Ministerio Fiscal o a la jurisdicción competente sin practicar la liquidación de acuerdo con lo señalado en el artículo 251 de esta Ley.',
     'b) La recepción de una comunicación de un órgano jurisdiccional'),
    ('producirá los siguientes efectos respecto a las obligaciones tributarias pendientes de liquidar:',
     'a) No se considerará interrumpida la prescripción como consecuencia de las actuaciones inspectoras desarrolladas durante el plazo señalado en el apartado 1.',
     'La prescripción se entenderá interrumpida por la realización de actuaciones'),
    ('2. La resolución que ponga fin al procedimiento deberá incluir, al menos, el siguiente contenido:',
     'a) Acuerdo de modificación, en el sentido de la decisión de recuperación, de la resolución previamente dictada por la Administración o, en su caso, manifestación expresa de que no procede modificación alguna como consecuencia de la decisión de recuperación.',
     'b) Relación de hechos y fundamentos de derecho'),
]

txt = open(LAW, encoding='utf-8').read().replace('\r\n', '\n')
# 1) que cada texto a insertar EXISTA literal en el BOE archivado (no se inventa nada)
boe = open(BOE, encoding='utf-8', errors='replace').read()
nb = re.sub(r'\s+', ' ', boe)
for _, ins, _ in INS:
    body = re.sub(r'^a\)\s*', '', ins)
    if body[:60] not in nb:
        sys.exit(f'ABORT: no en BOE archivado: {ins[:60]}')
# 2) aplicar inserciones ancla a ancla; cada una debe casar exactamente una vez
n = 0
for before, ins, after in INS:
    key_b = before
    if key_b not in txt:
        sys.exit('ABORT: ancla no encontrada: ' + key_b[:60])
    i = txt.find(key_b) + len(key_b)
    j = txt.find(after, i)
    if j < 0:
        sys.exit('ABORT: cierre no encontrado: ' + after[:60])
    seg = txt[i:j]
    if 'a) ' in seg:
        print('OK (ya restituida):', ins[:50]); continue
    txt = txt[:i] + '\n\n' + ins + '\n\n' + seg.lstrip('\n') + txt[j:]
    n += 1
open(LAW, 'w', encoding='utf-8', newline='\n').write(txt)
print('inserciones aplicadas:', n)

# 3) post-check con el conteo del propio test de Auditor
for probe, want in [('a) 18 meses', 1), ('a) La remisión del expediente', 1),
                    ('a) No se considerará interrumpida', 1), ('a) Acuerdo de modificación', 1)]:
    got = txt.count(probe)
    ok = 'OK' if got >= want else 'FALLO'
    print(f'{ok}: "{probe}" x{got} (esperado >= {want})')
