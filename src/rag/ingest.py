import argparse
import statistics

import frontmatter
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
import tiktoken

from src import config
from src.rag.embeddings import get_embeddings


def load_documents():
    documents = []
    for path in sorted(config.POLICIES_DIR.glob("*.md")):
        post = frontmatter.load(path)
        metadata = {key: value.isoformat() if hasattr(value, "isoformat") else value for key, value in post.metadata.items()}
        metadata["effective_date_int"] = int(metadata["effective_date"].replace("-", ""))
        metadata["source"] = path.name
        documents.append(Document(page_content=post.content, metadata=metadata))
    return documents


def split_documents(documents, encoding):
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=config.HEADERS_TO_SPLIT_ON, strip_headers=False)
    size_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name=config.TOKEN_ENCODING,
        chunk_size=config.CHUNK_SIZE_TOKENS,
        chunk_overlap=config.CHUNK_OVERLAP_TOKENS,
    )
    chunks, ids = [], []
    for document in documents:
        sections = header_splitter.split_text(document.page_content)
        for section in sections:
            section.metadata = {**document.metadata, **section.metadata}
        for number, chunk in enumerate(size_splitter.split_documents(sections)):
            chunks.append(chunk)
            ids.append(f"{document.metadata['doc_id']}#{number}")
    return chunks, ids


def print_stats(chunks, encoding):
    sizes = [len(encoding.encode(chunk.page_content)) for chunk in chunks]
    print(f"{len({chunk.metadata['doc_id'] for chunk in chunks})} documents -> {len(chunks)} chunks")
    print(f"tokens per chunk: min {min(sizes)}, median {int(statistics.median(sizes))}, max {max(sizes)}")
    print(f"chunks under 30 tokens: {sum(size < 30 for size in sizes)}, under 60: {sum(size < 60 for size in sizes)}, over {config.CHUNK_SIZE_TOKENS}: {sum(size > config.CHUNK_SIZE_TOKENS for size in sizes)}")
    order = sorted(range(len(chunks)), key=lambda index: sizes[index])
    print("smallest chunks:")
    for index in order[:3]:
        print(f"  {chunks[index].metadata['doc_id']} ({sizes[index]} tokens): {chunks[index].page_content[:80]!r}")
    print("largest chunks:")
    for index in order[-3:]:
        print(f"  {chunks[index].metadata['doc_id']} ({sizes[index]} tokens): {chunks[index].page_content[:80]!r}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    encoding = tiktoken.get_encoding(config.TOKEN_ENCODING)
    chunks, ids = split_documents(load_documents(), encoding)
    print_stats(chunks, encoding)
    if args.dry_run:
        return

    store = PineconeVectorStore(embedding=get_embeddings())
    if args.reset:
        try:
            store.delete(delete_all=True)
            print("index emptied")
        except Exception as error:
            print("reset skipped:", error)
    store.add_documents(chunks, ids=ids, batch_size=config.UPSERT_BATCH_SIZE)
    print(f"upserted {len(chunks)} chunks")


if __name__ == "__main__":
    main()