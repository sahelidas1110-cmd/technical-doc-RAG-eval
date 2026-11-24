# Phase 8: Automated Testing

## Overview

Phase 8 focuses on implementing automated tests for the RAG application using `pytest`.

The objective is to verify the correctness and reliability of individual application components, including the API endpoints, retriever and context builder, without depending on actual LLM calls or the vector database during every test.

Automated testing helps identify regressions, validate input handling, verify expected behaviours and improve the maintainability of the application as new features are introduced.

---

## Testing Framework and Setup

### Tools Used

- **pytest:** Used as the testing framework to execute tests, validate expected behaviours using assertions and identify failures.
- **httpx:** Used alongside FastAPI's `TestClient` to test API endpoints and HTTP request/response behaviour.

### Installation

The testing dependencies were installed as development dependencies using `uv`:

```bash
uv add --dev pytest httpx
```

This keeps testing-related dependencies separate from the application's primary runtime dependencies.

---

## Test Directory Structure

The automated tests were organized inside the `tests` directory.

```text
tests/
│
├── __init__.py
├── test_api.py
├── test_retriever.py
└── test_context_builder.py
```

### Test Modules

- `test_api.py` – Tests the FastAPI endpoints, request validation and error handling.
- `test_retriever.py` – Tests retrieval function input validation and interaction with the vector store.
- `test_context_builder.py` – Tests context construction, formatting and edge cases.

---

## 1. API Testing

### Objective

The API tests validate the behaviour of the FastAPI application, including endpoint responses, request validation and error handling.

### Tests Implemented

#### 1. Root Endpoint Test

- Validates that the root endpoint returns HTTP status code `200`.
- Verifies the expected response message.

#### 2. Health Endpoint Test

- Validates that the health endpoint returns HTTP status code `200`.
- Verifies that the API reports a healthy status.

#### 3. Query Endpoint Test

- Tests the `/query` endpoint using a mocked answer-generation function.
- Verifies the response structure.
- Validates that the generated answer and source information are returned correctly.

#### 4. Invalid Query Input Tests

The query endpoint was tested with the following invalid inputs:

- Empty string.
- Whitespace-only input.
- Input exceeding the maximum permitted length of 2,000 characters.

The tests verify that the API returns HTTP `422 Unprocessable Entity` for invalid requests.

#### 5. Internal Error Handling Test

- Simulates an internal failure in the answer-generation function.
- Verifies that the API handles the exception.
- Validates that the API returns a controlled HTTP `500 Internal Server Error` response.

### API Test Results

All 7 API tests passed successfully.

---

## 2. Retriever Testing

### Objective

The retriever tests validate the behaviour of the retrieval component independently of the actual vector database.

The tests focus on query validation, retrieval parameter validation and verifying the interaction between the retriever and vector store.

### Tests Implemented

#### 1. Empty Query Validation

- Tests retrieval with an empty query.
- Verifies that a `ValueError` is raised with the expected error message.

#### 2. Invalid Retrieval Parameter Validation

The retriever was tested with invalid values of `k`:

- `0`
- `-1`
- `2.5`
- `True`
- `"3"`

The tests verify that invalid retrieval parameters are rejected.

#### 3. Vector Store Interaction Test

- Uses a mocked vector store.
- Patches the vector store retrieval dependency.
- Verifies that the query is stripped of unnecessary whitespace.
- Verifies that the expected retrieval parameter `k=3` is passed.
- Validates the returned retrieval results.

### Retriever Test Results

All 7 retriever tests passed successfully.

---

## 3. Context Builder Testing

### Objective

The context builder tests validate how retrieved documents are transformed into a structured context string that is subsequently used by the LLM in the RAG pipeline.

### Tests Implemented

#### 1. Empty Retrieval Results

- Tests the context builder with an empty list of retrieved documents.
- Verifies that an empty string is returned.

#### 2. Document Formatting

- Validates the formatting of a retrieved document.
- Verifies that source, category, chunk index, retrieval distance and document content are included.
- Verifies that unnecessary leading and trailing whitespace is removed from document content.

#### 3. Empty Document Content

- Tests a retrieved document containing whitespace-only content.
- Verifies that the document is skipped during context construction.

#### 4. Missing Metadata Handling

- Tests a document with missing metadata fields.
- Verifies that default values are used for source, category and chunk index.
- Ensures that context construction does not fail when metadata is missing.

#### 5. Multiple Document Combination

- Tests context construction using multiple retrieved documents.
- Verifies that each document is included in the context.
- Validates source numbering and document content.
- Verifies that retrieved chunks are separated appropriately.

### Context Builder Test Results

All 5 context builder tests passed successfully.

---

## 4. Mocking in Automated Tests

Mocking was used to isolate application components during testing.

Instead of invoking actual external dependencies such as the LLM or vector database, mock objects were used to simulate their behaviour.

### Why Mocking Was Used

- Avoids unnecessary API calls during automated tests.
- Reduces testing costs.
- Makes tests faster and more predictable.
- Allows individual components to be tested independently.
- Makes it possible to simulate failures and validate error handling.

Mocking was used in the API and retriever tests to isolate the components under test from their external dependencies.

---

## 5. Running Automated Tests

### Running the Entire Test Suite

The complete test suite can be executed using:

```bash
python -m pytest -v
```

### Running Individual Test Modules

API tests:

```bash
python -m pytest tests/test_api.py -v
```

Retriever tests:

```bash
python -m pytest tests/test_retriever.py -v
```

Context builder tests:

```bash
python -m pytest tests/test_context_builder.py -v
```

The `-v` flag enables verbose output, displaying individual test names and their execution results.

---

## 6. Overall Test Results

The complete test suite was executed successfully.

| Component | Number of Tests | Result |
|---|---:|---|
| API | 7 | Passed |
| Retriever | 7 | Passed |
| Context Builder | 5 | Passed |
| **Total** | **19** | **19 Passed** |

### Final Execution Result

All 19 automated tests passed successfully.

The tests validated API behaviour, input validation, error handling, retrieval parameter validation, vector store interaction, context construction, metadata handling and multiple-document formatting.

---

## 7. Outcome of Phase 8

Phase 8 established an automated testing foundation for the RAG application.

The implementation provides:

- Automated validation of API endpoints and request handling.
- Testing of retrieval logic and retrieval parameter validation.
- Testing of context construction and formatting.
- Validation of edge cases and error handling.
- Isolation of components using mocking.
- A repeatable test execution workflow using pytest.

Automated testing improves confidence in the application's behaviour and provides a foundation for regression testing as the RAG system evolves.

The test suite can be extended in future iterations to include additional integration tests, test coverage analysis and automated testing within a CI/CD pipeline.