# Errata acuerdo 37 (acta 2026-09-22): retirada del marcador (Derogado) huérfano en [aveintiuno]
# Cita BOE verificable en el repo: evidencia/boe_consolidado_BOE-A-1986-10499.html — nota del art. 21:
#   «(Derogado). Se deroga por la disposición derogatoria única de la Ley 33/2011, de 4 de octubre.
#    Ref. BOE-A-2011-15623. Se modifica el inciso inicial del apartado 1 por la DA 8.4 de la LO 3/2007,
#    de 22 de marzo. Ref. BOE-A-2007-6115»  — y la nota NO registra derogación de apartado 3 alguno
#    (la única derogación parcial, letra b) del apdo 1, es del art. 20 por LO 1/1990, Ref. BOE-A-1990-2263).
# El marcador cuelga tras «3. El ejercicio de las competencias...», que según el consolidado es el
# apartado 3 del ARTÍCULO VEINTE — artefacto de conversión. El [aveintiuno] fusionado el 22-09 ya
# no contiene el art. 21. Con cita en mano: se retira con manifiesto.
import hashlib, json, sys

PATH = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md'
BAK  = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md.bak-2026-09-23'
data = open(PATH, 'rb').read()

i = data.find('## [aveintiuno]'.encode())
j = data.find('## [aveintidos]'.encode())
seg = data[i:j]
marker = b'          <strong>(Derogado)</strong>\r\n'
n = seg.count(marker)
print('estado: marcadores (Derogado) dentro de [aveintiuno] =', n)
if n == 0:
    print('La errata YA está retirada — no se toca.')
    sys.exit(0)
assert n == 1 and sum(1 for l in seg.split(b'\r\n') if l.strip() == 'Artículo veintiuno'.encode()) == 1, 'estado inesperado, alto'
assert b'La distribucion territorial' in seg or 'distribuci\u00f3n territorial'.encode() in seg, 'alto: no localizo el art. 21'
assert 'El ejercicio de las competencias enumeradas en este art\u00edculo'.encode() in seg, 'alto: no localizo el apdo 3'

# quitar el marcador + la línea en blanco sobrante que lo precede (queda 1 blanco de cierre)
new_seg = seg.replace(b'\r\n' + marker, b'', 1)
new_data = data[:i] + new_seg + data[j:]
assert new_data.count(b'(Derogado)') == data.count(b'(Derogado)') - 1
open(PATH, 'wb').write(new_data)

# verificación final
chk = open(PATH, 'rb').read()
i2 = chk.find('## [aveintiuno]'.encode()); j2 = chk.find('## [aveintidos]'.encode())
assert b'(Derogado)' not in chk[i2:j2]
# el resto del fichero intacto (solo cambió este bloque: prefijo y sufijo byte a byte)
assert chk[:i2] == data[:i] and chk[j2:] == data[j + (len(seg) - len(new_seg)):]
pal = lambda lb: len(lb.decode('utf-8').split())
res = {
  'fecha': '2026-09-23', 'sesion': '15/30',
  'ejecutor': 'Mónica García, Ministra de Sanidad (errata con cita, acuerdo 37 del acta 2026-09-22)',
  'ley': PATH,
  'sha256_fichero_antes': hashlib.sha256(data).hexdigest(),
  'sha256_fichero_despues': hashlib.sha256(chk).hexdigest(),
  'backup': BAK,
  'errata': {
    'bloque': 'aveintiuno',
    'lineas_antes': '301-347', 'lineas_despues': '301-345',
    'palabras_bloque_antes': pal(seg.split(b'\r\n')[0:]) if False else None,
    'detalle': ("Retirado el marcador huérfano '          <strong>(Derogado)</strong>' (línea 347) "
                "que colgaba tras el apartado 3 del bloque. Cita BOE verificable en el repo "
                "(evidencia/boe_consolidado_BOE-A-1986-10499.html): el art. 21 LGS está DEROGADO "
                "íntegramente por la disposición derogatoria única de la Ley 33/2011, de 4 de "
                "octubre (Ref. BOE-A-2011-15623), y su única modificación parcial es el inciso "
                "inicial del apartado 1 (LO 3/2007, DA 8.4, Ref. BOE-A-2007-6115) — sin registro "
                "alguno de derogación de un apartado 3. El párrafo sobre el que cuelga el marcador "
                "('3. El ejercicio de las competencias enumeradas en este artículo se llevará a "
                "cabo bajo la dirección de las autoridades sanitarias...') es, según el mismo "
                "consolidado, el apartado 3 del ARTÍCULO VEINTE (cuya letra b) sí está derogada "
                "por la LO 1/1990, Ref. BOE-A-1990-2263): artefacto de conversión que quedó "
                "descolgado al fusionar el bloque el 22-09 (acuerdo 35). Tras la fusión, el "
                "[aveintiuno] ya no contiene el art. 21: el marcador huérfano no se correspondía "
                "con ningún precepto del bloque y se retira con la cita pedida por el Consejo."),
    'palabras_retiradas': pal(seg) - pal(new_seg),
    'sha256_bloque_antes': hashlib.sha256(seg).hexdigest(),
    'sha256_bloque_despues': hashlib.sha256(new_seg).hexdigest(),
  },
  'verificacion': '0 marcadores dentro de [aveintiuno]; resto del fichero byte a byte intacto (prefijo/sufijo); 1 rótulo del art. 21',
}
res['errata'].pop('palabras_bloque_antes')
json.dump(res, open('ministerios/sanidad/evidencia/manifiesto_errata_aveintiuno_2026-09-23.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('OK errata retirada — palabras retiradas:', res['errata']['palabras_retiradas'])
