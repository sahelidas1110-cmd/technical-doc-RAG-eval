import json
import sys
from pathlib import Path
from collections import Counter


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "evaluation" / "golden_dataset.json"

# Allowed categories
VALID_CATEGORIES = {
    "factual",
    "conceptual",
    "comparison",
    "multi_hop",
    "complex",
    "unanswerable",
}

REQUIRED_FIELDS = {
    "id",
    "question",
    "expected_answer",
    "reference_context",
    "expected_sources",
    "category",
    "should_answer",
}


def load_dataset():
    """Load the golden evaluation dataset."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_dataset(dataset):
    """Validate dataset structure, consistency, and source files."""

    errors = []
    question_ids = set()
    category_counts = Counter()

    if not isinstance(dataset, list):
        return ["Dataset must be a JSON list."]

    if not dataset:
        return ["Dataset is empty."]

    for index, item in enumerate(dataset, start=1):

        prefix = f"Record {index}"

        # Check record type
        if not isinstance(item, dict):
            errors.append(f"{prefix}: Record must be a JSON object.")
            continue

        # Check required fields
        missing_fields = REQUIRED_FIELDS - set(item.keys())

        if missing_fields:
            errors.append(
                f"{prefix}: Missing fields: {sorted(missing_fields)}"
            )
            continue

        # Check ID
        question_id = item["id"]

        if not isinstance(question_id, str) or not question_id.strip():
            errors.append(f"{prefix}: ID must be a non-empty string.")
        elif question_id in question_ids:
            errors.append(f"{prefix}: Duplicate ID: {question_id}")
        else:
            question_ids.add(question_id)

        # Check question
        if not isinstance(item["question"], str) or not item["question"].strip():
            errors.append(f"{prefix}: Question must be non-empty.")

        # Check expected answer
        if (
            not isinstance(item["expected_answer"], str)
            or not item["expected_answer"].strip()
        ):
            errors.append(f"{prefix}: Expected answer must be non-empty.")

        # Check reference context
        if not isinstance(item["reference_context"], str):
            errors.append(f"{prefix}: Reference context must be a string.")

        # Check category
        category = item["category"]

        if category not in VALID_CATEGORIES:
            errors.append(
                f"{prefix}: Invalid category: {category}"
            )
        else:
            category_counts[category] += 1

        # Check should_answer
        should_answer = item["should_answer"]

        if not isinstance(should_answer, bool):
            errors.append(
                f"{prefix}: should_answer must be True or False."
            )

        # Check category and answerability consistency
        if (
            isinstance(should_answer, bool)
            and category in VALID_CATEGORIES
        ):
            expected_answerability = category != "unanswerable"

            if should_answer != expected_answerability:
                errors.append(
                    f"{prefix}: Category '{category}' conflicts "
                    f"with should_answer={should_answer}."
                )

        # Check expected sources
        sources = item["expected_sources"]

        if not isinstance(sources, list):
            errors.append(
                f"{prefix}: expected_sources must be a list."
            )
            continue

        if not all(
            isinstance(source, str) and source.strip()
            for source in sources
        ):
            errors.append(
                f"{prefix}: Every expected source must be a non-empty string."
            )
            continue

        # Answerable questions need reference evidence and sources
        if should_answer is True:

            if not item["reference_context"].strip():
                errors.append(
                    f"{prefix}: Answerable question has empty reference_context."
                )

            if not sources:
                errors.append(
                    f"{prefix}: Answerable question has no expected_sources."
                )

        # Unanswerable questions must not have expected sources
        if should_answer is False and sources:
            errors.append(
                f"{prefix}: Unanswerable question must have no expected_sources."
            )

        # Check whether referenced source files exist
        for source in sources:

            source_path = Path(source)

            if source_path.is_absolute():
                errors.append(
                    f"{prefix}: Source path must be relative: {source}"
                )
                continue

            resolved_path = (PROJECT_ROOT / source_path).resolve()

            if not resolved_path.is_relative_to(PROJECT_ROOT):
                errors.append(
                    f"{prefix}: Source path is outside the project: {source}"
                )
            elif not resolved_path.is_file():
                errors.append(
                    f"{prefix}: Source file does not exist: {source}"
                )

    return errors, category_counts


def main():

    print("Loading golden evaluation dataset...\n")

    try:
        dataset = load_dataset()
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Dataset loading failed: {error}")
        sys.exit(1)

    print("Dataset loaded successfully!")
    print(f"Total questions: {len(dataset)}\n")

    errors, category_counts = validate_dataset(dataset)

    if errors:
        print("Dataset validation failed!\n")

        for error in errors:
            print(f"ERROR: {error}")

        print(f"\nTotal validation errors: {len(errors)}")
        sys.exit(1)

    print("Dataset validation passed!")
    print("\nQuestion categories:")

    for category in sorted(VALID_CATEGORIES):
        print(f"{category}: {category_counts[category]}")

    print("\nAll source-file and consistency checks passed!")


if __name__ == "__main__":
    main()