import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT / "evaluation" / "golden_dataset.json"
)


def load_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    return dataset


if __name__ == "__main__":

    dataset = load_dataset()

    print("Dataset loaded successfully!")
    print("Total questions:", len(dataset))

    print("\nQuestion categories:")

    categories = {}

    for item in dataset:
        category = item["category"]
        categories[category] = categories.get(category, 0) + 1

    for category, count in categories.items():
        print(f"{category}: {count}")

    print("\nDataset validation completed!")