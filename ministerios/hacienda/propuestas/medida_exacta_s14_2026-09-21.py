import re, hashlib, json

path = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
with open(path, encoding="utf-8") as f:
    raw = f.read()

print("SHA256 fichero ley ANTES (y hoy no lo toco):", hashlib.sha256(raw.encode("utf-8")).hexdigest())

parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", raw)
repo = {}
lineno = {}
pos = 0
for i in range(1, len(parts), 2):
    lab = re.match(r"## (\[[a-z0-9\-]+\])", parts[i]).group(1)
    repo[lab] = parts[i + 1]
    lineno[lab] = raw[:pos].count("\n") + 1
    pos += len(parts[i - 1]) + len(parts[i])

def wc(s):
    return len(re.findall(r"\S+", s))

def sq(s):
    s = s.lower()
    s = re.sub(r"[^a-záéíóúüñ0-9\s]", "", s, flags=re.UNICODE)
    return s.replace(" ", "")

# Párrafos BOE a restaurar (extraídos del consolidado archivado, aparato editorial fuera)
frags = {
 "[a93]": [
  "a) Los retenedores y los obligados a realizar ingresos a cuenta deberán presentar relaciones de los pagos dinerarios o en especie realizados a otras personas o entidades.",
  "2. Las obligaciones a las que se refiere el apartado anterior deberán cumplirse con carácter general en la forma y plazos que reglamentariamente se determinen, o mediante requerimiento individualizado de la Administración tributaria que podrá efectuarse en cualquier momento posterior a la realización de las operaciones relacionadas con los datos o antecedentes requeridos.",
  "a) El secreto del contenido de la correspondencia.",
  "5. La obligación de los demás profesionales de facilitar información con trascendencia tributaria a la Administración tributaria no alcanzará a los datos privados no patrimoniales que conozcan por razón del ejercicio de su actividad cuya revelación atente contra el honor o la intimidad personal y familiar. Tampoco alcanzará a aquellos datos confidenciales de sus clientes de los que tengan conocimiento como consecuencia de la prestación de servicios profesionales de asesoramiento o defensa.",
 ],
 "[a101]": [
  "a) Las practicadas en el procedimiento inspector previa comprobación e investigación de la totalidad de los elementos de la obligación tributaria, salvo lo dispuesto en el apartado 4 de este artículo.",
  "4. En los demás casos, las liquidaciones tributarias tendrán el carácter de provisionales.",
  "a) Cuando alguno de los elementos de la obligación tributaria se determine en función de los correspondientes a otras obligaciones que no hubieran sido comprobadas, que hubieran sido regularizadas mediante liquidación provisional o mediante liquidación definitiva que no fuera firme, o cuando existan elementos de la obligación tributaria cuya comprobación con carácter definitivo no hubiera sido posible durante el procedimiento, en los términos que se establezcan reglamentariamente.",
 ],
 "[a187]": [
  "a) Comisión repetida de infracciones tributarias.",
  "1.º La base de la sanción; y",
  "Cuando el perjuicio económico sea superior al 10 por ciento e inferior o igual al 25 por ciento, el incremento será de 10 puntos porcentuales.",
  "c) Incumplimiento sustancial de la obligación de facturación o documentación.",
  "2. Los criterios de graduación son aplicables simultáneamente.",
 ],
}

tot_fal = 0
for lab, fs in frags.items():
    body = repo[lab]
    print("=" * 70)
    n_lab = len(re.findall(r"(?m)^Artículo \d+\.", body))
    print(f"{lab} | líneas {lineno[lab]}..{lineno[lab]+wc(body)} | palabras {wc(body)} | rótulos internos: {n_lab}")
    for fr in fs:
        present = sq(fr) in sq(body)
        w = wc(fr)
        tot_fal += 0 if present else w
        print(f"  {'PRESENTE' if present else 'FALTA   '} ({w:3d} pal): {fr[:60]}...")
print("TOTAL palabras de contenido BOE a restaurar (3 bloques):", tot_fal)
for lab in frags:
    print(lab, "sha256 cuerpo:", hashlib.sha256(repo[lab].encode('utf-8')).hexdigest()[:16])
