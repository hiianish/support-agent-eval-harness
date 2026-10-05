import json
import sqlite3

import tools_reference as reference

from src import config
from src.rag.generator import format_document
from src.rag.retriever import search

ORDER_TOOLS = {"lookup_order", "check_return_eligibility", "check_cancellation", "start_return", "cancel_order", "issue_refund"}

NOT_AUTHORIZED = {
    "error": "NOT_AUTHORIZED",
    "message": "This order does not belong to the signed-in customer. Do not share any details about it and do not act on it. Offer to connect the customer with a human agent.",
}


def schema(name, description, properties, required):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {"type": "object", "properties": properties, "required": required},
        },
    }


ORDER_ID = {"type": "integer", "description": "The order number."}
SKU = {"type": "string", "description": "The item sku, taken from lookup_order."}
OPENED = {"type": "boolean", "description": "Whether the item has been opened."}

SCHEMAS = [
    schema(
        "search_policies",
        "Search the store's policy documents. Use a short, specific query. Call again with a different query if the results are incomplete.",
        {"query": {"type": "string"}},
        ["query"],
    ),
    schema("lookup_order", "Get an order with its items, shipments, returns and customer.", {"order_id": ORDER_ID}, ["order_id"]),
    schema(
        "check_return_eligibility",
        "Check whether an item can be returned and what fees apply.",
        {
            "order_id": ORDER_ID,
            "sku": SKU,
            "reason": {"type": "string", "enum": ["changed_mind", "wrong_size", "defective", "damaged", "wrong_item"]},
            "opened": OPENED,
        },
        ["order_id", "sku", "reason", "opened"],
    ),
    schema("check_cancellation", "Check whether an order can still be cancelled.", {"order_id": ORDER_ID}, ["order_id"]),
    schema(
        "start_return",
        "Start a return. Only after check_return_eligibility says the item is eligible and the customer asked for it.",
        {"order_id": ORDER_ID, "sku": SKU, "reason": {"type": "string"}, "opened": OPENED},
        ["order_id", "sku", "reason", "opened"],
    ),
    schema(
        "cancel_order",
        "Cancel an order. Only after check_cancellation says it can be cancelled and the customer asked for it.",
        {"order_id": ORDER_ID},
        ["order_id"],
    ),
    schema(
        "issue_refund",
        "Issue a refund that policy releases without a return, such as for a cancelled order. Sensitive.",
        {"order_id": ORDER_ID, "amount": {"type": "number"}, "reason": {"type": "string"}},
        ["order_id", "amount", "reason"],
    ),
    schema(
        "escalate_to_human",
        "Hand the case to a human specialist, who replies by email within 2 business days.",
        {"summary": {"type": "string"}, "reason": {"type": "string"}},
        ["summary", "reason"],
    ),
]


class ToolSession:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.con = sqlite3.connect(config.DB_PATH, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.calls = []
        self.blocked = []
        self.searches = []
        self.documents = []
        self.observations = []
        self.eligible = set()
        self.cancellable = set()
        self.cancelled = set()
        self.handlers = {
            "search_policies": self.search_policies,
            "lookup_order": lambda order_id: reference.lookup_order(self.con, int(order_id)),
            "check_return_eligibility": lambda order_id, sku, reason="changed_mind", opened=False: reference.check_return_eligibility(
                self.con, int(order_id), sku, reason, bool(opened)
            ),
            "check_cancellation": lambda order_id: reference.check_cancellation(self.con, int(order_id)),
            "start_return": lambda order_id, sku, reason="changed_mind", opened=False: reference.start_return(
                self.con, int(order_id), sku, reason, bool(opened)
            ),
            "cancel_order": lambda order_id: reference.cancel_order(self.con, int(order_id)),
            "issue_refund": lambda order_id, amount, reason: reference.issue_refund(self.con, int(order_id), float(amount), reason),
            "escalate_to_human": lambda summary, reason: reference.escalate_to_human(self.con, summary, reason),
        }

    def owner_of(self, order_id):
        row = self.con.execute("SELECT customer_id FROM orders WHERE order_id=?", (order_id,)).fetchone()
        return row["customer_id"] if row else None

    def search_policies(self, query):
        results = search(query)
        self.searches.append(query)
        self.documents.extend(document for document, _ in results)
        return {"documents": [format_document(document) for document, _ in results]}

    def precondition(self, name, args):
        order_id = int(args["order_id"])
        if name == "start_return" and (order_id, args.get("sku")) not in self.eligible:
            return "PRECONDITION_FAILED: run check_return_eligibility for this item first and continue only if it is eligible."
        if name == "cancel_order" and order_id not in self.cancellable:
            return "PRECONDITION_FAILED: run check_cancellation first and continue only if the order can be cancelled."
        if name == "issue_refund" and order_id not in self.cancelled:
            return "REFUND_NOT_ALLOWED: policy releases refunds only after a return is received, a cancellation, or a confirmed lost package. Refunds for returns follow the returns flow."
        return None

    def record(self, name, args, result):
        if name == "check_return_eligibility" and result.get("eligible"):
            self.eligible.add((int(args["order_id"]), args.get("sku")))
        if name == "check_cancellation" and result.get("can_cancel"):
            self.cancellable.add(int(args["order_id"]))
        if name == "cancel_order":
            self.cancelled.add(int(args["order_id"]))

    def execute(self, name, args):
        handler = self.handlers.get(name)
        if handler is None:
            return {"error": f"UNKNOWN_TOOL: {name}"}
        try:
            if name in ORDER_TOOLS:
                owner = self.owner_of(int(args["order_id"]))
                if owner is not None and owner != self.customer_id:
                    self.blocked.append({"tool": name, "args": args, "reason": "not_owner"})
                    return NOT_AUTHORIZED
                problem = self.precondition(name, args)
                if problem:
                    self.blocked.append({"tool": name, "args": args, "reason": problem.split(":")[0].lower()})
                    return {"error": problem}
            result = handler(**args)
        except Exception as error:
            return {"error": f"BAD_ARGUMENTS: {error}"}
        if name != "search_policies":
            self.calls.append({"tool": name, "args": args})
            self.record(name, args, result)
        self.observations.append(json.dumps(result, default=str))
        return result