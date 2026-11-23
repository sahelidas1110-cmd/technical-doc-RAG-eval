
# Chunk Size Experiment — Retrieval Optimization

## 1. Objective

The objective of this experiment is to investigate how document chunk size and chunk overlap affect retrieval performance in our RAG system.

We will evaluate different chunking configurations using our golden evaluation dataset and custom retrieval metrics.

## 2. Hypothesis

Smaller chunks may improve retrieval precision by providing more focused content, but may reduce context completeness.

Larger chunks may provide more contextual information but could reduce retrieval precision by including less relevant content.

The optimal chunk configuration will depend on the characteristics of our technical documentation and evaluation queries.

## 3. Experimental Setup

- Dataset: Existing technical documentation corpus
- Evaluation dataset: Golden dataset
- Answerable questions: 85
- Unanswerable questions: 15 (excluded from retrieval metrics for this experiment)
- Embedding model: text-embedding-3-small
- Retrieval method: Dense vector similarity search
- Retrieval K: 3
- Query rewriting: Disabled
- Evaluation metrics:
  - Precision@3
  - Recall@3
  - Hit Rate@3
  - Mean Reciprocal Rank (MRR)

## 4. Chunking Configurations

| Experiment | Chunk Size (characters) | Chunk Overlap (characters) |
|---|---:|---:|
| Reference | 800 | 120 |
| C1 | 400 | 80 |
| C2 | 600 | 100 |
| C3 | 1000 | 150 |

The reference configuration represents the current chunking setup.

## 5. Controlled Variables

The following variables will remain unchanged:

- Document corpus
- Golden evaluation dataset
- Embedding model
- Retrieval method
- Retrieval K
- Evaluation metrics
- Query rewriting configuration (disabled)

Only chunk size and chunk overlap will be varied.

## 6. Evaluation Results

Results will be recorded after each experiment.

| Experiment | Chunk Size | Overlap | Precision@3 | Recall@3 | Hit Rate@3 | MRR |
|---|---:|---:|---:|---:|---:|---:|
| Reference | 800 | 120 | | | | |
| C1 | 400 | 80 | | | | |
| C2 | 600 | 100 | | | | |
| C3 | 1000 | 150 | | | | |

## 7. Analysis

After completing the experiments, we will:

- Compare retrieval metrics across configurations.
- Identify the configuration with the best overall retrieval performance.
- Analyze trade-offs between precision, recall, Hit Rate and MRR.
- Investigate notable retrieval regressions or improvements.
- Select a chunking configuration based on experimental evidence.

## 8. Conclusion

The final chunk size and overlap configuration will be selected based on the evaluation results.

The selected configuration will be documented along with the observed trade-offs and limitations.


===============================================
### C1 — Chunk Size 400 / Overlap 80

**Configuration**
- Chunk size: 400 characters
- Chunk overlap: 80 characters
- Embedding model: text-embedding-3-small
- Retrieval method: Dense similarity search
- Top-K: 3
- Query rewriting: Disabled
- Answerable questions evaluated: 85

**Ingestion**
- Documents: 30
- Chunks generated: 1,491

**Results**

| Metric | Score |
|---|---:|
| Precision@3 | 0.8431 |
| Recall@3 | 0.9765 |
| Hit Rate@3 | 0.9882 |
| MRR | 0.9471 |

**Comparison with reference (800/120)**

| Metric | Reference | C1 | Change |
|---|---:|---:|---:|
| Precision@3 | 0.8098 | 0.8431 | +0.0333 |
| Recall@3 | 0.9882 | 0.9765 | -0.0117 |
| Hit Rate@3 | 0.9882 | 0.9882 | 0.0000 |
| MRR | 0.9412 | 0.9471 | +0.0059 |

**Observation:** The 400/80 configuration improved Precision@3 and MRR compared with the reference configuration. Recall@3 declined slightly, while Hit Rate@3 remained unchanged.

**Evaluation report:** `evaluation/chunk_400_80_report.json`

================================================

### C2 — Chunk Size 600 / Overlap 100

**Configuration**
- Chunk size: 600 characters
- Chunk overlap: 100 characters
- Embedding model: text-embedding-3-small
- Retrieval method: Dense similarity search
- Top-K: 3
- Query rewriting: Disabled
- Answerable questions evaluated: 85

**Ingestion**
- Documents: 30
- Chunks generated: 952

**Results**

| Metric | Score |
|---|---:|
| Precision@3 | 0.8275 |
| Recall@3 | 0.9706 |
| Hit Rate@3 | 0.9882 |
| MRR | 0.9412 |

**Comparison with reference (800/120)**

| Metric | Reference | C2 | Change |
|---|---:|---:|---:|
| Precision@3 | 0.8098 | 0.8275 | +0.0177 |
| Recall@3 | 0.9882 | 0.9706 | -0.0176 |
| Hit Rate@3 | 0.9882 | 0.9882 | 0.0000 |
| MRR | 0.9412 | 0.9412 | 0.0000 |

**Observation:** The 600/100 configuration improved Precision@3 compared with the reference configuration. Recall@3 decreased slightly, while Hit Rate@3 and MRR remained unchanged.

**Evaluation report:** `evaluation/chunk_600_100_report.json`

==========================================

### C3 — Chunk Size 1000 / Overlap 150

**Configuration**
- Chunk size: 1000 characters
- Chunk overlap: 150 characters
- Embedding model: `text-embedding-3-small`
- Retrieval: Dense similarity search
- Top-K: 3
- Query rewriting: Disabled
- Evaluation: 85 answerable questions

**Ingestion**
- Documents processed: 30
- Chunks generated: 553
- Chunks added: 553
- Ingestion completed successfully.

**Evaluation Results**
- Precision@3: 0.8098
- Recall@3: 0.9706
- Hit Rate@3: 0.9882
- MRR: 0.9569

**Observation**

The 1000/150 configuration achieved the highest MRR among the tested configurations. However, precision and recall did not improve compared with the reference configuration. This suggests that larger chunks may help rank relevant sources earlier, but do not necessarily improve overall retrieval coverage or precision.

**Evaluation report:** `evaluation/chunk_1000_150_report.json`

===========================================================

### Consolidated Results

| Configuration | Precision@3 | Recall@3 | Hit Rate@3 | MRR |
|---|---:|---:|---:|---:|
| Reference — 800/120 | 0.8098 | 0.9882 | 0.9882 | 0.9412 |
| C1 — 400/80 | 0.8431 | 0.9765 | 0.9882 | 0.9471 |
| C2 — 600/100 | 0.8275 | 0.9706 | 0.9882 | 0.9412 |
| C3 — 1000/150 | 0.8098 | 0.9706 | 0.9882 | 0.9569 |

### Conclusion

The chunk-size experiment demonstrated that chunk size and overlap influence retrieval performance differently across metrics.

- **400/80** achieved the highest Precision@3.
- **1000/150** achieved the highest MRR.
- **800/120 (Reference)** achieved the highest Recall@3.
- Hit Rate@3 remained unchanged across all configurations.

There is no universally optimal chunk size across all evaluation metrics. The choice depends on the retrieval objectives and the trade-off between precision, recall, and ranking quality.

The 400/80 configuration demonstrated the strongest precision, while the 1000/150 configuration demonstrated the strongest ranking performance. The original 800/120 configuration retained the strongest recall.

These findings will inform subsequent retrieval optimization experiments.

### Experiment Status

Completed successfully. All four configurations were evaluated using the same corpus, answerable golden dataset, embedding model, dense retrieval approach, Top-K setting, and evaluation metrics.
