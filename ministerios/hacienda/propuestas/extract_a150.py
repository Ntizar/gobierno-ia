# Extrae texto completo de las variantes del apartado 1 del art. 150
import re

src = open("leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
blocks = re.split(r'\n(?=## \[)', src)
for b in blocks:
    if not b.startswith('## [a150]'):
        continue
    lines = [l.strip() for l in b.split('\n') if l.strip()]
    for i, l in enumerate(lines):
        if 'deberán concluir en el plazo' in l or 'concluir en el plazo de 12 meses' in l or l.startswith('1. Las actuaciones del procedimiento'):
            print('---')
            for j in range(i, min(i + 14, len(lines))):
                print(lines[j][:400])
    break
