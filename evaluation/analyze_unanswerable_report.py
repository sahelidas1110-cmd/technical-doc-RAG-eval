
import json
import re
from pathlib import Path

REPORT_DIR = Path("evaluation/reports")


ABSTENTION_PHRASES = [
    "could not find sufficient information",
    "does not specify",
    "not specified",
    "not stated",
    "does not provide",
    "no information",
    "cannot determine",
    "not available in the documentation",
    "not mentioned in the documentation",
    "does not establish",
    "there is no stated",
    "no stated",
    "not documented",
    "unable to determine",
]


def is_abstention(answer):
    """Check whether the answer appears to abstain from unsupported information."""
    answer_lower = answer.lower()

    return any(
        phrase in answer_lower
        for phrase in ABSTENTION_PHRASES
    )


def detect_specific_claims(answer):
    """Flag answers containing potentially unsupported numeric claims."""

    patterns = [
        r"\b\d+\s*(minutes?|mins?|hours?|days?|seconds?|secs?)\b",
        r"\b\d+\s*(workers?|connections?|requests?)\b",
        r"\b\d+(\.\d+)?\s*%\b",
        r"\$\s*\d+",
    ]

    return any(
        re.search(pattern, answer.lower())
        for pattern in patterns
    )


def analyze_result(result):
    answer = result.get("actual_output", "")
    contexts = result.get("retrieved_context", [])
    sources = result.get("retrieved_sources", [])

    abstained = is_abstention(answer)
    numeric_claim_flag = detect_specific_claims(answer)

    if abstained and numeric_claim_flag:
        classification = "Abstention with potentially specific claims"
    elif abstained:
        classification = "Likely abstention"
    elif numeric_claim_flag:
        classification = "Potential unsupported specific claim"
    else:
        classification = "Needs manual review"

    return {
        "id": result.get("id"),
        "question": result.get("question"),
        "classification": classification,
        "likely_abstention": abstained,
        "numeric_claim_flag": numeric_claim_flag,
        "retrieved_document_count": len(contexts),
        "retrieved_sources": sources,
        "actual_output": answer,
    }


def main():
    report_files = sorted(
        REPORT_DIR.glob("unanswerable_report_*.json")
    )

    if not report_files:
        print("No unanswerable evaluation reports found.")
        return

    latest_report = report_files[-1]

    with latest_report.open("r", encoding="utf-8") as file:
        report = json.load(file)

    results = report.get("results", [])

    analyses = [
        analyze_result(result)
        for result in results
    ]

    likely_abstentions = sum(
        item["likely_abstention"]
        for item in analyses
    )

    potential_claims = sum(
        item["numeric_claim_flag"]
        for item in analyses
    )

    total_questions = len(analyses)

    summary = {
        "source_report": str(latest_report),
        "total_questions": total_questions,
        "likely_abstentions": likely_abstentions,
        "likely_abstention_rate": (
            likely_abstentions / total_questions
            if total_questions else 0
        ),
        "potential_numeric_claims": potential_claims,
        "results": analyses,
    }

    timestamp = latest_report.stem.replace(
        "unanswerable_report_", ""
    )

    output_path = REPORT_DIR / (
        f"unanswerable_analysis_{timestamp}.json"
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 80)
    print("UNANSWERABLE QUESTION ANALYSIS")
    print("=" * 80)

    print(f"Source report: {latest_report}")
    print(f"Total questions: {total_questions}")
    print(f"Likely abstentions: {likely_abstentions}")
    print(
        f"Likely abstention rate: "
        f"{likely_abstentions / total_questions:.2%}"
        if total_questions else "N/A"
    )
    print(f"Potential numeric claims: {potential_claims}")

    print("\nQUESTION-LEVEL ANALYSIS")
    print("-" * 80)

    for item in analyses:
        print(f"\n{item['id']}: {item['question']}")
        print(f"Classification: {item['classification']}")
        print(
            f"Likely abstention: "
            f"{item['likely_abstention']}"
        )
        print(
            f"Numeric claim flag: "
            f"{item['numeric_claim_flag']}"
        )
        print(
            f"Retrieved documents: "
            f"{item['retrieved_document_count']}"
        )

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETED")
    print("=" * 80)
    print(f"Analysis report saved to: {output_path}")


if __name__ == "__main__":
    main()
