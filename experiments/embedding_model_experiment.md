# Embedding Model Comparison Experiment

## Objective

Evaluate whether changing the embedding model improves dense retrieval performance in the RAG evaluation harness.

## Hypothesis

A larger embedding model may improve semantic retrieval quality by better representing relationships between queries and technical documentation. However, improvements in retrieval metrics are not guaranteed.

## Experimental Setup

- Corpus: 30 Markdown documents
- Golden dataset: 100 questions
- Answerable questions: 85
- Unanswerable questions: 15 (excluded from retrieval evaluation)
- Chunk size: 400 characters
- Chunk overlap: 80 characters
- Retrieval: Dense similarity search
- Top-K: 3
- Query rewriting: Disabled

## Embedding Models

### Baseline
- Model: text-embedding-3-small

### Candidate
- Model: text-embedding-3-large

## Evaluation Metrics

- Precision@3
- Recall@3
- Hit Rate@3
- MRR

## Controlled Variables

The following will remain unchanged:

- Corpus
- Golden dataset
- Chunk size
- Chunk overlap
- Retrieval method
- Top-K
- Query rewriting setting
- Evaluation metrics

Only the embedding model will change.

## Results

| Configuration | Precision@3 | Recall@3 | Hit Rate@3 | MRR |
|---|---:|---:|---:|---:|
| text-embedding-3-small | | | | |
| text-embedding-3-large | | | | |

## Analysis

(To be completed after both evaluations.)

## Conclusion

(To be completed after both evaluations.)

========================================

### Baseline — text-embedding-3-small (400/80)

**Configuration**
- Embedding model: `text-embedding-3-small`
- Chunk size: 400 characters
- Chunk overlap: 80 characters
- Retrieval: Dense similarity search
- Top-K: 3
- Query rewriting: Disabled
- Answerable questions: 85

**Ingestion and Evaluation**
- Evaluation completed successfully.
- Successfully evaluated: 85
- Failed questions: 0

**Results**
- Precision@3: 0.8431
- Recall@3: 0.9765
- Hit Rate@3: 0.9882
- MRR: 0.9471

**Evaluation report:** `evaluation/embed_small_400_80_report.json`

This configuration serves as the baseline for comparing the candidate embedding model.

=========================================================

### Candidate — text-embedding-3-large (400/80)

**Configuration**
- Embedding model: `text-embedding-3-large`
- Chunk size: 400 characters
- Chunk overlap: 80 characters
- Retrieval: Dense similarity search
- Top-K: 3
- Query rewriting: Disabled
- Answerable questions: 85

**Ingestion and Evaluation**
- Evaluation completed successfully.
- Successfully evaluated: 85
- Failed questions: 0

**Results**
- Precision@3: 0.8725
- Recall@3: 0.9941
- Hit Rate@3: 1.0000
- MRR: 0.9765

**Evaluation report:** `evaluation/embed_large_400_80_report.json`

The candidate embedding model improved all four retrieval metrics compared with the baseline.

### Consolidated Results

| Configuration | Precision@3 | Recall@3 | Hit Rate@3 | MRR |
|---|---:|---:|---:|---:|
| text-embedding-3-small (400/80) | 0.8431 | 0.9765 | 0.9882 | 0.9471 |
| text-embedding-3-large (400/80) | 0.8725 | 0.9941 | 1.0000 | 0.9765 |

### Analysis

The candidate embedding model, `text-embedding-3-large`, improved all four retrieval metrics compared with `text-embedding-3-small`.

- Precision@3 increased from 0.8431 to 0.8725.
- Recall@3 increased from 0.9765 to 0.9941.
- Hit Rate@3 increased from 0.9882 to 1.0000.
- MRR increased from 0.9471 to 0.9765.

The candidate model demonstrated improved retrieval quality on the evaluated golden dataset.

However, retrieval quality is not the only consideration when selecting an embedding model. Computational cost, API cost, embedding generation latency, and overall application performance should also be considered.

### Conclusion

Based on the retrieval evaluation results, `text-embedding-3-large` is the preferred candidate for subsequent retrieval optimization experiments.

It achieved the highest scores across all four retrieval metrics in this controlled comparison.

The model will be provisionally selected for subsequent experiments, subject to consideration of cost and operational trade-offs.

### Experiment Status

Completed successfully.

Both embedding models were evaluated using the same corpus, golden dataset, chunk configuration, dense retrieval method, Top-K setting, and evaluation metrics.

Only the embedding model was changed.
