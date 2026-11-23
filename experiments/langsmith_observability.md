# LangSmith Observability

## 1. Overview

LangSmith was integrated into the Technical Documentation RAG Evaluation Harness to provide tracing and observability of the RAG pipeline.

The objective was to inspect individual execution steps, understand retrieval and answer-generation behavior, monitor execution time and token usage, and debug RAG responses.

## 2. Objectives

- Trace end-to-end RAG execution.
- Monitor individual pipeline components.
- Inspect retrieved documents and retrieval scores.
- Inspect LLM inputs and generated outputs.
- Observe execution time and token usage.
- Track model and pipeline configuration through metadata.
- Debug answerable and unanswerable queries.

## 3. LangSmith Configuration

LangSmith tracing was configured through environment variables in the project's `.env` file.

Configuration included:

- `LANGSMITH_TRACING=true`
- `LANGSMITH_API_KEY`
- `LANGSMITH_PROJECT=technical-doc-RAG-eval`
- `LANGSMITH_ENDPOINT=https://api.smith.langchain.com`

Sensitive credentials are stored locally in environment variables and are not committed to source control.

## 4. Instrumented Components

### 4.1 generate_answer

The main RAG pipeline function was instrumented using LangSmith's `@traceable` decorator.

The trace captures the overall RAG execution, including retrieval, context construction, answer generation, and abstention behavior.

Tags:

- rag
- retrieval
- answer-generation

Metadata:

- Pipeline name
- Embedding model
- Chunk size
- Chunk overlap
- Top-K retrieval
- Retrieval threshold

### 4.2 retrieve_documents

The document retrieval function was instrumented to inspect vector search execution.

The trace provides visibility into:

- Query input
- Retrieved documents
- Retrieval scores
- Vector-store retrieval behavior

Tags:

- rag
- retrieval
- vector-search

### 4.3 build_context

The context-construction function was instrumented to observe how retrieved document chunks are assembled into the context passed to the LLM.

This helps debug context construction and understand the information supplied to the answer-generation stage.

Tags:

- rag
- context-construction

## 5. Trace Hierarchy

The observed execution hierarchy included:

- `generate_answer`
  - `retrieve_documents`
  - `build_context`
  - LangChain prompt and LLM execution

This hierarchical tracing makes it possible to inspect the individual components of an end-to-end RAG execution.

## 6. Trace Validation

Tracing was validated using both answerable and unanswerable queries.

### 6.1 Answerable Query

Example:

"What is dependency injection in FastAPI?"

Observations:

- The RAG pipeline successfully retrieved relevant documentation chunks.
- Retrieved documents were visible within the retrieval trace.
- Context construction was visible as a nested trace.
- LLM input and generated answer could be inspected.
- Trace metadata was available.
- Execution time, token usage and cost information were visible in LangSmith.

### 6.2 Unanswerable Query

Example:

"Who is the president of France?"

Observations:

- The query was handled by the retrieval and relevance-filtering logic.
- The pipeline returned an abstention response when sufficient relevant documentation was unavailable.
- The response contained no document sources.
- The early-return execution path was successfully traced using the custom `generate_answer` instrumentation.

This validated that tracing captures both normal answer-generation paths and early-abstention paths.

## 7. Trace-Level Observability

The following information was inspected through LangSmith:

- Input query
- Retrieved documents
- Retrieval distances
- Context construction
- LLM output
- Execution hierarchy
- Execution duration
- Token usage
- Estimated execution cost
- Tags
- Metadata
- Model configuration

## 8. Trace Analysis — Q078

A trace-level investigation was conducted for question Q078 from the answerable evaluation dataset.

Question:

"A FastAPI service uses an OpenAI API key, database URL, and JWT signing secret. Explain how to centralize these settings with Pydantic Settings, load them from environment variables or a local .env file during development, and avoid exposing secrets in source control."

### Retrieval observations

- Three document chunks were retrieved.
- All retrieved chunks originated from `testing_deployment.md`.
- The retrieved context covered Pydantic Settings, environment variables, `.env` configuration and production secret management.
- All retrieved distances were below the configured retrieval threshold of 1.05.

### Answer observations

- The generated response was largely grounded in the retrieved context.
- The answer included a Pydantic Settings example.
- It explained environment-variable and `.env` usage.
- It addressed secure handling of secrets in production.
- A minor naming inconsistency was observed between the `jwt_secret_key` field and the `SECRET_KEY` environment variable in the example.

### Evaluation context

The question received an Answer Correctness score of approximately 0.7119 in the DeepEval answerable evaluation.

The trace was inspected to investigate potential answer-quality issues despite relevant retrieval.

### Conclusion

The retrieved context was relevant and sufficient for the question. The observed inconsistency was an answer-quality issue rather than evidence of a retrieval configuration problem.

No retrieval configuration changes were justified based on this trace alone.

## 9. Selected RAG Configuration

The configuration used during the observability experiments:

| Parameter | Value |
|---|---|
| Chat model | gpt-4.1-mini |
| Embedding model | text-embedding-3-large |
| Chunk size | 400 |
| Chunk overlap | 80 |
| Top-K retrieval | 3 |
| Retrieval threshold | 1.05 |
| Vector store | ChromaDB |
| Temperature | 0 |

## 10. LangSmith and DeepEval

LangSmith and DeepEval serve complementary purposes in this project.

### LangSmith

Used for execution-level observability:

- Trace inspection
- Debugging individual queries
- Inspecting retrieval and context construction
- Inspecting LLM inputs and outputs
- Monitoring execution time
- Observing token usage and cost
- Tracking metadata

### DeepEval

Used for systematic evaluation of RAG quality:

- Context Precision
- Context Recall
- Faithfulness
- Answer Relevancy
- Answer Correctness
- Abstention Correctness

LangSmith helps investigate individual executions, while DeepEval provides systematic evaluation across the evaluation dataset.

## 11. Limitations

- Trace inspection is observational and does not independently guarantee answer correctness.
- Individual trace analysis does not replace dataset-level evaluation.
- Token usage and cost observations are dependent on the traced execution and model configuration.
- Manual trace investigation is not a substitute for automated monitoring and regression testing.
- Successful abstention tests do not guarantee that the system will abstain correctly for every unsupported query.

## 12. Conclusion

LangSmith observability was successfully integrated into the RAG pipeline.

The main pipeline, document retrieval and context construction were instrumented and verified. Answerable and unanswerable execution paths were traced successfully, and individual traces were inspected for retrieved documents, generated answers, metadata, execution time and token usage.

LangSmith provides the observability layer for debugging and investigating individual RAG executions, complementing the project's systematic DeepEval evaluation framework.
