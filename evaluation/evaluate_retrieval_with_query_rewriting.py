
import json
import logging
from pathlib import Path
from statistics import mean

from src.retriever import retrieve_documents
from src.query_rewriter import rewrite_query
from evaluation.retrieval_metrics import calculate_retrieval_metrics


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "evaluation" / "golden_dataset.json"

REPORT_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "query_rewriting_comparison_report.json"
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
# AGGREGATE METRICS
# --------------------------------------------------

def aggregate_metrics(results):

    metric_names = [
        "precision_at_k",
        "recall_at_k",
        "hit_rate_at_k",
        "mrr"
    ]

    aggregate = {}

    for metric_name in metric_names:

        values = [
            result[metric_name]
            for result in results
        ]

        aggregate[metric_name] = (
            mean(values) if values else 0.0
        )

    return aggregate


# --------------------------------------------------
# EVALUATE ONE RETRIEVAL STRATEGY
# --------------------------------------------------

def evaluate_strategy(dataset, strategy):

    results = []
    failures = []

    answerable_count = 0
    skipped_count = 0

    for item in dataset:

        question_id = item["id"]
        question = item["question"]

        if not item["should_answer"]:
            skipped_count += 1
            continue

        answerable_count += 1

        expected_sources = item["expected_sources"]

        try:

            logger.info(
                "[%s] Evaluating %s",
                strategy,
                question_id
            )

            # ------------------------------------------
            # ORIGINAL QUERY
            # ------------------------------------------

            if strategy == "baseline":

                search_query = question

            # ------------------------------------------
            # REWRITTEN QUERY
            # ------------------------------------------

            elif strategy == "query_rewriting":

                search_query = rewrite_query(question)

            else:

                raise ValueError(
                    f"Unsupported strategy: {strategy}"
                )

            # ------------------------------------------
            # RETRIEVAL
            # ------------------------------------------

            retrieved_results = retrieve_documents(
                query=search_query,
                k=K
            )

            # ------------------------------------------
            # METRICS
            # ------------------------------------------

            metrics = calculate_retrieval_metrics(
                retrieved_results=retrieved_results,
                expected_sources=expected_sources,
                k=K
            )

            question_result = {
                "id": question_id,
                "question": question,
                "search_query": search_query,
                "category": item["category"],
                "expected_sources": expected_sources,
                **metrics
            }

            results.append(question_result)

        except Exception as error:

            logger.exception(
                "[%s] Evaluation failed for %s",
                strategy,
                question_id
            )

            failures.append({
                "id": question_id,
                "question": question,
                "error": str(error)
            })

    return {
        "strategy": strategy,
        "answerable_questions": answerable_count,
        "unanswerable_questions_skipped": skipped_count,
        "successfully_evaluated": len(results),
        "failed_questions": len(failures),
        "aggregate_metrics": aggregate_metrics(results),
        "question_results": results,
        "failures": failures
    }


# --------------------------------------------------
# COMPARE PER-QUESTION RESULTS
# --------------------------------------------------

