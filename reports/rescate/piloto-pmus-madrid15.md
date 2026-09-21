# Piloto PMUS/Madrid15 — Fase 6

**Estado:** PROTOCOLO LISTO, VALIDACIÓN PENDIENTE

## Pregunta de producto

> "¿Cómo cambiar esta norma para mejorar el acceso a empleo y servicios por modo, con coste y distribución territorial visibles?"

## Alcance

- **Ciudad:** Madrid
- **Norma:** Ordenanza Municipal de Movilidad de Madrid (o normativa equivalente)
- **3 medidas concretas:**
  1. **Zona de bajas emisiones ampliada** — extender la ZBE al radio de 5km del centro
  2. **Prioridad al transporte público** — carril BUS-VO en 10 ejes principales
  3. **Movilidad activa** — 50km de carriles bici protegidos conectados

## Dataset Madrid15

| Dataset | URL | Editor | Versión/Fecha | Licencia | Campos usados |
|---|---|---|---|---|---|
| Datos abiertos Madrid | datos.madrid.es | Ayto. Madrid | 2024 | Open Data Commons | Movilidad, emisiones, población |
| GTFS EMT Madrid | EMT Madrid | EMT | 2024 | Open Data Commons | Paradas, rutas, frecuencias |
| Padrón municipal | datos.madrid.es | INE/Ayto. | 2024 | Open Data Commons | Población por barrios |
| Accidentes DGT | dgterial.dgt.es | DGT | 2023 | Open Data Commons | Siniestralidad vial |

## Roles funcionales

| Rol | Responsabilidad |
|---|---|
| Lenguaje claro | Redactar propuestas en lenguaje comprensible por ciudadanos |
| Abogado del diablo | Señalar riesgos,objeciones y efectos no deseados |
| Impacto distributivo | Analizar ganadores/perdedores por zona, nivel socioeconómico, modo |
| Presupuesto | Estimar costes con fuentes verificables |
| Auditor de evidencia | Verificar que cada cifra tiene fuente, versión y hash |

## Protocolo de prueba

1. **5 usuarios objetivo:** 2 peatones, 1 conductor, 1 ciclista, 1 usuario de transporte público
2. **Tarea:** Completar una ruta从A a B usando la herramienta de comparación antes/después
3. **Métrica:** Tiempo de tarea, errores, satisfacción (1-5), intención de uso (sí/no)
4. **Umbral de validación:** 5/5 completan la tarea, ≥2 declaran que usarían el resultado en un encargo real
5. **Revisión:** 1 técnico de movilidad + 1 jurista

## Estado

| Entregable | Estado |
|---|---|
| Pregunta de producto | ✅ Definida |
| 3 medidas concretas | ✅ Definidas |
| Protocolo de prueba | ✅ Definido |
| Datos integrados | ⏳ Pendiente Fase 6 ejecución |
| Mapa antes/después | ⏳ Pendiente Fase 6 ejecución |
| Propuesta como parche | ⏳ Pendiente Fase 6 ejecución |
| Prueba con 5 usuarios | ⏳ PENDIENTE_REVISION_HUMANA |
| Revisión técnico + jurista | ⏳ PENDIENTE_REVISION_HUMANA |

## Resultado

**VALIDACION_USUARIO_PENDIENTE** — La fase técnica puede quedar completa, pero el piloto de producto no se declara validado hasta obtener 5 pruebas reales y 2 señales de uso profesional.
