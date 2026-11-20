
import logging

logger = logging.getLogger(__name__)


def normalize_source_path(source: str) -> str:
    """
    Normalize source paths so that Windows and Unix-style
    paths can be compared consistently.
    """
    return source.replace("\\", "/").removeprefix("./").strip()


def calculate_retrieval_metrics(
    retrieved_results: list,
    expected_sources: list,
    k: int = 3
) -> dict:
    """
    Calculate source-level retrieval metrics.

    retrieved_results:
        List of (Document, score) tuples returned by
        retrieve_documents().

    expected_sources:
        List of relevant source-file paths from the
        golden evaluation dataset.

    k:
        Maximum number of retrieved chunks to evaluate.
    """

    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer.")

    if not isinstance(expected_sources, list) or not expected_sources:
        raise ValueError("expected_sources must be a non-empty list.")

    if any(
        not isinstance(source, str) or not source.strip()
        for source in expected_sources
    ):
        raise ValueError(
            "Every expected source must be a non-empty string."
        )

    expected_set = {
        normalize_source_path(source)
        for source in expected_sources
    }

    # Extract unique source files from the top-k retrieved chunks.
    # Preserve the order in which each source first appears.
    retrieved_sources = []
    seen_sources = set()

    for document, score in retrieved_results[:k]:

        source = document.metadata.get("source")

        if not isinstance(source, str) or not source.strip():
            continue

        normalized_source = normalize_source_path(source)

        if normalized_source not in seen_sources:
            retrieved_sources.append(normalized_source)
            seen_sources.add(normalized_source)

    # Identify relevant retrieved source files.
    relevant_sources = [
        source
        for source in retrieved_sources
        if source in expected_set
    ]

    relevant_count = len(relevant_sources)

    # Precision: relevant unique sources / retrieved unique sources.
    precision = (
        relevant_count / len(retrieved_sources)
        if retrieved_sources
        else 0.0
    )

    # Recall: retrieved relevant sources / expected relevant sources.
    recall = relevant_count / len(expected_set)

    # Hit Rate: did retrieval find at least one relevant source?
    hit_rate = 1.0 if relevant_count > 0 else 0.0

    # MRR: reciprocal rank of the first relevant source.
    first_relevant_rank = None

    for rank, source in enumerate(retrieved_sources, start=1):
        if source in expected_set:
            first_relevant_rank = rank
            break

    mrr = (
        1.0 / first_relevant_rank
        if first_relevant_rank is not None
        else 0.0
    )

    metrics = {
        "precision_at_k": precision,
        "recall_at_k": recall,
        "hit_rate_at_k": hit_rate,
        "mrr": mrr,
        "retrieved_sources": retrieved_sources,
        "relevant_sources": relevant_sources,
        "first_relevant_rank": first_relevant_rank
    }

    logger.info(
        "Retrieval metrics calculated successfully."
    )

    return metrics