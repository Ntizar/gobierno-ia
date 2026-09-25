# Evidencia 2026-09-25: bloques vivos y propuestos de [da-9] y [a1-12], LF sin saltos finales
import hashlib, io, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
LAW = 'leyes/BOE-A-2021-8447.md'

PROP_DA9 = """## [da-9] Disposición adicional novena

Disposición adicional novena. Plan de reducción de consumo energético en la Administración General del Estado.

El Instituto para la Diversificación y Ahorro de la Energía (IDAE), dependiente del Ministerio para la Transición Ecológica y el Reto Demográfico, presentará antes del 31 de diciembre de 2027 un plan con el objetivo de que centros consumidores de energía, pertenecientes a la Administración General del Estado, reduzcan su consumo de energía en el año 2030, en consonancia con la «Estrategia a largo plazo para la rehabilitación energética en el sector de la edificación en España» y el «Plan Nacional Integrado de Energía y Clima 2021-2030», mediante la realización de medidas de ahorro y eficiencia energética.

El plan fijará una senda cuantificada de reducción expresada en gigavatios hora y en euros de factura evitada, y será aprobado por resolución de la Presidencia del IDAE antes del 31 de marzo de 2028. Su seguimiento se publicará antes del 30 de junio de cada año en la sede electrónica del Ministerio para la Transición Ecológica y el Reto Demográfico, sin generar una nueva remisión parlamentaria. El plazo inicial de un año desde la entrada en vigor venció el 22 de mayo de 2022 sin que conste en el expediente de esta ley la presentación del plan."""

PROP_A112 = """## [a1-12] Artículo 15 bis

Artículo 15 bis. Planificación, despliegue e instalación de infraestructura de recarga del vehículo eléctrico.

1. El Gobierno, a propuesta de la Ministra para la Transición Ecológica y el Reto Demográfico, aprobará antes del 31 de diciembre de 2027 un Plan estatal para el despliegue de la infraestructura pública de recarga del vehículo eléctrico con el fin de impulsar y acelerar la descarbonización del sector del transporte a través de la electrificación del transporte por carretera. El plan abordará las necesidades de despliegue de infraestructura pública de recarga, especialmente en aquellas áreas del país donde la iniciativa privada no proporcione las infraestructuras adecuadas, ya sea para vehículos ligeros o para las necesidades específicas de los vehículos pesados, y recogerá las medidas regulatorias, financieras, o de otro tipo que pudieran ser adecuadas para favorecer este despliegue. Dicho Plan se regirá por lo establecido en el Reglamento (UE) 2023/1804 del Parlamento Europeo y del Consejo de 13 de septiembre de 2023, relativo a la implantación de una infraestructura para los combustibles alternativos y por el que se deroga la Directiva 2014/94/UE y el correspondiente Marco de Acción Nacional para el desarrollo del mercado por lo que respecta a los combustibles alternativos en el sector del transporte y la implantación de la infraestructura correspondiente. Así mismo, deberá tener en cuenta lo previsto en el Plan Nacional Integrado de Energía y Clima y sus últimas revisiones. Durante el proceso de elaboración del citado Plan estatal se solicitará informe, no vinculante, al Grupo de Trabajo para el despliegue de la infraestructura de recarga (GTIRVE).

2. El Plan fijará una senda cuantificada de puntos de recarga de acceso público hasta 2030, con desglose entre vehículos ligeros y pesados, y su seguimiento corresponderá a la Dirección General de Energía, que publicará antes del 30 de junio de cada año un informe de ejecución, expresado en número de puntos de recarga en servicio y en megavatios de potencia instalada, con desglose por comunidad autónoma, sin generar una nueva remisión parlamentaria. El mandato de este apartado 1 carecía de plazo desde la entrada en vigor de la ley el 22 de mayo de 2021, sin que conste en el expediente la aprobación del Plan estatal."""

def get_block(tag):
    lines = io.open(LAW, encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')
    hdrs = [(i, l) for i, l in enumerate(lines) if l.startswith('## [')]
    pos = next(k for k, (j, l) in enumerate(hdrs) if l.startswith('## [' + tag + ']'))
    start = hdrs[pos][0]
    end = hdrs[pos + 1][0] if pos + 1 < len(hdrs) else len(lines)
    seg = lines[start:end]
    while seg and seg[-1].strip() == '':
        seg.pop()
    return '\n'.join(seg)

def h(x):
    return hashlib.sha256(x.encode('utf-8')).hexdigest()

out = []
for tag, prop in [('da-9', PROP_DA9), ('a1-12', PROP_A112)]:
    vivo = get_block(tag)
    fv = f'evidencia/bloque_vivo_{tag}_2026-09-25.txt'
    fp = f'evidencia/bloque_propuesto_{tag}_2026-09-25.txt'
    io.open(fv, 'w', encoding='utf-8', newline='\n').write(vivo)
    io.open(fp, 'w', encoding='utf-8', newline='\n').write(prop)
    out.append((tag, len(vivo.split()), h(vivo), len(prop.split()), h(prop)))

law_hash = h(io.open(LAW, encoding='utf-8', newline='').read().replace('\r\n', '\n'))
sums = [f'{law_hash}  leyes/BOE-A-2021-8447.md (L7 completa, 26.873 palabras, 71 bloques)']
for tag, *_ in out:
    sums.append(f'{h(io.open(f"evidencia/bloque_vivo_{tag}_2026-09-25.txt", encoding="utf-8", newline="").read().replace(chr(13)+chr(10), chr(10)))}  evidencia/bloque_vivo_{tag}_2026-09-25.txt')
    sums.append(f'{h(io.open(f"evidencia/bloque_propuesto_{tag}_2026-09-25.txt", encoding="utf-8", newline="").read().replace(chr(13)+chr(10), chr(10)))}  evidencia/bloque_propuesto_{tag}_2026-09-25.txt')
io.open('evidencia/SHA256SUMS_2026-09-25.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(sums) + '\n')

for tag, wv, hv, wp, hp in out:
    print(f'{tag}: vivo {wv} pal sha {hv}')
    print(f'{tag}: prop {wp} pal sha {hp} delta {wp - wv:+d}')
print('L7 sha256:', law_hash)
