# Query Rewriting Experiment — Q052

## 1. Objective

Investigate whether query reformulation can improve retrieval performance for Q052, a question that failed to retrieve its expected source document within the top 3 results during baseline retrieval evaluation.

The experiment compares the original question against a manually reformulated query using the same embedding model, vector database, retriever, top-K setting, and retrieval metrics.

## 2. Problem Identified

During the baseline retrieval evaluation, Q052 was the only answerable question that failed to retrieve its expected source document within the top 3 results.

**Question:**

Design an evaluation approach for a multi-step agent that searches a knowledge base and then uses a calculator. Which agent-specific behaviors should be measured, and what execution evidence could tracing provide when a task fails?

**Expected source:**

`data/raw/langchain/tools_and_evaluation.md`

The baseline retrieval diagnostic showed that the expected source was ranked 4th, outside the top-3 retrieval cutoff.

This indicated a retrieval-ranking problem rather than a missing source document.

## 3. Hypothesis

Reformulating the query using terminology and concepts explicitly represented in the source documentation may improve retrieval ranking and increase the likelihood of retrieving the expected source within the top-K results.

## 4. Experimental Setup

| Parameter | Value |
|---|---|
| Question ID | Q052 |
| Expected source | `data/raw/langchain/tools_and_evaluation.md` |
| Retrieval method | Similarity search |
| Top-K | 3 |
| Embedding model | text-embedding-3-small |
| Vector database | Chroma |
| Evaluation approach | Source-level retrieval metrics |
| Query rewriting | Manual reformulation |

The retriever, embedding model, vector store, top-K setting, and evaluation metrics remained unchanged.

Only the query text was modified.

## 5. Baseline Query

### Original question

Design an evaluation approach for a multi-step agent that searches a knowledge base and then uses a calculator. Which agent-specific behaviors should be measured, and what execution evidence could tracing provide when a task fails?

### Baseline retrieval results

| Rank | Source | Distance |
|---|---|---:|
| 1 | `agents.md` | 0.6977 |
| 2 | `agents.md` | 0.9007 |
| 3 | `agents.md` | 0.9035 |

The expected source was not retrieved within the top 3 results.

### Baseline metrics

| Metric | Value |
|---|---:|
| Precision@3 | 0.00 |
| Recall@3 | 0.00 |
| Hit Rate@3 | 0.00 |
| MRR | 0.00 |

## 6. Query Rewriting Experiment

The original query was reformulated using evaluation terminology and tracing-related concepts.

### Rewritten query

Agent evaluation metrics tool selection accuracy tool argument accuracy tool execution success task completion final answer quality safety. LangSmith tracing execution trace retrieved documents prompts LLM requests responses duration errors metadata.

### Rewritten query retrieval results

| Rank | Source | Distance |
|---|---|---:|
| 1 | `tools_and_evaluation.md` | 0.6368 |
| 2 | `agents.md` | 0.7822 |
| 3 | `tools_and_evaluation.md` | 0.7902 |

The expected source was retrieved at rank 1.

### Rewritten query metrics

| Metric | Value |
|---|---:|
| Precision@3 | 0.50 |
| Recall@3 | 1.00 |
| Hit Rate@3 | 1.00 |
| MRR | 1.00 |

## 7. Baseline vs. Experiment Comparison

| Metric | Baseline | Rewritten Query |
|---|---:|---:|
| Precision@3 | 0.00 | 0.50 |
| Recall@3 | 0.00 | 1.00 |
| Hit Rate@3 | 0.00 | 1.00 |
| MRR | 0.00 | 1.00 |
| Expected source retrieved | No | Yes |
| First relevant rank | Not found | 1 |

The manually reformulated query successfully retrieved the expected source at rank 1.

## 8. Analysis

The baseline query retrieved three chunks from `agents.md`. Although these chunks were semantically related to agent evaluation, the expected source `tools_and_evaluation.md` was not retrieved within the top 3.

The rewritten query explicitly incorporated terminology related to agent evaluation and tracing, including:

- Tool selection accuracy
- Tool argument accuracy
- Tool execution success
- Task completion
- Final answer quality
- Safety
- LangSmith tracing
- Execution trace
- Retrieved documents
- LLM requests and responses

The rewritten query retrieved `tools_and_evaluation.md` at rank 1.

This suggests that query formulation can influence semantic retrieval ranking.

The experiment demonstrates that the existing corpus and retrieval system can retrieve the expected source when the query is formulated using terminology more closely aligned with the source content.

## 9. Limitations

- The experiment was conducted on a single question, Q052.
- Query reformulation was performed manually.
- The experiment does not establish that query rewriting will improve retrieval performance across the entire golden dataset.
- The experiment does not evaluate answer generation quality.
- The experiment does not demonstrate that automated query rewriting will consistently improve retrieval.

## 10. Conclusion

Manual query reformulation improved Q052 retrieval performance.

The expected source was not retrieved within the top 3 results for the original query. After reformulation, the expected source was retrieved at rank 1.

The experiment provides evidence that query formulation is a potential retrieval optimization technique for the RAG application.

Further evaluation across the golden dataset is required before incorporating query rewriting into the production retrieval pipeline.

## 11. Experiment Artifacts

- Golden dataset: `evaluation/golden_dataset.json`
- Retrieval metrics implementation: `evaluation/retrieval_metrics.py`
- Retrieval evaluation script: `evaluation/evaluate_retrieval.py`
- Query variants diagnostic: `evaluation/diagnose_q052_query_variants.py`
- Controlled comparison: `evaluation/experiment_q052_query_rewrite.py`
- Retrieval report: `evaluation/retrieval_report.json`
