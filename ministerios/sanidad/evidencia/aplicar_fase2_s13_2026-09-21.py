# -*- coding: utf-8 -*-
"""
Fase 2 — sesión 13/30 (2026-09-21). Aplicación de los 4 diffs APROBADOS por el
Consejo que seguían sin aplicar sobre leyes/BOE-A-1986-10499.md (Ley 14/1986, LGS):

  [atres]      art. 3  — dedup: conservar la copia CON el apartado 3.4 (igualdad).
  [aseis]      art. 6  — dedup: conservar la copia CON el apartado 6.2 (igualdad).
  [aveinte]    art. 20 — 'legalidad pura': sustituir el párrafo TRUNCADO del BOE por
                         el texto COMPLETO aprobado por el Congreso (BOCG 09/04/1986)
                         y eliminar la nota de advertencia.
  [adieciseis] art. 16 — contenido NUEVO aprobado (sesión 11/30): añadir los apartados
                         sobre trazabilidad de listas de espera copiados LITERALMENTE
                         de propuestas/2026-09-17.md.

Reglas aplicadas:
 - copia de seguridad .bak-2026-09-21 ANTES de tocar.
 - sha256 del fichero antes/después (cadena de custodia).
 - NINGÚN texto se teclea sin verificar: cada párrafo destino se ASSERTA contra la
   fuente (el propio bloque origen, el BOE consolidado archivado o la propuesta
   aprobada del repo). Si un literal no cuadra, el script ABORTA.
 - se modifican SOLO los 4 bloques objetivo (verificación por segmentos).
"""
import re, hashlib, json, shutil, os

BASE = os.path.dirname(os.path.abspath(__file__))            # .../sanidad/evidencia
SAN  = os.path.dirname(BASE)                                 # .../sanidad
LEY  = os.path.join(SAN, 'leyes', 'BOE-A-1986-10499.md')
BAK  = LEY + '.bak-2026-09-21'
BOE  = os.path.join(BASE, 'boe_texto_plano.txt')
P17  = os.path.join(SAN, 'propuestas', '2026-09-17.md')

def sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def sha_file(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def norm(p):
    p = p.replace('\u00a0', ' ').replace('"', '"').replace('"', '"')
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', p)).strip()

raw = open(LEY, encoding='utf-8').read()
assert '\r\n' not in raw, 'fichero con CRLF inesperado'
lines = raw.splitlines()

def block_range(ls, bid):
    starts = [i for i, l in enumerate(ls) if re.match(r'^## \[' + bid + r'\]', l)]
    assert len(starts) == 1, f'{bid}: {len(starts)} cabeceras'
    s = starts[0]; e = len(ls)
    for j in range(s + 1, len(ls)):
        if re.match(r'^## \[a\w+\]', ls[j]):
            e = j; break
    return s, e

def paras(lns): return [l.strip() for l in lns if l.strip()]
def wc(lns): return sum(len(p.split()) for p in paras(lns))

def mk(header, rot, cuerpo):
    """bloque con el formato del repo: cabecera, blanco, rótulo, blanco, párrafos
       separados por blanco, y blanco final (antes de la siguiente cabecera)."""
    out = [header, '', rot, '']
    for p in cuerpo:
        out += [p, '']
    return out

manifiesto = {
    'fecha': '2026-09-21', 'sesion': '13/30', 'ley': 'BOE-A-1986-10499.md',
    'sha256_fichero_antes': sha_file(LEY), 'backup': os.path.basename(BAK),
}

# =============================================================== [atres]
s3, e3 = block_range(lines, 'atres')
b3 = lines[s3:e3]; p3 = paras(b3)
rot3 = 'Artículo tres'
P3_A = '1. Los medios y actuaciones del sistema sanitario estarán orientados prioritariamente a la promoción de la salud y a la prevención de las enfermedades.'
P3_B = '2. La asistencia sanitaria pública se extenderá a toda la población española. El acceso y las prestaciones sanitarias se realizarán en condiciones de igualdad efectiva.'
P3_C = '3. La política de salud estará orientada a la superación de los desequilibrios territoriales y sociales.'
P3_D = '4. Las políticas, estrategias y programas de salud integrarán activamente en sus objetivos y actuaciones el principio de igualdad entre mujeres y hombres, evitando que, por sus diferencias físicas o por los estereotipos sociales asociados, se produzcan discriminaciones entre ellos en los objetivos y actuaciones sanitarias.'
assert p3.count(rot3) == 2, f'[atres] rótulos: {p3.count(rot3)}'
for txt in (P3_A, P3_B, P3_C):
    assert p3.count(txt) == 2, f'[atres] {txt[:40]} x{p3.count(txt)}'
assert p3.count(P3_D) == 1, '[atres] 3.4 no único'
after3 = mk('## [atres] Artículo tres', rot3, [P3_A, P3_B, P3_C, P3_D])
assert all(p in p3 for p in [rot3, P3_A, P3_B, P3_C, P3_D]), '[atres] texto destino NO literal al origen'
elim3 = [rot3, P3_A, P3_B, P3_C]          # copia eliminada = versión SIN 3.4

# =============================================================== [aseis]
s6, e6 = block_range(lines, 'aseis')
b6 = lines[s6:e6]; p6 = paras(b6)
rot6 = 'Artículo seis'
P6_INTRO = 'Las actuaciones de las Administraciones Públicas Sanitarias estarán orientadas:'
P6_1 = '1. A la promoción de la salud.'
P6_2 = '2. A promover el interés individual, familiar y social por la salud mediante la adecuada educación sanitaria de la población.'
P6_3 = '3. A garantizar que cuantas acciones sanitarias se desarrollen estén dirigidas a la prevención de las enfermedades y no sólo a la curación de las mismas.'
P6_4 = '4. A garantizar la asistencia sanitaria en todos los casos de pérdida de la salud.'
P6_5 = '5. A promover las acciones necesarias para la rehabilitación funcional y reinserción social del paciente.'
P6_62 = '2. En la ejecución de lo previsto en el apartado anterior, las Administraciones públicas sanitarias asegurarán la integración del principio de igualdad entre mujeres y hombres, garantizando su igual derecho a la salud.'
assert p6.count(rot6) == 2, f'[aseis] rótulos: {p6.count(rot6)}'
assert p6.count(P6_INTRO) == 1, '[aseis] intro canónica no única'
# la 1ª versión tiene 1-5; la 2ª (desplazada) repite 2-5 pero OMITE «1. A la promoción de la salud.»
assert p6.count(P6_1) == 1, f'[aseis] 6.1 x{p6.count(P6_1)}'
for txt in (P6_2, P6_3, P6_4, P6_5):
    assert p6.count(txt) == 2, f'[aseis] {txt[:40]} x{p6.count(txt)}'
assert p6.count(P6_62) == 1, '[aseis] 6.2 no único'
after6 = mk('## [aseis] Artículo seis', rot6, [P6_INTRO, P6_1, P6_2, P6_3, P6_4, P6_5, P6_62])
assert all(p in p6 for p in [rot6, P6_INTRO, P6_1, P6_2, P6_3, P6_4, P6_5, P6_62]), '[aseis] destino NO literal'
elim6 = [rot6, '1. ' + P6_INTRO, P6_2, P6_3, P6_4, P6_5]   # 2ª versión (intro numerada + dups)

# =============================================================== [aveinte]
s20, e20 = block_range(lines, 'aveinte')
b20 = lines[s20:e20]; p20 = paras(b20)
rot20 = 'Artículo veinte'
TRUNCADO = 'Sobre la base de la plena integración de las actuaciones relativas a la salud mental en el sistema sanitario general y de la total equiparación del enfermo mental a las demás personas que recursos asistenciales a nivel ambulatorio y los sistemas de hospitalización parcial y atención a domicilio, que reduzcan al máximo posible la necesidad de hospitalización.'
NOTA = 'Se advierte que el texto definitivo aprobado por el Congreso de los Diputados y publicado en el Boletín Oficial de las Cortes Generales de 9 de abril de 1986 para el primer párrafo de este artículo era el siguiente:'
cand = [p for p in p20 if p.startswith('"Sobre la base de la plena integración')]
assert len(cand) == 1, f'[aveinte] cita del Congreso: {len(cand)}'
CONGRESO = cand[0].strip('"').strip()
assert TRUNCADO in p20 and NOTA in p20, '[aveinte] truncado/nota no localizados'
boe_norm = norm(open(BOE, encoding='utf-8').read())
assert norm(CONGRESO) in boe_norm, '[aveinte] el texto del Congreso NO está en el BOE archivado'
A20 = [
 '1. La atención a los problemas de salud mental de la población se realizará en el ámbito comunitario, potenciando los recursos asistenciales a nivel ambulatorio y los sistemas de hospitalización parcial y atención a domicilio, que reduzcan al máximo posible la necesidad de hospitalización.',
 'Se considerarán de modo especial aquellos problemas referentes a la psiquiatría infantil y psicogeriatría.',
 '2. La hospitalización de los pacientes por procesos que así lo requieran se realizará en las unidades psiquiátricas de los hospitales generales.',
 '3. Se desarrollarán los servicios de rehabilitación y reinserción social necesarios para una adecuada atención integral de los problemas del enfermo mental, buscando la necesaria coordinación con los servicios sociales.',
 '4. Los servicios de salud mental y de atención psiquiátrica del sistema sanitario general cubrirán, asimismo, en coordinación con los servicios sociales, los aspectos de prevención primaria y la atención a los problemas psicosociales que acompañan a la pérdida de salud en general.',
]
assert all(t in p20 for t in A20), '[aveinte] apartado no literal al origen'
after20 = mk('## [aveinte] Artículo veinte', rot20, [CONGRESO] + A20)

# =============================================================== [adieciseis] — art. 16
s16, e16 = block_range(lines, 'adieciseis')
b16 = lines[s16:e16]; p16 = paras(b16)
rot16 = 'Artículo dieciséis'
INTRO16 = 'Las normas de utilización de los servicios sanitarios serán iguales para todos, independientemente de la condición en que se acceda a los mismos. En consecuencia, los usuarios sin derecho a la asistencia de los Servicios de Salud, así como los previstos en el artículo 80, podrán acceder a los servicios sanitarios con la consideración de pacientes privados, de acuerdo con los siguientes criterios:'
A16_2 = '2. El ingreso en centros hospitalarios se efectuará a través de la unidad de admisión del hospital, por medio de una lista de espera única, por lo que no existirá un sistema de acceso y hospitalización diferenciado según la condición del paciente.'
A16_3 = '3. La facturación por la atención de estos pacientes será efectuada por las respectivas, administraciones de los Centros, tomando como base los costes efectivos. Estos ingresos tendrán la condición de propios de los Servicios de Salud. En ningún caso estos ingresos podrán revertir directamente en aquellos que intervienen en la atención de estos pacientes.'
assert all(t in p16 for t in (rot16, INTRO16, A16_2, A16_3)), '[a16] existente no literal'

N16_4 = '4. El Ministerio de Sanidad, a propuesta de la Dirección General de Cartilla SNS, establecerá los criterios técnicos y el sistema de información de las listas de espera del Sistema Nacional de Salud.'
N16_5 = '5. El sistema de información de las listas de espera garantizará, como mínimo:'
N16_a = 'a) La trazabilidad completa del paciente desde la derivación de Atención Primaria hasta la prestación del servicio, incluyendo todos los pasos intermedios (especialista, pruebas diagnósticas, quirófano, alta).'
N16_b = 'b) La verificación independiente de los datos por una autoridad técnica del Ministerio de Sanidad, con acceso directo a las historias clínicas electrónicas de los centros hospitalarios.'
N16_c = 'c) La publicación periódica de datos desglosados por comunidad autónoma, provincia, hospital, servicio médico y tipo de intervención, incluyendo la media de días de espera real y el porcentaje de pacientes operados dentro de los plazos clínicos recomendados.'
N16_d = 'd) La protección legal del personal sanitario que denuncie de buena fe cualquier alteración, manipulación o falseamiento de los datos de las listas de espera, sin que pueda ser objeto de represalia disciplinaria, laboral o profesional.'
N16_e = 'e) La auditoría aleatoria trimestral de un porcentaje mínimo del 5% de los expedientes de pacientes prioritarios en cada hospital, con resultado publicado en el portal de transparencia del Ministerio.'
N16_6 = '6. La alteración o manipulación de los datos de las listas de espera se considerará falta muy grave de responsabilidad disciplinaria para los gestores y directivos hospitalarios implicados, sin perjuicio de las responsabilidades penales que correspondan.'
NUEVO16 = [N16_4, N16_5, N16_a, N16_b, N16_c, N16_d, N16_e, N16_6]
fuente17 = set(l.strip() for l in open(P17, encoding='utf-8').read().splitlines())
falt = [p for p in NUEVO16 if p not in fuente17]
assert not falt, f'[a16] contenido nuevo NO literal a la propuesta -> {[f[:60] for f in falt]}'
assert not (set(NUEVO16) & set(p16)), '[a16] contenido nuevo ya presente en el bloque'
after16 = mk('## [adieciseis] Artículo dieciséis', rot16, [INTRO16, A16_2, A16_3] + NUEVO16)

# ------------------------------------------------------- reconstrucción del fichero
assert s3 < e3 <= s6 < e6 <= s16 < e16 <= s20 < e20, 'orden de bloques inesperado'
segs = [lines[:s3], lines[e3:s6], lines[e6:s16], lines[e16:s20], lines[e20:]]
newbl = [after3, after6, after16, after20]
out, k = [], 0
order = [(0, after3), (1, after6), (2, after16), (3, after20), (4, None)]
for idx, blk in order:
    out += segs[idx]
    if blk is not None:
        out += blk
assert len(out) == len(lines) - sum(len(x) for x in [b3, b6, b16, b20]) + sum(len(x) for x in newbl)
newtext = '\n'.join(out) + ('\n' if raw.endswith('\n') else '')

# --- verificación: SOLO cambian los 4 bloques (segmentos fuera de bloque IDÉNTICOS)
new_lines = newtext.splitlines()
pos = 0
chk = [ (-1, pos) ]
def slice_new(start, n):
    return new_lines[start:start + n]
cur = 0
new_segs = []
for idx, blk in order:
    if blk is None:
        new_segs.append(new_lines[cur:])
    else:
        new_segs.append(new_lines[cur:cur + len(segs[idx])])
        cur += len(segs[idx]) + len(blk)
for i, (o, nw) in enumerate(zip(segs, new_segs)):
    assert o == nw, f'segmento {i} CAMBIÓ fuera de bloque objetivo'
print('[OK] los 4 bloques objetivo son los ÚNICOS que cambian (5 segmentos intactos)')

# ------------------------------------------------------- aplicar
shutil.copy(LEY, BAK)
open(LEY, 'w', encoding='utf-8', newline='').write(newtext)

manifiesto['sha256_fichero_despues'] = sha_file(LEY)
manifiesto['lineas_antes'] = len(lines)
manifiesto['lineas_despues'] = len(new_lines)
manifiesto['palabras_antes'] = sum(len(l.split()) for l in lines)
manifiesto['palabras_despues'] = sum(len(l.split()) for l in new_lines)

def entry(etiqueta, antes, despues, origen, tipo, elim, final, extra=None):
    d = {
        'etiqueta': etiqueta,
        'lineas_antes': len(antes), 'lineas_despues': len(despues),
        'palabras_antes': wc(antes), 'palabras_despues': wc(despues),
        'tipo': tipo,
        'palabras_deduplicadas': max(0, wc(antes) - wc(despues)),
        'palabras_nuevas': extra.get('nuevas', 0) if extra else 0,
        'sha256_copia_eliminada': sha('\n'.join(elim)) if elim else None,
        'texto_eliminado_200': (' / '.join(elim))[:200],
        'texto_final_200': (final or '')[:200],
        'fichero_procedencia_texto': origen,
    }
    if extra:
        d.update({k: v for k, v in extra.items() if k != 'nuevas'})
    return d

manifiesto['diffs'] = {
 'atres': entry('[atres] Artículo 3 LGS', b3, after3,
                'propuestas/2026-09-16.md (Propuesta 1)', 'deduplicacion',
                elim3, P3_D, {'nuevas': 0,
                'fidelidad_BOE': 'la copia conservada (apartados 1-4) coincide literal con el BOE consolidado'}),
 'aseis': entry('[aseis] Artículo 6 LGS', b6, after6,
                'propuestas/2026-09-16.md (Propuesta 2)', 'deduplicacion',
                elim6, P6_62, {'nuevas': 0,
                'fidelidad_BOE': 'intro + apartados 1-5 + apartado 6.2 (igualdad) presentes en el BOE consolidado'}),
 'aveinte': entry('[aveinte] Artículo 20 LGS', b20, after20,
                'propuestas/2026-09-08.md (Propuesta 3) + BOCG 09/04/1986', 'correccion_legalidad',
                [TRUNCADO, NOTA], CONGRESO, {'nuevas': 0,
                'fidelidad_BOE': 'el texto del Congreso está citado literal en el BOE consolidado archivado'}),
 'adieciseis': entry('[adieciseis] Artículo 16 LGS', b16, after16,
                'propuestas/2026-09-17.md (Propuesta 1)', 'contenido_nuevo_aprobado',
                [], ' | '.join(NUEVO16), {
                'nuevas': sum(len(p.split()) for p in NUEVO16),
                'advertencia': ('La propuesta invocaba como texto previo unos apartados 2-3 de «planificación de la '
                                'actividad asistencial» que NO existen en el BOE archivado (0 ocurrencias de esa '
                                'frase). El acta del Consejo 2026-09-17 dice que la propuesta «amplía el art. 16 sin '
                                'alterar lo existente»: por eso se conserva ÍNTEGRO el art. 16 real (normas de '
                                'utilización de los servicios sanitarios) y solo se AÑADEN los apartados nuevos.'),
                'numeracion_literal': ('la propuesta numera el contenido nuevo como 4, 5 (con letras a-e) y 6; la '
                                       'agenda/acta lo resumen como «4-7». Se respeta el literal de la propuesta.'),
                'hueco_previa_detectado': ('el bloque NO contiene el apartado 1 del art. 16 («Por lo que se refiere a '
                                           'la atención primaria...») presente en el BOE; NO se restituye por estar '
                                           'fuera de los diffs aprobados (se reporta como incidencia).')}),
}
manifiesto['resumen'] = {
    'palabras_deduplicadas_total': sum(wc(x) - wc(y) for x, y in [(b3, after3), (b6, after6), (b20, after20)]),
    'palabras_nuevas_total': sum(len(p.split()) for p in NUEVO16),
    'palabras_fichero_netas': manifiesto['palabras_despues'] - manifiesto['palabras_antes'],
}
json.dump(manifiesto, open(os.path.join(BASE, 'manifiesto_fase2_s13_2026-09-21.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in manifiesto.items() if k != 'diffs'}, ensure_ascii=False, indent=1))
for k in ('atres', 'aseis', 'aveinte', 'adieciseis'):
    v = manifiesto['diffs'][k]
    print(f"  {k:11s} lineas {v['lineas_antes']:>3}->{v['lineas_despues']:<3} "
          f"palabras {v['palabras_antes']:>4}->{v['palabras_despues']:<4} "
          f"dedup {v['palabras_deduplicadas']:<4} nuevas {v['palabras_nuevas']}")
