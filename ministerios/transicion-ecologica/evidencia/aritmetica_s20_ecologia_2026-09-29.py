import json

# ---------- 1) Reparto por cuenca del 40,9 M€ (metodo: deficit en puntos vs media nacional) ----------
NACIONAL = 60.3
CUENCAS = {   # % oficiales del NdP MITECO 22-09-2026 archivado en el repo
    'Ebro': 47.9,
    'Júcar': 51.2,
    'Segura': 51.7,
    'Galicia Costa': 53.7,
    'Duero': 53.9,
}
MONTANTE = 40.9  # M€

deficits = {k: round(NACIONAL - v, 1) for k, v in CUENCAS.items()}
total_def = round(sum(deficits.values()), 1)
eur_por_punto = MONTANTE / total_def

reparto = {}
for k, d in deficits.items():
    reparto[k] = round(MONTANTE * d / total_def, 2)

print('deficits (puntos vs 60,3%):', deficits)
print('total deficit:', total_def)
print('M€ por punto de deficit:', round(eur_por_punto, 4))
print('reparto M€:', reparto)
print('SUMA reparto:', round(sum(reparto.values()), 2), 'vs montante', MONTANTE)
print('cuadre ok:', abs(sum(reparto.values()) - MONTANTE) < 0.05)

# ---------- 2) Escalada del precio de la luz de HOY (OMIE, 29-09-2026) ----------
horas = {
    '00-01': 209.80, '01-02': 202.51, '02-03': 186.07, '03-04': 175.04, '04-05': 162.52,
    '05-06': 167.69, '06-07': 190.70, '07-08': 224.15, '08-09': 220.10, '09-10': 172.80,
    '10-11': 87.34, '11-12': 15.22, '12-13': 3.89, '13-14': 1.53, '14-15': 1.08,
    '15-16': 1.11, '16-17': 4.08, '17-18': 55.25, '18-19': 121.98, '19-20': 204.75,
    '20-21': 213.02, '21-22': 181.41, '22-23': 172.90, '23-24': 147.40,
}
media_src = 130.10
maxi = max(horas.values()); mini = min(horas.values())
h_max = [h for h, v in horas.items() if v == maxi][0]
h_min = [h for h, v in horas.items() if v == mini][0]
central = ['11-12', '12-13', '13-14', '14-15', '15-16', '16-17']
media_central = sum(horas[h] for h in central) / len(central)
print('\nmax', maxi, 'a las', h_max, '| min', mini, 'a las', h_min)
print('spread max-min:', round(maxi - mini, 2), '€/MWh')
print('ratio max/min:', round(maxi / mini, 2), 'veces')
print('min como % de la media:', round(100 * mini / media_src, 2), '%')
print('media 11:00-17:00 (6 horas):', round(media_central, 3), '€/MWh')
print('horas por debajo de 16 €/MWh:', sum(1 for v in horas.values() if v < 16))
print('horas por encima de 200 €/MWh:', sum(1 for v in horas.values() if v > 200))
print('media aritmetica de las 24 horas del fichero OMIE:', round(sum(horas.values()) / 24, 2),
      '(la fuente publica 130,10)')

# ---------- 3) cuadre de la reasignacion de ayer ----------
print('\n1.362 - 40,9 =', round(1362 - 40.9, 1), 'M€ restantes')
print('40,9 / 9.615 =', round(100 * 40.9 / 9615, 3), '% del credito definitivo cap.4/6/7')
print('40,9 / 1.362 =', round(100 * 40.9 / 1362, 3), '% del no ejecutado')
print('9.615 - 8.252 =', round(9615 - 8252, 1), 'M€ (descuadre declarado de 1 M€ frente a la fuente: 1.362)')
