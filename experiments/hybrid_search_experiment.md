# Hybrid Search Experiment

## Objective

Evaluate whether combining dense vector retrieval and BM25 keyword retrieval using Reciprocal Rank Fusion (RRF) improves retrieval performance compared with dense retrieval alone.

## Hypothesis

Dense vector retrieval captures semantic similarity, while BM25 captures keyword and exact-term relevance.

Combining both retrieval approaches using RRF may improve the retrieval of technical documentation, particularly when queries contain specific technical terms, identifiers, acronyms, or terminology.

## Experimental Setup

- Corpus: 30 Markdown documents
- Golden dataset: 100 questions
- Answerable questions: 85
- Unanswerable questions: 15 (excluded from retrieval evaluation)
- Embedding model: text-embedding-3-large
- Chunk size: 400 characters
- Chunk overlap: 80 characters
- Dense retrieval: Vector similarity search
- Sparse retrieval: BM25 (BM25Okapi)
- Fusion strategy: Reciprocal Rank Fusion (RRF)
- RRF constant: 60
- Dense retrieval candidate pool: Top 20
- BM25 retrieval candidate pool: Top 20
- Final Top-K: 3
- Query rewriting: Disabled

## Baseline

Dense retrieval using text-embedding-3-large and 400/80 chunking.

## Hybrid Retrieval

Dense vector retrieval and BM25 keyword retrieval were combined using Reciprocal Rank Fusion (RRF).

The hybrid retriever retrieved candidate chunks independently using dense retrieval and BM25, then combined their rankings using RRF to produce the final ranked list.

## Evaluation Metrics

- Precision@3
- Recall@3
- Hit Rate@3
- Mean Reciprocal Rank (MRR)

## Controlled Variables

The following remained unchanged:

- Corpus
- Golden dataset
- Embedding model
- Chunk size
- Chunk overlap
- Evaluation metrics
- Final Top-K
- Query rewriting setting

The retrieval strategy and fusion mechanism were the experimental variables.

## Results

| Configuration | Precision@3 | Recall@3 | Hit Rate@3 | MRR |
|---|---:|---:|---:|---:|
| Dense Retrieval | 0.8431 | 0.9765 | 0.9882 | 0.9471 |
| Hybrid Retrieval (Dense + BM25 + RRF) | 0.8255 | 0.9647 | 0.9647 | 0.9529 |

## Analysis

Hybrid retrieval did not improve overall retrieval performance across all evaluation metrics.

Compared with the dense retrieval baseline:

- **Precision@3:** Decreased from 0.8431 to 0.8255.
- **Recall@3:** Decreased from 0.9765 to 0.9647.
- **Hit Rate@3:** Decreased from 0.9882 to 0.9647.
- **MRR:** Increased from 0.9471 to 0.9529.

The hybrid approach showed a slight improvement in MRR, suggesting a small improvement in the average ranking position of relevant sources across the evaluation set.

However, the decrease in Precision@3, Recall@3, and Hit Rate@3 indicates that combining dense retrieval with BM25 using the current RRF configuration did not improve the overall retrieval effectiveness of the system.

The experiment demonstrates that combining semantic and keyword-based retrieval does not necessarily lead to better retrieval performance. The effectiveness of hybrid retrieval depends on factors such as candidate selection, ranking fusion, corpus characteristics, query type, and the retrieval configuration.

## Conclusion

Dense retrieval using text-embedding-3-large with 400/80 chunking remains the preferred retrieval configuration based on the overall evaluation results.

Hybrid retrieval using Dense + BM25 + RRF produced a slight improvement in MRR but lower Precision@3, Recall@3, and Hit Rate@3 compared with the dense retrieval baseline.

Therefore, hybrid retrieval was not selected as the preferred retrieval strategy for the current system.

The experiment was completed successfully and provides a quantitative comparison between dense semantic retrieval and hybrid semantic-plus-keyword retrieval.

This experiment reinforces the importance of evaluating retrieval optimization techniques empirically rather than assuming that additional retrieval mechanisms will improve performance.
