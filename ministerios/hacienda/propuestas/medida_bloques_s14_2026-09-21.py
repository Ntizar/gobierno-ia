import re, hashlib

path = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
with open(path, encoding="utf-8") as f:
    txt = f.read()

# split by all block headers (convencion 335)
parts = re.split(r"(?m)^## (\[[a-z0-9\-]+\][^\n]*)$", txt)
blocks = {}
for i in range(1, len(parts), 2):
    blocks[parts[i]] = parts[i + 1]

def find(label):
    for k in blocks:
        if k.startswith(label):
            return k, blocks[k]
    return None, None

for label in ("[a93] ", "[a101] ", "[a187] "):
    k, body = find(label)
    words = len(re.findall(r"\S+", body))
    h = hashlib.sha256(body.encode("utf-8")).hexdigest()
    n_a = body.count("\na) ") + body.count("a) Las") + len(re.findall(r"(?m)^a\)", body))
    print("=" * 80)
    print(k, "| palabras:", words, "| sha256:", h[:16])
    print("ocurrencias 'a) ':", len(re.findall(r"(?m)^a\)", body)), "| 'b) ':", len(re.findall(r"(?m)^b\)", body)), "| 'c) ':", len(re.findall(r"(?m)^c\)", body)))
    print("rotulos 'Artículo NN.' dentro del cuerpo:", len(re.findall(r"(?m)^Artículo \d+\.", body)))
    # comprobaciones especificas
    if label == "[a187] ":
        print("contiene 'Comisión repetida':", "Comisión repetida" in body)
        print("contiene '10 puntos porcentuales':", "10 puntos porcentuales" in body)
        print("contiene 'base de la sanción':", "base de la sanción" in body)
        print("contiene '2. Los criterios de graduación son aplicables simultáneamente':", "Los criterios de graduación son aplicables simultáneamente" in body)
    if label == "[a101] ":
        print("contiene 'En los demás casos, las liquidaciones':", "En los demás casos, las liquidaciones" in body)
    if label == "[a93] ":
        print("contiene 'Los retenedores y los obligados a realizar ingresos a cuenta deberán presentar':", "deberán presentar relaciones" in body)
        print("contiene 'El secreto del contenido de la correspondencia':", "El secreto del contenido de la correspondencia" in body)
