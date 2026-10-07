FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt \
    && python -c "import tiktoken; tiktoken.get_encoding('cl100k_base')"

COPY . .

RUN useradd -m app && chown -R app /app
USER app

# Sessions live in memory, so run exactly one worker.
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'
