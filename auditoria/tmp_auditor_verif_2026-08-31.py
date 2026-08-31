# Verificacion forense del Auditor del Estado — 2026-08-31 (sesion 3/30)
# Independiente de los scripts ministeriales. Reejecutable:
#   python auditoria/tmp_auditor_verif_2026-08-31.py   (desde la raiz del repo)
# Metrica normalizada: sha256 por parrafo (lineas separadas por linea en blanco,
# espacios colapsados), palabras = len(split()).
import re, hashlib, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p): return open(os.path.join(ROOT,p), encoding='utf-8').read().replace('\r\n','\n')
def norm(p): return re.sub(r'\s+',' ',p).strip()
def wc(s): return len(s.split())

def blocks(txt):
    parts = re.split(r'^## (\[[^\]]+\])[^\n]*$', txt, flags=re.M)
    return [(parts[i], parts[i+1]) for i in range(1,len(parts)-1,2)]

def scan(body):
    paras=[norm(p) for p in body.split('\n\n') if norm(p)]
    h={}
    for p in paras:
        k=hashlib.sha256(p.encode()).hexdigest()
        h[k]=h.get(k,[0,wc(p)]); h[k][0]+=1
    return dict(paras=len(paras), dup_paras=sum(c-1 for c,w in h.values() if c>1),
                dup_words=sum((c-1)*w for c,w in h.values() if c>1), words=wc(body))

out={}
# ---------- LGT (Hacienda) ----------
lgt = load('ministerios/hacienda/leyes/BOE-A-2003-23186.md')
bl = dict(blocks(lgt)); order=[b[0] for b in blocks(lgt)]
out['LGT'] = {'total_headers': len(order), 'numeric_headers': len(re.findall(r'^## \[a\d+\]', lgt, flags=re.M)),
              'total_words': wc(lgt)}
# [a150]: bloque real
out['LGT_a150'] = scan(bl['[a150]'])
b150 = bl['[a150]']
out['LGT_a150']['old_12m_x2'] = b150.count('deberán concluir en el plazo de 12 meses')
out['LGT_a150']['new_x3'] = b150.count('deberán concluir en el plazo de:')
# "[a271]" del ministro = region [a271]..fin (su regex solo parte en [aN] numerico)
i0, i1 = order.index('[a271]'), order.index('[dtprimera]')
region_ids = order[i0:i1]
region = '\n\n'.join(bl[i] for i in region_ids)
out['LGT_region_a271'] = scan(region)
out['LGT_region_a271']['n_subregion_headers'] = len(region_ids)
out['LGT_region_a271']['DA5_x'] = region.count('Disposición adicional quinta. Declaraciones censales')
out['LGT_region_a271']['DA6_x'] = region.count('Disposición adicional sexta. Número de identificación fiscal')
out['LGT_region_a271']['DA11_x'] = region.count('Disposición adicional undécima')
out['LGT_region_a271']['DA18_x'] = region.count('Disposición adicional decimoctava')
out['LGT_region_a271']['DA20_x'] = region.count('Disposición adicional vigésima.')
out['LGT_region_a271']['DA22_x'] = region.count('Disposición adicional vigésimo segunda')
out['LGT_region_a271']['DA23_header_x'] = region.count('Disposición adicional vigésimo tercera')
out['LGT_region_a271']['DA24_header_x'] = region.count('Disposición adicional vigésimo cuarta')
out['LGT_region_a271']['multa_5000_x'] = region.count('5.000 euros')
# metodo del ministro (lineas sueltas >40 chars, no parrafos) sobre la misma region:
paras_min = [l.strip() for l in region.split('\n') if l.strip() and len(l.strip())>40 and not l.strip().startswith('## [')]
h={}
for p in paras_min:
    k=hashlib.sha256(re.sub(r'\s+',' ',p).encode()).hexdigest()
    h[k]=h.get(k,[0,len(p.split())]); h[k][0]+=1
out['LGT_region_a271_ministro_metodo'] = {'paras': len(paras_min), 'words': sum(len(p.split()) for p in paras_min),
    'dup_words': sum((c-1)*w for c,w in h.values() if c>1)}
# global dup LGT por bloque (margen para 106/271 y 52.383)
G=sum(scan(b)['dup_words'] for _,b in blocks(lgt)); GB=sum(1 for _,b in blocks(lgt) if scan(b)['dup_paras'])
out['LGT_global_perblock'] = {'dup_words_all_headers': G, 'blocks_with_dup': GB}
# ---------- LGS (Sanidad) ----------
lgs = load('ministerios/sanidad/leyes/BOE-A-1986-10499.md')
sb = dict(blocks(lgs))
out['LGS'] = {'total_headers': len(sb), 'total_words': wc(lgs),
              'dup_words_global': sum(scan(b)['dup_words'] for b in sb.values()),
              'blocks_with_dup': sum(1 for b in sb.values() if scan(b)['dup_paras'])}
out['LGS_art18'] = scan(sb['[adieciocho]'])
out['LGS_art18']['header_x'] = sb['[adieciocho]'].count('Artículo dieciocho')
out['LGS_art35'] = scan(sb['[atreintaycinco]'])
out['LGS_art35']['registro_x'] = sb['[atreintaycinco]'].count('Registro Estatal de Profesionales Sanitarios')
out['LGS_art35']['sin_1a'] = '1.ª' not in sb['[atreintaycinco]']
# ---------- L7/2021 (Ecologia) ----------
l7 = load('ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md')
tb = dict(blocks(l7)); lines = l7.split('\n')
out['L7'] = {'total_headers': len(tb), 'total_words': wc(l7),
             'dup_words_global': sum(scan(b)['dup_words'] for b in tb.values()),
             'blocks_with_dup': sum(1 for b in tb.values() if scan(b)['dup_paras'])}
out['L7_art15'] = scan(tb['[a1-7]'])
out['L7_art15']['label_x'] = tb['[a1-7]'].count('Artículo 15. Instalación de puntos de recarga eléctrica')
out['L7_art15']['v1_words_387_414'] = wc('\n'.join(lines[386:414]))
out['L7_art15']['v2_words_415_443'] = wc('\n'.join(lines[414:443]))
out['L7_art15']['v3_words_445_473'] = wc('\n'.join(lines[444:473]))
out['L7_art15']['plazo_12_x'] = tb['[a1-7]'].count('plazo de 12 meses')
out['L7_art15']['plazo_21_x'] = tb['[a1-7]'].count('veintiún meses')
out['L7_art15']['dir_2014_94_x'] = tb['[a1-7]'].count('2014/94')
# listas que empiezan en b) sin a) previa (defecto de conversion) — las 3 leyes
def lists_start_b(body):
    hits=0
    paras=[norm(p) for p in body.split('\n\n') if norm(p)]
    for j,p in enumerate(paras):
        if re.match(r'^b\)', p):
            prev = paras[j-1] if j>0 else ''
            if not (prev.startswith('a)') or prev.rstrip().endswith('a)') or re.search(r'a\)\s', prev[-80:])):
                hits+=1
    return hits
out['listas_b_sin_a'] = {n: sum(lists_start_b(b) for _,b in blocks(t))
                         for n,t in [('LGT',lgt),('LGS',lgs),('L7',l7)]}
print(json.dumps(out, indent=1, ensure_ascii=False))
