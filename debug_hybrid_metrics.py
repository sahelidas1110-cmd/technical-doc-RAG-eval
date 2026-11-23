import json

from src.hybrid_retriever import retrieve_hybrid_documents
from evaluation.retrieval_metrics import calculate_retrieval_metrics

with open("evaluation/golden_dataset.json", "r", encoding="utf-8") as file:
    dataset = json.load(file)

question = next(item for item in dataset if item["should_answer"])

retrieved = retrieve_hybrid_documents(
    query=question["question"],
    k=3
)

metrics = calculate_retrieval_metrics(
    retrieved_results=retrieved,
    expected_sources=question["expected_sources"],
    k=3
)

print("\nReturned metric dictionary:")
print(metrics)

print("\nReturned metric keys:")
print(list(metrics.keys()))
