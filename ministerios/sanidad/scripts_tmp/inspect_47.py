import re, sys
p = 'ministerios/sanidad/leyes/BOE-A-1986-10499.md'
data = open(p, 'rb').read()
print('total bytes', len(data))
print('CRLF', data.count(b'\r\n'), 'bare LF', data.count(b'\n') - data.count(b'\r\n'))
i = data.find('## [acuarentaysiete]'.encode('utf-8'))
j = data.find('## [acuarentayocho]'.encode('utf-8'))
block = data[i:j]
print('block bytes', len(block), 'block CRLF', block.count(b'\r\n'), 'block bare LF', block.count(b'\n')-block.count(b'\r\n'))
print('---- block repr (lines, first 90 chars each) ----')
for k, ln in enumerate(block.split(b'\n')):
    s = ln.decode('utf-8', 'replace')
    print(k, repr(s[:90]))
