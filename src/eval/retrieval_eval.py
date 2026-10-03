import argparse
import asyncio
import json
import os
import sys

from deepeval.metrics import ContextualPrecisionMetric, ContextualRecallMetric
from deepeval.test_case import LLMTestCase

from src import config
from src.eval import report
from src.rag.retriever import get_store

CONCURRENT_QUESTIONS = 5
PREFIX = "retrieval_eval"


def load_questions(limit):
    with open(config.QUESTIONS_PATH, encoding="utf-8") as file:
        questions = [json.loads(line) for line in file if line.strip()]
    questions = [question for question in questions if question["required_citations"]]
    return questions[:limit] if limit else questions


def build_case(question, store):
    results = store.similarity_search_with_score(question["question"], k=config.RETRIEVAL_K)
    return LLMTestCase(
        input=question["question"],
        actual_output=question["gold_answer"],
        expected_output=question["gold_answer"],
        retrieval_context=[document.page_content for document, _ in results],
    )


def make_metrics(judge_model):
    options = {"model": judge_model, "include_reason": False, "async_mode": True}
    return [ContextualRecallMetric(**options), ContextualPrecisionMetric(**options)]


async def judge_case(question, case, judge_model, semaphore):
    metrics = make_metrics(judge_model)
    async with semaphore:
        outcomes = await asyncio.gather(*(metric.a_measure(case) for metric in metrics), return_exceptions=True)
    scores = {}
    for metric, outcome in zip(metrics, outcomes):
        if isinstance(outcome, Exception):
            print(f"  {question['id']} {metric.__name__} failed: {outcome}", file=sys.stderr)
            scores[metric.__name__] = None
        else:
            scores[metric.__name__] = metric.score
    return {"id": question["id"], "trap_type": question["trap_type"], "scores": scores}


async def judge_all(prepared, judge_model):
    semaphore = asyncio.Semaphore(CONCURRENT_QUESTIONS)
    tasks = [judge_case(question, case, judge_model, semaphore) for question, case in prepared]
    rows = []
    for number, finished in enumerate(asyncio.as_completed(tasks), start=1):
        rows.append(await finished)
        if number % 10 == 0:
            print(f"  {number}/{len(tasks)} done")
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    judge_model = os.environ.get(config.JUDGE_MODEL_ENV)
    if not judge_model:
        sys.exit(f"Set {config.JUDGE_MODEL_ENV} in .env to the OpenAI model name for the judge.")
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("Set OPENAI_API_KEY in .env.")

    store = get_store()
    questions = load_questions(args.limit)
    print(f"{len(questions)} questions with required documents, k={config.RETRIEVAL_K}, judge={judge_model}")

    prepared = [(question, build_case(question, store)) for question in questions]
    rows = asyncio.run(judge_all(prepared, judge_model))

    names = list(rows[0]["scores"])
    table = report.summarize(rows, names)
    print()
    report.print_table(table, names)

    stamp = report.new_stamp()
    run_info = {"judge_model": judge_model, "k": config.RETRIEVAL_K, "limit": args.limit or "all"}
    print(f"\ntable saved to {report.save_table(PREFIX, stamp, table, names, run_info)}")


if __name__ == "__main__":
    main()