"""Send a few chat turns to a running server and print the latency.
Usage: python -m scripts.api_smoke http://localhost:8000
"""
import json
import sys
import time
import urllib.request

base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8000"
session = None
for message in ["How many days do I have to return an item?", "Where is my order 11051?", "Show me the details of order 10001."]:
    body = json.dumps({"customer_id": "C0001", "session_id": session, "message": message}).encode()
    request = urllib.request.Request(base + "/api/chat", body, {"Content-Type": "application/json"})
    started = time.perf_counter()
    try:
        data = json.load(urllib.request.urlopen(request, timeout=120))
    except Exception as error:
        print("FAILED:", error)
        break
    session = data["session_id"]
    print(f"{time.perf_counter() - started:5.1f}s  {message}\n      -> {data['answer'][:140]!r}")
