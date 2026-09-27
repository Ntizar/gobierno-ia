# -*- coding: utf-8 -*-
# Sesion 18/30 - GENERACION FINAL y determinista de los dos textos propuestos:
# [a65] y [a81] = capa vigente (ultima copia completa del canon, byte a byte del vivo)
#                 + letras vigentes del propio sedimento restituidas EN POSICION
#                 (bytes literales del mismo bloque vivo; ancla: la b) que las sigue).
# Nada se re-redacta. Verificaciones publicadas: canon ⊆ propuesto (substring y frases),
# 1 copia de cada encabezamiento, propuesto ⊆ vivo (uniones de fragmentos literales).
import json, re, os, unicodedata, hashlib
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
EV = 'ministerios/hacienda/evidencia'

def sha(t): return hashlib.sha256(t.replace('\r\n', '\n').rstrip('\n').encode('utf-8')).hexdigest()
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'")
    return re.sub(r'\s+', ' ', s).strip().lower()

vivo_raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}

def bloque(tag):
    m = re.search(r'(?m)^(## \[' + tag + r'\][^\n]*)\n(.*?)(?=\n## \[|\Z)', vivo_raw, re.S)
    return m.group(1), m.group(2)

REP = {}

# ---------- [a65] ----------
cab, body = bloque('a65')
vivo65 = (cab + '\n' + body).rstrip('\n')
head65 = 'Artículo 65. Aplazamiento y fraccionamiento del pago.'
ap65 = '1. Las deudas tributarias que se encuentren en período voluntario o ejecutivo podrán aplazarse'
cola65 = body[body.rfind(ap65):].rstrip()
assert norm(arts['a65']['texto'].strip()) in norm(cola65)
# letra a) del 65.2: byte literal del ejemplar consolidado archivado
html = open(EV + '/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
mm = re.search(r'a\)\s*(?:<[^>]+>\s*)*[Aa]quellas cuya exacción se realice por medio de efectos timbrados\.', html)
letra65 = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', mm.group(0))).strip()
ancla = re.search(r'(?m)^b\) Las correspondientes a obligaciones tributarias que deban cumplir el retenedor', cola65)
assert ancla
prop65_texto = cola65[:ancla.start()] + letra65 + '\n' + cola65[ancla.start():]
foot65 = ('\n\n> Consolidación 2026-09-27 (Ministerio de Hacienda): se retiran las cuatro capas históricas; '
          'cuerpo = capa vigente byte a byte del texto vivo + letra a) del apartado 2 restituida en su posición '
          '(literal del ejemplar BOE consolidado archivado en evidencia/, sha256 de la frase: f986375cfbe85eb4…) '
          'que la copia actual había perdido. Aparato del repo, no norma.\n')
prop65 = cab + '\n\n' + head65 + '\n\n' + prop65_texto + foot65

# ---------- [a81] ----------
cab, body = bloque('a81')
vivo81 = (cab + '\n' + body).rstrip('\n')
head81 = 'Artículo 81. Medidas cautelares.'
ap81 = '1. Para asegurar el cobro de las deudas para cuya recaudación sea competente'
cola81 = body[body.rfind(ap81):].rstrip()
assert norm(arts['a81']['texto'].strip()) in norm(cola81)
# letra a) del 81.4 desde el SEDIMENTO del propio bloque (byte literal)
ml = re.search(r'(?m)^a\) La retención del pago de devoluciones tributarias.*?acuerdo de devolución\.$', body, re.S)
letra81 = ml.group(0).strip()
assert norm(letra81) not in norm(cola81) and norm(letra81) in norm(body)
ancla81 = re.search(r'(?m)^b\) El embargo preventivo de bienes y derechos', cola81)
assert ancla81
prop81_texto = cola81[:ancla81.start()] + letra81 + '\n\n' + cola81[ancla81.start():]
foot81 = ('\n\n> Consolidación 2026-09-27 (Ministerio de Hacienda): se retiran las cuatro capas históricas; '
          'cuerpo = capa vigente byte a byte del texto vivo + letra a) del apartado 4 restituida en su posición '
          'desde el sedimento del propio bloque (coincide literalmente con el texto vigente del BOE consolidado '
          'archivado). Dos frases vigentes más del art. 81 (apartados 7.in fine y 8 «cuando en la tramitación de '
          'una solicitud de suspensión…») NO viven en el fichero: se declaran como hueco de fidelidad aparte, no '
          'se cuelan en este dedupe. Aparato del repo, no norma.\n')
prop81 = cab + '\n\n' + head81 + '\n\n' + prop81_texto + foot81

# ---------- verificaciones ----------
def verificar(tag, vivo, prop, artno):
    nc = norm(arts[tag]['texto'].strip()); npr = norm(prop)
    frases = [f.strip() for f in re.split(r'(?<=[.;:])\s+', nc) if len(f.strip()) >= 15]
    head = next(l.strip() for l in prop.split('\n') if re.match(r'Art[íi]culo \d+\.', l.strip()))
    # fragmentos del propuesto que no salen del canon -> deben ser bytes del vivo (restitucion) o aparato
    extra = []
    for p in prop.split('\n\n'):
        n = norm(p)
        if not n or n in nc: continue
        if p.strip().startswith('## [') or p.strip().startswith('Artículo') or p.strip().startswith('>'): continue
        if n in norm(vivo): extra.append(('sedimento_vivo', p.strip()[:70]))
        elif n in norm(re.sub(r'<[^>]+>', ' ', html)): extra.append(('boe_consolidado', p.strip()[:70]))
        else: extra.append(('SIN_TRAZA', p.strip()[:70]))
    return {
        'vivo_pal': len(vivo.split()), 'prop_pal': len(prop.split()),
        'ahorro': len(vivo.split()) - len(prop.split()),
        'canon_substring_en_propuesto': nc in npr,
        'frases_canon': len(frases), 'frases_ausentes': sum(1 for f in frases if f not in npr),
        'copias_head_propuesto': prop.count(head), 'copias_head_vivo': vivo.count(head),
        'piezas_extra_y_su_traza': extra,
        'sha_vivo': sha(vivo), 'sha_prop': sha(prop),
    }

REP['a65'] = verificar('a65', vivo65, prop65, 65)
REP['a81'] = verificar('a81', vivo81, prop81, 81)
open(f'{EV}/bloque_vivo_a65_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(vivo65 + '\n')
open(f'{EV}/bloque_propuesto_a65_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(prop65)
open(f'{EV}/bloque_vivo_a81_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(vivo81 + '\n')
open(f'{EV}/bloque_propuesto_a81_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(prop81)
json.dump(REP, open(f'{EV}/manifiesto_propuestas_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(REP, ensure_ascii=False, indent=1))
