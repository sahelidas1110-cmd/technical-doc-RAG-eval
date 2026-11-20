from src.retriever import retrieve_documents
from src.query_rewriter import rewrite_query
from evaluation.retrieval_metrics import calculate_retrieval_metrics


original_query = (
    "Design an evaluation approach for a multi-step agent "
    "that searches a knowledge base and then uses a calculator. "
    "Which agent-specific behaviors should be measured, and "
    "what execution evidence could tracing provide when a task fails?"
)


expected_sources = [
    "data/raw/langchain/tools_and_evaluation.md"
]


# --------------------------------------------------
# AUTOMATED QUERY REWRITING
# --------------------------------------------------

rewritten_query = rewrite_query(original_query)


# --------------------------------------------------
# EXPERIMENT QUERIES
# --------------------------------------------------

queries = {
    "Baseline - Original Query": original_query,
    "Automated - Rewritten Query": rewritten_query,
}


# --------------------------------------------------
# RETRIEVAL EVALUATION
# --------------------------------------------------

for experiment_name, query in queries.items():

    results = retrieve_documents(query=query, k=3)

    metrics = calculate_retrieval_metrics(
        retrieved_results=results,
        expected_sources=expected_sources,
        k=3,
    )

    print("\n" + "=" * 80)
    print(experiment_name)
    print("=" * 80)

    if experiment_name == "Automated - Rewritten Query":
        print("\nRewritten Query:")
        print(query)

    print("\nRetrieved Results:")

    for rank, (doc, score) in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print(f"Distance: {score:.4f}")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Chunk index: {doc.metadata.get('chunk_index')}")

    print("\nMetrics:")

    for metric_name, metric_value in metrics.items():
        print(f"{metric_name}: {metric_value}")