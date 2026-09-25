import io, os, glob
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
for f in sorted(glob.glob('evidencia/bloque_*_2026-09-25.txt')):
    if 'vivo' in f: continue
    s = io.open(f, encoding='utf-8').read()
    print(f.split('/')[-1].replace(chr(92),'/'), '->', len(s.split()), 'palabras', len(s), 'caracteres')
