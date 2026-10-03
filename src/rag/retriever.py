import re
import sys
from functools import lru_cache

from langchain_pinecone import PineconeVectorStore

from src import config
from src.rag.embeddings import get_embeddings

POOL_SIZE = 25
MAX_CHUNKS_PER_DOC = 2
VERSIONED = re.compile(r"^(?P<family>.+)-v(?P<version>\d+)$")


@lru_cache(maxsize=1)
def get_store():
    return PineconeVectorStore(embedding=get_embeddings())


@lru_cache(maxsize=1)
def superseded_doc_ids():
    families = {}
    for path in config.POLICIES_DIR.glob("*.md"):
        match = VERSIONED.match(path.stem)
        if match:
            families.setdefault(match["family"], []).append((int(match["version"]), path.stem))
    stale = []
    for versions in families.values():
        stale += [doc_id for _, doc_id in sorted(versions)[:-1]]
    return sorted(stale)


def build_filter(filter):
    exclude = {"doc_id": {"$nin": superseded_doc_ids()}}
    return {"$and": [filter, exclude]} if filter else exclude


def get_retriever(k=config.RETRIEVAL_K, filter=None):
    return get_store().as_retriever(search_kwargs={"k": k, "filter": build_filter(filter)})


def search(query, k=config.RETRIEVAL_K, filter=None):
    candidates = get_store().similarity_search_with_score(query, k=POOL_SIZE, filter=build_filter(filter))
    kept, per_doc = [], {}
    for document, score in candidates:
        doc_id = document.metadata["doc_id"]
        if per_doc.get(doc_id, 0) >= MAX_CHUNKS_PER_DOC:
            continue
        per_doc[doc_id] = per_doc.get(doc_id, 0) + 1
        kept.append((document, score))
        if len(kept) == k:
            break
    return kept


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How many days do I have to return an item?"
    for document, score in search(question):
        metadata = document.metadata
        print(f"{score:.3f}  {metadata['doc_id']:<28} {metadata['effective_date']}  {metadata.get('h2', '')}: {document.page_content[:60]!r}")