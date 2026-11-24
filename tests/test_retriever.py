import pytest
from src.retriever import retrieve_documents


def test_retriever_rejects_empty_query():
    with pytest.raises(ValueError, match="Query must be a non-empty string."):
        retrieve_documents("")

@pytest.mark.parametrize(
    "k",
    [
        0,
        -1,
        2.5,
        True,
        "3",
    ]
)
def test_retriever_rejects_invalid_k(k):
    with pytest.raises(ValueError, match="k must be a positive integer."):
        retrieve_documents("What is FastAPI?", k=k)

from unittest.mock import MagicMock


def test_retriever_calls_vector_store_correctly(monkeypatch):
    mock_vector_store = MagicMock()

    expected_results = [
        ("document_1", 0.25),
        ("document_2", 0.40),
        ("document_3", 0.55),
    ]

    mock_vector_store.similarity_search_with_score.return_value = expected_results

    monkeypatch.setattr(
        "src.retriever.get_vector_store",
        lambda: mock_vector_store
    )

    results = retrieve_documents("  What is FastAPI?  ", k=3)

    mock_vector_store.similarity_search_with_score.assert_called_once_with(
        query="What is FastAPI?",
        k=3
    )

    assert results == expected_results