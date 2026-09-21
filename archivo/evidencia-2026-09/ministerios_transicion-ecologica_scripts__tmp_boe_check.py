import re, html
t = open(r'C:/Users/d_ant/AppData/Local/Temp/ley7.html', encoding='utf-8').read()
i = t.find('Principios rectores')
seg = html.unescape(re.sub(r'<[^>]+>', ' ', t[i:i+3000]))
print(re.sub(r'\s+', ' ', seg)[:2000])
