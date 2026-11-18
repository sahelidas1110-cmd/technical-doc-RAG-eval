
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = PROJECT_ROOT / "evaluation" / "golden_dataset.json"

VALID_CATEGORIES = {
    "factual",
    "conceptual",
    "comparison",
    "multi_hop",
    "complex",
    "unanswerable"
}

REQUIRED_FIELDS = {
    "id",
    "question",
    "expected_answer",
    "reference_context",
    "expected_sources",
    "category",
    "should_answer"
}


def load_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_dataset(dataset):

    errors = []

    if not isinstance(dataset, list):
        return ["Dataset must be a JSON list."]

    if not dataset:
        return ["Dataset is empty."]

    question_ids = set()

    for index, item in enumerate(dataset):

        location = f"Question at index {index}"

        if not isinstance(item, dict):
            errors.append(f"{location} must be a JSON object.")
            continue

        # Check required fields
        missing_fields = REQUIRED_FIELDS - item.keys()

        if missing_fields:
            errors.append(
                f"{location} is missing fields: {missing_fields}"
            )
            continue

        # Check unique IDs
        question_id = item["id"]

        if not isinstance(question_id, str) or not question_id.strip():
            errors.append(f"{location} has an invalid ID.")
        elif question_id in question_ids:
            errors.append(f"Duplicate question ID: {question_id}")
        else:
            question_ids.add(question_id)

        # Check question and expected answer
        if not isinstance(item["question"], str) or not item["question"].strip():
            errors.append(f"{location} has an empty or invalid question.")

        if not isinstance(item["expected_answer"], str) or not item["expected_answer"].strip():
            errors.append(f"{location} has an empty or invalid expected answer.")

        # Check reference context
        if not isinstance(item["reference_context"], str):
            errors.append(f"{location} has an invalid reference_context.")

        # Check expected sources
        if not isinstance(item["expected_sources"], list):
            errors.append(f"{location} expected_sources must be a list.")
        elif not all(
            isinstance(source, str) and source.strip()
            for source in item["expected_sources"]
        ):
            errors.append(f"{location} contains an invalid source path.")

        # Check category
        if item["category"] not in VALID_CATEGORIES:
            errors.append(
                f"{location} has an invalid category: {item['category']}"
            )

        # Check should_answer
        if not isinstance(item["should_answer"], bool):
            errors.append(f"{location} should_answer must be True or False.")

        # Check answerable and unanswerable records
        if item["should_answer"] is True:
            if not item["expected_sources"]:
                errors.append(
                    f"{location} is answerable but has no expected sources."
                )

        elif item["should_answer"] is False:
            if item["expected_sources"]:
                errors.append(
                    f"{location} is unanswerable but has expected sources."
                )

    return errors


if __name__ == "__main__":

    try:
        dataset = load_dataset()

        print("Dataset loaded successfully!")
        print("Total questions:", len(dataset))

        errors = validate_dataset(dataset)

        if errors:
            print("\nDataset validation failed!")

            for error in errors:
                print("-", error)

        else:
            print("\nDataset validation passed!")

        if isinstance(dataset, list):
            print("\nQuestion categories:")

            categories = {}

            for item in dataset:
                if isinstance(item, dict) and isinstance(item.get("category"), str):
                    category = item["category"]
                    categories[category] = categories.get(category, 0) + 1

            for category, count in categories.items():
                print(f"{category}: {count}")

    except (FileNotFoundError, json.JSONDecodeError) as error:
        print("Could not load dataset:", error)