# Helper: dump readable text from a saved HTML file (argv[1]), first N chars (argv[2])
import re, html, sys
t = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
t = re.sub(r'<[^>]+>', ' ', t)
t = html.unescape(t)
t = re.sub(r'[ \t]+', ' ', t)
t = re.sub(r'\n\s*\n+', '\n', t)
n = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
print(t[:n])
