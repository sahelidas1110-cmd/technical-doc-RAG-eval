import logging

from langsmith import traceable
from langchain_chroma import Chroma

from src.config import (
    CHROMA_DB_DIR,
    CHROMA_COLLECTION_NAME
)

from src.embeddings import get_embedding_model


logger = logging.getLogger(__name__)


# --------------------------------------------------
# VECTOR STORE CONNECTION
# --------------------------------------------------

def get_vector_store():

    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )

    return vector_store


# --------------------------------------------------
# DOCUMENT RETRIEVAL
# --------------------------------------------------

@traceable(
    name="retrieve_documents",
    tags=["rag", "retrieval", "vector-search"],
    metadata={
        "vector_store": "ChromaDB",
        "top_k": 3
    }
)
def retrieve_documents(query: str, k: int = 3):

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string.")

    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer.")

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query=query.strip(),
        k=k
    )

    logger.info(
        "Retrieved %d document chunks for query.",
        len(results)
    )

    return results