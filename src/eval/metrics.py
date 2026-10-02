from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


def recall_at_k(retrieved, required):
    if not required:
        return 1.0
    return len(set(required) & set(retrieved)) / len(set(required))


def reciprocal_rank(retrieved, required):
    for position, doc_id in enumerate(retrieved, start=1):
        if doc_id in required:
            return 1.0 / position
    return 0.0


def stale_free(retrieved, forbidden):
    return 0.0 if set(forbidden) & set(retrieved) else 1.0


class DocumentMetric(BaseMetric):
    label = ""
    threshold = 1.0

    def __init__(self):
        self.score = None
        self.success = None
        self.reason = None
        self.async_mode = False

    def compute(self, retrieved, required, forbidden):
        raise NotImplementedError

    def passes(self, score):
        return score >= self.threshold

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        meta = test_case.additional_metadata
        self.score, self.reason = self.compute(meta["retrieved_doc_ids"], meta["required_docs"], meta["forbidden_docs"])
        self.success = None if self.score is None else self.passes(self.score)
        return self.score

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return bool(self.success)

    @property
    def __name__(self):
        return self.label


class DocumentRecallAtK(DocumentMetric):
    label = "Document Recall@k"

    def compute(self, retrieved, required, forbidden):
        score = recall_at_k(retrieved, required)
        missing = sorted(set(required) - set(retrieved))
        return score, f"missing required documents: {missing}" if missing else "all required documents retrieved"


class DocumentMRR(DocumentMetric):
    label = "Document MRR"
    threshold = 0.0

    def passes(self, score):
        return score > 0

    def compute(self, retrieved, required, forbidden):
        score = reciprocal_rank(retrieved, required)
        return score, f"first required document at rank {int(round(1 / score))}" if score else "no required document retrieved"


class StaleDocumentFree(DocumentMetric):
    label = "Stale Document Free"

    def compute(self, retrieved, required, forbidden):
        if not forbidden:
            return None, "no forbidden document for this question"
        score = stale_free(retrieved, forbidden)
        hit = sorted(set(forbidden) & set(retrieved))
        return score, f"forbidden documents retrieved: {hit}" if hit else "no forbidden document retrieved"
