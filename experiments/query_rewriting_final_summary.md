
# Query Rewriting Experiment — Final Summary

## 1. Objective

The objective of this experiment was to investigate whether LLM-based query rewriting could improve retrieval performance in our RAG application.

We also investigated whether query rewriting could improve retrieval of relevant documentation for queries containing multiple technical concepts.

## 2. Evaluation Setup

- Evaluation dataset: Golden dataset
- Total questions: 100
- Answerable questions evaluated: 85
- Unanswerable questions skipped for retrieval evaluation: 15
- Retrieval configuration: Top-3
- Evaluation metrics:
  - Precision@3
  - Recall@3
  - Hit Rate@3
  - Mean Reciprocal Rank (MRR)

## 3. Baseline Results

| Metric | Baseline |
|---|---:|
| Precision@3 | 0.8098 |
| Recall@3 | 0.9882 |
| Hit Rate@3 | 0.9882 |
| MRR | 0.9412 |

## 4. Experiment 1 — Initial Automated Query Rewriting

An LLM-based query rewriting component was implemented in `src/query_rewriter.py`.

The rewritten query was used for retrieval, while the original query was retained for baseline comparison.

### Results

| Metric | Baseline | Query Rewriting |
|---|---:|---:|
| Precision@3 | 0.8098 | 0.8275 |
| Recall@3 | 0.9882 | 0.9824 |
| Hit Rate@3 | 0.9882 | 1.0000 |
| MRR | 0.9412 | 0.9588 |

### Observations

- Precision@3 improved.
- Recall@3 decreased slightly.
- Hit Rate@3 improved to 1.0000.
- MRR improved.
- Q052, which previously missed the expected source within top-3, was successfully recovered.

The experiment demonstrated that query rewriting could improve retrieval performance, although the improvement was not uniform across all metrics or questions.

## 5. Experiment 2 — Query Rewriting Prompt Refinement

The query rewriting prompt was refined to emphasize:

- Preservation of all distinct concepts.
- Preservation of multi-part requirements.
- Balanced coverage of different concepts.
- Avoiding overemphasis on a dominant concept.

The purpose was to reduce retrieval regressions observed in questions such as Q043 and Q092.

### Results

| Metric | Baseline | Revised Query Rewriting |
|---|---:|---:|
| Precision@3 | 0.8098 | 0.8333 |
| Recall@3 | 0.9882 | 0.9824 |
| Hit Rate@3 | 0.9882 | 0.9882 |
| MRR | 0.9412 | 0.9471 |

### Comparison with Experiment 1

| Metric | Initial Prompt | Revised Prompt |
|---|---:|---:|
| Precision@3 | 0.8275 | 0.8333 |
| Recall@3 | 0.9824 | 0.9824 |
| Hit Rate@3 | 1.0000 | 0.9882 |
| MRR | 0.9588 | 0.9471 |

### Observations

- Precision@3 improved slightly with the revised prompt.
- Recall@3 remained unchanged compared with the initial query rewriting experiment.
- Hit Rate@3 declined compared with the initial experiment.
- MRR also declined compared with the initial experiment.

The revised prompt did not improve the overall balance of retrieval metrics compared with the initial query rewriting prompt.

## 6. Decision

The initial query rewriting prompt will be retained as the preferred experimental version for now.

The revised prompt refinement will not be selected because it did not provide a better overall balance of evaluation metrics.

The initial query rewriting experiment demonstrated improvements in Precision@3, Hit Rate@3 and MRR compared with the baseline, while Recall@3 decreased slightly.

Query rewriting will remain an experimental retrieval enhancement rather than being considered a universally beneficial solution.

## 7. Limitations

- Query rewriting introduces an additional LLM call.
- It may increase latency and API cost.
- Rewriting can alter the emphasis of the original question.
- Improvements are not consistent across all questions or metrics.
- The evaluation is based on a finite golden dataset.
- Retrieval metrics do not directly measure generated answer quality.

## 8. Artifacts

- `src/query_rewriter.py`
- `evaluation/evaluate_retrieval_with_query_rewriting.py`
- `evaluation/query_rewriting_comparison_report.json`
- `evaluation/analyze_query_rewriting_comparison.py`
- `evaluation/diagnose_query_rewriting_regressions.py`
- `evaluation/experiment_q052_query_rewrite.py`
- `experiments/query_rewriting_q052.md`

## 9. Conclusion

LLM-based query rewriting was evaluated as a retrieval optimization technique.

The initial experiment improved Precision@3, Hit Rate@3 and MRR compared with the baseline, but slightly reduced Recall@3.

A prompt refinement experiment was conducted to investigate retrieval regressions. The revised prompt did not outperform the initial prompt across the overall metric balance.

The initial query rewriting prompt is therefore retained as the preferred experimental version.

Further retrieval optimization will investigate chunking strategies, embedding models, hybrid search, reranking and retrieval depth.
