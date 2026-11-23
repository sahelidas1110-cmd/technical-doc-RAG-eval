
import json
import logging
from pathlib import Path
from statistics import mean

from src.retriever import retrieve_documents
from evaluation.retrieval_metrics import calculate_retrieval_metrics


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "evaluation" / "golden_dataset.json"

REPORT_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "threshold_experiment_report.json"
)

K = 3

THRESHOLDS = [1.0, 1.05, 1.10, 1.20]


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

def load_golden_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, list) or not dataset:
        raise ValueError(
            "Golden dataset must be a non-empty list."
        )

    return dataset


# --------------------------------------------------
# EVALUATE THRESHOLDS
# --------------------------------------------------

def evaluate_thresholds():

    dataset = load_golden_dataset()

    answerable_questions = [
        item for item in dataset
        if item["should_answer"]
    ]

    logger.info(
        "Loaded %d answerable questions.",
        len(answerable_questions)
    )

    results_by_threshold = {
        threshold: []
        for threshold in THRESHOLDS
    }

    failures = []

    # Retrieve once per question, then reuse results
    # for every threshold.

    for item in answerable_questions:

        question_id = item["id"]
        question = item["question"]
        expected_sources = item["expected_sources"]

        try:

            logger.info(
                "Evaluating %s: %s",
                question_id,
                question
            )

            raw_results = retrieve_documents(
                query=question,
                k=K
            )

            # Evaluate each threshold using the same
            # original top-k retrieval results.

            for threshold in THRESHOLDS:

                filtered_results = [
                    (document, score)
                    for document, score in raw_results[:K]
                    if score <= threshold
                ]

                metrics = calculate_retrieval_metrics(
                    retrieved_results=filtered_results,
                    expected_sources=expected_sources,
                    k=K
                )

                results_by_threshold[threshold].append(
                    {
                        "id": question_id,
                        "question": question,
                        "category": item["category"],
                        "threshold": threshold,
                        "accepted_chunks": len(
                            filtered_results
                        ),
                        **metrics
                    }
                )

        except Exception as error:

            logger.exception(
                "Evaluation failed for %s.",
                question_id
            )

            failures.append(
                {
                    "id": question_id,
                    "question": question,
                    "error": str(error)
                }
            )

    # --------------------------------------------------
    # AGGREGATE METRICS
    # --------------------------------------------------

    metric_names = [
        "precision_at_k",
        "recall_at_k",
        "hit_rate_at_k",
        "mrr"
    ]

    threshold_summary = {}

    for threshold, results in results_by_threshold.items():

        aggregate_metrics = {}

        for metric_name in metric_names:

            values = [
                result[metric_name]
                for result in results
            ]

            aggregate_metrics[metric_name] = (
                mean(values) if values else 0.0
            )

        accepted_chunk_counts = [
            result["accepted_chunks"]
            for result in results
        ]

        threshold_summary[str(threshold)] = {
            "evaluated_questions": len(results),
            "aggregate_metrics": aggregate_metrics,
            "average_accepted_chunks": (
                mean(accepted_chunk_counts)
                if accepted_chunk_counts
                else 0.0
            ),
            "question_results": results
        }

    # --------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------

    report = {
        "evaluation_type": "retrieval_threshold_experiment",
        "k": K,
        "thresholds": THRESHOLDS,
        "answerable_questions": len(answerable_questions),
        "failed_questions": len(failures),
        "threshold_results": threshold_summary,
        "failures": failures
    }

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    # --------------------------------------------------
    # DISPLAY SUMMARY
    # --------------------------------------------------

    print("\n" + "=" * 75)
    print("RETRIEVAL THRESHOLD EXPERIMENT")
    print("=" * 75)

    print(f"Answerable questions: {len(answerable_questions)}")
    print(f"Failed questions: {len(failures)}")

    print("\nAggregate Results")
    print("-" * 75)

    print(
        f"{'Threshold':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'Hit Rate':<12}"
        f"{'MRR':<12}"
        f"{'Avg Chunks':<12}"
    )

    for threshold, summary in threshold_summary.items():

        metrics = summary["aggregate_metrics"]

        print(
            f"{threshold:<12}"
            f"{metrics['precision_at_k']:<12.4f}"
            f"{metrics['recall_at_k']:<12.4f}"
            f"{metrics['hit_rate_at_k']:<12.4f}"
            f"{metrics['mrr']:<12.4f}"
            f"{summary['average_accepted_chunks']:<12.2f}"
        )

    print("\nReport saved to:")
    print(REPORT_PATH)

    print("=" * 75)

    return report


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    evaluate_thresholds()
