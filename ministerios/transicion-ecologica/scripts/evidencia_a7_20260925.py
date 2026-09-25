# Evidencia 2026-09-25: bloque propuesto [a7] (apartado 2 fechado) + actualización SHA256SUMS
import hashlib, io, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
LAW = 'leyes/BOE-A-2021-8447.md'

PROP_A7 = """## [a7] Artículo 7

Artículo 7. Generación eléctrica en dominio público hidráulico.

1. Al objeto de cumplir los objetivos en materia de energías renovables establecidos en esta ley, las nuevas concesiones que se otorguen, de acuerdo con lo establecido en la legislación de aguas sobre el dominio público hidráulico para la generación de energía eléctrica, tendrán como prioridad el apoyo a la integración de las tecnologías renovables en el sistema eléctrico. A tal fin, se promoverán, en particular, las centrales hidroeléctricas reversibles, siempre que cumplan con los objetivos ambientales de las masas de agua y los regímenes de caudales ecológicos fijados en los planes hidrológicos de cuenca y sean compatibles con los derechos otorgados a terceros, con la gestión eficiente del recurso y su protección ambiental.

2. El Ministerio para la Transición Ecológica y el Reto Demográfico aprobará antes del 31 de diciembre de 2027, mediante real decreto, las condiciones técnicas para llevar a cabo el bombeo, almacenamiento y turbinado para maximizar la integración de energías renovables, previo informe de la Comisión Nacional de los Mercados y la Competencia y de la Red Eléctrica de España, con una referencia cuantificada de capacidad de almacenamiento flexible en servicio antes del 31 de diciembre de 2030. Dichas condiciones tendrán en cuenta lo dispuesto en el apartado anterior. Su seguimiento se publicará antes del 30 de junio de cada año, sin generar una nueva remisión parlamentaria.

3. Al objeto de avanzar en nuevos desarrollos tecnológicos en materia de energías renovables y contribuir al logro de los objetivos previstos en la ley se promoverá, para usos propios del ciclo urbano del agua, el aprovechamiento para la generación eléctrica de los fluyentes de los sistemas de abastecimiento y saneamiento urbanos, siempre condicionado al cumplimiento de los objetivos de dichos sistemas cuando sea técnica y económicamente viable."""

def h(x):
    return hashlib.sha256(x.encode('utf-8')).hexdigest()

fp = 'evidencia/bloque_propuesto_a7_2026-09-25.txt'
io.open(fp, 'w', encoding='utf-8', newline='\n').write(PROP_A7)
vivo = io.open('evidencia/bloque_vivo_a7_2026-09-25.txt', 'w', encoding='utf-8', newline='\n')
lines = io.open(LAW, encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')
seg = lines[278:287]
while seg and seg[-1].strip() == '':
    seg.pop()
vivo.write('\n'.join(seg))
vivo.close()
vivo_txt = '\n'.join(seg)
print('a7 vivo:', len(vivo_txt.split()), 'pal', h(vivo_txt))
print('a7 prop:', len(PROP_A7.split()), 'pal', h(PROP_A7))

# reescribir SHA256SUMS con los 3 bloques
raw = 'ce0c010b9d000f0f088f55e33af44510c2460c65b6557606eef940037d52e336'
entries = []
for tag in ['a7', 'da-9', 'a1-12']:
    v = io.open(f'evidencia/bloque_vivo_{tag}_2026-09-25.txt', encoding='utf-8', newline='').read().replace('\r\n','\n')
    p = io.open(f'evidencia/bloque_propuesto_{tag}_2026-09-25.txt', encoding='utf-8', newline='').read().replace('\r\n','\n')
    entries.append(f'{h(v)}  evidencia/bloque_vivo_{tag}_2026-09-25.txt')
    entries.append(f'{h(p)}  evidencia/bloque_propuesto_{tag}_2026-09-25.txt')
io.open('evidencia/SHA256SUMS_2026-09-25.txt', 'w', encoding='utf-8', newline='\n').write(
    f'# hash RAW del fichero (el que verifica el Auditor): {raw}  leyes/BOE-A-2021-8447.md\n'
    f'# ley intacta: 26.873 palabras, 71 bloques, sha256 (LF-normalizado) 18923a93ec2b629bb78698a81ad270216c41ded03aa8b83409f8264faf1a3516\n'
    + '\n'.join(entries) + '\n')
print('SHA256SUMS_2026-09-25.txt reescrito con 3 bloques')
