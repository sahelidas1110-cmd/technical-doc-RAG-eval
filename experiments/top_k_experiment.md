# Top-K Retrieval Tuning Experiment

## Objective

Determine the optimal number of chunks to retrieve from the vector store by evaluating different K values using the custom retrieval evaluation framework.

## Experimental Setup

- Dataset: 85 answerable questions from the golden dataset
- Corpus: 30 Markdown documents
- Embedding model: text-embedding-3-large
- Chunk size: 400
- Chunk overlap: 80
- Retrieval method: Dense similarity retrieval
- Query rewriting: Disabled
- Reranking: Disabled
- K values evaluated: 1, 3, 5, 8, 10
- Metrics: Precision@K, Recall@K, Hit Rate@K, MRR

## Results

| K | Precision@K | Recall@K | Hit Rate@K | MRR |
|---|---:|---:|---:|---:|
| 1 | 0.9529 | 0.9294 | 0.9529 | 0.9529 |
| 3 | 0.8725 | 0.9941 | 1.0000 | 0.9765 |
| 5 | 0.7739 | 0.9941 | 1.0000 | 0.9765 |
| 8 | 0.6882 | 1.0000 | 1.0000 | 0.9765 |
| 10 | 0.6302 | 1.0000 | 1.0000 | 0.9765 |

## Analysis

K=1 achieved the highest precision, but recall and hit rate were lower, indicating that retrieving only one chunk can limit retrieval coverage.

K=3 provided a strong balance between precision and retrieval coverage. Recall reached 0.9941, Hit Rate reached 1.0000, and MRR reached 0.9765.

Increasing K to 5 did not improve recall, hit rate, or MRR compared with K=3, but precision decreased.

K=8 and K=10 achieved a recall of 1.0000. However, precision decreased substantially, indicating that additional retrieved chunks introduced more irrelevant sources.

## Conclusion

K=3 was selected as the preferred retrieval configuration because it provided an effective balance between retrieval precision, recall, hit rate, and ranking quality.

K=1 was too restrictive for the dataset, while larger K values introduced additional irrelevant sources without meaningful improvements in the other retrieval metrics.

The selected K for subsequent RAG experiments is 3.

## Artifacts

- `evaluation/evaluate_top_k.py`
- `evaluation/top_k_experiment_report.json`

## Experiment Status

Completed. K=3 was retained as the selected retrieval configuration.