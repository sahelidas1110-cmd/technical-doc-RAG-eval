
import json
from pathlib import Path
from collections import defaultdict
from statistics import mean


PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORT_PATH = PROJECT_ROOT / "evaluation" / "retrieval_report.json"


def analyze_report():

    with open(REPORT_PATH, "r", encoding="utf-8") as file:
        report = json.load(file)

    results = report["question_results"]

    categories = defaultdict(list)

    for result in results:
        categories[result["category"]].append(result)

    metric_names = [
        "precision_at_k",
        "recall_at_k",
        "hit_rate_at_k",
        "mrr"
    ]

    # -----------------------------------------
    # CATEGORY-WISE PERFORMANCE
    # -----------------------------------------

    print("\nCATEGORY-WISE RETRIEVAL PERFORMANCE")
    print("=" * 75)

    for category, questions in sorted(categories.items()):

        print(f"\nCategory: {category}")
        print(f"Questions evaluated: {len(questions)}")

        for metric in metric_names:

            values = [
                question[metric]
                for question in questions
            ]

            print(
                f"{metric}: {mean(values):.4f}"
            )

    # -----------------------------------------
    # QUESTIONS WITH NO RELEVANT RETRIEVAL
    # -----------------------------------------

    missed_questions = [
        result
        for result in results
        if result["hit_rate_at_k"] == 0
    ]

    print("\n\nQUESTIONS WITH NO RELEVANT SOURCE")
    print("=" * 75)

    if not missed_questions:
        print("No missed questions!")

    for question in missed_questions:

        print(f"\nID: {question['id']}")
        print(f"Question: {question['question']}")
        print(f"Expected: {question['expected_sources']}")
        print(f"Retrieved: {question['retrieved_sources']}")

    # -----------------------------------------
    # QUESTIONS WITH INCOMPLETE SOURCE RECALL
    # -----------------------------------------

    incomplete_questions = [
        result
        for result in results
        if result["recall_at_k"] < 1.0
    ]

    print("\n\nQUESTIONS WITH INCOMPLETE RECALL")
    print("=" * 75)

    for question in incomplete_questions:

        print(f"\nID: {question['id']}")
        print(f"Question: {question['question']}")
        print(f"Recall@3: {question['recall_at_k']:.4f}")
        print(f"Expected: {question['expected_sources']}")
        print(f"Retrieved: {question['retrieved_sources']}")


if __name__ == "__main__":
    analyze_report()