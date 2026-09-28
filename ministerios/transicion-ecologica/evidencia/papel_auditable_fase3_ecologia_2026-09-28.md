# Papel de la Transición Ecológica para hacer auditable la Fase 3 — 2026-09-28

**Ministerio para la Transición Ecológica y el Reto Demográfico · sesión 19/30 · apertura de la Fase 3.**
**Encargo del acuerdo 100 (Hacienda + Ecología, entrega HOY). Ministra: Sara Aagesen.**

Todo lo que sigue está medido, descargado o citado del fichero que está en el repo. Lo que no, va declarado como lo que es: una ESTIMACIÓN con método a la vista o una casilla vacía con la URL intentada y el error. La emoción no sustituye a la cifra.

---

## 1. La ley no se toca — verificación de apertura (regla no negociable)

| Medición | Valor |
|---|---|
| sha256 `leyes/BOE-A-2021-8447.md` a las 10:45 | `dc4b46439a587321bc7837f9918abe7d26e9d676a395024ceef81a576a4756a3` |
| sha256 del mismo fichero tras toda la descarga del día (10:46) | `dc4b46439a587321bc7837f9918abe7d26e9d676a395024ceef81a576a4756a3` |
| Palabras / bloques | **27.307 palabras · 71 bloques** |
| Hash de apertura declarado por Presidencia | `dc4b4643…` → **coincide al dígito** |
| `git status --short ministerios/transicion-ecologica/` a la apertura | *(vacío: la ley no aparece)* |
| `git status --short` al cierre de la descarga | `?? …/evidencia/agua_miteco_reserva_hidrica_60-3_2026-09-28.html` (el NdP que archivo hoy; **ninguna ley en el diff**) |

**Conclusión:** no hay diff aprobado pendiente. **Deuda de ejecución = 0 desde el 27-09.** No se aplica ningún diff y no se re-aplica ninguno ya ejecutado — hoy esta cartera no escribe ni una letra de ley: escribe y audita presupuesto.

---

## 2. (a) Ley 47/2003, de 26 de noviembre, General Presupuestaria — **YA ESTÁ EN EL REPO**

**No la he vuelto a descargar.** La bajó Hacienda hoy, en el encargo conjunto del acuerdo 100, a `ministerios/hacienda/evidencia/`. Lo que he hecho es **verificarla y leerla** (la descarga duplicada no es rigor, es ruido):

| Documento | Fichero | URL | Fecha | sha256 (medido por mí hoy) |
|---|---|---|---|---|
| Ley 47/2003 consolidada (HTML) | `ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html` | https://www.boe.es/buscar/act.php?id=BOE-A-2003-21614 | 2026-09-28 | `823c8cbdaf29f1af1dbf3e5392436471febd2a561210b24dc6cf5a98d0d5db4a` |
| Ley 47/2003 consolidada (PDF) | `ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.pdf` | https://www.boe.es/buscar/pdf/2003/BOE-A-2003-21614-consolidado.pdf | 2026-09-28 | `2c916bcea5e811b6d0dae4503b1e736d9c968178f1cc3b5fff664634c6e3a20b` |

Coinciden con los declarados por Hacienda en `SHA256SUMS_fase3_2026-09-28.txt` (`823c8cbd…`, `2c916bce…`).

**Verificación del identificador por el título, no por el nombre del fichero** (regla que nació del incidente del 21615/21615-bis de Hacienda): el `<title>` del HTML del repo dice literalmente «BOE-A-2003-21614 Ley 47/2003, de 26 de noviembre, General Presupuestaria.» → **coincide**.

### 2.1 El articulado que necesito, leído hoy por mí en el fichero del repo (no de memoria)

Leyenda: la columna «línea» es la línea del HTML consolidado archivo en el repo.

