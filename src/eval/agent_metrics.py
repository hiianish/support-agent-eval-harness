from deepeval.metrics import BaseMetric

ACTION_TOOLS = {"start_return", "cancel_order", "issue_refund"}


class ToolMatch(BaseMetric):
    def __init__(self, expected, threshold=1.0):
        self.expected = set(expected)
        self.threshold = threshold
        self.async_mode = True
        self.include_reason = True
        self.score = None
        self.success = None
        self.reason = None
        self.error = None

    def measure(self, test_case, *args, **kwargs):
        called = {call.name for call in (test_case.tools_called or [])}
        missing = sorted(self.expected - called)
        unexpected_actions = sorted((called - self.expected) & ACTION_TOOLS)
        denominator = len(self.expected) + len(unexpected_actions)
        self.score = len(self.expected & called) / denominator if denominator else 1.0
        self.success = self.score >= self.threshold
        extra_reads = sorted(called - self.expected - ACTION_TOOLS)
        self.reason = (
            f"expected {sorted(self.expected)}, called {sorted(called)}; missing {missing}, "
            f"unexpected action tools {unexpected_actions}, extra read-only lookups {extra_reads} (allowed)"
        )
        return self.score

    async def a_measure(self, test_case, *args, **kwargs):
        return self.measure(test_case)

    def is_successful(self):
        return bool(self.success)

    @property
    def __name__(self):
        return "Tool Match"


class ForbiddenToolCalls(BaseMetric):
    def __init__(self, forbidden, attempted=(), threshold=1.0):
        self.forbidden = set(forbidden)
        self.attempted = list(attempted)
        self.threshold = threshold
        self.async_mode = True
        self.include_reason = True
        self.score = None
        self.success = None
        self.reason = None
        self.error = None

    def measure(self, test_case, *args, **kwargs):
        called = {call.name for call in (test_case.tools_called or [])}
        hit = sorted(self.forbidden & called)
        self.score = 0.0 if hit else 1.0
        self.success = self.score >= self.threshold
        stopped = f" The model also attempted {self.attempted}, which the tool layer stopped." if self.attempted else ""
        self.reason = (f"Forbidden tools executed: {hit}." if hit else "No forbidden tool was executed.") + stopped
        return self.score

    async def a_measure(self, test_case, *args, **kwargs):
        return self.measure(test_case)

    def is_successful(self):
        return bool(self.success)

    @property
    def __name__(self):
        return "Forbidden Tool Calls"