# -*- coding: utf-8 -*-
# Sesion 18/30 - decision final por bloque: ¿viaja la letra a) vigente en la cola canonica?
import json, re, os, unicodedata
os.chdir('C:/Users/d_ant/Projects/gobierno-ia')
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('<sup>', '').replace('</sup>', '')
    return re.sub(r'\s+', ' ', s).strip().lower()
cons_raw = open('ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html', encoding='utf-8', errors='ignore').read()
cons = norm(re.sub(r'<[^>]+>', ' ', cons_raw))
vivo = open('ministerios/hacienda/leyes/BOE-A-2003-23186.md', encoding='utf-8').read()

def cola(tag, apertura):
    m = re.search(r'(?m)^## \[' + tag + r'\].*?(?=^## \[|\Z)', vivo, re.S)
    b = m.group(0)
    p = b.rfind(apertura)
    return b[p:]

c68 = cola('a68', '1. El plazo de prescripción del derecho a que se refiere el párrafo a) del artículo 66 de esta Ley se interrumpe:')
print('cola a68 palabras:', len(c68.split()))
print('  letra a) 68.1 en cola:', norm('a) Por cualquier acción de la Administración tributaria, realizada con conocimiento formal del obligado tributario, conducente al reconocimiento, regularización, comprobación, inspección y recaudación, y de la potestad sancionadora') in norm(c68))
print('  letra a) 68.1 en consolidado:', norm('Por cualquier acción de la Administración tributaria, realizada con conocimiento formal del obligado tributario, conducente al reconocimiento') in cons)
c81 = cola('a81', '1. Para asegurar el cobro de las deudas para cuya recaudación sea competente')
print('cola a81 palabras:', len(c81.split()))
la = norm('a) La retención del pago de devoluciones tributarias o de otros pagos que deba realizar la Administración tributaria. La retención cautelar total o parcial de una devolución tributaria deberá ser notificada al interesado junto con el acuerdo de devolución')
print('  letra a) 81.4 en cola:', la in norm(c81))
print('  letra a) 81.4 en consolidado:', norm('La retención del pago de devoluciones tributarias o de otros pagos que deba realizar la Administración tributaria') in cons)
# ¿que dice el consolidado alrededor de "podran consistir en"?
i = cons.find('las medidas cautelares podrán consistir')
print('  ctx consolidado 81.4:', cons[i:i+260] if i >= 0 else 'NO')