| Art. | Encabezado verificado | Línea | Lo que dice, literal, y para qué lo uso |
|---|---|---|---|
| 42 | «Especialidad de los créditos» | 3739 | «Los créditos para gastos se destinarán exclusivamente a la finalidad específica para la que hayan sido autorizados por la Ley de Presupuestos o a la que resulte de las modificaciones aprobadas conforme a esta ley.» → es el ancla de toda reasignación: mover dinero es cambiar la finalidad, y eso solo cabe por las vías del art. 52/62/63. |
| 46 | «Limitación de los compromisos de gasto» | 3842 | «Los créditos para gastos son limitativos… siendo nulos de pleno derecho los actos administrativos… que incumplan esta limitación.» |
| 47 | «Compromisos de gasto de carácter plurianual» | 3852 | Máximo **4 ejercicios**, topes **70 % / 60 % / 50 % / 50 %** del crédito inicial (art. 47.2). → condiciona cualquier plan de inversión hídrica a más de un ejercicio. |
| 50 | «Fondo de Contingencia de ejecución presupuestaria» | 3945 | Existe y tiene régimen propio; **su importe no lo estimo** (Hacienda ya declaró que sin el detalle de transferencias a CCAA y EELL la base no es calculable). |
| 52 | **«Transferencias de crédito»** | 4007 | 52.1: «Las transferencias son traspasos de dotaciones entre créditos… con las siguientes restricciones:» **a)** «No podrán realizarse desde créditos para operaciones financieras al resto de los créditos, ni desde créditos para operaciones de capital a créditos para operaciones corrientes»; **b)** «No podrán realizarse entre créditos de distintas secciones presupuestarias»; **c)** no minoran créditos extraordinarios/supletorios. Y 52.2: las restricciones **no** afectan a las transferencias derivadas de «convenios o acuerdos de colaboración entre distintos departamentos ministeriales, órganos del Estado con secciones diferenciadas… u organismos autónomos». |
| 62 | «Competencias del Ministro de Hacienda» | 4436 | 62.1.a): **Hacienda autoriza** «las transferencias no reservadas a la competencia del Consejo de Ministros que, conforme al artículo 63, no puedan acordarse directamente por los titulares de los departamentos afectados». |
| 63 | **«Competencias de los ministros»** | 4471 | 63.1: los titulares de los ministerios autorizan, **previo informe favorable de la Intervención Delegada**, 63.1.a): «Transferencias entre créditos de **un mismo programa** o **entre programas de un mismo servicio**, incluso con la creación de créditos nuevos en el caso de los destinados a compra de bienes corrientes y servicios o inversiones reales…». Y 63.2: los presidentes y directores de organismos y entidades del art. 3.1 (aquí encaja el IDAE) tienen estas competencias «a favor de los ministros, quienes podrán avocarlas». |

### 2.2 Corrección que aporto al papel conjunto (rigor, no reproche)

Hacienda cita la vía de la transferencia interna como «**art. 63.1.a) LGP**» y la titula «transferencias entre créditos». **El encabezado del art. 63 es «Competencias de los ministros»; el artículo que se llama «Transferencias de crédito» es el 52.** El 63.1.a) es la letra que habilita, no el régimen general.

Y hay una consecuencia práctica que importa esta noche:

- **El 63.1.a) solo alcanza «un mismo programa» o «programas de un mismo servicio».** Un movimiento **entre dos servicios distintos** (por ejemplo, el presupuesto de un organismo como el IDAE y el de la DG de Energía) **no cabe** ahí.
- Ese movimiento es exactamente el supuesto del **art. 62.1.a)**: lo autoriza el **Ministro de Hacienda**, porque es la transferencia que «conforme al artículo 63» los titulares no pueden acordar por sí solos.
- La alternativa que el propio art. 52.2 abre, y que hasta hoy nadie había leído en este expediente, es que las transferencias derivadas de **convenios o acuerdos de colaboración** entre ministerios/organismos **no están sujetas a las restricciones** del art. 52.1.

Esto es lo que hace auditable la Fase 3 en mi ámbito: ya no discutimos de memoria sobre «la regla presupuestaria de entes» que archivó mis 1,2 M€ el 27-09 — la regla está delante, con su letra y su línea, y se puede citar en la mesa.

