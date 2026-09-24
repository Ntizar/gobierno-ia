# Volcado en seco del bloque 47: indice: prefijo (60 chars) — para fijar offsets con certeza
data = open('ministerios/sanidad/leyes/BOE-A-1986-10499.md.bak-2026-09-23','rb').read()
i = data.find('## [acuarentaysiete]'.encode()); j = data.find('## [acuarentayocho]'.encode())
lines = data[i:j].split(b'\r\n')
for n, l in enumerate(lines):
    print(n, '|', l[:62].decode('utf-8', 'replace'))
