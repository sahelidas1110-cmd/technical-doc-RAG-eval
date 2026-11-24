from src.context_builder import build_context


def test_context_builder_returns_empty_string_when_no_documents():
    result = build_context([])

    assert result == ""

from types import SimpleNamespace


def test_context_builder_formats_document_correctly():
    doc = SimpleNamespace(
        page_content="  FastAPI is a Python web framework.  ",
        metadata={
            "source": "fastapi_basics.md",
            "category": "FastAPI",
            "chunk_index": 2,
        },
    )

    retrieved_documents = [(doc, 0.2567)]

    result = build_context(retrieved_documents)

    assert "[Source 1]" in result
    assert "File: fastapi_basics.md" in result
    assert "Category: FastAPI" in result
    assert "Chunk Index: 2" in result
    assert "Retrieval Distance: 0.2567" in result
    assert "FastAPI is a Python web framework." in result
    assert "  FastAPI is a Python web framework.  " not in result

def test_context_builder_skips_empty_document_content():
    doc = SimpleNamespace(
        page_content="   ",
        metadata={
            "source": "empty.md",
            "category": "Test",
            "chunk_index": 0,
        },
    )

    retrieved_documents = [(doc, 0.5)]

    result = build_context(retrieved_documents)

    assert result == ""

def test_context_builder_handles_missing_metadata():
    doc = SimpleNamespace(
        page_content="This is a test document.",
        metadata={},
    )

    retrieved_documents = [(doc, 0.5)]

    result = build_context(retrieved_documents)

    assert "File: Unknown source" in result
    assert "Category: Unknown category" in result
    assert "Chunk Index: Unknown" in result
    assert "This is a test document." in result

def test_context_builder_combines_multiple_documents():
    doc1 = SimpleNamespace(
        page_content="FastAPI is a web framework.",
        metadata={
            "source": "fastapi.md",
            "category": "FastAPI",
            "chunk_index": 1,
        },
    )

    doc2 = SimpleNamespace(
        page_content="Dependency injection manages dependencies.",
        metadata={
            "source": "dependency_injection.md",
            "category": "FastAPI",
            "chunk_index": 2,
        },
    )

    retrieved_documents = [
        (doc1, 0.25),
        (doc2, 0.35),
    ]

    result = build_context(retrieved_documents)

    assert "[Source 1]" in result
    assert "[Source 2]" in result
    assert "File: fastapi.md" in result
    assert "File: dependency_injection.md" in result
    assert "FastAPI is a web framework." in result
    assert "Dependency injection manages dependencies." in result
    assert "---" in result