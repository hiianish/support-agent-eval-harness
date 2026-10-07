import asyncio
import json
import logging
import os
import re
import sqlite3
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from src import config

REQUIRED_ENV = ["OPENAI_API_KEY", "PINECONE_API_KEY", "PINECONE_INDEX_NAME", config.GENERATOR_MODEL_ENV, config.GUARD_MODEL_ENV]

# Demo customers shown in the UI. Picking one simulates signing in.
DEMO_CUSTOMERS = ["C0001", "C0002", "C0005", "C0373", "C0274"]

MAX_MESSAGE_CHARS = int(os.environ.get("MAX_MESSAGE_CHARS", 500))
MAX_TURNS_PER_SESSION = int(os.environ.get("MAX_TURNS_PER_SESSION", 20))
MAX_SESSIONS = int(os.environ.get("MAX_SESSIONS", 100))
SESSION_TTL_SECONDS = int(os.environ.get("SESSION_TTL_SECONDS", 1800))
RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", 10))
DAILY_TURN_CAP = int(os.environ.get("DAILY_TURN_CAP", 300))
MAX_CONCURRENT_TURNS = int(os.environ.get("MAX_CONCURRENT_TURNS", 4))
TURN_TIMEOUT_SECONDS = int(os.environ.get("TURN_TIMEOUT_SECONDS", 90))

log = logging.getLogger("api")
logging.basicConfig(level=logging.INFO)

CUSTOMER_ID = re.compile(r"^C\d{4}$")


@dataclass
class Session:
    agent: object
    customer_id: str
    last_used: float = field(default_factory=time.monotonic)
    turns: int = 0
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


class State:
    def __init__(self):
        self.ready = asyncio.Event()
        self.sessions = {}
        self.hits = defaultdict(deque)
        self.valid_customers = set()
        self.day = time.strftime("%Y-%m-%d", time.gmtime())
        self.turns_today = 0
        self.slots = asyncio.Semaphore(MAX_CONCURRENT_TURNS)


state = State()


def db():
    con = sqlite3.connect(f"file:{config.DB_PATH}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def warm_up():
    """Pay the one-off start-up costs (clients, connections, guard objects) before the first visitor."""
    started = time.perf_counter()
    try:
        from src.rag import guards
        from src.rag.retriever import search

        search("return policy")
        guards.check_input("hello")
        guards.check_output("Hello.", "hello", [])
        log.info("warm-up done in %.1fs", time.perf_counter() - started)
    except Exception as error:
        log.warning("warm-up failed (the first request will be slow): %s", error)


@asynccontextmanager
async def lifespan(app):
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")
    with db() as con:
        state.valid_customers = {row[0] for row in con.execute("SELECT customer_id FROM customers")}

    async def boot():
        await asyncio.to_thread(warm_up)
        state.ready.set()

    task = asyncio.create_task(boot())
    yield
    task.cancel()


app = FastAPI(title="Brightwell support agent", lifespan=lifespan)


class ChatIn(BaseModel):
    customer_id: str
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_CHARS)
    session_id: str | None = None


def check_limits(ip):
    today = time.strftime("%Y-%m-%d", time.gmtime())
    if today != state.day:
        state.day, state.turns_today = today, 0
    if state.turns_today >= DAILY_TURN_CAP:
        raise HTTPException(429, "The demo has reached its daily usage limit. Please try again tomorrow.")
    now = time.monotonic()
    window = state.hits[ip]
    while window and now - window[0] > 60:
        window.popleft()
    if len(window) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(429, "You're sending messages too quickly. Please wait a moment.")
    window.append(now)
    if len(state.hits) > 5000:
        state.hits = defaultdict(deque, {key: value for key, value in state.hits.items() if value})


def get_session(session_id, customer_id):
    now = time.monotonic()
    for key in [key for key, item in state.sessions.items() if now - item.last_used > SESSION_TTL_SECONDS and not item.lock.locked()]:
        del state.sessions[key]
    existing = state.sessions.get(session_id) if session_id else None
    if existing:
        if existing.customer_id != customer_id:
            raise HTTPException(409, "This conversation belongs to a different customer. Start a new chat.")
        return session_id, existing
    if len(state.sessions) >= MAX_SESSIONS:
        idle = [(item.last_used, key) for key, item in state.sessions.items() if not item.lock.locked()]
        if not idle:
            raise HTTPException(503, "The demo is busy right now. Please try again shortly.")
        del state.sessions[min(idle)[1]]
    from src.agent.agent import Agent

    new_id = uuid.uuid4().hex
    agent = Agent(customer_id, guardrails=True, session_id=new_id)
    state.sessions[new_id] = Session(agent=agent, customer_id=customer_id)
    return new_id, state.sessions[new_id]


