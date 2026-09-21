import json, io, os, sys, hashlib, re

p = os.path.expandvars(r"$LOCALAPPDATA/hermes/cron/jobs.json")
with io.open(p, encoding="utf-8") as f:
    data = json.load(f)
jobs = data if isinstance(data, list) else data.get("jobs", data)
if isinstance(jobs, dict):
    jobs = list(jobs.values())

KEYS = ["REGLA DE RESILIENCIA", "ANTI-SUPLANTACI", "CONCURRENCIA", "backoff", "120 segundos"]
print("total jobs:", len(jobs))
for j in jobs:
    jid = j.get("job_id") or j.get("id")
    name = j.get("name", "")
    pr = j.get("prompt") or ""
    if not pr:
        print(f"- {jid} | {name} | [sin prompt / script] schedule={j.get('schedule')} script={j.get('script')}")
        continue
    flags = [k for k in KEYS if k in pr]
    print(f"- {jid} | {name} | {len(pr)} chars | schedule={j.get('schedule')} | model={j.get('model')} | marcas={flags}")
