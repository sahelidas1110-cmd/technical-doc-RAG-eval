# Retrieval Distance Threshold Experiment

## Objective

Evaluate the impact of the retrieval distance threshold on source-level retrieval performance in the RAG system.

The experiment investigates whether adjusting the distance threshold can improve retrieval quality by allowing relevant document chunks that were previously filtered out.

## Experimental Setup

| Parameter | Configuration |
|---|---|
| Dataset | Golden evaluation dataset |
| Answerable questions | 85 |
| Retrieval method | Dense retrieval |
| Embedding model | text-embedding-3-large |
| Chunk size | 400 |
| Chunk overlap | 80 |
| Top-K | 3 |
| Thresholds evaluated | 1.00, 1.05, 1.10, 1.20 |

All configurations used the same retrieved top-3 results for each question. Threshold filtering was applied to these results before calculating the retrieval metrics.

## Results

| Threshold | Precision@3 | Recall@3 | Hit Rate@3 | MRR | Average Accepted Chunks |
|---|---:|---:|---:|---:|---:|
| 1.00 | 0.8000 | 0.9529 | 0.9529 | 0.9118 | 2.66 |
| 1.05 | 0.8294 | 0.9882 | 0.9882 | 0.9412 | 2.81 |
| 1.10 | 0.8235 | 0.9882 | 0.9882 | 0.9412 | 2.87 |
| 1.20 | 0.8157 | 0.9882 | 0.9882 | 0.9412 | 2.98 |

## Analysis

Threshold 1.00 demonstrated lower recall, hit rate and MRR, indicating that some relevant sources were not retained after distance filtering.

Increasing the threshold to 1.05 improved precision from 0.8000 to 0.8294, recall from 0.9529 to 0.9882, hit rate from 0.9529 to 0.9882, and MRR from 0.9118 to 0.9412.

Further increases to 1.10 and 1.20 did not improve recall, hit rate or MRR. Precision declined slightly, while the average number of accepted chunks increased.

## Decision

Threshold 1.05 was selected as the preferred configuration.

It provided the highest precision among the tested configurations while maintaining strong recall, hit rate and MRR without unnecessarily accepting additional chunks.

## Limitations

- The experiment evaluates source-level retrieval metrics rather than answer quality directly.
- Distance scores are dependent on the embedding model and retrieval configuration.
- The evaluation dataset represents a finite collection of questions.
- The selected threshold should also be assessed using end-to-end answer quality metrics, including faithfulness, answer relevance, context precision, context recall and answer correctness.

## Reproducibility

Experiment script:

`evaluation/evaluate_thresholds.py`

Generated report:

`evaluation/threshold_experiment_report.json`

Selected threshold: `1.05`
