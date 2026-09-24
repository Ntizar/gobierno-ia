# Ejecución del acuerdo [acuarentaysiete] (aprobado 30-08, acta 2026-08-30, acuerdo 6)
# Deduplicación del art. 47 LGS: 3 rótulos -> 1, copias 1-4 -> 1, apdo 5: se conserva
# la versión reformada (DA 6ª Ley 25/1990) con su marcador (Derogado) (Ley 16/2003, DF 1ª).
import hashlib, json, re, sys

PATH = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md'
BAK  = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md.bak-2026-09-23'

data = open(PATH, 'rb').read()
bak  = open(BAK, 'rb').read()
assert data == bak, 'el fichero no coincide con su .bak (estado inesperado)'

i = data.find('## [acuarentaysiete] Artículo cuarenta y siete\r\n'.encode())
j = data.find('## [acuarentayocho]'.encode())
assert i != -1 and j != -1 and i < j
block = data[i:j]
lines = block.split(b'\r\n')

# Estado antes: comprobación estricta de la forma esperada (NO re-aplicar si ya está limpio)
rotulos = sum(1 for l in lines if l.strip() == 'Artículo cuarenta y siete'.encode())
copia1 = [l for l in lines if l.startswith(b'1. Se crea el Consejo')]
copia5_antigua = [l for l in lines if l.startswith('5. A los efectos previstos'.encode())]
copia5_reformada = [l for l in lines if l.startswith('5. Se crea un Comite'.encode())]
derogados = sum(1 for l in lines if b'<strong>(Derogado)</strong>' in l)
print('ANTES: rótulos sueltos =', rotulos, '| copias del 1. =', len(copia1),
      '| apdo 5 antiguo =', len(copia5_antigua), '| apdo 5 reformado =', len(copia5_reformada),
      '| marcadores Derogado =', derogados)

if rotulos == 1 and len(copia1) == 1 and len(copia5_antigua) == 0:
    print('El bloque YA está deduplicado — no se toca (regla anti-re-aplicación).')
    sys.exit(0)

def words(lb):
    return len(lb.decode('utf-8').split())

before_words = sum(words(l) for l in lines if l.strip())
before_sha = hashlib.sha256(block).hexdigest()

# Construir bloque final: etiqueta ## + 1 rótulo cuerpo + apartados 1-4 (primera copia, idéntica)
# + apartado 5 reformado (el del BOE consolidado vigente hasta la derogación) + (Derogado)
out = [
    lines[0],                                # ## [acuarentaysiete] Artículo cuarenta y siete
    b'',
    b'Art\xc3\xadculo cuarenta y siete',      # Articulo cuarenta y siete
    b'',
    lines[8], b'',                           # 1.
    lines[10], b'',                          # 2.
    lines[12], b'',                          # 3.
    lines[14], b'',                          # Asimismo...
    lines[16], b'',                          # 4.
    lines[30], b'',                          # 5. reformado
    lines[33], b'', b'',                     # <strong>(Derogado)</strong> + 1 línea en blanco de cierre
]
# Sana comprobación de que cogimos las líneas correctas:
assert out[4] == lines[8] and out[4].startswith(b'1. Se crea')
assert out[12] == lines[16] and out[12].startswith(b'4. Ser')
assert out[14] == lines[30] and out[14].startswith(b'5. Se crea un Comite')
assert b'(Derogado)' in out[16]
# Y que NO se pierde ni una letra del apdo 1-4 conservado respecto de la otra copia:
second = [l for l in lines if l.startswith(b'1. Se crea') or l.startswith(b'2. El Consejo') or
          l.startswith(b'3. El Consejo') or l.startswith(b'Asimismo') or l.startswith(b'4. Ser')]
assert len(second) == 10, f'esperaba 2 copias de 5 parrafos, hay {len(second)}'
half = len(second)//2
assert second[:half] == second[half:], 'las dos copias de 1-4 divergen — alto'

new_block = b'\r\n'.join(out)
after_words = sum(words(l) for l in out if l.strip())
after_sha = hashlib.sha256(new_block).hexdigest()

new_data = data[:i] + new_block + data[j:]
assert len(new_data) < len(data)
open(PATH, 'wb').write(new_data)

