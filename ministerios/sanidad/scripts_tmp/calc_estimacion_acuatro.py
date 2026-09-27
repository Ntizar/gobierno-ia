# ESTIMACION [acuatro] — sesion 18 — 2026-09-27 — Monica Garcia, Sanidad
# METODO Etiquetado ESTIMACION: censo oficial de lista de espera quirurgica (datos 2025
# corregidos, publicados 24-09-2026) x coste medio oficial por alta del SNS (RAE-CMBD 2024,
# provisional). Escenario de tope maximo: resolver EL 100% del censo con actividad
# ordinaria (sin margen de productividad ni ahorro por sustitucion). NO es el coste de
# garantizar el plazo: es el techo del coste de la cola actual.
# Fuentes verificadas hoy en disco:
#  F1 censo 853.740 pacientes y media nacional 122 dias: ConSalud 2026-09-24 (Min. Sanidad),
#     https://www.consalud.es/politica/ministerio-sanidad/sanidad-actualiza-los-datos-de-lista-de-espera-aumenta-la-media-nacional.html
#     (grep propio en espera.html descargada hoy: '853.740' y 'hasta los 122 dias')
#  F2 RAE-CMBD 2024 (Min. Sanidad, PROVISIONAL): 1.245.134 altas de los 25 procesos
#     QUIRURGICOS mas frecuentes a 8.758,7 EUR/alta; total altas hospitalizacion agudos SNS
#     3.829.395 a 6.004,9 EUR/alta.
#     https://www.sanidad.gob.es/estadEstudios/estadisticas/docs/CMBD/2024_nota_metodologica_costes.pdf
#     https://vsf-iwsold-pro-portal.sanidad.gob.es/eu/estadEstudios/estadisticas/docs/CMBD/2024Obstetricos_Quirurgicos.pdf
censo = 853740
coste_quir = 8758.7
coste_global = 6699.0
techo = censo * coste_quir / 1e6
suelo = censo * coste_global / 1e6
print("CENSO (F1): " + f"{censo:,}" + " pacientes en lista de espera quirurgica")
print("MEDIA NACIONAL (F1): 122 dias -> >90: el plazo prioritario del texto aprobado de la 17 se incumple ya de media; <180: el ordinario se cumple de media")
print("TECHO escenario 100x100 censo al coste de los 25 procesos quirurgicos mas frecuentes (F2): " + f"{techo:,.1f}" + " M EUR")
print("SUELO mismo censo al coste medio de los 25 procesos mas frecuentes (F2): " + f"{suelo:,.1f}" + " M EUR")
print("-> RANGO a afinar por la IGAE: entre " + f"{suelo:,.0f}" + " y " + f"{techo:,.0f}" + " M EUR")
