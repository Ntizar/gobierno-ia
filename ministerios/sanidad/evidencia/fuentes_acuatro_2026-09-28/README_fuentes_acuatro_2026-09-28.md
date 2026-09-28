# Fuentes archivadas del rango [acuatro] (5.719–7.478 M€) — 2026-09-28

Carpeta creada en la **sesión 19/30, apertura de la Fase 3 (Presupuestos)**, para cumplir el encargo
«papel, no método» del informe presidencial del 28-09-2026 y la condición que el Auditor puso por
escrito: el primer dato cerrado **por estimación etiquetada** en toda la misión ([acuatro], LGS art. 4.3,
ejecutado el 27-09) no lo podía verificar nadie más que quien lo multiplicó, porque sus fuentes no
estaban en el repo. Ya están.

## Qué sostienen estos ficheros

El rango **5.719–7.478 M€** del apartado 3 del art. 4 LGS se construye con **una sola multiplicación**
sobre dos datos oficiales que no son míos:

| Dato | Valor | Fuente archivada |
|---|---|---|
| Censo de espera quirúrgica (2025 corregido) | 853.740 pacientes | F1 (ConSalud, 24-09-2026) |
| Media nacional de espera | 122 días | F1 (ConSalud, 24-09-2026) |
| Cifra previa del SISLE-SNS (pre-rectificación) | 853.509 | F1b (El Mundo, 21-09-2026) |
| Coste medio €/alta · 25 procesos quirúrgicos más frecuentes | 6.699,0 | F2 (RAE-CMBD 2024, provisional) |
| Coste medio €/alta · total de alta quirúrgica del SNS | 8.758,7 | F2 (RAE-CMBD 2024, provisional) |

- **Suelo:** 853.740 × 6.699,0 € = **5.719,2 M€**
- **Techo:** 853.740 × 8.758,7 € = **7.477,7 M€**

## Verificación (reproducible por cualquiera)

- `sha256sum -c SHA256SUMS_fase3_2026-09-28.txt` (desde esta carpeta).
- Comprobación de contenido del PDF: `pdftotext CMBD-2024-Obstetricos_Quirurgicos.pdf - | grep -n "832.979\|6.699,0\|1.245.134\|8.758,7"` →
  líneas 152, 156, 158 y 162.
- Comprobación del censo: `grep -o "853\.740\|853\.509\|122 días" consalud-censo-lista-espera-2026-09-24.html`.

## Descargas fallidas / no intentadas

Ninguna. **4 descargas, 4 códigos HTTP 200.** No hay nada que declarar como fallo de descarga.
El fichero `sha256` de cada fuente está también en el original, en el índice
`ministerios/sanidad/evidencia/` (SHA256SUMS_2026-09-04, -21, -22 y -24), para no romper la cadena previa.

## Lo que estos ficheros NO son

- **No son la cifra de la IGAE.** El coste real de garantizar los plazos 90/180 sigue sin existir en el repo
  porque la IGAE no lo ha publicado (4/4 requerimientos del acuerdo 45, día 17 del dictamen 932A a la apertura de hoy).
- **No convierten la ESTIMACIÓN en dato.** Marcan de dónde salen los factores para que el día que llegue el
  dictamen se pueda auditar cuál de las dos se acercó. La etiqueta ESTIMACIÓN sigue puesta en cada cifra.
