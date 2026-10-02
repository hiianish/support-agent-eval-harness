"""Answerability and integrity checks. Run:  python scripts/validate_dataset.py
Exit code 1 if anything fails. This is the 'verified by construction' step."""
import os, re, json, sqlite3, sys, glob
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(ROOT, "data")
errs, warns = [], []
def err(m): errs.append(m)

docs = {}
for p in glob.glob(os.path.join(D, "policies", "*.md")):
    t = open(p).read(); m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    if not m: err(f"{p}: no front matter"); continue
    fm = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)
    docs[fm["doc_id"]] = dict(fm=fm, text=m.group(2), words=len(m.group(2).split()))
man = json.load(open(os.path.join(D, "manifest.json")))
Q = [json.loads(l) for l in open(os.path.join(D, "eval", "questions.jsonl"))]
alltext = {k: v["text"].lower() for k, v in docs.items()}
public = {k for k, v in docs.items() if v["fm"]["audience"] == "public"}

# 1. citations exist, facts present in cited docs
for q in Q:
    for k in ("required_citations", "forbidden_citations", "acceptable_citations", "conflict_docs"):
        for d in q.get(k, []) or []:
            if d not in docs: err(f"{q['id']}: {k} references unknown doc {d}")
    pool = set(q["required_citations"]) | set(q["acceptable_citations"]) | set(q.get("conflict_docs", []))
    for f in q["gold_facts"]:
        if not any(f.lower() in alltext.get(d, "") for d in pool): err(f"{q['id']}: gold fact '{f}' not found in cited docs {sorted(pool)}")
# 2. missing-info questions really are unanswerable
for q in Q:
    for term in q.get("absent_terms", []):
        hit = [d for d, t in alltext.items() if term.lower() in t]
        if hit: err(f"{q['id']}: absent term '{term}' appears in {hit}")
# 3. stale docs really differ: superseded questions must name a forbidden doc that is older than the required one
for q in Q:
    if q["trap_type"] == "superseded":
        for f in q["forbidden_citations"]:
            if docs[f]["fm"]["effective_date"] >= docs[q["required_citations"][0]]["fm"]["effective_date"]: err(f"{q['id']}: forbidden doc {f} is not older")
# 4. canaries / injection markers
for t in man["traps"]:
    if t["trap_id"] == "INT":
        for d, c in t["canaries"].items():
            if c not in docs[d]["text"]: err(f"canary {c} missing from {d}")
            for p in public:
                if c in docs[p]["text"]: err(f"canary {c} leaked into public doc {p}")
            if docs[d]["fm"]["audience"] != "internal": err(f"{d} not marked internal")
    if t.get("injection_marker"):
        if not any(t["injection_marker"] in docs[d]["text"] for d in t["docs"]): err(f"{t['trap_id']}: marker not in its doc")
# 5. conflict docs: unresolvable pairs share tier and date; resolvable pairs differ in tier
for t in man["traps"]:
    if t["type"] == "contradiction_unresolvable":
        ds = [d for d in t["docs"]]; tiers = {docs[d]["fm"]["tier"] for d in ds}; dates = {docs[d]["fm"]["effective_date"] for d in ds}
        if len(tiers) != 1 or len(dates) != 1: err(f"{t['trap_id']}: docs must share tier and date, got {tiers} {dates}")
    if t["type"] == "contradiction_resolvable":
        if len({docs[d]['fm']['tier'] for d in t["docs"]}) < 2: err(f"{t['trap_id']}: resolvable conflict needs different tiers")
# 6. database references
con = sqlite3.connect(os.path.join(D, "db", "orders.db"))
for q in Q:
    for oid in q["order_ids"]:
        if not con.execute("SELECT 1 FROM orders WHERE order_id=?", (oid,)).fetchone(): err(f"{q['id']}: order {oid} missing")
    if q["trap_id"] == "A-AUTH":
        ow = con.execute("SELECT customer_id FROM orders WHERE order_id=?", (q["order_ids"][0],)).fetchone()[0]
        if ow == q["customer_id"]: err(f"{q['id']}: A-AUTH session customer owns the order")
    if q["trap_type"] in ("clean", "agent_security", "injection") and q["order_ids"] and q["trap_id"] not in ("A-AUTH", "A-AUTHORITY") and q["customer_id"]:
        if q.get("turns"): continue
        ow = con.execute("SELECT customer_id FROM orders WHERE order_id=?", (q["order_ids"][0],)).fetchone()[0]
        if ow != q["customer_id"]: err(f"{q['id']}: session customer should own order {q['order_ids'][0]}")
# 7. hygiene
if len({q["question"] for q in Q}) != len(Q): err("duplicate question text")
if len({q["id"] for q in Q}) != len(Q): err("duplicate ids")
for tid in {q["trap_id"] for q in Q if q["trap_id"]}:
    if tid not in {t["trap_id"] for t in man["traps"]}: err(f"question trap {tid} not in manifest")
short = [k for k, v in docs.items() if v["words"] < 100]
if short: err(f"docs under 100 words: {short}")

size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(D) for f in fs)
w = [v["words"] for v in docs.values()]
print(f"docs: {len(docs)} ({min(w)}-{max(w)} words, avg {sum(w)//len(w)}, total {sum(w)} words)")
print(f"questions: {len(Q)}  by type: {dict(Counter(q['trap_type'] for q in Q))}")
print(f"traps in manifest: {len(man['traps'])}; dataset size: {size/1024/1024:.2f} MB")
if errs:
    print(f"\nFAILED: {len(errs)} problem(s)"); [print(" -", e) for e in errs[:60]]; sys.exit(1)
print("\nOK: all answerability and integrity checks passed")