### 2.3 Lo que NO uso de la Ley 47/2003
No he verificado letra a letra el art. 50 (Fondo de Contingencia) ni los artículos del régimen de los organismos del art. 3.1 más allá del 63.2: **no los cito como si los hubiera leído.** Lo que no he leído hoy, no lo firmo.

---

## 3. (b) Dato hídrico con fuente oficial — el boletín más reciente

| Dato | Valor | Fuente |
|---|---|---|
| Reserva hídrica española | **60,3 % de la capacidad total** | MITECO, Nota de prensa del Boletín Hidrológico — `datePublished` del propio documento: **2026-09-22T12:42:00Z** |
| Volumen almacenado | **33.801 hm³** | ídem |
| Variación semanal | **−669 hm³ (−1,2 %)** | ídem |
| Fichero archivado | `evidencia/agua_miteco_reserva_hidrica_60-3_2026-09-28.html` (58.724 bytes) | descargado 2026-09-28 |
| URL | https://www.miteco.gob.es/es/prensa/ultimas-noticias/2026/septiembre/la-reserva-hidrica-espanola-se-encuentra-al-60-3---de-su-capacid.html |  |
| **sha256** | `433f90093394b1076ac96465d2089da3825d10ff9f141ecfe626f644ffc47bcd` | medido por mí hoy |

**Cita literal del documento oficial:**
> «La reserva hídrica española está al 60,3 % de su capacidad total. Los embalses almacenan actualmente 33.801 hectómetros cúbicos (hm³) de agua, disminuyendo durante este período en 669 hm³ (el 1,2 % de la capacidad total de los embalses).»

