import re
p = 'C:/Users/d_ant/Projects/gobierno-ia/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md'
t = open(p, encoding='utf-8').read().split('\n')
# localizar listas: líneas que empiezan por 'b) ' y comprobar si existe 'a) ' en las 5 líneas anteriores
for i, l in enumerate(t):
    if l.strip().startswith('b) '):
        prev = '\n'.join(t[max(0, i-5):i])
        has_a = re.search(r'^a\) ', prev, re.M) or re.search(r'^\*\*a\)\*\*|^a\)', prev, re.M)
        if not has_a:
            print(f'linea {i+1}: b) sin a) previo -> {l.strip()[:90]}')
# igual para 2) tras 1)
for i, l in enumerate(t):
    if re.match(r'^b\) ', l.strip()) is None and l.strip().startswith('c) '):
        prev = '\n'.join(t[max(0, i-6):i])
        if not re.search(r'^b\) ', prev, re.M):
            print(f'linea {i+1}: c) sin b) previo -> {l.strip()[:90]}')
