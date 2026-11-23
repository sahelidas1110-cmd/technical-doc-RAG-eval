
import json
from pathlib import Path
from datetime import datetime

from src.rag_pipeline import generate_answer


DATASET_PATH = Path("evaluation/unanswerable_dataset.json")
REPORT_DIR = Path("evaluation/reports")


def extract_document(item):
    """Extract a Document from either a Document or a tuple."""

    if hasattr(item, "metadata") and hasattr(item, "page_content"):
        return item

    if isinstance(item, tuple):
        for element in item:
            if hasattr(element, "metadata") and hasattr(element, "page_content"):
                return element

    return None


def main():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    print("=" * 80)
    print("UNANSWERABLE QUESTION EVALUATION")
    print("=" * 80)

    for item in dataset:
        question = item["question"]

        print(f"\nEvaluating {item['id']}: {question}")

        rag_result = generate_answer(question)

        retrieved_documents = rag_result.get(
            "retrieved_documents",
            [],
        )

        valid_documents = [
            extract_document(doc)
            for doc in retrieved_documents
        ]

        valid_documents = [
            doc for doc in valid_documents
            if doc is not None
        ]

        answer = rag_result.get("answer", "")

        result = {
            "id": item["id"],
            "question": question,
            "expected_answer": item.get("expected_answer", ""),
            "actual_output": answer,
            "retrieved_sources": [
                doc.metadata.get("source", "unknown")
                for doc in valid_documents
            ],
            "retrieved_context": [
                doc.page_content
                for doc in valid_documents
            ],
        }

        results.append(result)

        print(f"Answer: {answer}")
        print(f"Retrieved documents: {len(valid_documents)}")

    report = {
        "evaluation_timestamp": datetime.now().isoformat(),
        "dataset_size": len(dataset),
        "evaluation_type": "unanswerable_questions",
        "results": results,
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = REPORT_DIR / (
        f"unanswerable_report_{timestamp}.json"
    )

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("UNANSWERABLE EVALUATION COMPLETED")
    print("=" * 80)

    print(f"Total questions evaluated: {len(results)}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
