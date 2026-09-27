# -*- coding: utf-8 -*-
"""Reproduce los hashes de bloque declarados por Hacienda el 2026-09-27 e imprime la convención.

Convención identificada por Presidencia (cierra el problema abierto desde la sesión 14):
    sha256( texto del bloque normalizado a LF .strip() )   -> codificado en UTF-8
Se contrasta además con la convención de Presidencia (bytes del rango con CRLF),
para dejar escrito que son dos varas distintas.
"""
from pathlib import Path
import hashlib

EV = Path(__file__).resolve().parents[1] / 'ministerios/hacienda/evidencia'
DECLARADOS = {
    'bloque_vivo_a65_2026-09-27.txt': 'de9c8891',
    'bloque_propuesto_a65_2026-09-27.txt': 'fef14290',
    'bloque_vivo_a112_2026-09-27.txt': '0c614a73',
    'bloque_propuesto_a112_2026-09-27.txt': 'ccf815ad',
}

print('Convencion A (la de Hacienda): sha256(texto LF .strip())')
print('Convencion B (la de Presidencia): sha256(bytes del rango con CRLF, sin salto final)')
print()
ok = True
for f, d in DECLARADOS.items():
    t = (EV / f).read_text(encoding='utf-8')
    a = hashlib.sha256(t.strip().encode('utf-8')).hexdigest()
    bb = hashlib.sha256(t.replace('\n', '\r\n').encode('utf-8')).hexdigest()
    ok = ok and a.startswith(d)
    print('%-42s declarado %s | A %s %s | B %s' % (f, d, a[:8], 'OK' if a.startswith(d) else 'NO', bb[:8]))
print()
print('RESULTADO:', '4/4 reproducidos con la convencion A' if ok else 'NO reproducidos')
