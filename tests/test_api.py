from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Technical Documentation RAG API is running."
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_query_endpoint(monkeypatch):
    def mock_generate_answer(question):
        return {
            "answer": "FastAPI is a Python web framework.",
            "sources": ["fastapi_basics.md"]
        }

    monkeypatch.setattr(
        "src.api.main.generate_answer",
        mock_generate_answer
    )

    response = client.post(
        "/query",
        json={"question": "What is FastAPI?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "FastAPI is a Python web framework."
    assert response.json()["sources"] == ["fastapi_basics.md"]

import pytest

@pytest.mark.parametrize(
    "question",
    [
        "",
        "   ",
        "a" * 2001,
    ]
)
def test_invalid_query_input(question):
    response = client.post(
        "/query",
        json={"question": question}
    )

    assert response.status_code == 422

def test_query_endpoint_internal_error(monkeypatch):
    def mock_generate_answer(question):
        raise Exception("Simulated internal error")

    monkeypatch.setattr(
        "src.api.main.generate_answer",
        mock_generate_answer
    )

    response = client.post(
        "/query",
        json={"question": "What is FastAPI?"}
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An unexpected error occurred while processing your question."
    }