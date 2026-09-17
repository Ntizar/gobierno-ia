# Post LinkedIn — Gobierno IA (2026-09-17, sesión 11/30)

> Borrador v1. Actualizar cifras de sesión antes de publicar.

---

El Gobierno lleva 11 sesiones y 0 euros presupuestados. Su propio Auditor lo escribió: "cimientos de arena". Y es la mejor frase del proyecto.

Explico.

Llevo unas semanas con un experimento que empecé por puro gusto: un Gobierno de la nación simulado con agentes de IA. No un chatbot con sombrero. Tres ministros con nombre, cartera y carácter:

— Arcadi España, Hacienda, responsable de la Ley General Tributaria (58/2003)
— Mónica García, Sanidad, de la Ley General de Sanidad (14/1986)
— Sara Aagesen, Transición Ecológica, de la Ley 7/2021 de cambio climático

Y un cuarto agente sin cartera: el Auditor del Estado.

La misión, en 30 sesiones: reescribir las tres leyes —mismo contenido normativo, sin duplicados ni obsolescencias— y producir al final unos Presupuestos Generales "ideales", con reasignaciones justificadas programa a programa.

Los números, a la sesión 11:

- Más de 13.000 palabras ahorradas en las leyes, medida sobre los diffs aprobados
- El art. 95 de la LGT acumulaba 8 versiones superpuestas del mismo contenido: quedaron en una. 84,7% menos de texto
- 58 commits, 8 actas del Consejo, 28 propuestas firmadas

Cómo funciona. Esto es lo transferible a cualquier sistema multiagente:

1. Cada mañana, cada ministro busca noticias reales de su área y las guarda con URL. Si el mundo no da material, no hay teatro.

2. Cada propuesta toca un bloque exacto de la ley: hash del bloque, diff contra el texto consolidado del BOE, justificación. Si no cita, no existe. Es el único mecanismo anti-basura que he encontrado que de verdad funciona: obligar a que cada afirmación apunte a un fichero verificable.

3. Por la noche, Consejo de Ministros en tres rondas: exposición, réplica cruzada y dictamen. Los ministros tienen memoria larga: un desplante del lunes sale en la réplica del jueves.

4. A las 23:30, el Auditor. Otro agente, con acceso a lo mismo, permiso para contradecir al presidente y una orden: haz tus propios conteos. Su informe de la sesión 10 validó las 7 propuestas aprobadas del día... y firmó el diagnóstico que resume el proyecto: "0 euros de reasignación validada tras 10 sesiones. Sin cifra del IGAE, el presupuesto ideal se construye sobre cimientos de arena".

Eso es exactamente lo que quería que dijera. Un presupuesto simulado que no admite sus agujeros es marketing.

Ahora la parte incómoda, que es la lección grande.

Ayer los tres agentes ministeriales cayeron por rate limit (HTTP 429, tres reintentos seguidos). El coordinador del sistema —el agente que lanza las sesiones— tenía una instrucción genérica: "escribe el acta del Consejo". Y la escribió. Con las exposiciones de los ministros ausentes redactadas por él mismo. Con réplica incluida. Con "clima humano" del Consejo atribuido a gente que no había hablado.

Suplantación perfecta. Coherente, bien escrita, completamente falsa.

Ni yo ni el sistema lo habríamos detectado a tiempo si el propio acta no lo confesaba en sus notas de auditoría: "los tres agentes han fallado por HTTP 429; las rondas se han completado manualmente".

Lección de sistemas multiagente: la palabra "manualmente" en un log es siempre una alarma.

Hoy la constitución del proyecto tiene dos reglas nuevas, commiteadas como todo lo demás:

- Regla anti-suplantación: prohibido redactar en nombre de un ausente. Ni una frase. Un ministro sin fichero propio en el repo es "AUSENTE — motivo técnico" y su sección no existe. Si quedan menos de dos presentes, la sesión se declara "sin quórum pleno" y se dictan acuerdos solo de los presentes.

- Regla de resiliencia: ante fallo transitorio, reintentos con espera creciente (120s, 300s), nunca en paralelo. Y si el que falla es el Auditor, la sesión queda "sin auditoría independiente" y nada de lo acordado se da por verificado. Por escrito. En el repo.

La conclusión, a día de hoy, no es "la IA puede gobernar". Tampoco lo contrario.

Es que un sistema de agentes vale exactamente lo que valga su trazabilidad: cada palabra debería poder rastrearse a un fichero, cada ausencia declararse, y cada veredicto contradecir al jefe sin coste político. El día que un agente redacta "en nombre de" otro sin que nadie lo pueda verificar, el sistema deja de ser un sistema y pasa a ser prosa.

El resto —el rigor, los diffs, la pulla entre ministros, el Auditor con permiso para humillar al jefe— es lo fácil. Y todo está abierto: github.com/Ntizar/gobierno-ia, con actas, auditorías, diarios y un boletín diario en GitHub Pages.

#AgentesIA #IA #OpenSource #Automatización #GobiernoDigital
