
import json
import logging
from pathlib import Path
from statistics import mean


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORT_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "query_rewriting_comparison_report.json"
)


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# LOAD REPORT
# --------------------------------------------------

def load_report():

    with open(REPORT_PATH, "r", encoding="utf-8") as file:
        report = json.load(file)

    logger.info("Comparison report loaded successfully.")

    return report


# --------------------------------------------------
# METRIC CONFIGURATION
# --------------------------------------------------

METRIC_NAMES = [
    "precision_at_k",
    "recall_at_k",
    "hit_rate_at_k",
    "mrr"
]


# --------------------------------------------------
# ANALYZE METRIC CHANGES
# --------------------------------------------------

def analyze_metric_changes(comparisons):

    print("\n" + "=" * 70)
    print("QUESTION-LEVEL METRIC CHANGES")
    print("=" * 70)

    for metric_name in METRIC_NAMES:

        improved = []
        regressed = []
        unchanged = []

        for item in comparisons:

            delta = item["metric_deltas"][metric_name]

            if delta > 0:

                improved.append(item["id"])

            elif delta < 0:

                regressed.append(item["id"])

            else:

                unchanged.append(item["id"])

        print(f"\nMetric: {metric_name}")

        print(f"Improved: {len(improved)}")
        print(f"Regressed: {len(regressed)}")
        print(f"Unchanged: {len(unchanged)}")

        if improved:

            print("Improved question IDs:", improved)

        if regressed:

            print("Regressed question IDs:", regressed)


# --------------------------------------------------
# ANALYZE RECALL REGRESSIONS
# --------------------------------------------------

def analyze_recall_regressions(comparisons):

    recall_regressions = [
        item
        for item in comparisons
        if item["metric_deltas"]["recall_at_k"] < 0
    ]

    print("\n" + "=" * 70)
    print("RECALL REGRESSIONS")
    print("=" * 70)

    print(
        f"Questions with recall regression: "
        f"{len(recall_regressions)}"
    )

    for item in recall_regressions:

        print("\n" + "-" * 70)

        print(f"Question ID: {item['id']}")
        print(f"Category: {item['category']}")

        print(f"\nQuestion:")
        print(item["question"])

        print("\nExpected sources:")
        print(item["expected_sources"])

        print("\nBaseline retrieved sources:")
        print(item["baseline_retrieved_sources"])

        print("\nRewritten retrieved sources:")
        print(item["optimized_retrieved_sources"])

        print("\nRecall change:")
        print(
            item["metric_deltas"]["recall_at_k"]
        )

        print("\nOriginal query:")
        print(item["baseline_search_query"])

        print("\nRewritten query:")
        print(item["rewritten_search_query"])


# --------------------------------------------------
# CATEGORY-LEVEL ANALYSIS
# --------------------------------------------------

def analyze_categories(comparisons):

    categories = {}

    for item in comparisons:

        category = item["category"]

        categories.setdefault(category, []).append(item)

    print("\n" + "=" * 70)
    print("CATEGORY-LEVEL METRIC COMPARISON")
    print("=" * 70)

    for category, items in sorted(categories.items()):

        print("\n" + "-" * 70)
        print(f"Category: {category}")
        print(f"Questions: {len(items)}")

        for metric_name in METRIC_NAMES:

            baseline_values = [
                item["baseline_metrics"][metric_name]
                for item in items
            ]

            optimized_values = [
                item["optimized_metrics"][metric_name]
                for item in items
            ]

            baseline_average = mean(baseline_values)
            optimized_average = mean(optimized_values)

            delta = optimized_average - baseline_average

            print(
                f"{metric_name}: "
                f"Baseline={baseline_average:.4f}, "
                f"Rewritten={optimized_average:.4f}, "
                f"Change={delta:+.4f}"
            )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def analyze_report():

    report = load_report()

    comparisons = (
        report["comparison"]["per_question_comparison"]
    )

    analyze_metric_changes(comparisons)

    analyze_recall_regressions(comparisons)

    analyze_categories(comparisons)


# --------------------------------------------------
# EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    analyze_report()
