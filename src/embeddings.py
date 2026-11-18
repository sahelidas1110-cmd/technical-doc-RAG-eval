from langchain_openai import OpenAIEmbeddings

from src.config import EMBEDDING_MODEL


def get_embedding_model():

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    return embeddings