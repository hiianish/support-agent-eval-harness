import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

POLICIES_DIR = ROOT / "data" / "policies"
QUESTIONS_PATH = ROOT / "data" / "eval" / "questions.jsonl"
RESULTS_DIR = ROOT / "results"

EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-small")
EMBED_DIMENSIONS = {"text-embedding-3-small": 1536, "text-embedding-3-large": 3072}
TOKEN_ENCODING = "cl100k_base"

CHUNK_SIZE_TOKENS = 250
CHUNK_OVERLAP_TOKENS = 50
HEADERS_TO_SPLIT_ON = [("#", "h1"), ("##", "h2"), ("###", "h3")]

UPSERT_BATCH_SIZE = 100

RETRIEVAL_K = 5
JUDGE_MODEL_ENV = "JUDGE_MODEL"
GENERATOR_MODEL_ENV = "GENERATOR_MODEL"