# MANIFIESTO VERÍDICO errata [aveintiuno] (acuerdo 37, acta 2026-09-22) — sesión 2026-09-23.
# Lo que pasó de verdad, sin inventar ni un hash:
#  1) Ejecuté apply_errata21_2026-09-23.py: el script ABORTÓ en su propia aserción de estado
#     (contaba los rótulos «Artículo veintiuno» línea a línea y la cabecera ## [aveintiuno] no
#     coincidía literal) y NO modificó el fichero. Verificado después: el marcador (Derogado)
#     sigue en su sitio (l. 347) y el sha del fichero no cambió del estado post-47.
#  2) Comprobación de la cita con las 3 fuentes BOE del repo:
#     - evidencia/boe_texto_plano.txt l.4018-4026 + boe_consolidado html + canon JSON: el marcador
#       (Derogado) es la nota de derogación del PROPIO art. 21 (Ley 33/2011, Ref. BOE-A-2011-15623).
#     - El párrafo «3. El ejercicio de las competencias enumeradas en este artículo se llevará a
#       cabo bajo la dirección de las autoridades sanitarias…» NO EXISTE en las 3 fuentes (0
#       coincidencias tras normalizar acentos/espacios) — es artefacto de conversión; tampoco es
#       citable como «apartado del 20» (el art. 20 del .md, l.285-299, es salud mental).
#  3) Regla del acuerdo 37 («con cita, o no se borra»): la cita verificada dice que NO se borra el
#     marcador. Y el párrafo fantasma no se toca hoy porque requiere propuesta propia del Consejo
#     (retirada de texto sin anclaje BOE), no una errata ajena. ERRATA 37: NO EJECUTADA, con motivo.
import hashlib, json
p = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md'
cur = open(p, 'rb').read()
sha = hashlib.sha256(cur).hexdigest()
assert sha == '92ef137244a82d6406f4a6acae5754e11ed58d3769f1092e9ce1597f42ec3542'
res = {
 'fecha': '2026-09-23', 'sesion': '15/30',
 'acuerdo_37': 'errata marcador (Derogado) huérfano [aveintiuno] — RESUELTO: NO SE BORRA, con cita',
 'sha256_fichero_hoy': sha,
 'backup': 'ministerios/sanidad/leyes/BOE-A-1986-10499.md.bak-2026-09-23',
 'marcadores_derogado_totales': cur.count(b'(Derogado)'),
 'intentos_ejecucion': ('1 intento automatizado, abortado por aserción de seguridad del propio script; '
                        '0 bytes cambiados por esa vía. Ningún manifiesto de retirada: no hubo retirada.'),
 'cita_boe': ('evidencia/boe_texto_plano.txt l.4018-4026 (y boe_consolidado html / canon JSON): '
              '«Artículo veintiuno. (Derogado). Se deroga por la disposición derogatoria única de la '
              'Ley 33/2011, de 4 de octubre. Ref. BOE-A-2011-15623.» → el marcador pertenece al propio '
              'art. 21 y su retirada habría borrado una derogación vigente.'),
 'hallazgo_colateral': ('El párrafo l.340-344 («3. El ejercicio de las competencias…») no aparece en '
                        'ninguna fuente BOE del repo (0 coincidencias normalizadas). Candidato a '
                        'retirada COMO PROPUESTA (propuestas/2026-09-23.md D.2), no como errata.'),
}
json.dump(res, open('ministerios/sanidad/evidencia/manifiesto_errata_aveintiuno_2026-09-23.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('OK manifiesto verídico; sha hoy:', sha[:16])