# Verificación final sobre el fichero escrito
chk = open(PATH, 'rb').read()
ci = chk.find('## [acuarentaysiete]'.encode()); cj = chk.find('## [acuarentayocho]'.encode())
cb = chk[ci:cj]
cl = cb.split(b'\r\n')
r2 = sum(1 for l in cl if l.strip() == b'Art\xc3\xadculo cuarenta y siete')
c1 = sum(1 for l in cl if l.startswith(b'1. Se crea'))
c5a = sum(1 for l in cl if l.startswith('5. A los efectos'.encode()))
c5b = sum(1 for l in cl if l.startswith(b'5. Se crea un Comite'))
dg = sum(1 for l in cl if b'(Derogado)' in l)
print('DESPUÉS: rótulos =', r2, '| copia del 1. =', c1, '| 5 antiguo =', c5a, '| 5 reformado =', c5b, '| Derogado =', dg)
assert (r2, c1, c5a, c5b, dg) == (1, 1, 0, 1, 1), 'verificación final fallida'
# El resto del fichero intacto:
assert chk[:ci] == data[:i] and chk[cj:] == data[j:]

res = {
    'fecha': '2026-09-23',
    'sesion': '15/30',
    'ejecutor': 'Mónica García, Ministra de Sanidad (pase de lista, deuda de ejecución)',
    'acuerdo': 'Acta 2026-08-30, acuerdo 6 — Deduplicación art. 47 (Consejo Interterritorial), aprobado 30-08 y no aplicado hasta hoy',
    'ley': PATH,
    'sha256_fichero_antes': hashlib.sha256(data).hexdigest(),
    'sha256_fichero_despues': hashlib.sha256(chk).hexdigest(),
    'backup': BAK,
    'bloque': {
        'clave': 'acuarentaysiete',
        'lineas_antes': '711-745',
        'lineas_despues': '711-737',
        'palabras_bloque_antes': before_words,
        'palabras_bloque_despues': after_words,
        'palabras_retiradas': before_words - after_words,
        'sha256_bloque_antes': before_sha,
        'sha256_bloque_despues': after_sha,
        'estado_antes': {'rotulos_articulo': rotulos, 'copias_apartados_1_4': 2,
                          'versiones_apartado_5': 2, 'marcadores_derogado': derogados},
        'estado_despues': {'rotulos_articulo': r2, 'copias_apartados_1_4': c1,
                           'versiones_apartado_5': c5b, 'marcadores_derogado': dg},
        'detalle': ('Se eliminan: 2 rótulos «Artículo cuarenta y siete» repetidos; la segunda '
                    'copia completa de los apartados 1-4 (byte a byte idéntica a la primera, '
                    'verificado); y la versión ANTIGUA del apartado 5 («Comité Consultivo ... '
                    'integrado paritariamente por representantes de las organizaciones '
                    'empresariales y sindicales más representativas»), anterior a la reforma '
                    'por la DA 6ª de la Ley 25/1990. Se conserva la redacción reformada del '
                    'apartado 5 con el marcador <strong>(Derogado)</strong> — derogación por '
                    'la DF 1ª de la Ley 16/2003, Ref. BOE-A-2003-10715, según el ejemplar '
                    'consolidado archivado en ministerios/sanidad/evidencia/'),
    },
    'verificacion': ('1 rótulo por bloque, 1 copia de los apartados 1-4, 1 sola versión del '
                     'apartado 5 (la reformada, vigente hasta la derogación) con su marcador; '
                     'resto del fichero byte a byte intacto (assert de prefijos/sufijos)'),
    'fuente_consolidado': 'ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html — «[Bloque 64: #acuarentaysiete] Artículo cuarenta y siete (Derogado). Se deroga por la disposición derogatoria 1 de la Ley 16/2003, de 28 de mayo. Ref. BOE-A-2003-10715. Se modifica el apartado 5 por la disposición adicional 6 de la Ley [25/]1990, de 20 de diciembre. Ref. BOE-A-1990-30938»',
}
json.dump(res, open('ministerios/sanidad/evidencia/manifiesto_acuarentaysiete_2026-09-23.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)
print('PALABRAS BLOQUE: antes', before_words, '-> después', after_words, '| retiradas:', before_words - after_words)
print('OK manifiesto escrito')