@app.get("/health")
def health():
    return {"status": "ok", "ready": state.ready.is_set()}


@app.get("/api/demo-customers")
def demo_customers():
    result = []
    with db() as con:
        for customer_id in DEMO_CUSTOMERS:
            customer = con.execute("SELECT name, country FROM customers WHERE customer_id=?", (customer_id,)).fetchone()
            if not customer:
                continue
            orders = con.execute(
                "SELECT o.order_id, o.status, group_concat(i.name, ' + ') AS items FROM orders o "
                "JOIN order_items i USING(order_id) WHERE o.customer_id=? GROUP BY o.order_id ORDER BY o.order_ts DESC LIMIT 5",
                (customer_id,),
            ).fetchall()
            result.append({
                "customer_id": customer_id,
                "name": customer["name"],
                "country": customer["country"],
                "orders": [{"order_id": row["order_id"], "status": row["status"], "items": row["items"]} for row in orders],
            })
    return result


async def start_turn(body, request):
    """Validate the request and find or create the session. Raises HTTPException before anything is streamed."""
    if not CUSTOMER_ID.match(body.customer_id) or body.customer_id not in state.valid_customers:
        raise HTTPException(400, "Unknown customer.")
    check_limits(request.client.host if request.client else "unknown")
    try:
        await asyncio.wait_for(state.ready.wait(), timeout=TURN_TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        raise HTTPException(503, "The demo is still starting up. Please try again in a moment.")
    return get_session(body.session_id, body.customer_id)


async def run_turn(session_id, session, message, on_status=None):
    async with session.lock:
        if session.turns >= MAX_TURNS_PER_SESSION:
            raise HTTPException(429, "This conversation reached its message limit. Start a new chat.")
        session.turns += 1
        session.last_used = time.monotonic()
        state.turns_today += 1
        session.agent.on_status = on_status
        try:
            async with state.slots:
                result = await asyncio.wait_for(session.agent.say(message), timeout=TURN_TIMEOUT_SECONDS)
        except Exception as error:
            # The agent's message history may be half-written, so drop the session.
            log.exception("chat turn failed: %s", error)
            state.sessions.pop(session_id, None)
            raise HTTPException(500, "Something went wrong on our side. Please start a new chat.")
        finally:
            session.agent.on_status = None
            await asyncio.to_thread(flush_traces)
    return result.answer, MAX_TURNS_PER_SESSION - session.turns


@app.post("/api/chat")
async def chat(body: ChatIn, request: Request):
    session_id, session = await start_turn(body, request)
    answer, turns_left = await run_turn(session_id, session, body.message)
    return {"session_id": session_id, "answer": answer, "turns_left": turns_left}


background = set()


@app.post("/api/chat/stream")
async def chat_stream(body: ChatIn, request: Request):
    """Server-sent events: {"type":"status"} while the agent works, then one {"type":"final"} or {"type":"error"}."""
    session_id, session = await start_turn(body, request)
    queue = asyncio.Queue()

    async def push(text):
        await queue.put({"type": "status", "text": text})

    async def work():
        try:
            answer, turns_left = await run_turn(session_id, session, body.message, push)
            await queue.put({"type": "final", "session_id": session_id, "answer": answer, "turns_left": turns_left})
        except HTTPException as error:
            await queue.put({"type": "error", "status": error.status_code, "detail": error.detail})
        finally:
            await queue.put(None)

    task = asyncio.create_task(work())
    background.add(task)
    task.add_done_callback(background.discard)

    async def events():
        while (item := await queue.get()) is not None:
            yield f"data: {json.dumps(item)}\n\n"

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


def flush_traces():
    try:
        import tools_reference

        tools_reference.CALL_LOG.clear()
        from src.observability import flush

        flush()
    except Exception:
        pass


@app.exception_handler(HTTPException)
async def http_error(request, error):
    return JSONResponse({"detail": error.detail}, status_code=error.status_code)


@app.get("/")
def index():
    return FileResponse(config.ROOT / "static" / "index.html")
