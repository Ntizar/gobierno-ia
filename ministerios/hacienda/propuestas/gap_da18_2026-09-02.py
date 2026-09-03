# Gap DA18: parrafos del repo vs parrafos del BOE vivo (match por sha256 normalizado)
import re, io, sys, json, hashlib, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def norm(p): return re.sub(r"\s+", " ", p).strip()
def sha(s): return hashlib.sha256(norm(s).encode()).hexdigest()

boe = json.load(open("../evidencia/da18_boe_full_2026-09-02.json", encoding="utf-8"))
boe_pars = [p for p in boe if p["class"] in ("parrafo", "parrafo_2", "nota_pie", "p", "pie_unico")]
boe_shas = {sha(p["text"]): p for p in boe_pars}

txt = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[)", txt, flags=re.S | re.M)
repo_pars = [p for p in re.split(r"\n\s*\n", m.group(1)) if norm(p)]
print("repo:", len(repo_pars), "parrafos /", len(" ".join(repo_pars).split()), "palabras")
print("boe :", len(boe_pars), "parrafos /", sum(len(p["text"].split()) for p in boe_pars), "palabras")
hit = miss = 0
for k, p in enumerate(repo_pars):
    h = sha(p)
    tag = "EN_BOE" if h in boe_shas else "SOBRANTE"
    if tag == "EN_BOE": hit += 1
    else: miss += 1
    print(k, tag, "|", len(p.split()), "pal |", norm(p)[:85])
print("matches:", hit, "sobrantes:", miss, "| palabras sobrantes:",
      sum(len(p.split()) for p in repo_pars if sha(p) not in boe_shas))
