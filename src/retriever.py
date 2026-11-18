from langchain_chroma import Chroma

from src.config import CHROMA_DB_DIR, CHROMA_COLLECTION_NAME
from src.embeddings import get_embedding_model


def get_vector_store():
    """
    Connect to the existing persistent ChromaDB collection.
    """
    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )

    return vector_store


def retrieve_documents(query: str, k: int = 3):
    """
    Retrieve the top-k most relevant document chunks.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query=query,
        k=k
    )

    return results