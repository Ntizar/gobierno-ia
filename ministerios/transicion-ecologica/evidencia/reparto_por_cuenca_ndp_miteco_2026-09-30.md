# Reparto por cuenca de la reserva hídrica estratégica (art. 19.4.h L7/2021) — NdP OFICIAL del MITECO

**Sesión 21/30 · 2026-09-30 · Ministerio para la Transición Ecológica (Sara Aagesen).**
Entrega de la **condición 2 del acuerdo 110** en su versión corregida por fuente primaria. Sustituye al reparto entregado el 29-09 (que se hizo sin el boletín oficial delante).

## Fuente primaria (en el repo)

`evidencia/fuentes_s21_2026-09-30/NdP_reserva_hidrica_2026-09-29.pdf`
«La reserva hídrica española se encuentra al 59,2 % de su capacidad» — Nota de prensa del MITECO, 29-09-2026.
Descargada hoy: **HTTP 200**, **242.492 bytes**, 2 páginas, sha256 `46d9ecc7918d7e0e600ad7e14cb5b919ddb04192a892659c3a88b0cf00ba1767`.
Datos del cuadro adjunto del NdP: **TOTAL PENINSULAR 56.043 hm³ de capacidad / 33.204 hm³ embalsados / 30.827 hace un año / 24.984 media de diez años**; **−597 hm³ (−1,1 %) en una semana**; precipitaciones «nulas en la vertiente Mediterránea y prácticamente nulas en la vertiente Atlántica»; máxima en A Coruña, 10,6 l/m².

## Método (declarado entero, sin partes implícitas)

1. **Universo**: cuencas peninsulares cuya reserva publicada está **por debajo de la media nacional** (59,2 %). Quedan fuera, y se enumeran para que nadie tenga que preguntarlo: Guadiana 72,1 %, Guadalete-Barbate 75,9 %, Cuencas internas de Cataluña 73,6 %, Cuencas internas del País Vasco 71,4 %, Guadalquivir 69,6 %, Tinto-Odiel y Piedras 65,1 %, Cuenca Mediterránea Andaluza 64,3 %, Cantábrico Oriental 60,3 %.
2. **Peso**: **déficit en puntos porcentuales** frente a la media nacional (no hm³, no superficie).
3. **Importe a repartir**: **40,90 M€**, el aprobado en el acuerdo 122. **No cambia el total, ni el destino (capítulo 6), ni la vía jurídica: solo cambia el reparto.**
4. Aritmética con script: `evidencia/aritmetica_s21_ecologia_2026-09-30.py` → `aritmetica_s21_ecologia_2026-09-30.json`. € por punto = 40,90 / 50,6 = **0,8083**.

## Reparto resultante

| Cuenca | Reserva (NdP 29-09) | Déficit (puntos) | M€ |
|---|---|---|---|
| Ebro | 46,0 % | 13,2 | 10,67 |
| Segura | 50,1 % | 9,1 | 7,36 |
| Duero | 51,4 % | 7,8 | 6,30 |
| Galicia Costa | 51,8 % | 7,4 | 5,98 |
| Júcar | 51,9 % | 7,3 | 5,90 |
| Tajo | 54,9 % | 4,3 | 3,48 |
| Miño-Sil | 58,3 % | 0,9 | 0,73 |
| Cantábrico Occidental | 58,6 % | 0,6 | 0,48 |
| **Suma** | media nacional **59,2 %** | **50,6** | **40,90** |

**Cuadre: 40,90 M€ repartidos sobre 40,90 M€ a repartir (diferencia 0,00).**

## Cotejo con el reparto del 29-09 (y la enmienda, dicha por su autora)

| Cuenca | 29-09 (M€) | 30-09 (M€) | Δ |
|---|---|---|---|
| Ebro | 11,77 | 10,67 | **−1,10** |
| Segura | 8,16 | 7,36 | **−0,80** |
| Duero | 6,07 | 6,30 | **+0,23** |
| Galicia Costa | 6,26 | 5,98 | **−0,28** |
| Júcar | 8,64 | 5,90 | **−2,74** |
| Tajo | — | 3,48 | **+3,48 (entra)** |
| Miño-Sil | — | 0,73 | **+0,73 (entra)** |
| Cantábrico Occidental | — | 0,48 | **+0,48 (entra)** |
| **Total** | **40,90** | **40,90** | **0,00** |

**La enmienda es mía y la firmo yo:** el reparto de ayer usaba una foto que no era la del boletín oficial. Con la fuente primaria delante, mi propio criterio («cuencas por debajo de la media nacional») exige **ocho** cuencas, no cinco, y las tres que faltaban entran. El dinero no cambia de sitio ni de capítulo: cambia de cuenca, y cambia porque el dato es otro.

## Vía jurídica (Ley 47/2003 General Presupuestaria, fichero del repo)

- **Art. 63.1.a)** (línea 1551 de `evidencia/lgp_texto_limpio_s21_ecologia_2026-09-30.txt`): transferencias entre créditos de un mismo programa o de programas de un mismo servicio, «incluso con la creación de créditos nuevos en el caso de los destinados a compra de bienes corrientes y servicios o **inversiones reales**», previo informe favorable de la **Intervención Delegada** (línea 1550).
- **Art. 52.1.a)** (línea 1294): no hay salto de operaciones de capital a corrientes — el destino se queda en **capítulo 6**.
- **Arts. 42** (línea 1143) y **46** (línea 1194): especialidad y limitación de los créditos → **coste fiscal neto 0 €**.
- Si el destino cae en un servicio distinto: **art. 62.1.a)** (línea 1536, firma del Ministro de Hacienda).

## Indicadores de éxito (medibles, con plazo)

1. Reparto por cuenca **firmado y publicado antes del 30-06-2027**.
2. **hm³ designados** bajo figura de reserva estratégica antes del 30-06-2027 — línea base **0 hm³**; el hm³ exige el coste unitario por actuación: **hoy no se estima** (casilla vacía).
3. **Ejecución del capítulo 6 del MITECO ≥ 95 % en 2027** — línea base 85,82 % (2024, **ESTIMACIÓN** de fuente secundaria).
4. Plazo de la transferencia: **antes del 31-12-2026** (92 días).

*Sara Aagesen, 2026-09-30.*
