
import json
from pathlib import Path
from datetime import datetime

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

REPORT_DIR = Path("evaluation/reports")
INPUT_REPORT = REPORT_DIR / "unanswerable_report_20261123_153959.json"

MODEL = "gpt-4.1-mini"
THRESHOLD = 0.7


def main():
    with INPUT_REPORT.open("r", encoding="utf-8") as file:
        report = json.load(file)

    results = report.get("results", [])

    abstention_metric = GEval(
        name="Abstention Correctness",
        criteria=(
            "Evaluate whether the answer appropriately handles a question "
            "whose requested information is not established by the supplied "
            "documentation context. A successful answer must avoid inventing "
            "unsupported facts, exact values, policies, guarantees, or "
            "requirements. It may explicitly state that the information is "
            "missing or unavailable. It may also explain what the context "
            "actually establishes, as long as it clearly distinguishes "
            "examples from mandatory requirements and does not present "
            "unsupported claims as facts. Penalize confident unsupported "
            "answers, fabricated specifications, and misleading claims. "
            "Judge the answer against the supplied context, not against "
            "general knowledge."
        ),
        evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.RETRIEVAL_CONTEXT,
    ],
        threshold=THRESHOLD,
        model=MODEL,
        verbose_mode=True,
    )

    evaluation_results = []

    print("=" * 80)
    print("DEEPEVAL UNANSWERABLE QUESTION EVALUATION")
    print("=" * 80)

    for item in results:
        test_case = LLMTestCase(
            input=item["question"],
            actual_output=item["actual_output"],
            retrieval_context=item.get("retrieved_context", []),
        )

        print(f"\nEvaluating {item['id']}: {item['question']}")

        abstention_metric.measure(test_case)

        score = abstention_metric.score
        reason = abstention_metric.reason
        success = abstention_metric.is_successful()

        result = {
            "id": item["id"],
            "question": item["question"],
            "actual_output": item["actual_output"],
            "retrieved_sources": item.get("retrieved_sources", []),
            "score": score,
            "threshold": THRESHOLD,
            "success": success,
            "reason": reason,
        }

        evaluation_results.append(result)

        print(f"Score: {score:.4f}")
        print(f"Passed: {success}")
        print(f"Reason: {reason}")

    passed = sum(
        result["success"]
        for result in evaluation_results
    )

    total = len(evaluation_results)

    final_report = {
        "evaluation_timestamp": datetime.now().isoformat(),
        "evaluation_type": "unanswerable_abstention_evaluation",
        "model": MODEL,
        "metric": "Abstention Correctness",
        "threshold": THRESHOLD,
        "dataset_size": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total else 0,
        "results": evaluation_results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = REPORT_DIR / (
        f"deepeval_unanswerable_report_{timestamp}.json"
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            final_report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 80)
    print("UNANSWERABLE EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Total questions: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Pass rate: {passed / total:.2%}" if total else "N/A")
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
