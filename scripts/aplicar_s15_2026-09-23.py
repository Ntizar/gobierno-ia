#!/usr/bin/env python
"""Ejecucion de los acuerdos aprobados en el Consejo de la sesion 15/30 (2026-09-23).
Presidencia aplica los diffs con canon BOE archivado del repo, .bak, sha256 antes/despues
y manifiesto por bloque. Dry-run por defecto; --apply escribe.
"""
import re, sys, json, hashlib, shutil, pathlib, datetime

RAIZ = pathlib.Path(r'C:/Users/d_ant/Projects/gobierno-ia')
FECHA = '2026-09-23'
APLICAR = '--apply' in sys.argv

APARATO = ('Se modifica','Se deroga','Se convierten','Subir','Última actualización','Seleccionar redacción','Texto original','Se añade','Se declara','Se introduce','Se suprime','Modificación publicada','Texto añadido','Se renumera','Se corrige','Véase')

def leer(p):
    return pathlib.Path(p).read_text(encoding='utf-8').replace('\r\n','\n')

def bloques(txt):
    L = txt.split('\n')
    idx = [(i, re.match(r'^## \[([^\]]+)\]', l).group(1)) for i,l in enumerate(L) if re.match(r'^## \[([^\]]+)\]', l)]
    B = {}
    for n,(i,k) in enumerate(idx):
        end = idx[n+1][0] if n+1 < len(idx) else len(L)
        B[k] = (i, end, L[i:end], L[i].strip())
    return L, B, len(idx)

C_TXT = leer(RAIZ/'ministerios/sanidad/evidencia/boe_texto_plano.txt')
C_L = C_TXT.split('\n')
cmarks = [(i, re.search(r'#([a-z0-9]+)\]', l).group(1)) for i,l in enumerate(C_L) if re.search(r'\[Bloque \d+: #[a-z0-9]+\]', l)]
CM = {}
for n,(i,k) in enumerate(cmarks):
    end = cmarks[n+1][0] if n+1 < len(cmarks) else len(C_L)
    CM[k] = C_L[i+1:end]

def cuerpo_canon(tag):
    out = []
    for l in CM[tag]:
        t = l.strip()
        if not t:
            continue
        if t.startswith(APARATO) or t.startswith('[Bloque') or re.match(r'^(CAPÍTULO|TÍTULO|Sección|Disposición|ANEXO)', t):
            break
        out.append(t)
    return out

# ---------- LGT (Hacienda) ----------
LGT = RAIZ/'ministerios/hacienda/leyes/BOE-A-2003-23186.md'
lgt = leer(LGT)
Ll, Bl, nb_l = bloques(lgt)

nuevos = {}
for tag, ev in [('a82','bloque_propuesto_a82_2026-09-23.txt'), ('a104','bloque_propuesto_a104_2026-09-23.txt')]:
    txt = leer(RAIZ/f'ministerios/hacienda/evidencia/{ev}').rstrip('\n')
    nuevos[tag] = txt.split('\n')
    pal = len([w for w in re.split(r'\s+', txt.strip()) if w])
    rot = len([l for l in nuevos[tag] if re.match(r'^Artículo \d', l.strip())])
    print(f'LGT [{tag}] nuevo bloque: {pal} palabras, {rot} rotulo(s) de cuerpo')

# ---------- LGS (Sanidad) ----------
LGS = RAIZ/'ministerios/sanidad/leyes/BOE-A-1986-10499.md'
lgs = leer(LGS)
Ls, Bs, nb_s = bloques(lgs)
print(f'LGS bloques actuales: {nb_s}')

def normaliza(sl):
    out = []
    for l in sl:
        if l.strip() == '':
            if out and out[-1].strip() == '':
                continue
            out.append('')
        else:
            out.append(l.rstrip())
    while out and out[-1].strip() == '':
        out.pop()
    return out + ['']

def cab(k):
    return Bs[k][3]

def envuelve(k, cuerpo):
    return normaliza([cab(k), ''] + sum([[p, ''] for p in cuerpo], []))

lgs_nuevos = {}
# aonce: canon + marcador de derogacion del apartado 4 en la convencion del repo
c = cuerpo_canon('aonce')
c = [x for x in c if x != '(Derogado)']
c += ['4.<strong> (Derogado)</strong>']
lgs_nuevos['aonce'] = envuelve('aonce', c)
# aveintisiete: solo la redaccion vigente (canon)
lgs_nuevos['aveintisiete'] = envuelve('aveintisiete', cuerpo_canon('aveintisiete'))
# aveintidos / asesentayuno: quitar rotulo duplicado (texto + marcador se conservan, convencion del repo)
for k in ['aveintidos','asesentayuno']:
    sl = Bs[k][2]
    visto = False; out = []
    for l in sl:
        if l.strip() == cab(k).replace('## [%s] ' % k, ''):
            if visto: continue
            visto = True
        out.append(l)
    lgs_nuevos[k] = normaliza(out)
# acuarentaytres: quitar rotulo duplicado
sl = Bs['acuarentaytres'][2]; visto = False; out = []
for l in sl:
    if l.strip() == 'Artículo cuarenta y tres':
        if visto: continue
        visto = True
    out.append(l)
