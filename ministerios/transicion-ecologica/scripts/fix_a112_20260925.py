import hashlib, io, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
p = 'evidencia/bloque_propuesto_a1-12_2026-09-25.txt'
s = io.open(p, encoding='utf-8').read()
old = 'El mandato de este apartado 1 carecía de plazo desde la entrada en vigor de la ley el 22 de mayo de 2021, sin que conste en el expediente la aprobación del Plan estatal.'
new = 'El mandato de este apartado 1 carecía de plazo cierto desde su inclusión en el texto consolidado, sin que conste en el expediente de esta ley la aprobación del Plan estatal.'
assert old in s, 'no encontrada la frase'
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
h = hashlib.sha256(s.encode()).hexdigest()
words = len(s.split())
print('a1-12 propuesto: palabras', words, 'sha256', h)
# actualizar SHA256SUMS_2026-09-25.txt
f = 'evidencia/SHA256SUMS_2026-09-25.txt'
lines = io.open(f, encoding='utf-8').read().split('\n')
for i, l in enumerate(lines):
    if 'bloque_propuesto_a1-12_2026-09-25.txt' in l:
        lines[i] = h + '  evidencia/bloque_propuesto_a1-12_2026-09-25.txt'
io.open(f, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('SHA256SUMS actualizado')
