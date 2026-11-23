
import json
from pathlib import Path

DATASET_PATH = Path("evaluation/deepeval_dataset.json")

with DATASET_PATH.open("r", encoding="utf-8") as file:
    dataset = json.load(file)

print(f"Total records: {len(dataset)}")

empty_context_records = []
abstention_records = []

for record in dataset:
    retrieval_context = record.get("retrieval_context", [])

    if not retrieval_context:
        empty_context_records.append(record)

    if "could not find sufficient information" in record.get(
        "actual_output", ""
    ).lower():
        abstention_records.append(record)

print(f"Records with empty retrieval context: {len(empty_context_records)}")
print(f"Records with abstention answers: {len(abstention_records)}")

print("\n--- Empty Context Records ---")

for record in empty_context_records:
    print(
        f"ID: {record.get('id')} | "
        f"Question: {record.get('input')}"
    )

print("\n--- Abstention Records ---")

for record in abstention_records:
    print(
        f"ID: {record.get('id')} | "
        f"Question: {record.get('input')}"
    )
    print(f"Answer: {record.get('actual_output')}")
    print(f"Context count: {len(record.get('retrieval_context', []))}")

print("\n--- First 3 Records: Context Inspection ---")

for record in dataset[:3]:
    print(f"\nID: {record.get('id')}")
    print(f"Question: {record.get('input')}")
    print(f"Context count: {len(record.get('retrieval_context', []))}")

    for i, context in enumerate(record.get("retrieval_context", []), start=1):
        print(f"\nContext {i} (first 300 characters):")
        print(context[:300])
