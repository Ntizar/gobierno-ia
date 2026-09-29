# Reparto por cuenca de la reserva hídrica — entrega de la condición 2 del acuerdo 110
**Sesión 20/30 · 2026-09-29 · MITECO — Transición Ecológica**

## Qué se entrega
El acuerdo 110 (sesión 19) aprobó con dos condiciones la reactivación de la línea «Reserva hídrica estratégica»: (1) la base de 1.362 M€ es fuente secundaria y el importe queda etiquetado como estimación; (2) **el reparto por cuenca se publica con hm³ designados antes del 30-06-2027**. Esto es la entrega de la condición 2 en su parte hoy posible: **método declarado + reparto en euros por cuenca + plazo del hm³**.

## Ancla legal (corregida hoy, ver `verificacion_apertura_s20_2026-09-29.md`)
- **Ley 7/2021 (repo: `leyes/BOE-A-2021-8447.md`), bloque `[a1-11]` — art. 19.4.h)**, texto literal: «Elaborar el plan de financiación de las actuaciones asegurando la financiación para abordar los riesgos del apartado primero.»
- **NO** el `[a1-7]`: verificado línea a línea, ese bloque es «Artículo 15. Instalación de puntos de recarga eléctrica» (líneas 401-433). La cita anterior era errónea y queda rectificada.
- Vía presupuestaria: **art. 63.1.a) LGP** (mismo programa / mismo servicio, previo informe favorable de la Intervención Delegada) o, si el destino cae en otro servicio, **art. 62.1.a) LGP**.

## Datos de partida (oficiales, ya en el repo)
NdP del MITECO «La reserva hídrica española se encuentra al 60,3 % de su capacidad» (22-09-2026), archivado en `evidencia/agua_miteco_reserva_hidrica_60-3_2026-09-28.html`, sha256 `433f9009…`. Reserva nacional: **33.801 hm³ = 60,3 %**. Por ámbitos, los cinco que están por debajo de la media nacional:

| Ámbito | Reserva | Déficit vs media (puntos) |
|---|---|---|
| Ebro | 47,9 % | 12,4 |
| Júcar | 51,2 % | 9,1 |
| Segura | 51,7 % | 8,6 |
| Galicia Costa | 53,7 % | 6,6 |
| Duero | 53,9 % | 6,4 |
| **Total déficit** | | **43,1 puntos** |

(El resto de ámbitos está en o por encima de la media: Tajo 55,5 %, Cantábrico Oriental y Miño-Sil 60,3 %, Cantábrico Occidental 61,2 %, Cuenca Mediterránea Andaluza 65,1 %, Tinto-Odiel-Piedras 67,7 %, Guadalquivir 70,3 %, País Vasco 71,4 %, Guadiana 72,4 %, Cataluña 74,4 %, Guadalete-Barbate 76,3 %.)

## Método (convención de la proponente, declarada)
1. Se reparte **solo entre las cinco cuencas por debajo de la media nacional**.
2. El peso de cada cuenca es su **déficit en puntos porcentuales** respecto de la media nacional (60,3 %). Ni superficie, ni población, ni litros de titular: **déficit medido**.
3. Montante a repartir: **40,9 M€** (el 3 % —convención de la proponente— de los 1.362 M€ de crédito no ejecutado del capítulo 4/6/7 del MITECO en 2024, fuente secundaria declarada).
4. Aritmética ejecutada con script (`evidencia/aritmetica_s20_ecologia_2026-09-29.py`), no de cabeza.

## Reparto resultante (M€; 0,949 M€ por punto de déficit)

| Cuenca | M€ | % del total |
|---|---|---|
| Ebro | **11,77** | 28,8 % |
| Júcar | **8,64** | 21,1 % |
| Segura | **8,16** | 20,0 % |
| Galicia Costa | **6,26** | 15,3 % |
| Duero | **6,07** | 14,8 % |
| **Suma** | **40,90** | 100 % |

Cuadre verificado: la suma de las cinco cifras es **40,90 M€** frente al montante de 40,9 M€ (diferencia 0,00).

## Lo que AÚN NO se entrega (y por qué no se inventa)
- **hm³ designados**: la conversión de euros a hm³ exige el **coste unitario por hm³ de actuación** (depende de la medida: restauración, reutilización, regulación, demanda). No lo tengo ni con fuente oficial ni con serie histórica homogénea para las cinco cuencas. Se entrega el **€ y el método**, y el hm³ se fecha: **antes del 30-06-2027**, con el coste unitario fijado por las confederaciones hidrográficas y la Intervención Delegada. Es la letra de la condición 2.
- **Base oficial de 1.362 M€**: sigue pendiente la liquidación del MITECO (6 URL en dos días, sin documento). La cifra va marcada **ESTIMACIÓN (fuente secundaria)**.

## Indicadores de éxito (medibles, con plazo)
1. **Reparto por cuenca publicado y firmado antes del 30-06-2027** — hoy: entregado el € por cuenca y el método; falta el hm³.
2. **hm³ designados bajo figura de reserva estratégica antes del 30-06-2027** — hoy: 0 hm³ con esa figura (§ el `[a1-11]` no la crea: la crea la línea presupuestaria y su acuerdo de designación).
3. **Grado de ejecución del capítulo 6 del MITECO ≥ 95 % en 2027** — línea base: 85,82 % en 2024 (fuente secundaria declarada).
