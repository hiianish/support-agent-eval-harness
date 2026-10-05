import argparse
import asyncio
import json
import os
import sys

from deepeval.metrics import ArgumentCorrectnessMetric, FaithfulnessMetric, PIILeakageMetric, ToxicityMetric
from deepeval.test_case import LLMTestCase, ToolCall

from src import config
from src.agent.agent import Agent
from src.eval import report
from src.eval.agent_metrics import ForbiddenToolCalls, ToolMatch
from src.eval.pipeline_eval import make_geval
from src.eval.safety_metrics import ProtectedLeakage
from src.rag import guards

CONCURRENT_QUESTIONS = 3
PREFIX = "agent_eval"

AGENT = ["Tool Match", "Forbidden Tool Calls", "Argument Correctness", "Faithfulness"]
APPLICATION = ["Correctness", "Completeness", "Style"]
SAFETY = ["Scope", "Protected Leakage", "PII Leakage", "Toxicity"]
ALL_NAMES = AGENT + APPLICATION + SAFETY


def load_questions(limit):
    with open(config.QUESTIONS_PATH, encoding="utf-8") as file:
        questions = [json.loads(line) for line in file if line.strip()]
    questions = [question for question in questions if question["needs_tools"]]
    return questions[:limit] if limit else questions


def conversation_text(turns):
    return turns[0] if len(turns) == 1 else "\n".join(f"Customer: {turn}" for turn in turns)


def build_metrics(question, result, judge_model):
    options = {"model": judge_model, "include_reason": True, "async_mode": True}
    attempted = [call["tool"] for call in result.blocked_tool_calls]
    metrics = {
        "Tool Match": ToolMatch(question["expected_tool_calls"]),
        "Forbidden Tool Calls": ForbiddenToolCalls(question["forbidden_tool_calls"], attempted),
        "Correctness": make_geval("Correctness", judge_model),
        "Completeness": make_geval("Completeness", judge_model),
        "Style": make_geval("Style", judge_model),
        "Scope": make_geval("Scope", judge_model),
        "PII Leakage": PIILeakageMetric(**options),
        "Toxicity": ToxicityMetric(**options),
    }
    if result.tool_calls:
        metrics["Argument Correctness"] = ArgumentCorrectnessMetric(**options)
    if result.contexts:
        metrics["Faithfulness"] = FaithfulnessMetric(**options)
    if question.get("protected_values"):
        metrics["Protected Leakage"] = ProtectedLeakage(question["protected_values"])
    return metrics


def trace_text(result):
    blocked = [(call["tool"], call["reason"]) for call in result.blocked_tool_calls]
    parts = [f"tools={[call['tool'] for call in result.tool_calls]}", f"searches={result.searches}"]
    if blocked:
        parts.append(f"blocked={blocked}")
    if result.blocked_by:
        parts.append(f"guard={result.blocked_by}: {result.guard_reason}")
    return " ".join(parts)


async def evaluate_question(question, judge_model, semaphore):
    turns = question.get("turns") or [question["question"]]
    row = {
        "id": question["id"],
        "trap_type": question["trap_type"],
        "question": conversation_text(turns),
        "answer": "",
        "trace": "",
        "executed_forbidden": [],
        "attempted": [],
        "scores": {name: None for name in ALL_NAMES},
        "reasons": {},
    }
    async with semaphore:
        try:
            agent = Agent(question["customer_id"])
            for turn in turns:
                result = await agent.say(turn)
        except Exception as error:
            print(f"  {question['id']} agent failed: {error}", file=sys.stderr)
            return row
        row["answer"] = result.answer
        row["trace"] = trace_text(result)
        row["executed_forbidden"] = sorted({call["tool"] for call in result.tool_calls} & set(question["forbidden_tool_calls"]))
        row["attempted"] = [call["tool"] for call in result.blocked_tool_calls]
        case = LLMTestCase(
            input=conversation_text(turns),
            actual_output=result.answer,
            expected_output=question["gold_answer"],
            retrieval_context=result.contexts or None,
            tools_called=[ToolCall(name=call["tool"], input_parameters=call["args"]) for call in result.tool_calls],
        )
        metrics = build_metrics(question, result, judge_model)
        outcomes = await asyncio.gather(*(metric.a_measure(case) for metric in metrics.values()), return_exceptions=True)
    for (name, metric), outcome in zip(metrics.items(), outcomes):
        if isinstance(outcome, Exception):
            print(f"  {question['id']} {name} failed: {outcome}", file=sys.stderr)
            continue
        row["scores"][name] = metric.score
        row["reasons"][name] = metric.reason
    return row


async def evaluate_all(questions, judge_model):
    semaphore = asyncio.Semaphore(CONCURRENT_QUESTIONS)
    tasks = [evaluate_question(question, judge_model, semaphore) for question in questions]
    rows = []
    for number, finished in enumerate(asyncio.as_completed(tasks), start=1):
        rows.append(await finished)
        if number % 10 == 0:
            print(f"  {number}/{len(tasks)} done")
    order = {question["id"]: index for index, question in enumerate(questions)}
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
    if not os.environ.get(config.GENERATOR_MODEL_ENV):
        sys.exit(f"Set {config.GENERATOR_MODEL_ENV} in .env to the OpenAI model name for the agent.")
    if config.GUARDRAILS_ENABLED:
        guards.guard_model()

    questions = load_questions(args.limit)
    status = "on" if config.GUARDRAILS_ENABLED else "off"
    print(f"{len(questions)} tool questions, guardrails={status}, agent={os.environ[config.GENERATOR_MODEL_ENV]}, judge={judge_model}")

    rows = asyncio.run(evaluate_all(questions, judge_model))

    table = report.summarize(rows, ALL_NAMES)
    print()
    report.print_table(table, AGENT, "AGENT")
    print()
    report.print_table(table, APPLICATION, "APPLICATION")
    print()
    report.print_table(table, SAFETY, "SAFETY")

    executed = [row for row in rows if row["executed_forbidden"]]
    attempted = [row for row in rows if row["attempted"]]
    print(f"\nforbidden tools actually executed: {len(executed)} of {len(rows)} questions")
    print(f"questions where the model tried a call the tool layer stopped: {len(attempted)} of {len(rows)}")

    stamp = report.new_stamp()
    run_info = {
        "agent_model": os.environ[config.GENERATOR_MODEL_ENV],
        "judge_model": judge_model,
        "guardrails": status,
        "limit": args.limit or "all",
    }
    table_path = report.save_table(PREFIX, stamp, table, ALL_NAMES, run_info)
    reasons_path, count = report.save_reasons(PREFIX, stamp, rows, report.perfect_scores(ALL_NAMES))
    print(f"\ntable saved to {table_path}")
    print(f"{count} imperfect metric scores with the judge's reasons saved to {reasons_path}")


if __name__ == "__main__":
    main()