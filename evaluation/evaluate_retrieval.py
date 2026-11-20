
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
    PROJECT_ROOT / "evaluation" / "retrieval_report.json"
)

K = 3


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# LOAD GOLDEN DATASET
# --------------------------------------------------

def load_golden_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, list) or not dataset:
        raise ValueError("Golden dataset must be a non-empty list.")

    logger.info(
        "Loaded %d questions from golden dataset.",
        len(dataset)
    )

    return dataset


# --------------------------------------------------
# EVALUATE RETRIEVAL
# --------------------------------------------------

def evaluate_retrieval():

    dataset = load_golden_dataset()

    results = []
    failures = []

    answerable_count = 0
    skipped_count = 0

    for item in dataset:

        question_id = item["id"]
        question = item["question"]

        # Unanswerable questions are evaluated separately.
        if not item["should_answer"]:
            skipped_count += 1
            continue

        answerable_count += 1

        expected_sources = item["expected_sources"]

        try:

            logger.info(
                "Evaluating question %s: %s",
                question_id,
                question
            )

            # Retrieve the top-k document chunks.
            retrieved_results = retrieve_documents(
                query=question,
                k=K
            )

            # Calculate source-level retrieval metrics.
            metrics = calculate_retrieval_metrics(
                retrieved_results=retrieved_results,
                expected_sources=expected_sources,
                k=K
            )

            question_result = {
                "id": question_id,
                "question": question,
                "category": item["category"],
                "expected_sources": expected_sources,
                **metrics
            }

            results.append(question_result)

        except Exception as error:

            logger.exception(
                "Evaluation failed for question %s.",
                question_id
            )

            failures.append({
                "id": question_id,
                "question": question,
                "error": str(error)
            })

    # --------------------------------------------------
    # AGGREGATE METRICS
    # --------------------------------------------------

    metric_names = [
        "precision_at_k",
        "recall_at_k",
        "hit_rate_at_k",
        "mrr"
    ]

    aggregate_metrics = {}

    for metric_name in metric_names:

        values = [
            result[metric_name]
            for result in results
        ]

        aggregate_metrics[metric_name] = (
            mean(values) if values else 0.0
        )

    # --------------------------------------------------
    # GENERATE REPORT
    # --------------------------------------------------

    report = {
        "evaluation_type": "retrieval_evaluation",
        "k": K,
        "total_questions": len(dataset),
        "answerable_questions": answerable_count,
        "unanswerable_questions_skipped": skipped_count,
        "successfully_evaluated": len(results),
        "failed_questions": len(failures),
        "aggregate_metrics": aggregate_metrics,
        "question_results": results,
        "failures": failures
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    print("\n" + "=" * 55)
    print("RETRIEVAL EVALUATION REPORT")
    print("=" * 55)

    print(f"Total questions: {len(dataset)}")
    print(f"Answerable questions: {answerable_count}")
    print(f"Unanswerable questions skipped: {skipped_count}")
    print(f"Successfully evaluated: {len(results)}")
    print(f"Failed questions: {len(failures)}")

    print("\nAggregate Retrieval Metrics")
    print("-" * 40)

    for metric_name, value in aggregate_metrics.items():

        print(f"{metric_name}: {value:.4f}")

    print("\nReport saved to:")
    print(REPORT_PATH)

    print("=" * 55)

    return report


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    evaluate_retrieval()