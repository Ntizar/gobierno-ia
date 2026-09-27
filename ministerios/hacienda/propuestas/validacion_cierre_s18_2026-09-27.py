# -*- coding: utf-8 -*-
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '').replace('\u2019', "'").replace('\u00ab', '"').replace('\u00bb', '"')
    for a, b in [('&uacute;','ú'),('&oacute;','ó'),('&aacute;','á'),('&ntilde;','ñ'),('&iacute;','í'),('&eacute;','é'),('&Iacute;','Í'),('&Aacute;','Á'),('&Uacute;','Ú'),('&ccedil;','ç'),('&nbsp;',' ')]:
        s = s.replace(a, b)
    s = re.sub(r'&[a-zA-Z]+;', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()
html = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
cons = norm(re.sub(r'<[^>]+>', ' ', html))
tx = re.sub(r'<br\s*/?>', '\n', html); tx = re.sub(r'</p>', '\n', tx); tx = re.sub(r'<[^>]+>', ' ', tx)
lns = [re.sub(r'\s+', ' ', l).strip() for l in tx.split('\n') if l.strip()]
END = re.compile(r'^(Artículo \d+\. |T[íi]tulo |Disposici|Anexo|CAP[ÍI]TULO|SECCI[ÓO]N)')
APAR = re.compile(r'(seleccionar redacci|última actualizaci|modificación|publicada|publicado|en vigor|ref\. boletin|ref\. boe|boe-a-\d|subir \[|se añade|se modifica|se renumera|renumeran|téngase en cuenta|jurisprudencia|texto original|único\.\d|de la [Ll]ey \d|real decreto|disposición transitoria)', re.I)
def vig(artno):
    idx = [i for i, l in enumerate(lns) if re.match(rf'Artículo {artno}\. ', l)]
    i = idx[-1]; j = i + 1
    while j < len(lns) and not END.match(lns[j]): j += 1
    keep = [l for l in lns[i:j] if not APAR.search(l) and not l.startswith('#') and not re.match(r'^\d+\.\d+\.? de la', l)]
    return ' '.join(keep)
# (a) [a229]: ¿la redaccion vigente del consolidado cabe en el propuesto del 25-09?
prop229 = norm(open('ministerios/hacienda/evidencia/bloque_propuesto_a229_2026-09-25.txt', encoding='utf-8').read())
v229 = vig(229); n229 = norm(v229)
fr229 = [f.strip() for f in re.split(r'(?<=[.;:])\s+', n229) if len(f.strip()) >= 20]
aus = [f for f in fr229 if f not in prop229]
print('a229 vigente (filtrada):', len(v229.split()), 'pal | frases', len(fr229), '| ausentes del propuesto-25:', len(aus))
for f in aus[:6]: print('   ·', f[:100])
# (b) [a81] y [a65] post-restitucion: ¿cuantas vigentes faltan ahora?
for tag, artno in [('a81', 81), ('a65', 65)]:
    p = norm(open(f'ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-27.txt', encoding='utf-8').read())
    v = vig(artno); nv = norm(v)
    fs = [f.strip() for f in re.split(r'(?<=[.;:])\s+', nv) if len(f.strip()) >= 20]
    a = [f for f in fs if f not in p]
    print(f'{tag} post-restitucion: vigentes', len(fs), '| ausentes', len(a))
    for f in a: print('   ·', f[:100])
# (c) [a150] reanudacion: ¿traza en el consolidado (texto vigente de la Ley 230/1963?)
r = norm('Los ingresos realizados desde el inicio del procedimiento hasta la reanudación de las actuaciones')
print('a150 reanudacion en consolidado:', r in cons, '| en propuesto-a229:', r in prop229)
