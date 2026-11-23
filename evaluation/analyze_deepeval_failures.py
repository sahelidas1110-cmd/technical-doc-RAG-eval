
import json
from pathlib import Path
from collections import Counter

REPORT_PATH = Path(
    "evaluation/reports/deepeval_report_85_20261124_004459.json"
)


def main():
    with REPORT_PATH.open("r", encoding="utf-8") as file:
        report = json.load(file)

    results = report["results"]

    failed_cases = []
    metric_failure_counts = Counter()

    for case in results:
        failed_metrics = [
            metric
            for metric in case["metrics"]
            if not metric["success"]
        ]

        if failed_metrics:
            failed_cases.append(
                {
                    "id": case["id"],
                    "question": case["input"],
                    "failed_metrics": failed_metrics,
                }
            )

            for metric in failed_metrics:
                metric_failure_counts[metric["metric"]] += 1

    print("=" * 80)
    print("DEEPEVAL FAILURE ANALYSIS")
    print("=" * 80)

    print(f"\nTotal evaluated questions: {len(results)}")
    print(f"Questions with at least one failed metric: {len(failed_cases)}")
    print(f"Questions passing all metrics: {len(results) - len(failed_cases)}")

    print("\n" + "=" * 80)
    print("FAILURES BY METRIC")
    print("=" * 80)

    for metric_name, count in metric_failure_counts.most_common():
        print(f"{metric_name}: {count}")

    print("\n" + "=" * 80)
    print("FAILED QUESTIONS AND DETAILS")
    print("=" * 80)

    for case in failed_cases:
        print("\n" + "-" * 80)
        print(f"Question ID: {case['id']}")
        print(f"Question: {case['question']}")

        print("\nFailed metrics:")

        for metric in case["failed_metrics"]:
            print(f"\n  Metric: {metric['metric']}")
            print(f"  Score: {metric['score']}")
            print(f"  Threshold: {metric['threshold']}")

            print("  Reason:")
            print(f"  {metric['reason']}")

    print("\n" + "=" * 80)
    print("FAILURE ANALYSIS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()
