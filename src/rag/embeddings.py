from langchain_openai import OpenAIEmbeddings

from src import config


def get_embeddings():
    return OpenAIEmbeddings(model=config.EMBED_MODEL)