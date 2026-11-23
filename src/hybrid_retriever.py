
import logging
import re
from functools import lru_cache

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from src.retriever import get_vector_store

logger = logging.getLogger(__name__)

RRF_CONSTANT = 60
CANDIDATE_K = 20


def get_document_key(document: Document) -> str:
    """Create a stable key for identifying a document chunk."""

    source = document.metadata.get("source", "")
    chunk_index = document.metadata.get("chunk_index", "")

    if source and chunk_index != "":
        return f"{source}::{chunk_index}"

    return document.page_content


def tokenize(text: str) -> list[str]:
    """Tokenize text while preserving technical identifiers."""

    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


@lru_cache(maxsize=1)
def get_bm25_index():
    """Build and cache the BM25 index from the selected Chroma collection."""

    vector_store = get_vector_store()

    collection_data = vector_store._collection.get(
        include=["documents", "metadatas"]
    )

    documents = collection_data["documents"]
    metadatas = collection_data["metadatas"]

    if not documents:
        raise ValueError("No documents found in the Chroma collection.")

    corpus_documents = [
        Document(
            page_content=content,
            metadata=metadata or {}
        )
        for content, metadata in zip(documents, metadatas)
    ]

    tokenized_corpus = [
        tokenize(document.page_content)
        for document in corpus_documents
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    logger.info("BM25 index built with %d chunks.", len(corpus_documents))

    return corpus_documents, bm25


def retrieve_hybrid_documents(
    query: str,
    k: int = 3,
    candidate_k: int = CANDIDATE_K
):
    """Retrieve documents using Dense + BM25 and combine rankings with RRF."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string.")

    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer.")

    if not isinstance(candidate_k, int) or isinstance(candidate_k, bool) or candidate_k <= 0:
        raise ValueError("candidate_k must be a positive integer.")

    query = query.strip()

    vector_store = get_vector_store()

    # Dense retrieval
    dense_results = vector_store.similarity_search_with_score(
        query=query,
        k=candidate_k
    )

    dense_documents = [document for document, _ in dense_results]

    # BM25 retrieval
    corpus_documents, bm25 = get_bm25_index()

    tokenized_query = tokenize(query)

    bm25_scores = bm25.get_scores(tokenized_query)

    bm25_ranked_indices = sorted(
        range(len(bm25_scores)),
        key=lambda index: bm25_scores[index],
        reverse=True
    )[:candidate_k]

    bm25_documents = [
        corpus_documents[index]
        for index in bm25_ranked_indices
    ]

    # Reciprocal Rank Fusion
    fused_scores = {}
    fused_documents = {}

    for rank, document in enumerate(dense_documents, start=1):
        document_key = get_document_key(document)

        fused_scores[document_key] = (
            fused_scores.get(document_key, 0)
            + 1 / (RRF_CONSTANT + rank)
        )

        fused_documents[document_key] = document

    for rank, document in enumerate(bm25_documents, start=1):
        document_key = get_document_key(document)

        fused_scores[document_key] = (
            fused_scores.get(document_key, 0)
            + 1 / (RRF_CONSTANT + rank)
        )

        fused_documents[document_key] = document

    ranked_keys = sorted(
        fused_scores,
        key=lambda key: fused_scores[key],
        reverse=True
    )

    final_results = [
        (fused_documents[key], fused_scores[key])
        for key in ranked_keys[:k]
    ]

    logger.info(
        "Hybrid retrieval returned %d chunks.",
        len(final_results)
    )

    return final_results
