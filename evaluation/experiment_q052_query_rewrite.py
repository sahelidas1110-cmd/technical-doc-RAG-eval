from src.retriever import retrieve_documents
from evaluation.retrieval_metrics import calculate_retrieval_metrics


# Original Q052 question
original_query = (
    "Design an evaluation approach for a multi-step agent "
    "that searches a knowledge base and then uses a calculator. "
    "Which agent-specific behaviors should be measured, and "
    "what execution evidence could tracing provide when a task fails?"
)


# Experimentally rewritten query
rewritten_query = (
    "Agent evaluation metrics tool selection accuracy "
    "tool argument accuracy tool execution success "
    "task completion final answer quality safety. "
    "LangSmith tracing execution trace retrieved documents "
    "prompts LLM requests responses duration errors metadata."
)


expected_sources = [
    "data/raw/langchain/tools_and_evaluation.md"
]


queries = {
    "Baseline - Original Query": original_query,
    "Experiment - Rewritten Query": rewritten_query,
}


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

    for rank, (doc, score) in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print(f"Distance: {score:.4f}")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Chunk index: {doc.metadata.get('chunk_index')}")

    print("\nMetrics:")
    for metric_name, metric_value in metrics.items():
        print(f"{metric_name}: {metric_value}")