
import json
from pathlib import Path


SOURCE_PATH = Path("evaluation/golden_dataset.json")
OUTPUT_PATH = Path("evaluation/unanswerable_dataset.json")


def main():
    with SOURCE_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    unanswerable_questions = [
        item for item in dataset
        if item.get("should_answer") is False
    ]

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(unanswerable_questions, file, indent=2, ensure_ascii=False)

    print("=" * 60)
    print("UNANSWERABLE DATASET PREPARATION")
    print("=" * 60)

    print(f"Original dataset size: {len(dataset)}")
    print(f"Unanswerable questions extracted: {len(unanswerable_questions)}")
    print(f"Dataset saved to: {OUTPUT_PATH}")

    print("\nUnanswerable question IDs:")

    for item in unanswerable_questions:
        print(f"{item['id']}: {item['question']}")

    print("\nDataset preparation completed successfully.")


if __name__ == "__main__":
    main()
