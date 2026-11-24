# Phase 6 — FastAPI Backend Development

## 1. Objective

The objective of Phase 6 was to expose the existing Technical Documentation RAG pipeline through a REST API using FastAPI.

The backend provides an interface through which external applications can submit questions and receive answers and source information from the RAG pipeline.

## 2. Architecture

The backend connects the API layer with the existing RAG pipeline.

**Application flow:**

1. Client submits a question through the API.
2. FastAPI receives the HTTP request.
3. Pydantic validates the request.
4. The API invokes `generate_answer()` from `src/rag_pipeline.py`.
5. The RAG pipeline retrieves relevant documents from ChromaDB.
6. Retrieved documents are filtered and context is constructed.
7. The LLM generates a grounded answer or abstains if sufficient information is unavailable.
8. FastAPI returns the answer and source information to the client.

### Architecture components

- **FastAPI:** Backend API framework.
- **Pydantic:** Request validation and response schema definition.
- **Uvicorn:** ASGI server used to run the FastAPI application.
- **RAG Pipeline:** Existing RAG implementation.
- **ChromaDB:** Vector database for document retrieval.
- **OpenAI:** Embedding and LLM services.
- **LangSmith:** Tracing and observability.

## 3. Project Structure

The following API files were created:

```text
src/
└── api/
    ├── main.py
    └── schemas.py
```

### `src/api/main.py`

Responsible for:

- Creating the FastAPI application.
- Defining API endpoints.
- Invoking the existing RAG pipeline.
- Returning structured API responses.
- Handling unexpected exceptions.

### `src/api/schemas.py`

Responsible for:

- Defining request models.
- Defining response models.
- Validating question input.
- Enforcing question length constraints.
- Rejecting whitespace-only questions.

## 4. API Endpoints

### GET `/`

Purpose: Verify that the API application is running.

Response:

```json
{
  "message": "Technical Documentation RAG API is running."
}
```

### GET `/health`

Purpose: Provide a basic health-check endpoint.

Response:

```json
{
  "status": "healthy"
}
```

### POST `/query`

Purpose: Accept a user question and invoke the RAG pipeline.

Request:

```json
{
  "question": "What is dependency injection in FastAPI?"
}
```

The endpoint invokes:

```python
generate_answer(request.question)
```

The response contains:

- `answer`: The answer returned by the RAG pipeline.
- `sources`: Source information returned by the RAG pipeline.

## 5. Request and Response Schemas

### QueryRequest

The request schema validates incoming questions.

Validation rules:

- The question is required.
- The question must be a string.
- Minimum length is one character.
- Maximum length is 2,000 characters.
- Leading and trailing whitespace is removed.
- Whitespace-only questions are rejected.

### QueryResponse

The response schema defines:

- `answer`: String containing the generated answer.
- `sources`: List containing source information.

## 6. Request Validation

Pydantic validation is applied before the RAG pipeline executes.

The following validation scenarios were tested:

| Test | Expected behavior | Result |
|---|---|---|
| Valid question | Accepted | Passed |
| Empty question | Rejected | Passed |
| Whitespace-only question | Rejected | Passed |
| Question exceeding 2,000 characters | Rejected | Passed |

Invalid requests return HTTP 422 Unprocessable Entity.

## 7. RAG Pipeline Integration

The FastAPI endpoint integrates with the existing RAG pipeline through:

```python
from src.rag_pipeline import generate_answer
```

The endpoint calls:

```python
result = generate_answer(request.question)
```

The existing RAG pipeline is responsible for:

- Document retrieval.
- Retrieval-distance filtering.
- Context construction.
- Prompt construction.
- LLM invocation.
- Answer generation.
- Abstention when sufficient relevant information is unavailable.
- Source information generation.

The API layer does not duplicate the RAG implementation. It acts as an interface to the existing pipeline.

## 8. Error Handling

Unexpected errors during query processing are handled using FastAPI's `HTTPException`.

The API:

- Attempts to execute the RAG pipeline.
- Catches unexpected exceptions.
- Prints the error in the terminal for debugging.
- Returns HTTP 500 Internal Server Error.
- Provides a generic error message to the client rather than exposing internal implementation details.

This represents basic API-level error handling.

## 9. Swagger UI

FastAPI automatically generates interactive API documentation.

Swagger UI was accessed at:

`http://127.0.0.1:8000/docs`

Swagger UI was used to:

- Inspect the API endpoints.
- Submit API requests.
- Test request validation.
- Inspect response bodies.
- Verify HTTP response codes.

## 10. Running the API

The API was launched using:

```powershell
python -m uvicorn src.api.main:app --reload
```

Command components:

- `python -m uvicorn`: Runs Uvicorn through the active Python environment.
- `src.api.main`: Identifies the Python module.
- `app`: Identifies the FastAPI application instance.
- `--reload`: Enables automatic server reload when code changes.

## 11. API Testing

Testing was performed through Swagger UI.

### Test 1 — Root endpoint

Endpoint: `GET /`

Result: Successfully returned the application-running message.

### Test 2 — Health endpoint

Endpoint: `GET /health`

Result: Successfully returned the health status.

### Test 3 — Answerable question

Endpoint: `POST /query`

Question:

"What is dependency injection in FastAPI?"

Result:

- Request successfully processed.
- RAG pipeline invoked.
- Relevant documentation retrieved.
- LLM generated an answer.
- Source information returned.
- LangSmith trace generated.

### Test 4 — Unanswerable question

Question:

"Who is the president of France?"

Result:

- RAG pipeline invoked.
- Insufficient relevant information detected.
- Abstention response returned.
- Sources returned as an empty list.
- LangSmith trace generated.

### Test 5 — Whitespace-only question

Result: Rejected with HTTP 422.

### Test 6 — Question exceeding maximum length

Result: Rejected with HTTP 422.

### Test 7 — Empty question

Result: Rejected with HTTP 422.

## 12. LangSmith Observability

The API invokes the existing instrumented RAG pipeline.

LangSmith tracing was verified for:

- Answerable API requests.
- Unanswerable API requests.
- `generate_answer`.
- Nested retrieval execution.
- Context construction.

This enables observability of the RAG pipeline during API-based execution.

## 13. Phase 6 Outcome

Phase 6 successfully exposed the existing RAG pipeline through a FastAPI backend.

The API now supports:

- Basic application status endpoint.
- Health-check endpoint.
- Query endpoint.
- Pydantic request validation.
- Structured response validation.
- RAG pipeline integration.
- Basic exception handling.
- Abstention behavior through the existing RAG pipeline.
- Swagger UI-based testing.
- LangSmith tracing during API execution.

## 14. Current Limitations and Future Enhancements

The backend currently implements basic API functionality.

Potential future enhancements include:

- More comprehensive logging.
- Advanced exception handling.
- Authentication and authorization.
- Rate limiting.
- API monitoring.
- Asynchronous request processing where appropriate.
- Automated API tests.
- Docker-based deployment.
- CI/CD integration.

## Conclusion

The FastAPI backend establishes the application layer for the Technical Documentation RAG assistant.

The existing retrieval, context construction, answer generation, evaluation, and observability components can now be accessed through a REST API.

This backend will serve as the integration layer for the Streamlit frontend and future deployment infrastructure.
