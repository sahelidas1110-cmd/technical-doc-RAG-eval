
import logging
from functools import lru_cache

from sentence_transformers import CrossEncoder

from src.retriever import retrieve_documents

logger = logging.getLogger(__name__)

RERANKING_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


@lru_cache(maxsize=1)
def get_reranking_model():
    """Load and cache the Cross-Encoder model."""

    logger.info("Loading reranking model: %s", RERANKING_MODEL)

    model = CrossEncoder(RERANKING_MODEL)

    logger.info("Reranking model loaded successfully.")

    return model


def retrieve_reranked_documents(
    query: str,
    k: int = 3,
    candidate_k: int = 20
):
    """Retrieve dense candidates and rerank them using a Cross-Encoder."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string.")

    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer.")

    if not isinstance(candidate_k, int) or isinstance(candidate_k, bool) or candidate_k <= 0:
        raise ValueError("candidate_k must be a positive integer.")

    if k > candidate_k:
        raise ValueError("k cannot be greater than candidate_k.")

    query = query.strip()

    # Step 1: Retrieve candidate documents using dense retrieval
    candidate_results = retrieve_documents(
        query=query,
        k=candidate_k
    )

    candidate_documents = [
        document for document, _ in candidate_results
    ]

    if not candidate_documents:
        logger.warning("No candidate documents retrieved.")
        return []

    # Step 2: Load the Cross-Encoder
    model = get_reranking_model()

    # Step 3: Create query-document pairs
    pairs = [
        (query, document.page_content)
        for document in candidate_documents
    ]

    # Step 4: Score query-document pairs
    reranking_scores = model.predict(pairs)

    # Step 5: Combine documents and reranking scores
    reranked_results = list(
        zip(candidate_documents, reranking_scores)
    )

    # Step 6: Sort by relevance score (highest first)
    reranked_results.sort(
        key=lambda item: float(item[1]),
        reverse=True
    )

    # Step 7: Return final Top-K
    final_results = [
        (document, float(score))
        for document, score in reranked_results[:k]
    ]

    logger.info(
        "Reranked %d candidates and returned %d documents.",
        len(candidate_documents),
        len(final_results)
    )

    return final_results
