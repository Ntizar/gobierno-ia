# -*- coding: utf-8 -*-
# Sesion 18/30 - TEST DE REORDENAMIENTO (la bandera que mato a [a229]):
# ¿el propuesto v3 conserva el orden logico de numeracion/apartados respecto al vivo?
# Medida: secuencia de numeros de apartado/letras en el propuesto vs su primera aparicion en el vivo.
import json, re, os
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
EV = 'ministerios/hacienda/evidencia'
def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\u00a0', ' ')).strip().lower()

for tag in ['a81', 'a68', 'a65', 'a112']:
    vivo = open(f'{EV}/bloque_vivo_{tag}_2026-09-27.txt', encoding='utf-8').read()
    prop = open(f'{EV}/bloque_propuesto_{tag}_2026-09-27.txt', encoding='utf-8').read()
    def apartados(t):
        return [m.group(1) for m in re.finditer(r'(?m)^(?:(\d{1,2})\.|([a-z])\)|(\d{1,2}\.ª))\s', t) for _ in [0]]
    def seq(t):
        out = []
        for m in re.finditer(r'(?m)^(\d{1,2})\.\s+[A-ZÁÉÍÓÚÑ«]|^([a-z])\)\s|^(\d{1,2}\.ª)\s', t):
            g = m.group(1) or m.group(2) or m.group(3)
            out.append(g)
        return out
    sp = seq(prop)
    # primera aparicion en el vivo del MISMO item (linea identica normalizada) -> orden esperado
    lines_vivo = [l for l in vivo.split('\n') if l.strip()]
    first_pos = {}
    for i, l in enumerate(lines_vivo):
        m = re.match(r'^(\d{1,2})\.\s+[A-ZÁÉÍÓÚÑ«]|^([a-z])\)\s|^(\d{1,2}\.ª)\s', l.strip())
        if m:
            k = (m.group(1) or m.group(2) or m.group(3))
            key = (k, norm(l)[:40])
            first_pos.setdefault(key, i)
    # orden en el vivo de las lineas supervivientes
    surv_keys = []
    for l in [x for x in prop.split('\n') if x.strip()]:
        m = re.match(r'^(\d{1,2})\.\s+[A-ZÁÉÍÓÚÑ«]|^([a-z])\)\s|^(\d{1,2}\.ª)\s', l.strip())
        if m:
            k = (m.group(1) or m.group(2) or m.group(3))
            surv_keys.append((k, norm(l)[:40]))
    pos_en_vivo = [first_pos.get(k, -1) for k in surv_keys]
    desorden = sum(1 for a, b in zip(pos_en_vivo, pos_en_vivo[1:]) if b < a and a >= 0 and b >= 0)
    print(tag, '| items en propuesto:', len(sp), '| inversiones de orden respecto al vivo:', desorden)
    print('   seq propuesto:', ' '.join(sp[:40]))
