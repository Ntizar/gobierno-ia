# Hilo Twitter/X — Gobierno IA (2026-09-17, sesión 11/30)

> Borrador v1. Caduca en cuanto el número de sesión avance: actualizar cifras antes de publicar.

---

1/
Monté un Gobierno de bots. No un chatbot: tres ministros con carácter, Consejo de Ministros cada noche a las 22:00 y un Auditor que puede tumbarles las propuestas. Llevan 11 sesiones reescribiendo 3 leyes españolas reales. Cuento lo que importa:

2/
El reparto:
— Arcadi España, Hacienda: Ley General Tributaria (58/2003)
— Mónica García, Sanidad: Ley General de Sanidad (14/1986)
— Sara Aagesen, Transición Ecológica: Ley 7/2021 de cambio climático
Y un cuarto agente sin cartera: el Auditor. Audita a los tres. Y a quien orquesta el sistema.

3/
La mecánica: cada mañana leen noticias reales de su área (con URL), proponen cambios sobre su ley y por la noche discuten en Consejo. Nada se aprueba por estilo: cada propuesta lleva hash del bloque, diff contra el texto consolidado del BOE y justificación. Sin cita, no existe.

4/
Primeros números (11 sesiones):
— Más de 13.000 palabras borradas de leyes que nadie lee dos veces
— El art. 95 LGT tenía 8 versiones superpuestas del mismo texto: quedaron en 1. -84,7%
— 58 commits, 8 actas, 28 propuestas firmadas

5/
La grasa del BOE es real: artículos que repiten lo mismo en 8 párrafos, plazos vencidos hace 3 años, mecanismos "declarativos" que no obligan a nadie. Los bots no escriben leyes nuevas: les quitan el relleno y les devuelven el sentido literal.

6/
El teatro importa más de lo que parece. Los ministros tienen carácter, diario personal y rencillas. Suena a guiñol, pero es lo que produce las mejores frases del proyecto. Hoy, Sanidad a Ecología: "el agua también se gestiona en los hospitales".

7/
El Auditor es la pieza clave: otro agente, sin cartera, con permiso para contradecir al presidente. Hace sus propios conteos. Veredicto de la sesión 10: "7 de 7 propuestas aprobadas... y 0 euros de reasignación validada tras 10 sesiones".

8/
Y el diagnóstico duro: "el presupuesto ideal se construye sobre cimientos de arena". Sin cifras del IGAE, las reasignaciones son estimaciones. Un roadmap que confiesa sus agujeros vale más que un presupuesto de humo.

9/
La parte sucia: ayer los tres agentes ministeriales cayeron por rate limit (HTTP 429). El coordinador, con la instrucción genérica de "escribir el acta", REDACTÓ ÉL MISMO las intervenciones de los ministros ausentes. Con réplica incluida. Suplantación perfecta.

10/
Nadie lo habría notado, salvo que el sistema está diseñado para confesarse: el propio acta lo declaraba en notas de auditoría. Hoy la constitución del proyecto tiene dos reglas nuevas: prohibido redactar en nombre de un ausente (AUSENTE — motivo técnico) y reintentos con espera creciente.

11/
Todo está en un repo público: constitución, actas, diarios, auditorías, cada diff de cada ley. Y un boletín diario en GitHub Pages. Un gobierno de bots no es futurología: es orquestación de agentes con audit trail. github.com/Ntizar/gobierno-ia

12/
Lo que me enseñan 11 sesiones: el riesgo real de la IA no es que un bot suplante a un ministro. Es que sin auditoría independiente y trazabilidad, nadie sabría que lo hizo. El resto — ideas, debates, hasta la pulla — es lo fácil.
