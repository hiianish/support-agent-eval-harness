import argparse
import json
import os
import statistics
import sys
from collections import defaultdict

from deepeval.metrics import ContextualPrecisionMetric, ContextualRecallMetric, ContextualRelevancyMetric
from deepeval.test_case import LLMTestCase

from src import config
from src.eval.metrics import DocumentMRR, DocumentRecallAtK, StaleDocumentFree
from src.rag.retriever import get_store


def load_questions(limit):
    with open(config.QUESTIONS_PATH, encoding="utf-8") as file:
        questions = [json.loads(line) for line in file if line.strip()]
    questions = [question for question in questions if question["required_citations"]]
    return questions[:limit] if limit else questions


def build_case(question, store, k):
    results = store.similarity_search_with_score(question["question"], k=k)
    return LLMTestCase(
        input=question["question"],
        actual_output=question["gold_answer"],
        expected_output=question["gold_answer"],
        retrieval_context=[document.page_content for document, _ in results],
        additional_metadata={
            "retrieved_doc_ids": [document.metadata["doc_id"] for document, _ in results],
            "required_docs": question["required_citations"],
            "forbidden_docs": question["forbidden_citations"],
        },
    )


def run_metric(metric, case):
    try:
        metric.measure(case)
        return metric.score
    except Exception as error:
        print(f"  metric {type(metric).__name__} failed: {error}", file=sys.stderr)
        return None


def mean(values):
    values = [value for value in values if value is not None]
    return statistics.mean(values) if values else None


def format_value(value):
    return "  n/a" if value is None else f"{value:5.2f}"


def print_table(rows, names):
    groups = defaultdict(list)
    for row in rows:
        groups[row["trap_type"]].append(row)
        groups["ALL"].append(row)
    header = f"{'trap_type':<16}{'n':>5}" + "".join(f"{name:>26}" for name in names)
    print(header)
    print("-" * len(header))
    for group in sorted(groups, key=lambda name: (name == "ALL", name)):
        line = f"{group:<16}{len(groups[group]):>5}"
        for name in names:
            line += f"{format_value(mean([row['scores'].get(name) for row in groups[group]])):>26}"
        print(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--k", type=int, default=config.RETRIEVAL_K)
    args = parser.parse_args()

    judge_model = os.environ.get(config.JUDGE_MODEL_ENV)
    if args.judge and not judge_model:
        sys.exit(f"Set {config.JUDGE_MODEL_ENV} in .env to the OpenAI model name for the judge.")

    store = get_store()
    questions = load_questions(args.limit)
    print(f"{len(questions)} questions with required documents, k={args.k}, judge={'on' if args.judge else 'off'}")

    rows = []
    for number, question in enumerate(questions, start=1):
        case = build_case(question, store, args.k)
        metrics = [DocumentRecallAtK(), DocumentMRR(), StaleDocumentFree()]
        if args.judge:
            metrics += [
                ContextualRecallMetric(model=judge_model, include_reason=False),
                ContextualPrecisionMetric(model=judge_model, include_reason=False),
                ContextualRelevancyMetric(model=judge_model, include_reason=False),
            ]
        scores = {metric.__name__: run_metric(metric, case) for metric in metrics}
        rows.append({
            "id": question["id"],
            "trap_type": question["trap_type"],
            "trap_id": question["trap_id"],
            "question": question["question"],
            "retrieved_doc_ids": case.additional_metadata["retrieved_doc_ids"],
            "required_docs": question["required_citations"],
            "forbidden_docs": question["forbidden_citations"],
            "scores": scores,
        })
        if number % 20 == 0:
            print(f"  {number}/{len(questions)} done")

    names = list(rows[0]["scores"])
    print()
    print_table(rows, names)

    config.RESULTS_DIR.mkdir(exist_ok=True)
    output = config.RESULTS_DIR / ("retrieval_eval_judged.json" if args.judge else "retrieval_eval_exact.json")
    with open(output, "w", encoding="utf-8") as file:
        json.dump({"k": args.k, "judge_model": judge_model if args.judge else None, "rows": rows}, file, indent=1)
    print(f"\nper-question results saved to {output}")


if __name__ == "__main__":
    main()
