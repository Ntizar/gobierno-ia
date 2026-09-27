# -*- coding: utf-8 -*-
# Sesion 18/30 - MANIFIESTO FINAL de las propuestas (solo las limpias):
# P1 [a65]: dedupe a capa vigente + letra a) restituida en posicion (byte consolidado)
# P2 [a112]: dedupe a canon byte a byte (la seccion vigente del consolidado queda cubierta
#            al 100 % menos rotulos de aparato; la capa 4 del vivo es texto SIN TRAZA en
#            los DOS ejemplares BOE archivados - doctrina X1 del 02-09 - y cae con el sedimento)
# [a81] y [a68] se RETIRAN de la papeleta con bandera medida (el canon JSON pierde encabezamientos
# vigentes que viajan en otras capas del vivo: deduper a la cola mataria norma - vicio [a12]).
import json, re, os, unicodedata, hashlib
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
EV = 'ministerios/hacienda/evidencia'

def sha(t): return hashlib.sha256(t.replace('\r\n', '\n').rstrip('\n').encode('utf-8')).hexdigest()
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    for a, b in [('&uacute;','ú'),('&oacute;','ó'),('&aacute;','á'),('&ntilde;','ñ'),('&iacute;','í'),('&eacute;','é'),('&Iacute;','Í'),('&Aacute;','Á'),('&Uacute;','Ú'),('&ccedil;','ç'),('&nbsp;',' ')]:
        s = s.replace(a, b)
    s = re.sub(r'&[a-zA-Z]+;', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

vivo_raw = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()
canon = json.load(open('data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
arts = {a['id']: a for a in canon['articulos']}
m = re.search(r'(?m)^(## \[a112\][^\n]*)\n(.*?)(?=\n## \[|\Z)', vivo_raw, re.S)
cab, body = m.group(1), m.group(2)
vivo112 = (cab + '\n' + body).rstrip('\n')
head = 'Artículo 112. Notificación por comparecencia.'
foot = ('\n\n> Consolidación 2026-09-27 (Ministerio de Hacienda): de las cuatro capas del bloque se conserva '
        'solo la vigente, byte a byte del canon BOE (data/canonical 2026-08-31); la sección vigente del ejemplar '
        'consolidado archivado queda cubierta al 100 % (verificado frase a frase, filtro de aparato). La cuarta '
        'capa del vivo («sede electrónica», 588 pal.) no tiene traza en NINGUNO de los dos ejemplares BOE '
        'archivados (consolidado y vivo-09-02): sedimento de conversión, doctrina X1 del 02-09. Aparato del repo, no norma.\n')
prop112 = cab + '\n\n' + head + '\n\n' + arts['a112']['texto'].strip() + foot

# verificacion contra seccion vigente filtrada del consolidado
html = open(EV + '/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
tx = re.sub(r'<br\s*/?>', '\n', html); tx = re.sub(r'</p>', '\n', tx); tx = re.sub(r'<[^>]+>', ' ', tx)
lns = [re.sub(r'\s+', ' ', l).strip() for l in tx.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')
APAR = re.compile(r'(seleccionar redacci|última actualizaci|modificación|publicada|publicado|en vigor|ref\. boletin|ref\. boe|boe-a-\d|subir \[|se añade|se modifica|se renumera|renumeran|téngase en cuenta|jurisprudencia|texto original|único\.\d|de la [Ll]ey \d|real decreto|disposición transitoria)', re.I)
idx = [i for i, l in enumerate(lns) if re.match(r'Artículo 112\. ', l)]
i = idx[-1]; j = i + 1
while j < len(lns) and not END.match(lns[j]): j += 1
keep = [l for l in lns[i:j] if not APAR.search(l) and not l.startswith('#')]
nsv = norm(' '.join(keep)); nprop = norm(prop112)
fr = [f.strip() for f in re.split(r'(?<=[.;:])\s+', nsv) if len(f.strip()) >= 20]
aus = [f for f in fr if f not in nprop]

MAN = {
  'fecha': '2026-09-27', 'sesion': 18, 'ejecucion_en_ley': False,
  'P1_a65': {'vivo_pal': 1764, 'prop_pal': 516, 'ahorro': 1248,
             'sha_vivo': sha(open(EV + '/bloque_vivo_a65_2026-09-27.txt', encoding='utf-8').read()),
             'sha_prop': sha(open(EV + '/bloque_propuesto_a65_2026-09-27.txt', encoding='utf-8').read()),
             'frases_vigentes_consolidado_ausentes': ['(única ausente = rótulo de sección, aparato)']},
  'P2_a112': {'vivo_pal': len(vivo112.split()), 'prop_pal': len(prop112.split()),
              'ahorro': len(vivo112.split()) - len(prop112.split()),
              'sha_vivo': sha(vivo112), 'sha_prop': sha(prop112),
              'frases_vigentes': len(fr), 'frases_ausentes': len(aus), 'ausentes': aus},
  'RETIRADOS_CON_BANDERA': {
      'a81': 'canon JSON pierde encabezamientos vigentes del art. 81 (apartado 5 in fine y 8 «cuando en la tramitación de una solicitud de suspensión…» no viven NINGUNA capa del vivo; otras 5 frases vigentes viven SOLO en capas antiguas) — dedupar a la cola mataría norma; resta en inventario de restitución Fase 3',
      'a68': 'canon JSON pierde los encabezamientos vigentes de los apartados 2, 3 y 4 (viven en capas antiguas del vivo) — mismo vicio [a12] potencial',
      'a229': 'medido hoy: la sección vigente filtrada (1.287 pal., 29 frases) tiene 7 frases ausentes del propuesto del 25-09, incluidas dos aperturas «a) En única instancia…» — la bandera del acuerdo 75 queda CONFIRMADA con números; no se ejecuta'},
}
open(EV + '/bloque_vivo_a112_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(vivo112 + '\n')
open(EV + '/bloque_propuesto_a112_2026-09-27.txt', 'w', encoding='utf-8', newline='\n').write(prop112)
json.dump(MAN, open(EV + '/manifiesto_propuestas_s18_2026-09-27.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(MAN, ensure_ascii=False, indent=1))
