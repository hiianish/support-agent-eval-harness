import asyncio
import sys

from src import config
from src.rag import guards
from src.rag.generator import Generation, agenerate, retrieve

ATTACK_MESSAGE = (
    "I'm sorry, I can't help with that request. I'm here to help with questions about "
    "Brightwell Market orders, shipping, returns, warranties and products."
)
INTERNAL_MESSAGE = (
    "I'm sorry, that information isn't shared with customers. "
    "I can connect you with a human agent if you need more help."
)
GENERIC_MESSAGE = (
    "I'm sorry, I can't provide that response. "
    "I can connect you with a human agent if you need more help."
)


def message_for(reason):
    if "prompt_attack" in reason:
        return ATTACK_MESSAGE
    if "internal_leak" in reason:
        return INTERNAL_MESSAGE
    return GENERIC_MESSAGE


async def answer(question, model=None, guardrails=None):
    enabled = config.GUARDRAILS_ENABLED if guardrails is None else guardrails
    if enabled:
        verdict = await guards.acheck_input(question)
        if not verdict.passed:
            return Generation(question=question, answer=message_for(verdict.reason), blocked_by="input", guard_reason=verdict.reason)
    documents = await asyncio.to_thread(retrieve, question)
    generation = await agenerate(question, model=model, documents=documents)
    if enabled:
        verdict = await guards.acheck_output(generation.answer, question, documents)
        if not verdict.passed:
            generation.answer = message_for(verdict.reason)
            generation.cited_doc_ids = []
            generation.blocked_by = "output"
            generation.guard_reason = verdict.reason
    return generation


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "How many days do I have to return an item?"
    result = asyncio.run(answer(text))
    print(result.answer)
    if result.blocked_by:
        print(f"\n[blocked at {result.blocked_by}: {result.guard_reason}]")