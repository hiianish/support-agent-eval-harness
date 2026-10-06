import os
import re
from contextlib import ExitStack, contextmanager

from src import config

ENABLED = os.environ.get("TRACING", "off").strip().lower() == "on"

if ENABLED:
    os.environ["OTEL_SDK_DISABLED"] = "false"
    os.environ.setdefault("LANGFUSE_TRACING_ENVIRONMENT", "production")
else:
    os.environ["LANGFUSE_TRACING_ENABLED"] = "false"

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?<!\d)(?:\+?\d{1,2}[\s.-]?)?(?:\(\d{3}\)\s?|\d{3}[\s.-])\d{3}[\s.-]?\d{4}(?!\d)|\b\d{3}[-.\s]\d{4}\b")


def mask_text(value):
    return PHONE.sub("[phone]", EMAIL.sub("[email]", value))


def mask(data=None, **kwargs):
    if isinstance(data, str):
        return mask_text(data)
    if isinstance(data, dict):
        return {key: mask(value) for key, value in data.items()}
    if isinstance(data, (list, tuple)):
        return [mask(item) for item in data]
    return data


if ENABLED:
    from langfuse import Langfuse, get_client, observe, propagate_attributes
    from langfuse.openai import AsyncOpenAI, OpenAI

    try:
        Langfuse(mask=mask)
    except Exception:
        pass
else:
    from openai import AsyncOpenAI, OpenAI

    def observe(*args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            return args[0]
        return lambda function: function


@contextmanager
def observation(as_type, name, tags=None, user_id=None, session_id=None, **fields):
    stack = ExitStack()
    span = None
    if ENABLED:
        try:
            span = stack.enter_context(get_client().start_as_current_observation(as_type=as_type, name=name, **fields))
            if user_id or session_id or tags:
                stack.enter_context(propagate_attributes(user_id=user_id, session_id=session_id, tags=tags or []))
        except Exception:
            span = None
    try:
        yield span
    finally:
        try:
            stack.close()
        except Exception:
            pass


def trace_context(user_id, session_id, name="chat-turn", tags=None):
    return observation("agent", name, tags=tags, user_id=str(user_id), session_id=str(session_id))


def tool_span(name, arguments):
    return observation("tool", name, input=arguments)


def record(span, **fields):
    if span is None:
        return
    try:
        span.update(**fields)
    except Exception:
        pass


def flush():
    if not ENABLED:
        return
    try:
        get_client().flush()
    except Exception:
        pass
