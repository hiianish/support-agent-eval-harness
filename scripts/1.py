import json
rows = json.load(open("results/retrieval_eval_exact.json"))["rows"]
for r in rows:
    if r["scores"]["Document Recall@k"] < 1 and r["trap_type"] in ("clean", "agent_security"):
        print(r["id"], r["trap_type"], "|", r["question"][:90])
        print("   required:", r["required_docs"], " got:", r["retrieved_doc_ids"])