lgs_nuevos['acuarentaytres'] = normaliza(out)
# resto: canon literal
for k in ['atreintayseis','aochentaydos','aciento','acientocinco']:
    lgs_nuevos[k] = envuelve(k, cuerpo_canon(k))
# aochentaycuatro: canon con marcador en formato del repo
c = cuerpo_canon('aochentaycuatro')
c = ['1.<strong> (Derogado)</strong>' if x == '1. (Derogado)' else x for x in c]
lgs_nuevos['aochentaycuatro'] = envuelve('aochentaycuatro', c)
# aveintiuno: retirada del parrafo huerfano (C.3), verificado 0 coincidencias en las 3 fuentes BOE
sl = list(Bs['aveintiuno'][2]); out = []
i = 0
while i < len(sl):
    if sl[i].startswith('3. El ejercicio de las competencias enumeradas en este artículo'):
        i += 1
        while i < len(sl) and sl[i].strip() != '':
            i += 1
        continue
    out.append(sl[i]); i += 1
lgs_nuevos['aveintiuno'] = normaliza(out)

print()
for k in ['aonce','aveintisiete','aveintidos','asesentayuno','acuarentaytres','atreintayseis',
          'aochentaydos','aochentaycuatro','aciento','acientocinco','aveintiuno']:
    ant = Bs[k][2]
    nue = lgs_nuevos[k]
    pa = len([w for w in re.split(r'\s+', '\n'.join(ant).strip()) if w])
    pn = len([w for w in re.split(r'\s+', '\n'.join(nue).strip()) if w])
    rot = len([l for l in nue if re.match(r'^(Artículo|cabecera)', l.strip()) and not l.startswith('##')])
    print(f'LGS [{k}] {pa} -> {pn} palabras ({pn-pa:+d}) | rotulos cuerpo: {rot}')

print()
print('--- MUESTRA bloques nuevos (LGS) ---')
for k in ['aochentaycuatro','aciento','aveintiuno','aveintidos','asesentayuno','acuarentaytres']:
    print(f'>>>>> [{k}]')
    print('\n'.join(l[:220] for l in lgs_nuevos[k]))
    print()

if not APLICAR:
    print('DRY-RUN: nada escrito. Usa --apply')
    sys.exit(0)

man = {'sesion':'15/30','fecha':FECHA,'autor':'Presidencia (ronda 3)','bloques':[]}

def aplica(path, nuevos, nombre_man):
    global man
    p = pathlib.Path(path)
    before = hashlib.sha256(p.read_bytes()).hexdigest()
    bak = pathlib.Path(str(p) + f'.bak-{FECHA}')
    if not bak.exists():
        shutil.copy2(p, bak)
    txt = leer(p)
    L, B, n = bloques(txt)
    # aplicar de abajo arriba
    orden = sorted(nuevos.keys(), key=lambda k: -B[k][0])
    for k in orden:
        i, end, sl, _ = B[k]
        man['bloques'].append({
            'fichero': p.name, 'bloque': f'[{k}]',
            'lineas_antes': f'{i+1}-{end}', 'lineas_ahora': f'{i+1}-{i+1+len(nuevos[k])-1}',
            'palabras_antes': len([w for w in re.split(r'\s+', '\n'.join(sl).strip()) if w]),
            'palabras_despues': len([w for w in re.split(r'\s+', '\n'.join(nuevos[k]).strip()) if w]),
            'sha256_bloque_antes': hashlib.sha256('\n'.join(sl).encode()).hexdigest()[:16],
            'sha256_bloque_despues': hashlib.sha256('\n'.join(nuevos[k]).encode()).hexdigest()[:16],
            'rotulos_antes': len([l for l in sl if l.startswith('Artículo ')]),
            'rotulos_despues': len([l for l in nuevos[k] if l.startswith('Artículo ')]),
        })
        L[i:end] = nuevos[k]
    nuevo_txt = '\n'.join(L)
    p.write_text(nuevo_txt, encoding='utf-8')
    after = hashlib.sha256(p.read_bytes()).hexdigest()
    L2, B2, n2 = bloques(nuevo_txt)
    man['ficheros'] = man.get('ficheros', [])
    man['ficheros'].append({'fichero': str(p.relative_to(RAIZ)), 'sha256_antes': before,
                            'sha256_despues': after, 'bloques_antes': n, 'bloques_despues': n2})
    print(f'{p.name}: {before[:12]} -> {after[:12]} | bloques {n} -> {n2}')

aplica(LGT, nuevos, 'manifiesto_consejo_s15_2026-09-23.json')
aplica(LGS, lgs_nuevos, 'manifiesto_consejo_s15_2026-09-23.json')

destino = RAIZ/'consejo/evidencia'
destino.mkdir(parents=True, exist_ok=True)
(destino/f'manifiesto_consejo_s15_{FECHA}.json').write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding='utf-8')
print('manifiesto ->', destino/f'manifiesto_consejo_s15_{FECHA}.json')
