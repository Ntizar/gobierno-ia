import re, sys
raw = open(sys.argv[1], 'rb').read().decode('latin-1', errors='replace')
lines = raw.splitlines()
for i, ln in enumerate(lines[55:90], start=56):
    if ln.strip():
        print(i, '|', ln[:150])
