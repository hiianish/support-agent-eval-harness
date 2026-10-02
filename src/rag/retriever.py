import sys
from functools import lru_cache

from langchain_pinecone import PineconeVectorStore

from src.rag.embeddings import get_embeddings


@lru_cache(maxsize=1)
def get_store():
    return PineconeVectorStore(embedding=get_embeddings())


def get_retriever(k=5, filter=None):
    return get_store().as_retriever(search_kwargs={"k": k, "filter": filter})


def search(query, k=5, filter=None):
    return get_store().similarity_search_with_score(query, k=k, filter=filter)


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How many days do I have to return an item?"
    for document, score in search(question):
        metadata = document.metadata
        print(f"{score:.3f}  {metadata['doc_id']:<28} {metadata['effective_date']}  {metadata.get('h2', '')}: {document.page_content[:60]!r}")
