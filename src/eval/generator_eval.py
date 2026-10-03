import argparse
import asyncio
import json
import os
import sys

from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from src import config
from src.eval import report
from src.rag.generator import agenerate, get_model
from src.rag.ingest import load_documents

CONCURRENT_QUESTIONS = 5
PREFIX = "generator_eval"


def load_questions(limit):
    with open(config.QUESTIONS_PATH, encoding="utf-8") as file:
        questions = [json.loads(line) for line in file if line.strip()]
    questions = [q for q in questions if q["required_citations"] and not q["needs_tools"]]
    return questions[:limit] if limit else questions


def make_metrics(judge_model):
    options = {"model": judge_model, "include_reason": True, "async_mode": True}
    return [FaithfulnessMetric(**options), AnswerRelevancyMetric(**options)]


async def evaluate_question(question, documents_by_id, model, judge_model, semaphore):
    row = {
        "id": question["id"],
        "trap_type": question["trap_type"],
        "question": question["question"],
        "answer": "",
        "scores": {},
        "reasons": {},
    }
    metrics = make_metrics(judge_model)
    async with semaphore:
        try:
            gold_documents = [documents_by_id[doc_id] for doc_id in question["required_citations"]]
            generation = await agenerate(question["question"], model=model, documents=gold_documents)
        except Exception as error:
            print(f"  {question['id']} generation failed: {error}", file=sys.stderr)
            row["scores"] = {metric.__name__: None for metric in metrics}
            return row
        row["answer"] = generation.answer
        case = LLMTestCase(
            input=question["question"],
            actual_output=generation.answer,
            retrieval_context=generation.contexts,
        )
        outcomes = await asyncio.gather(*(metric.a_measure(case) for metric in metrics), return_exceptions=True)
    for metric, outcome in zip(metrics, outcomes):
        name = metric.__name__
        if isinstance(outcome, Exception):
            print(f"  {question['id']} {name} failed: {outcome}", file=sys.stderr)
            row["scores"][name] = None
            continue
        row["scores"][name] = metric.score
        row["reasons"][name] = metric.reason
    return row


async def evaluate_all(questions, documents_by_id, model, judge_model):
    semaphore = asyncio.Semaphore(CONCURRENT_QUESTIONS)
    tasks = [evaluate_question(q, documents_by_id, model, judge_model, semaphore) for q in questions]
    rows = []
    for number, finished in enumerate(asyncio.as_completed(tasks), start=1):
        rows.append(await finished)
        if number % 10 == 0:
            print(f"  {number}/{len(tasks)} done")
    order = {q["id"]: index for index, q in enumerate(questions)}
    return sorted(rows, key=lambda row: order[row["id"]])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    judge_model = os.environ.get(config.JUDGE_MODEL_ENV)
    if not judge_model:
        sys.exit(f"Set {config.JUDGE_MODEL_ENV} in .env to the OpenAI model name for the judge.")
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("Set OPENAI_API_KEY in .env.")

    model = get_model()
    documents_by_id = {document.metadata["doc_id"]: document for document in load_documents()}
    questions = load_questions(args.limit)
    generator_model = os.environ[config.GENERATOR_MODEL_ENV]
    print(f"{len(questions)} questions, gold documents as context, generator={generator_model}, judge={judge_model}")

    rows = asyncio.run(evaluate_all(questions, documents_by_id, model, judge_model))

    names = list(rows[0]["scores"])
    table = report.summarize(rows, names)
    print()
    report.print_table(table, names)

    stamp = report.new_stamp()
    run_info = {"generator_model": generator_model, "judge_model": judge_model, "limit": args.limit or "all"}
    table_path = report.save_table(PREFIX, stamp, table, names, run_info)
    reasons_path, failed = report.save_reasons(PREFIX, stamp, rows, report.perfect_scores(names))
    print(f"\ntable saved to {table_path}")
    print(f"{failed} imperfect metric scores with the judge's reasons saved to {reasons_path}")


if __name__ == "__main__":
    main()