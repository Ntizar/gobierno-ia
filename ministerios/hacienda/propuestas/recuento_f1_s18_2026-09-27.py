# -*- coding: utf-8 -*-
# Sesion 18/30 - recuento F1 ACTUALIZADO de la LGT (encargo del acta 17, obs. 3)
# Cuadra el inventario vivo del 23-09 (159 preceptos) contra el pareo por frases de HOY.
import json
d = json.load(open('C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/estado_sesion18_2026-09-27.json', encoding='utf-8'))
inv = json.load(open('C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json', encoding='utf-8'))
canon = json.load(open('C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json', encoding='utf-8'))
pa = inv['preceptos_afectados']
casos = sum(v['casos'] for v in pa.values())
pals = sum(v['palabras'] for v in pa.values())
print('inventario s15 (23-09):', len(pa), 'bloques,', casos, 'casos,', pals, 'palabras')
print('canon: preceptos =', len(canon['articulos']), '| claves del JSON =', list(canon.keys()))
hoy_def = {t for t, _, _ in d['f1_remedido']['deficientes']}
siguen = [b for b in pa if b.strip('[]') in hoy_def]
print('preceptos del inventario s15 aun deficientes hoy:', len(siguen), siguen[:20])
print('pareo hoy:', d['f1_remedido']['preceptos_con_texto'], '/', d['f1_remedido']['preceptos_canon'],
      '| frases ausentes', d['f1_remedido']['frases_ausentes'], 'de', d['f1_remedido']['frases_canon_total'],
      '| palabras ausentes', d['f1_remedido']['palabras_ausentes'])
print('bloques del repo sin homologo en canon (43):', d['f1_remedido']['bloques_vivo_sin_homologo_en_canon'])