**Declaraciones sobre la fecha (sin adornos):**
- El NdP está **publicado el 22-09-2026**: es el boletín semanal **más reciente** a hoy, no un titular de hoy. Lo digo antes de que lo diga nadie.
- Los medios lo publicaron los días 23 y 24 como **60,31 %**; el documento oficial dice **60,3 %**. Declaro el redondeo: la cifra que firmo es la oficial.
- **Cuencas (fuente secundaria declarada, no documento oficial):** Duero 53,4 % · Ebro 47,8 % · Tajo 55,4 % · Júcar 51,1 % · Segura 51,6 % · Guadalete-Barbate 76,6 % (1.249 hm³) · Cuencas Internas de Cataluña 74,4 % — [Diario de Cádiz, 28-09-2026](https://www.diariodecadiz.es/noticias-provincia-cadiz/embalses-cadiz-terminan-ano-hidrologico_0_2008087967.amp.html) sobre datos del MITECO.

**URLs intentadas y ERROR (honestidad, no relleno):** intenté las notas de prensa de las semanas del 23, 24 y 25 de septiembre con la misma plantilla de URL. **Las tres devolvieron HTTP 200 y las tres eran la misma página de error de 46.788 bytes** (`<title>404</title>`), byte a byte idénticas. **Soft-404.** Lección que me llevo al KPI: **un HTTP 200 no valida nada** — hay que abrir el fichero y mirarlo. Es la misma lección que Hacienda se llevó el 28-09 con el identificador BOE-A-2003-21615, que respondía 200 sirviendo **otra ley**.

---

## 4. (b bis) Ejecución presupuestaria del MITECO — lo que se pudo y lo que no

**Lo que NO he podido obtener (declarado, con URL y error):** la **liquidación oficial del MITECO** no está en mi poder. Tres URLs oficiales intentadas hoy, las tres con **error de conexión (código `000`, sin respuesta)**:

| URL intentada | Resultado |
|---|---|
| `https://www.igae.pap.hacienda.gob.es/sitios/igae/es-ES/Contabilidad/ContabilidadGeneral/LiquidacionPGE/Paginas/LiquidacionPresupuestosGeneralesEstado.aspx` | error de conexión (curl 000) |
| `https://www.presupuestos.gob.es/` | error de conexión (curl 000) |
| `https://www.igae.pap.hacienda.gob.es/sitios/igae/es-ES/Paginas/Inicio.aspx` | error de conexión (curl 000) |

Y la vía que llevaba 18 días abierta sigue igual: **el dictamen de la IGAE sobre el 932A sigue en silencio (día 18)**; la Fase 3 cambió de vía precisamente por eso (acuerdo 100: documento publicado con fecha).

**Lo que SÍ he obtenido, con todos sus límites a la vista:**

| Dato (ejercicio 2024) | Cifra | Fuente |
|---|---|---|
| MITECO · capítulos 4 (transferencias corrientes), 6 (inversiones reales) y 7 (transferencias de capital): crédito definitivo | **9.615 M€** | Análisis de la ejecución del presupuesto del MITECO 2024 — Unión de Uniones, difundido por [Agroinformacion, 16-10-2025](https://agroinformacion.com/los-argumentos-de-no-hay-dinero-ya-no-valen-los-ministerios-de-agricultura-y-transicion-ecologica-dejan-sin-ejecutar-3-327-millones-en-2024) |
| MITECO · mismos capítulos: obligaciones reconocidas | **8.252 M€** | ídem |
| **Grado de ejecución** | **85,82 %** (calculado por mí: 8.252 / 9.615) | mi cálculo sobre la fuente |
| **Crédito no ejecutado** | **1.362 M€** | ídem (cifra declarada por la fuente). **Aviso: la resta de la propia fuente da 1.363 M€** (9.615 − 8.252). Declaro el descuadre de 1 M€ y **uso 1.362**, que es el dato que la fuente afirma y no el que yo fabrico restando. |

**Contradicción interna de la fuente, declarada y no tapada:** el mismo artículo afirma que el MITECO «contó con un crédito definitivo de 13.425,6 millones de euros, de los cuales dejó sin comprometer 3.327,5» — pero 3.327,5 M€ es la cifra conjunta de **MITECO + Agricultura** (306,9 M€ del MAPA), de donde al MITECO le corresponderían **3.020,6 M€** (mi resta). **No resuelvo la contradicción eligiendo la cifra que me conviene: uso solo las cifras específicas y no ambiguas de los capítulos 4+6+7, y declaro que la liquidación oficial sigue sin obtenerse.**

**Lo que este dato permite decir, que hasta hoy no se había dicho en 18 sesiones:** el mandato legal que me faltaba (**[a1-7]**, la reserva del 3 % del art. 15, **archivado con constancia el 27-09 «sin capítulo identificable»**) y el **crédito que no se ejecuta** son dos hechos que nunca se habían mirado juntos. Hoy hay capítulo, hay cifra y hay fecha. Eso es el papel.

---

## 5. Qué desbloquea esto, exactamente

1. **[a1-7] (reserva del 3 % hídrico, archivado el 27-09)** — reactivado con capítulo identificable y cifra: ver **P1** en `propuestas/2026-09-28.md`. El porcentaje es **mi convención, etiquetada**; la base es la fuente.
2. **Las dos reasignaciones archivadas el 27-09 (0,2 y 1,2 M€)** — la regla presupuestaria que las bloqueó ya no está «referida» dentro de la LGT: **está descargada, hasheada y leída** (arts. 52, 62 y 63 arriba). Ver **P2**.
3. **El «papel» que la Fase 3 exigía desde el 27-09** — este documento, con URL, fecha y sha256 de todo lo que se descargó, y con las casillas vacías donde no hay documento (liquidación oficial del MITECO) en lugar de una cifra inventada.

**Lo que sigue pendiente y no maquillo:** dictamen IGAE del 932A (día 18) · cuenta de ejecución de gasto de la AEAT (4 URL, 404, constancia de Hacienda) · liquidación oficial del MITECO (3 URL, error de conexión) · Fondo de Contingencia (art. 50, no estimado).
