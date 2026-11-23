# Cross-Encoder Reranking Experiment

## Objective

Evaluate whether Cross-Encoder reranking improves retrieval quality by reranking the top 20 candidates retrieved through dense retrieval and selecting the final top 3 documents.

## Experimental Setup

- Dataset: 85 answerable questions from the golden dataset
- Corpus: 30 Markdown documents
- Embedding model: text-embedding-3-large
- Chunk size: 400
- Chunk overlap: 80
- Candidate retrieval: Dense retrieval, top 20
- Final retrieval: Top 3 after reranking
- Reranking model: cross-encoder/ms-marco-MiniLM-L-6-v2
- Query rewriting: Disabled
- Evaluation metrics: Precision@3, Recall@3, Hit Rate@3, MRR

## Results

| Metric | Dense Baseline | Dense + Reranking |
|---|---:|---:|
| Precision@3 | 0.8431 | 0.7784 |
| Recall@3 | 0.9765 | 0.9941 |
| Hit Rate@3 | 0.9882 | 1.0000 |
| MRR | 0.9471 | 0.9471 |

## Analysis

Cross-Encoder reranking improved Recall@3 and Hit Rate@3. All 85 answerable questions achieved a Hit Rate@3 of 1.0000, meaning at least one expected source was retrieved within the top three results for every evaluated question.

However, Precision@3 decreased from 0.8431 to 0.7784, indicating that the final top-three results contained a lower proportion of relevant sources on average.

MRR remained unchanged at 0.9471, indicating no overall improvement in the ranking position of the first relevant source.

## Conclusion

Cross-Encoder reranking improved retrieval coverage but reduced precision and did not improve MRR.

The selected dense retrieval baseline remains the preferred retrieval strategy for this project because it offers a better overall balance across the evaluation metrics.

Reranking remains a potential optimization for applications where retrieval coverage is more important than precision.

## Artifacts

- `src/reranker.py`
- `evaluation/evaluate_reranking.py`
- `evaluation/reranking_report.json`

## Experiment Status

Completed. Reranking was evaluated but not selected as the default retrieval strategy.