# ¿De dónde sale el texto actual del [aveintiuno]? Rastreo en la evidencia de septiembre (fidelidad/letras).
import json, re
for f in ['fidelidad_21_huerfanas_2026-09-01.json', 'letras_a_restituir_LGS.json',
          'letras_a_restuirdas_BOE.json', 'scan_2026-09-03.json', 'restauracion_puntos_2026-09-01.json',
          'a_restituir_completas_2026-09-01.json']:
    try:
        raw = open('ministerios/sanidad/evidencia/' + f, encoding='utf-8').read()
    except FileNotFoundError:
        print(f, '-- no existe'); continue
    for pat in ['microclima', 'salud integral del trabajador', 'mapa de riesgos',
                'perspectiva de género', 'veintiuno']:
        print(f'{f[:42]:44} {pat[:28]:30} ->', raw.lower().count(pat.lower()))
    m = re.search(r'"[^"]*veintiuno[^"]*"\s*:\s*("[^"]{0,220}")', raw, re.I)
    if m: print('   muestra:', m.group(1)[:200])
    print()
