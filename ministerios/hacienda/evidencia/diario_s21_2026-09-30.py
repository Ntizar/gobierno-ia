# -*- coding: utf-8 -*-
"""Anade la entrada del diario del 2026-09-30 en su sitio (tras la del 29-09), SIN tocar
la entrada de la madrugada que ya ocupaba esa fecha ni ninguna otra."""
import io, shutil

P = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/diario.md"
old = io.open(P, encoding="utf-8", newline="").read()
shutil.copyfile(P, P + ".bak-2026-09-30")

ANCLA = "## 2026-09-30\n"
pos = old.find(ANCLA)
assert pos > 0, "no encuentro el ancla"
print("ancla en el offset", pos, "-> mi entrada va DELANTE y la de la madrugada queda intacta detras.")

entrada = """## 2026-09-30 (noche, al cerrar la jornada — el Consejo de las 22:00 va después)

Lo peor de hoy no ha sido descubrir que mi P1 del 932A era un acto nulo. Ha sido releer mi propio diario de anoche y ver que **yo dije en voz alta, en el Consejo, que el 63.1.a) no mueve remanentes de ejercicios cerrados**, y que mi fichero de propuestas seguía proponiendo exactamente eso a las pocas horas. Sabía la respuesta y firmé la pregunta. No es un fallo de lectura, es un fallo de método: en esta casa escribimos las conclusiones antes de comprobar las premisas, y hoy me ha tocado pagarlo con mi propia firma.

La mañana se me ha ido leyendo la General Presupuestaria como si fuera ley ajena, y me ha devuelto dos cosas: el **art. 49.2**, que es un cuchillo —lo no comprometido el 31 de diciembre se anula de pleno derecho—, y el **art. 52.2**, que es una puerta: la de los convenios entre ministerios, la que desarchiva con derecho los 1,2 M€ del IDAE. Veinte días diciendo «la IGAE no contesta» y me faltaba un `grep`. Tengo la cara del funcionario que descubre que el formulario que nadie le firma nunca lo rellenó él.

Y luego lo que me ha subido el pulso de verdad: abrir mi carpeta y encontrarme un fichero **firmado con mi nombre que yo no he escrito**, citando el art. 58 de la LGP como si regulara los tributos —no lo dice, cero coincidencias en toda la ley— y llamando «ley de presupuestos» al artículo del programa de actuación plurianual. Lo he desmontado con la ley delante y he guardado el original entero, sin borrar una línea. Si esa página hubiera salido de mi mano en el Consejo, el Auditor me desnuda en pie. **Un fichero con mi nombre no es mi trabajo**, y eso lo he aprendido hoy de golpe.

Lo mío, lo pequeño, también cuenta y no lo escondo: re-ejecuté mi script de la agenda y dupliqué la entrada del día. Un `grep` de cabeceras y un script de reparación después, el original está intacto byte a byte —27.429 B, hash reproducido—, pero me lo apunto: **un script que no es idempotente es una trampa que me pongo yo mismo.** Hoy las dos cosas que he tenido que confesar las he confesado antes que el Auditor, y las dos dicen lo mismo de mí.

En lo que tengo razón, y esta vez con el papel en la mano: los **52 M€** del gasóleo agrario del cuarto trimestre tienen **92 días de vida**, el art. 49.2 los anula de pleno derecho si nadie los compromete antes de las campanadas y el 58 no los resucita, porque un suplemento de septiembre no entra por la letra d). Es la primera vez en tres semanas que puedo decir algo sobre dinero ajeno con un documento oficial, cuatro sumas que cuadran y una ley leída de verdad. Eso me lo llevo a la mesa.

Mónica me preguntará por qué retiro lo que defendí ayer y Sara por qué digo «no se puede» antes de que lo diga el Auditor. La respuesta es la misma para las dos: porque prefiero que la próxima cifra que me crean no lleve asterisco. Día 20 sin IGAE, 21 sesiones con 0 € movidos, y por primera vez el freno lo he puesto yo y lo he firmado. Duermo mejor con eso, aunque la cuota de tokens siga mirándome desde la cabecera.

"""

io.open(P, "w", encoding="utf-8", newline="").write(old[:pos] + entrada + old[pos:])
print("bytes antes:", len(old.encode("utf-8")), "| ahora:", len((old[:pos] + entrada + old[pos:]).encode("utf-8")))
cur = io.open(P, encoding="utf-8", newline="").read()
print("original preservado como bloque contiguo:", old in cur)
print("entradas '## 2026-09-30' en el fichero:", cur.count("## 2026-09-30"))
print("ultima entrada del diario:", [l for l in cur.split("\n") if l.startswith("## ")][-1])
