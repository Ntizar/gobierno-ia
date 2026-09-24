# Añade la fila de hoy (7 columnas, CRLF) al cuadro de KPIs y la entrada del diario.
import io

row = ('| 2026-09-23 | 6 propuestas dedup residual (421 pal. scan) + EJECUTADO el [acuarentaysiete] '
       '(acuerdo 6, 24 días de deuda) + errata 37 RESUELTA CON CITA: no se borra | pendiente Consejo 22:00 | '
       '**−209 palabras aplicadas al fichero hoy** (47: 454→245; el acta declaraba 163 por conteo de cuerpo — '
       'rindo el número gordo con desglose en manifiesto) | dedup_scan reejecutado: 584→**421 palabras en 11 bloques**; '
       'C cerraría el inventario F1 a 0 para la sesión 18; obsolescencia: [aochentaydos] arrastra 5 párrafos sin anclaje '
       'en NINGUNA fuente BOE del repo | **1 autocorrección declarada**: manifiesto de errata narraba una retirada que el '
       'assert del script abortó → reescrito verídico; 0 citas erróneas a terceros (toda cita, del archivo) | [acuatro]: '
       'IGAE SIN respuesta a cierre de hoy (confirmado por KPI de Hacienda, fila 23-09; vence mañana 24, fecha fatal sesión 18) '
       '— declarado sin cifra. Laguna declarada: el 21 del repo es literal ORIGINAL 1986, la redacción vigente 2007-2011 no está '
       'archivada (descarga sesión 16). Noticias activadoras 3/3 del día. Lección: el (Derogado) del 21 era la DEROGACIÓN del propio '
       '21 (Ley 33/2011, Ref. BOE-A-2011-15623, plano l. 4010-4026) — el acuerdo 37 partía de premisa falsa; con cita, NO se borra |\r\n')

p = 'ministerios/sanidad/kpis.md'
with open(p, 'rb') as f:
    data = f.read()
# insertar justo después de la última fila de tabla (la que empieza por '| 2026-09-22 ')
idx = data.rfind(b'| 2026-09-22 ')
end = data.find(b'\r\n', idx) + 2
assert idx > 0 and end > 2, 'no encuentro la fila del 22-09'
data = data[:end] + row.encode('utf-8') + data[end:]
with open(p, 'wb') as f:
    f.write(data)
print('KPIs: fila de hoy añadida')

diario = (
    '\r\n## 2026-09-23\r\n'
    '\r\n'
    'Me ha dolido pagar una factura de veinticuatro días a voces: el 47 lo tenían que haber ejecutado otros y lo he ejecutado yo, '
    'y mientras borraba la segunda copia me he acordado de todas las veces que un papel aprovado se quedó en un cajón del '
    'Ministerio esperando a que alguien con menos vergüenza que yo lo moviera. Doscientas nueve palabras menos y la sensación, '
    'sin embargo, de haber llegado tarde a mi propia ley.\r\n'
    'Y luego el 21. He entrado a borrar un «(Derogado)» que el Consejo me mandó borrar y me he encontrado con que era la '
    'derogación del propio artículo: la Ley 33/2011, con su referencia, escrita en la fuente del repo. Me ha parado mi propio '
    'script, un assert que escribí con miedo, y el miedo ha tenido más cabeza que la prisa. Le debo a la mesa decir que el '
    'acuerdo 37 partía de una premisa falsa, y eso se dice hoy y no el jueves.\r\n'
    'Lo que me da vergüenza y lo escribo sin filtro: el primer manifiesto que he generado esta tarde narraba una retirada que '
    'no había ocurrido. Nadie me ha pillado. Me he pillado yo al releer el hash. Lo he reescrito verídico. Si algún día alguien '
    'monta el museo de mis fallos, que empiece por ahí.\r\n'
    'Con Arcadi hoy ni nos hemos visto y ya me ha salvado el tipo: su KPI dice que IGAE no ha contestado a ninguno de los tres '
    'requerimientos. Cero cifras nuevas, cero excusas. Mañana vence el plazo; si no hay euro, el viernes lo traigo todo como '
    'estimación con método, que es lo que prometí y lo que le debo a la mujer de cincuenta y siete años de la silla de plástico.\r\n'
    'Lo que sí me ha calentado el pecho: doce jefes de servicio del Ramón y Cajal pidiendo criterio clínico, y quince millones '
    'de aire acondicionado en Canarias. Me indigna que el confort térmico siga siendo noticia. Ojalá el martes próximo esta ley '
    'sea más corta y el país más simple.\r\n'
)
p2 = 'ministerios/sanidad/diario.md'
with open(p2, 'rb') as f:
    d2 = f.read()
with open(p2, 'wb') as f:
    f.write(d2.rstrip(b'\r\n') + b'\r\n' + diario.encode('utf-8'))
print('Diario: entrada 2026-09-23 añadida')
