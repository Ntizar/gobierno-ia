import re, sys
raw = open(sys.argv[1], 'rb').read()
txt = raw.decode('latin-1', errors='replace')
lines = txt.splitlines()
# find the three aggregate rows and print surrounding context (previous text lines)
for i, ln in enumerate(lines):
    if '832.979' in ln or '1.245.134' in ln or '3.829.395' in ln:
        # print the label: look back for nearest line containing letters
        lab = ''
        for j in range(i, max(i-6, -1), -1):
            words = re.findall(r'[A-Za-zÁÉÍÓÚÑáéíóúñ][A-Za-zÁÉÍÓÚÑáéíóúñ .()º/-]{6,}', lines[j])
            if words:
                lab = words[-1].strip()
                break
        print(i+1, '|', ln[:90], '| LABEL~', lab[:60])
