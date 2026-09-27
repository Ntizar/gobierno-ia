# -*- coding: utf-8 -*-
# Control de calidad: ¿el metodo v3 aprobado en [a203]/[a188] dejo secuencia limpia?
# Comparar la secuencia de iniciadores de apartado/letra del propuesto APROBADO (25-09)
# con la de mis 4 candidatos de hoy. Umbral de honestidad: repetir lo aprobado es legitimo;
# pero si mi bloque sale con invertidas y el aprobado no, lo declaro con bandera o no va.
import re, os
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def seq(t):
    out = []
    for l in t.split('\n'):
        m = re.match(r'^(\d{1,2})\.\s+[A-ZÁÉÍÓÚÑ«]|^([a-z])\)\s', l.strip())
        if m:
            out.append(m.group(1) or m.group(2))
    return out
for f, label in [
  ('ministerios/hacienda/evidencia/bloque_propuesto_a203_2026-09-25.txt', 'APROBADO-72 [a203]'),
  ('ministerios/hacienda/evidencia/bloque_propuesto_a188_2026-09-25.txt', 'APROBADO-73 [a188]'),
  ('ministerios/hacienda/evidencia/bloque_propuesto_a81_2026-09-27.txt', 'candidato [a81]'),
  ('ministerios/hacienda/evidencia/bloque_propuesto_a68_2026-09-27.txt', 'candidato [a68]'),
  ('ministerios/hacienda/evidencia/bloque_propuesto_a65_2026-09-27.txt', 'candidato [a65]'),
  ('ministerios/hacienda/evidencia/bloque_propuesto_a112_2026-09-27.txt', 'candidato [a112]')]:
    if not os.path.exists(f):
        print(label, '| fichero no existe:', f); continue
    s = seq(open(f, encoding='utf-8').read())
    nums = [x for x in s if x.isdigit()]
    inv = sum(1 for a, b in zip(nums, nums[1:]) if int(b) < int(a))
    print(f'{label:22s} | iniciadores: {" ".join(s[:44])}')
    print(f'{"":22s} | repeticiones de numeral: {len(nums) - len(set(nums))} | inversiones: {inv}')