def compare_question_results(baseline, optimized):

    baseline_lookup = {
        result["id"]: result
        for result in baseline["question_results"]
    }

    optimized_lookup = {
        result["id"]: result
        for result in optimized["question_results"]
    }

    common_ids = sorted(
        set(baseline_lookup) & set(optimized_lookup)
    )

    comparisons = []

    metric_names = [
        "precision_at_k",
        "recall_at_k",
        "hit_rate_at_k",
        "mrr"
    ]

    for question_id in common_ids:

        baseline_result = baseline_lookup[question_id]
        optimized_result = optimized_lookup[question_id]

        metric_deltas = {}

        for metric_name in metric_names:

            baseline_value = baseline_result[metric_name]
            optimized_value = optimized_result[metric_name]

            metric_deltas[metric_name] = round(
                optimized_value - baseline_value,
                4
            )

        comparisons.append({
            "id": question_id,
            "question": baseline_result["question"],
            "category": baseline_result["category"],
            "baseline_metrics": {
                metric_name: baseline_result[metric_name]
                for metric_name in metric_names
            },
            "optimized_metrics": {
                metric_name: optimized_result[metric_name]
                for metric_name in metric_names
            },
            "metric_deltas": metric_deltas,
            "baseline_retrieved_sources": (
                baseline_result.get("retrieved_sources", [])
            ),
            "optimized_retrieved_sources": (
                optimized_result.get("retrieved_sources", [])
            ),
            "expected_sources": baseline_result["expected_sources"],
            "baseline_search_query": (
                baseline_result["search_query"]
            ),
            "rewritten_search_query": (
                optimized_result["search_query"]
            )
        })

    # ----------------------------------------------
    # CLASSIFY HIT-RATE CHANGES
    # ----------------------------------------------

    improved = []
    regressed = []
    unchanged = []

    for comparison in comparisons:

        baseline_hit = (
            comparison["baseline_metrics"]["hit_rate_at_k"]
        )

        optimized_hit = (
            comparison["optimized_metrics"]["hit_rate_at_k"]
        )

        if optimized_hit > baseline_hit:

            improved.append(comparison["id"])

        elif optimized_hit < baseline_hit:

            regressed.append(comparison["id"])

        else:

            unchanged.append(comparison["id"])

    return {
        "common_questions_evaluated": len(comparisons),
        "hit_rate_improved_questions": improved,
        "hit_rate_regressed_questions": regressed,
        "hit_rate_unchanged_questions": unchanged,
        "per_question_comparison": comparisons
    }


# --------------------------------------------------
# MAIN EVALUATION
# --------------------------------------------------

def evaluate_query_rewriting():

    dataset = load_golden_dataset()

    logger.info("Running baseline evaluation.")

    baseline = evaluate_strategy(
        dataset=dataset,
        strategy="baseline"
    )

    logger.info("Running query rewriting evaluation.")

    optimized = evaluate_strategy(
        dataset=dataset,
        strategy="query_rewriting"
    )

    logger.info("Comparing per-question results.")

    comparison = compare_question_results(
        baseline=baseline,
        optimized=optimized
    )

    # ----------------------------------------------
    # REPORT
    # ----------------------------------------------

    report = {
        "evaluation_type": "query_rewriting_comparison",
        "k": K,
        "total_questions": len(dataset),
        "baseline": baseline,
        "query_rewriting": optimized,
        "comparison": comparison
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    # ----------------------------------------------
    # DISPLAY
    # ----------------------------------------------

    print("\n" + "=" * 65)
    print("QUERY REWRITING COMPARATIVE EVALUATION")
    print("=" * 65)

    print(f"Total dataset questions: {len(dataset)}")
    print(
        f"Common questions evaluated: "
        f"{comparison['common_questions_evaluated']}"
    )

    print("\nBASELINE METRICS")
    print("-" * 45)

    for metric_name, value in (
        baseline["aggregate_metrics"].items()
    ):

        print(f"{metric_name}: {value:.4f}")

    print("\nQUERY REWRITING METRICS")
    print("-" * 45)

    for metric_name, value in (
        optimized["aggregate_metrics"].items()
    ):

        print(f"{metric_name}: {value:.4f}")

    print("\nHIT RATE COMPARISON")
    print("-" * 45)

    print(
        "Improved questions:",
        len(comparison["hit_rate_improved_questions"])
    )

    print(
        "Regressed questions:",
        len(comparison["hit_rate_regressed_questions"])
    )

    print(
        "Unchanged questions:",
        len(comparison["hit_rate_unchanged_questions"])
    )

    print("\nImproved question IDs:")

    print(
        comparison["hit_rate_improved_questions"]
    )

    print("\nRegressed question IDs:")

    print(
        comparison["hit_rate_regressed_questions"]
    )

    print("\nEvaluation failures")

    print(
        "Baseline:",
        baseline["failed_questions"]
    )

    print(
        "Query rewriting:",
        optimized["failed_questions"]
    )

    print("\nReport saved to:")

    print(REPORT_PATH)

    print("=" * 65)

    return report


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    evaluate_query_rewriting()
