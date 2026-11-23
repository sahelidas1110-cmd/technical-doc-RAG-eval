import json
import argparse
from pathlib import Path
from datetime import datetime

from deepeval import evaluate
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    GEval,
)
from deepeval.test_case import LLMTestCase, SingleTurnParams


DATASET_PATH = Path("evaluation/deepeval_dataset.json")
REPORT_DIR = Path("evaluation/reports")

MODEL = "gpt-4.1-mini"
METRIC_THRESHOLD = 0.7


def load_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def create_test_cases(dataset):
    test_cases = []

    for record in dataset:
        test_case = LLMTestCase(
            input=record["input"],
            actual_output=record["actual_output"],
            expected_output=record["expected_output"],
            retrieval_context=record["retrieval_context"],
        )

        test_cases.append(test_case)

    return test_cases


def create_metrics():

    contextual_precision = ContextualPrecisionMetric(
        threshold=METRIC_THRESHOLD,
        model=MODEL,
        include_reason=True,
    )

    contextual_recall = ContextualRecallMetric(
        threshold=METRIC_THRESHOLD,
        model=MODEL,
        include_reason=True,
    )

    faithfulness = FaithfulnessMetric(
        threshold=METRIC_THRESHOLD,
        model=MODEL,
        include_reason=True,
    )

    answer_relevancy = AnswerRelevancyMetric(
        threshold=METRIC_THRESHOLD,
        model=MODEL,
        include_reason=True,
    )

    answer_correctness = GEval(
        name="Answer Correctness",
        criteria=(
            "Evaluate whether the actual answer correctly and sufficiently "
            "answers the question compared with the expected answer. "
            "Consider factual accuracy, coverage of important information, "
            "and whether the answer directly addresses the question. "
            "An abstention when the expected answer contains information "
            "should be considered incorrect."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        threshold=METRIC_THRESHOLD,
        model=MODEL,
    )

    return [
        contextual_precision,
        contextual_recall,
        faithfulness,
        answer_relevancy,
        answer_correctness,
    ]


def save_report(evaluation_result, dataset, limit):

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = REPORT_DIR / f"deepeval_report_{limit}_{timestamp}.json"

    test_results = getattr(evaluation_result, "test_results", [])

    report = {
        "evaluation_timestamp": datetime.now().isoformat(),
        "dataset_size": len(dataset),
        "evaluation_limit": limit,
        "model": MODEL,
        "metric_threshold": METRIC_THRESHOLD,
        "results": [],
    }

    dataset_lookup = {
        record["input"]: record
        for record in dataset
    }

    for test_result in test_results:

        result_input = getattr(test_result, "input", None)

        matched_record = dataset_lookup.get(result_input)

        if matched_record is None:
            print(f"Warning: Could not match test result: {result_input}")
            continue

        result_record = {
            "id": matched_record.get("id"),
            "input": result_input,
            "actual_output": getattr(
                test_result,
                "actual_output",
                matched_record["actual_output"],
            ),
            "expected_output": getattr(
                test_result,
                "expected_output",
                matched_record["expected_output"],
            ),
            "metrics": [],
        }

        metrics_data = getattr(test_result, "metrics_data", [])

        for metric_data in metrics_data:

            result_record["metrics"].append(
                {
                    "metric": getattr(metric_data, "name", None),
                    "score": getattr(metric_data, "score", None),
                    "threshold": getattr(metric_data, "threshold", None),
                    "success": getattr(metric_data, "success", None),
                    "reason": getattr(metric_data, "reason", None),
                }
            )

        report["results"].append(result_record)

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print(f"\nEvaluation report saved to: {report_path}")


def main():

    parser = argparse.ArgumentParser(
        description="Run DeepEval evaluation on the RAG application."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Number of dataset records to evaluate. Use 85 for all answerable cases.",
    )

    args = parser.parse_args()

    dataset = load_dataset()

    if args.limit <= 0:
        raise ValueError("--limit must be greater than zero.")

    dataset = dataset[:args.limit]

    print(f"Evaluating {len(dataset)} test cases...")
    print(f"Evaluation model: {MODEL}")
    print(f"Threshold: {METRIC_THRESHOLD}")

    test_cases = create_test_cases(dataset)
    metrics = create_metrics()

    evaluation_result = evaluate(
        test_cases=test_cases,
        metrics=metrics,
    )

    save_report(
        evaluation_result=evaluation_result,
        dataset=dataset,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()