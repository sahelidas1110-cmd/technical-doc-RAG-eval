
# DeepEval Failure Analysis

## Objective

Analyze the failed test cases from the full DeepEval evaluation of
85 answerable questions to identify recurring weaknesses in retrieval
and answer generation.

## Evaluation Setup

- Evaluation dataset: 85 answerable questions
- Evaluation model: gpt-4.1-mini
- Metric threshold: 0.7
- Metrics:
  - Contextual Precision
  - Contextual Recall
  - Faithfulness
  - Answer Relevancy
  - Answer Correctness (GEval)

## Overall Results

| Metric | Average Score | Pass Rate | Passed | Failed |
|---|---:|---:|---:|---:|
| Contextual Precision | 0.92 | 89.41% | 76 | 9 |
| Contextual Recall | 0.96 | 92.94% | 79 | 6 |
| Faithfulness | 0.97 | 96.47% | 82 | 3 |
| Answer Relevancy | 0.98 | 100.00% | 85 | 0 |
| Answer Correctness (GEval) | 0.89 | 96.47% | 82 | 3 |

Overall test case pass rate: 78.82% (67/85)

## Failure Categories

### 1. Contextual Precision

9 failures.

Relevant chunks were sometimes ranked below irrelevant chunks.

Affected questions:

- Q009: Python loop else and break
- Q013: File modes w and a
- Q048: RAG evaluation and regression testing
- Q056: Pydantic field and model validators
- Q067: OAuth2 and JWT validation
- Q077: OAuth2 scopes
- Q087: FastAPI Query constraints
- Q081: FastAPI documentation endpoints
- Q092: FastAPI endpoint testing

Observation:

In several cases, relevant information was present in the retrieved
contexts but was not ranked sufficiently high. This indicates potential
retrieval ranking weaknesses.

### 2. Contextual Recall

6 failures.

The retrieved context did not fully support all the information
required by the expected answer.

Affected questions:

- Q014: Python __main__ behavior
- Q067: OAuth2 token validation
- Q073: Uvicorn worker configuration
- Q082: OAuth2 password flow and JWT validation
- Q083: Middleware and exception handling
- Q092: Testing FastAPI endpoints with external dependencies

Observation:

Some multi-part questions require several related pieces of information.
The retrieved context may contain only a portion of the information
required for a complete answer.

Potential contributing factors include chunk boundaries, retrieval
coverage, corpus completeness and multi-part query complexity.

### 3. Faithfulness

3 failures.

Affected questions:

- Q052: Agent evaluation and tracing
- Q060: FastAPI route ordering
- Q096: FastAPI deployment and memory considerations

Observation:

These failures require inspection of the actual answer and retrieved
context to determine whether the generated answer contradicted,
misrepresented or inadequately used the retrieved evidence.

### 4. Answer Correctness (GEval)

3 failures.

Affected questions:

- Q045: Offline vs online evaluation
- Q048: RAG evaluation strategy
- Q091: Asynchronous FastAPI testing

Observation:

The failures indicate incomplete coverage of the expected answer or
inaccurate technical details.

### 5. Answer Relevancy

No failures.

All 85 questions passed Answer Relevancy.

Observation:

The application consistently generates responses relevant to the
user's questions.

## Overall Analysis

The RAG application demonstrates strong answer relevance,
faithfulness and contextual recall overall.

However, the evaluation identifies several areas for investigation:

1. Retrieval ranking: relevant chunks are not always ranked optimally.
2. Context completeness: some multi-part questions lack complete
   supporting context.
3. Grounding: a small number of answers contradict retrieved evidence.
4. Answer completeness and technical precision: some answers omit
   important details required by the expected answers.

The failure analysis is diagnostic. No retrieval configuration,
embedding model, prompt or threshold was changed based solely
on these results.

## Next Steps

1. Evaluate the 15 unanswerable questions separately.
2. Analyze abstention behavior.
3. Investigate representative retrieval and generation failures.
4. Decide on targeted improvements based on evidence.
5. Re-evaluate using the same evaluation dataset.

## Report

Full evaluation report:

evaluation/reports/deepeval_report_85_20261123_132636.json

=============================================================

# DeepEval Failure Analysis — Final Verified Run

## Evaluation Summary

- Dataset: 85 answerable questions
- Evaluation model: gpt-4.1-mini
- Metric threshold: 0.7
- Overall pass rate: 82.35% (70/85)
- Questions with at least one failed metric: 15
- Evaluation cost: $0.5131432

## Failure Distribution

| Metric | Failures |
|---|---:|
| Contextual Precision | 10 |
| Contextual Recall | 6 |
| Answer Correctness | 3 |

Failure counts overlap because a question can fail multiple metrics.

## 1. Retrieval Ranking Issues

Several questions had relevant chunks retrieved, but irrelevant or less relevant chunks were ranked higher.

Examples:
- Q009 — Loop else and break behavior
- Q013 — Python file modes (`w` vs `a`)
- Q033 — Multi-query retrieval
- Q048 — RAG evaluation and regression detection
- Q056 — Pydantic field and model validators
- Q067 — OAuth2 token validation
- Q077 — OAuth2 scopes
- Q081 — FastAPI documentation endpoints
- Q087 — Query parameter validation
- Q092 — FastAPI testing and dependency injection

### Observation

The presence of relevant information in the retrieved context does not guarantee high contextual precision. Retrieval ranking remains an improvement area.

## 2. Context Completeness Issues

Questions that failed Contextual Recall:

- Q014 — Python module execution and `__name__`
- Q056 — Field-validator examples and explanation
- Q067 — JWT validation and account checks
- Q082 — Complete OAuth2 password-form and JWT flow
- Q083 — Middleware and exception-handler responsibilities
- Q092 — Mocking external dependencies in endpoint tests

### Observation

Some retrieved contexts supported only a portion of the expected answer. Multi-part questions particularly exposed missing contextual information.

## 3. Answer Correctness Issues

- Q048 — Missing evaluation dimensions such as latency, cost, and separate retrieval/generation evaluation.
- Q045 — Incomplete comparison between offline and online evaluation.
- Q091 — Asynchronous testing details were incomplete; HTTPX AsyncClient and ASGITransport were expected.

### Observation

Answer correctness failures were primarily associated with incomplete coverage of the requested concepts or procedural details.

## 4. Improvement Opportunities

1. Investigate retrieval-ranking errors.
2. Improve contextual coverage for multi-part questions.
3. Improve answer completeness for comparison and procedural questions.
4. Use failed questions as regression-test cases for future experiments.
5. Evaluate future changes using the same dataset and metrics.

## 5. Conclusion

The verified evaluation achieved an overall pass rate of 82.35%.

Faithfulness and answer relevancy achieved 100% pass rates, while contextual precision, contextual recall, and answer correctness revealed opportunities for further improvement.

The failure analysis provides a structured basis for future retrieval, context-construction, and answer-generation experiments.