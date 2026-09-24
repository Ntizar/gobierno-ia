import urllib.request, re
req = urllib.request.Request('https://www.sanidad.gob.es/gabinete/notap_rss.do', headers={'User-Agent':'Mozilla/5.0'})
raw = urllib.request.urlopen(req, timeout=25).read().decode('utf-8','replace')
items = re.findall(r'<item>(.*?)</item>', raw, re.S)
for it in items[:6]:
    t = re.search(r'<title>(.*?)</title>', it, re.S)
    d = re.search(r'<pubDate>(.*?)</pubDate>', it, re.S)
    l = re.search(r'<link>(.*?)</link>', it, re.S)
    print('TITLE:', (t.group(1) if t else '?')[:110])
    print('DATE :', d.group(1) if d else '?')
    print('LINK :', l.group(1) if l else '?')
    print('---')
