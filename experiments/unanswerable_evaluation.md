# Unanswerable Question Evaluation

## Objective

Evaluate whether the RAG system appropriately abstains when the knowledge base does not contain sufficient information to answer a question.

The evaluation focuses on preventing unsupported facts, fabricated numerical values, policies, deployment guarantees, and configuration requirements.

## Dataset

- Total questions: 15
- Dataset source: `evaluation/unanswerable_dataset.json`
- Questions were selected from the golden dataset with `should_answer = false`.

## Evaluation Methodology

The evaluation was performed in two stages.

### Stage 1: Initial diagnostic

The RAG pipeline was executed against all 15 unanswerable questions.

The generated responses, retrieved documents, retrieved sources, and retrieved context were saved for analysis.

A heuristic diagnostic script was used to identify likely abstentions and flag potentially specific numerical claims.

### Stage 2: LLM-as-a-judge evaluation

DeepEval GEval was used to assess the correctness of abstention behavior.

**Metric:** Abstention Correctness

**Evaluation model:** `gpt-4.1-mini`

**Threshold:** 0.7

The judge evaluated whether responses:

- Avoided unsupported facts and exact values.
- Acknowledged missing or unavailable information.
- Distinguished illustrative examples from mandatory requirements.
- Avoided fabricated specifications, guarantees, and policies.
- Adhered to the retrieved context.

## Results

| Metric | Result |
|---|---:|
| Questions evaluated | 15 |
| Passed | 15 |
| Failed | 0 |
| Pass rate | 100% |
| GEval threshold | 0.7 |

## Analysis

All 15 unanswerable test cases passed the GEval evaluation.

Most responses explicitly stated that sufficient information could not be found in the documentation.

Q074 was a notable case. The system explained that the documentation provided an example of four Uvicorn workers but did not mandate a fixed worker count for every production application regardless of CPU and memory resources.

The evaluator considered this response appropriate because it distinguished an example from a mandatory requirement.

## Report Artifacts

- `evaluation/unanswerable_dataset.json`
- `evaluation/reports/unanswerable_report_20261123_153959.json`
- `evaluation/reports/unanswerable_analysis_20261123_153959.json`
- `evaluation/reports/deepeval_unanswerable_report_20261123_160926.json`

## Conclusion

The RAG system achieved a 100% pass rate on the 15-question unanswerable evaluation set using the Abstention Correctness GEval metric.

This result provides evidence that the system appropriately handles the selected out-of-knowledge-base questions and avoids unsupported claims when evaluated against the retrieved context.

This result is specific to the evaluated dataset, evaluator, and threshold and should not be interpreted as a guarantee that the system will never hallucinate.