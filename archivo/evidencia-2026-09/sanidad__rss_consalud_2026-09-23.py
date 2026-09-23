# Extraigo titulares del RSS de ConSalud (política) fechados hoy 23-09-2026
import urllib.request, re, html
req = urllib.request.Request('https://www.consalud.es/rss/politica.xml', headers={'User-Agent':'Mozilla/5.0'})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','replace')
items = re.findall(r'<item>(.*?)</item>', raw, re.S)
print('items:', len(items))
for it in items:
    t = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', it, re.S)
    d = re.search(r'<pubDate>(.*?)</pubDate>', it, re.S)
    l = re.search(r'<link>(.*?)</link>', it, re.S)
    title = html.unescape((t.group(1) if t else '?')).strip()
    date = d.group(1) if d else '?'
    link = (l.group(1) if l else '?')
    link = re.sub(r'<!\[CDATA\[|\]\]>', '', link)
    link = html.unescape(link).strip()
    if '23 Sep 2026' in date:
        print('-', title[:130], '|', date)
        print(' ', link[:170])
