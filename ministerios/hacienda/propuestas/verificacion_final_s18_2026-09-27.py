# -*- coding: utf-8 -*-
# Sesion 18/30 - verificacion final ANTES de publicar propuestas:
# 1) [a150]: ¿la letra 'reanudación de las actuaciones' existe en el source.html crudo?
#    (F1 real pendiente vs artefacto del manifiesto truncado)
# 2) [a112]: consolidado filtrado ⊆ propuesto-cola -> dedupe seguro
# 3) [a65]: localizar el byte literal de 'a) Aquellas cuya exacción...' en el consolidado
#    y construir el propuesto final (cola + a) restituida en posicion)
import json, re, os, unicodedata, hashlib
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')

def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'")
    s = s.replace('&uacute;', 'ú').replace('&oacute;', 'ó').replace('&aacute;', 'á').replace('&ntilde;', 'ñ').replace('&Iacute;', 'Í').replace('&iacute;', 'í').replace('&eacute;', 'é').replace('&agrave;', 'à').replace('&ccedil;', 'ç')
    s = re.sub(r'&[a-zA-Z]+;', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

# 1) a150
src_raw = open('data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html', encoding='utf-8', errors='ignore').read()
nsrc = norm(re.sub(r'<[^>]+>', ' ', src_raw))
vivo = norm(open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read())
for fr in ['los ingresos realizados desde el inicio del procedimiento hasta la reanudación de las actuaciones',
           'los ingresos realizados desde el inicio del procedimiento hasta la primera actuación practicada']:
    print('a150 |', fr[:66], '| source_raw:', fr in nsrc, '| vivo:', fr in vivo)

# 2) a112
html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
tx = re.sub(r'<br\s*/?>', '\n', html); tx = re.sub(r'</p>', '\n', tx); tx = re.sub(r'<[^>]+>', ' ', tx)
lns = [re.sub(r'\s+', ' ', l).strip() for l in tx.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')
APAR = re.compile(r'(seleccionar redacci|última actualizaci|modificación|publicada|publicado|en vigor|ref\. boletin|ref\. boe|boe-a-\d|subir \[|se añade|se modifica|se renumera|renumeran|téngase en cuenta|jurisprudencia|texto original|único\.\d|de la [Ll]ey \d|real decreto)', re.I)
def seccion(artno):
    idx = [i for i, l in enumerate(lns) if re.match(rf'Artículo {artno}\. ', l)]
    i = idx[-1]; j = i + 1
    while j < len(lns) and not END.match(lns[j]): j += 1
    return ' '.join(l for l in lns[i:j] if not APAR.search(l))

prop112 = open('ministerios/hacienda/evidencia/bloque_propuesto_a112_2026-09-27.txt', encoding='utf-8').read()
sv112 = seccion(112); nsv = norm(sv112); nprop = norm(prop112)
f112 = [x.strip() for x in re.split(r'(?<=[.;:])\s+', nsv) if len(x.strip()) >= 20]
aus = [x for x in f112 if x not in nprop]
print('a112: frases vigentes (filtradas) =', len(f112), '| ausentes del propuesto =', len(aus))
for x in aus: print('   ·', x[:110])

# 3) a65: byte literal de la letra a) en el HTML consolidado (con acentos reales)
m = re.search(r'a\)\s*(?:<[^>]+>\s*)*[Aa]quellas cuya exacción se realice por medio de efectos timbrados\.', html)
print('a65 letra a) encontrada en consolidado:', bool(m))
if m:
    frag_html = m.group(0)
    letra = re.sub(r'<[^>]+>', '', frag_html)
    letra = re.sub(r'\s+', ' ', letra).strip()
    print('   byte literal (normalizado a espacios):', letra[:120])
    sha = hashlib.sha256(letra.encode('utf-8')).hexdigest()
    print('   sha256:', sha[:16])
